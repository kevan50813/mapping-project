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

            for point in feature["geometry"]["coordinates"]:
                # Id for the current node
                id = len(self.nodes)

                # Append a new node
                self.nodes.append({"id": id,
                                   "name": "",
                                   "coordinates": (point[0], point[1])})

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
            This should be a method as PoIs could change between parser runs,
            the map is much less likely to and it would be best to re-parse
            everything anyway
        """
        with open(self.path + "/PoIs.json", "r") as file:
            json_poi = json.loads(file.read())

        for poi in json_poi["features"]:
            # find closest point in self.nodes
            pass

    def print_lists(self):
        # Dump lists of nodes and edges
        print("Nodes:")
        for node in self.nodes:
            print(node)
        print("\nEdges:")
        print(self.edges)
