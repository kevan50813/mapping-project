'''
    Python class for parsing json files into nodes and edges
    for path finding.

    Requirements:   $ pip install pygeodesy

    To use this class:
        from Parser import Parser
        parser = Parser(<<path to directory containing json files>>)
'''
import json
# from rich import print  # uncomment for prettyprint dicts
# from typing import Coroutine  # for easier code editing
from pygeodesy.sphericalNvector import LatLon
from pygeodesy import boundsOf


class Parser:
    edges = []
    nodes = []
    pois = []

    # Constructor
    def __init__(self, path):
        self.path = path

        # parse the files
        self.parse_nodes()
        self.parse_rooms()
        self.parse_pois()

    def __in_bounding_box(self, node, room):
        """
            Check if a LatLon object is within the
            bounding box of a list of LatLon objects.

            This is much fater than using isenclosedBy, check with bounding
            box first, then check with isenclosedBy later

            Args:
                node (LatLon): point you wish to check is in a bounding box
                room (LatLon[]): list of LatLon objects that form a polygon

            Returns:
                True if node is in the bounding box of the polygon described
                by room

                False if the node is not in the bounding box
        """
        bounds = boundsOf(room, LatLon=LatLon)
        NE = bounds.latlonNE
        SW = bounds.latlonSW

        if SW.lat <= node.lat and node.lat <= NE.lat \
           and SW.lon <= node.lon and node.lon <= NE.lon:
            return True

        return False

    def parse_nodes(self):
        """
            Parse nodes from the Ways.json layer of a given map
            Ways.json should be GEOJson file containing only LineString
            features (no MultiLineString).

            Also assigns to edges (sparse adajcency matrix)

            Node data structure

            node = {
                "id": int,
                "name": "",
                "lat": float,
                "lon": float
            }

            Edges are tuples of 2 ids (in self.nodes)
        """
        # Read Ways.json
        with open(self.path + "/Ways.json", "r") as file:
            json_ways = json.loads(file.read())

        # For every "way"
        for feature in json_ways["features"]:
            prevId = -1

            for points in feature["geometry"]["coordinates"]:
                p = (points[0], points[1])
                # is p already in self.nodes ?
                # else add it, then do the rest
                for existing in self.nodes:
                    if (existing["lat"], existing["lon"]) == p:
                        id = existing["id"]
                        break
                else:
                    # Id for the current node
                    # TODO change this? -> Include ID information of what map
                    # we are looking at
                    id = len(self.nodes)

                    # Append a new node
                    self.nodes.append({
                        "id": id,
                        "name": None,
                        "lon": p[0],
                        "lat": p[1]
                    })
                # Append a new edge
                if (prevId != -1):
                    self.edges.append((prevId, id))

                # Store id
                prevId = id

    def parse_rooms(self):
        """
            Give each node a name that corresponds
            to the room that it is located in

            Reads from Rooms.json and Access.json to assign room names
            tags each accordingly (room vs access) for routing later.
        """
        # Read Rooms.json
        with open(self.path + "/Rooms.json", "r") as file:
            json_rooms = json.loads(file.read())
            for f in json_rooms["features"]:
                f["type"] = "room"

        with open(self.path + "/Access.json", "r") as file:
            json_access = json.loads(file.read())
            for f in json_access["features"]:
                f["type"] = "access"
                json_rooms["features"].append(f)

        for node in self.nodes:
            node_coords = LatLon(node["lat"],
                                 node["lon"])

            # check bounding boxes first, much faster
            candidates = []
            for feature in json_rooms["features"]:
                room = feature["geometry"]["coordinates"][0]
                room_vertices = [LatLon(v[1], v[0]) for v in room]

                if self.__in_bounding_box(node_coords, room_vertices):
                    candidates.append(feature)

            final_feature = None
            if len(candidates) == 1:
                final_feature = candidates[0]
            else:
                for feature in candidates:
                    room = feature["geometry"]["coordinates"][0]
                    room_vertices = [LatLon(v[1], v[0]) for v in room]

                    if node_coords.isenclosedBy(room_vertices):
                        final_feature = feature
                        break

            if final_feature is not None:
                room_name = final_feature["properties"]["room-name"]
                room_number = final_feature["properties"]["room-no"]
                room_type = final_feature["type"]

                node["name"] = room_name
                node["number"] = room_number
                node["type"] = room_type
            else:
                node["name"] = None
                node["number"] = None
                node["type"] = None

    def parse_pois(self):
        """
            Match points-of-interest to the nearest node in the ways nodes

            POI data structure
            poi = {
                "id": int,
                "name": str,
                "lat": float
                "lon": float,
                "nearest_path_node": int # ID of nearest in self.nodes
            }

            NOTE:
            I think if I do it this way there might be consistency issues
            if Rooms.json was to change, this is why DB is definitely a better
            idea (we can parse the json then use the parsed objects to write
            into a DB table?)
        """
        with open(self.path + "/PoIs.json", "r") as file:
            json_poi = json.loads(file.read())

        with open(self.path + "/Rooms.json", "r") as file:
            json_rooms = json.loads(file.read())

        with open(self.path + "/Access.json", "r") as file:
            json_access = json.loads(file.read())
            for f in json_access["features"]:
                json_rooms["features"].append(f)

        for poi in json_poi["features"]:
            id = len(self.pois)
            point = poi["geometry"]["coordinates"]
            poi_lat_lon = LatLon(point[1], point[0])

            candidates = []
            # Generate a list of candidate rooms that the POI is in the
            # bounding box of
            for feature in json_rooms["features"]:
                room = feature["geometry"]["coordinates"][0]
                room_name = feature["properties"]["room-name"]
                room_vertices = [LatLon(v[1], v[0]) for v in room]

                if self.__in_bounding_box(poi_lat_lon, room_vertices):
                    candidates.append(feature)

            # If there's only one candidate then we know it's that room
            # Otherwise, we have to check with the slower 'isenclosedBy'
            if len(candidates) == 1:
                feature = candidates[0]
                room_name = feature["properties"]["room-name"]
            else:
                for feature in candidates:
                    room = feature["geometry"]["coordinates"][0]
                    room_vertices = [LatLon(v[1], v[0]) for v in room]
                    if poi_lat_lon.isenclosedBy(room_vertices):
                        room_name = feature["properties"]["room-name"]
                        # Since we've found it we break, if the map is badly
                        # constructed there's a chance a point could be in two
                        # rooms at once, but we'll assume it's in the first one
                        # we find
                        break

            # Get only the path nodes that are in the current room
            room_nodes = [n for n in self.nodes if n["name"] == room_name]

            # Loop through all the path nodes that are in the room and find the
            # closest one, this is probably the fastest way of doing
            # nearest-neighbour (and there aren't that many nodes)
            nearest = None
            min_distance = float('inf')
            for node in room_nodes:
                node_lat_lon = LatLon(node["lat"],
                                      node["lon"])
                distance = poi_lat_lon.distanceTo(node_lat_lon)

                if distance < min_distance:
                    nearest = node
                    min_distance = distance

            if nearest is not None:
                nearest_path_node = nearest["id"]
            else:
                nearest_path_node = None

            self.pois.append({
                "id": id,
                "name": poi["properties"]["name"],
                "lon": point[0],
                "lat": point[1],
                "nearest_path_node": nearest_path_node
            })
