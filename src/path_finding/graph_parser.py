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

    def parse_nodes(self):
        """
            Node data structure

            node = {
                "id": -1,
                "name": "",
                "coordinates": ()
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
                    if existing["coordinates"] == p:
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
                        "coordinates": p
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

        checks = 0
        # For every node
        for node in self.nodes:
            # For every "room"
            for feature in json_rooms["features"]:
                checks += 1
                # Get tuple with node coordinates
                node_coords = LatLon(node["coordinates"][0],
                                     node["coordinates"][1])

                if len(feature["geometry"]["coordinates"]) != 1:
                    print('Rooms', len(feature["geometry"]["coordinates"]))
                room = feature["geometry"]["coordinates"][0]

                # For every room vertex
                room_vertices = []
                for vertex in room:
                    room_vertices.append(LatLon(vertex[0], vertex[1]))

                # Check if the node is within room
                if (node_coords.isenclosedBy(room_vertices)):
                    # Get room name
                    room_name = feature["properties"]["room-name"]
                    room_number = feature["properties"]["room-no"]
                    room_type = feature["type"]

                    # Edit "name" of the node
                    node["name"] = room_name
                    node["number"] = room_number
                    node["type"] = room_type

                    break
        print(checks)

    def parse_pois(self):
        """
            Match points-of-interest to the nearest node in the ways nodes

            poi = {
                "id": -1,
                "name": "",
                "coordinates": ()
                "nearest_path_node": -1 # ID of nearest in self.nodes
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

            for feature in json_rooms["features"]:
                # find what room the POI is in first
                room_name = feature["properties"]["room-name"]
                for room in feature["geometry"]["coordinates"]:
                    room_vertices = []
                    for vertex in room:
                        room_vertices.append(LatLon(vertex[0], vertex[1]))

                # Check if the node is within room
                if (poi_lat_lon.isenclosedBy(room_vertices)):
                    # Edit "name" of the node
                    break

            # TODO this is completely broken lol
            min_distance = float('inf')

            # Get only the path nodes that are in the current room
            room_nodes = [x for x in self.nodes if x["name"] == room_name]

            # Now find the closest path node in the room
            for node in room_nodes:
                node_lat_lon = LatLon(node["coordinates"][0],
                                      node["coordinates"][1])
                distance = poi_lat_lon.distanceTo(node_lat_lon)

                if distance < min_distance:
                    nearest = node
                    min_distance = distance

            nearest_path_node = nearest["id"]

            self.pois.append({
                "id": id,
                "name": poi["properties"]["name"],
                "coordinates": (point[0], point[1]),
                "nearest_path_node": nearest_path_node
            })
