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
    # Constructor
    def __init__(self, path):
        # Node data structure
        node = {
            "id": -1,
            "name": "",
            "coordinates": ()
        }

        # Nodes (initially empty)
        self.nodes = [node]
        self.nodes.pop()

        # Edges (initially empty)
        self.edges = [()]
        self.edges.pop()

        # Fill edges and nodes from the files.
        # Read Ways.json
        file = open(path + "/Ways.json", "r")
        jsonWays = json.loads(file.read())

        # For every "way"
        for feature in jsonWays["features"]:
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

        # Write node names
        # Read Rooms.json
        file = open(path + "/Rooms.json", "r")
        jsonRooms = json.loads(file.read())

        # For every "room"
        for feature in jsonRooms["features"]:
            # Get room name
            name = feature["properties"]["room-name"]

            for room in feature["geometry"]["coordinates"]:
                # Get room vertices
                roomVertices = [LatLon(0, 0)]
                roomVertices.pop()

                # For every vertex
                for vertex in room:
                    roomVertices.append(LatLon(vertex[0], vertex[1]))

                # For every node
                for node in self.nodes:
                    # Get tuple with node coordinates
                    nodeCoords = LatLon(node["coordinates"][0],
                                        node["coordinates"][1])

                    # Check if the node is within room
                    if (nodeCoords.isenclosedBy(roomVertices)):
                        # Edit "name" of the node
                        node["name"] = name

    # Dump lists of nodes and edges
    def printLists(self):
        print("Nodes:")
        for node in self.nodes:
            print(node)
        print("\nEdges:")
        print(self.edges)
