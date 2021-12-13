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
        bounds = boundsOf(room, LatLon=LatLon)
        NE = bounds.latlonNE
        SW = bounds.latlonSW

        if SW.lat <= node.lat and node.lat <= NE.lat \
           and SW.lon <= node.lon and node.lon <= NE.lon:
            return True

        return False

    def parse_nodes(self):
        """
            Node data structure

            node = {
                "id": int,
                "name": "",
                "lat": float,
                "lon": float
            }

            Edges are tuples of 2 ids (in nodes)
        """
        # Read Ways.json
        with open(self.path + "/Ways.json", "r") as file:
            json_ways = json.loads(file.read())

        # For every "way"
        for feature in json_ways["features"]:
            # Prev edge id
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
                    # TODO change this?
                    id = len(self.nodes)

                    # Append a new node
                    self.nodes.append({
                        "id": id,
                        "name": None,
                        "lat": p[0],
                        "lon": p[1]
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
                room_vertices = [LatLon(v[0], v[1]) for v in room]

                if self.__in_bounding_box(node_coords, room_vertices):
                    candidates.append(feature)

            final_feature = None
            if len(candidates) == 1:
                final_feature = candidates[0]
            else:
                for feature in candidates:
                    room = feature["geometry"]["coordinates"][0]
                    room_vertices = [LatLon(v[0], v[1]) for v in room]

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

            poi = {
                "id": int,
                "name": str,
                "lat": float
                "lon": float,
                "nearest_path_node": int # ID of nearest in self.nodes
            }

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
            poi_lat_lon = LatLon(point[0], point[1])

            candidates = []
            for feature in json_rooms["features"]:
                room = feature["geometry"]["coordinates"][0]
                # find what room the POI is in first
                room_name = feature["properties"]["room-name"]
                room_vertices = [LatLon(v[0], v[1]) for v in room]

                if self.__in_bounding_box(poi_lat_lon, room_vertices):
                    candidates.append(feature)

            if len(candidates) == 1:
                feature = candidates[0]
                room_name = feature["properties"]["room-name"]
            else:
                for feature in candidates:
                    room = feature["geometry"]["coordinates"][0]
                    room_vertices = [LatLon(v[0], v[1]) for v in room]
                    if poi_lat_lon.isenclosedBy(room_vertices):
                        room_name = feature["properties"]["room-name"]
                        break

            min_distance = float('inf')

            # Get only the path nodes that are in the current room
            room_nodes = [x for x in self.nodes if x["name"] == room_name]

            # Now find the closest path node in the room
            nearest = None
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
                "lat": point[0],
                "lon": point[1],
                "nearest_path_node": nearest_path_node
            })
