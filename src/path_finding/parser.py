'''
    Python class for parsing json files into nodes and edges
    for path finding.

    Requirements:   $ pip install pygeodesy

    To use this class:
        from Parser import Parser
        parser = Parser(<<path to directory containing json files>>)
'''
import json
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
                for p in points:
                    # Id for the current node
                    # TODO change this?
                    id = len(self.nodes)

                    # Append a new node
                    self.nodes.append({"id": id,
                                       "name": "",
                                       "coordinates": (p[0], p[1])})

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

        # For every "room"
        for feature in json_rooms["features"]:
            # Get room name
            name = feature["properties"]["room-name"]

            for room in feature["geometry"]["coordinates"]:
                # For every room vertex
                room_vertices = []
                for vertex in room:
                    room_vertices.append(LatLon(vertex[0], vertex[1]))

                # For every node
                for node in self.nodes:
                    # Get tuple with node coordinates
                    node_coords = LatLon(node["coordinates"][0],
                                         node["coordinates"][1])

                    # Check if the node is within room
                    if (node_coords.isenclosedBy(room_vertices)):
                        # Edit "name" of the node
                        node["name"] = name

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

        for poi in json_poi["features"]:
            id = len(self.pois)
            point = poi["geometry"]["coordinates"]

            min_distance = float('inf')
            for feature in json_rooms["features"]:
                # Load room features and vertices
                room_name = feature["properties"]["room-name"]
                for room in feature["geometry"]["coordinates"]:
                    room_vertices = []
                    for vertex in room:
                        room_vertices.append(LatLon(vertex[0], vertex[1]))

                    # Get only the path nodes that are in the current room
                    room_nodes = [
                        x for x in self.nodes if x["name"] == room_name]

                    # Now find the closest path node in the room
                    for node in room_nodes:
                        poi_lat_lon = LatLon(point[0], point[1])
                        node_lat_lon = LatLon(node["coordinates"][0],
                                              node["coordinates"][1])
                        distance = poi_lat_lon.distanceTo(node_lat_lon)

                        if distance < min_distance:
                            nearest = node
                            min_distance = distance

                    nearest_path_node = nearest["id"]

            self.pois.append({"id": id,
                              "name": poi["properties"]["name"],
                              "coordinates": (point[0], point[1]),
                              "nearest_path_node": nearest_path_node})

    def print_lists(self):
        # Dump lists of nodes and edges
        print("Nodes:")
        for node in self.nodes:
            print(node)
        print("\nEdges:")
        print(self.edges)
