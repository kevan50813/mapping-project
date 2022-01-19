"""
    Class that deals with polygon parsing and generating paths through them
"""
import logging
import asyncio
from typing import List
import shapely.geometry
from src.types.map_types import Polygon, PathNode, PoI


class PolygonParser:
    """
        Class that deals with polygon parsing and generating paths through them
    """

    def __init__(self, graph_name: str, polygon_json: str):
        self.log = logging.getLogger(__name__)
        self.graph_name = graph_name
        self.json_polygons = polygon_json
        self.polygons = []
        self.__geodesy_polygons = []

    def in_poly(self, node: shapely.geometry.Point, level: float):
        """
            Checks if a node is in a given room
            first by bounding box then by isEnclosedBy
        """
        lookup_polys = {}
        for poly in self.polygons:
            lookup_polys[poly.id] = poly

        rooms_on_level = filter(lambda x: x["level"] == level,
                                self.__geodesy_polygons)

        for room in rooms_on_level:
            if room["polygon"].contains(node):
                return lookup_polys[room["id"]]

        return None

    def load_polygons(self):
        """
            Loads and pre-computes properties about the rooms
        """
        self.log.debug("Loading poygons")
        for feature in self.json_polygons["features"]:
            id = len(self.polygons)
            room = feature["geometry"]["coordinates"][0]
            level = feature["properties"]["level"]
            properties = feature["properties"]

            vertices = [(v[1], v[0]) for v in room]
            geo_poly = shapely.geometry.Polygon(vertices)

            lats = [lat for lat, _ in vertices]
            lons = [lon for _, lon in vertices]

            NE = (max(lats), max(lons))
            SW = (min(lats), min(lons))

            try:
                levels = level.split(";")
                level_span = [float(level) for level in levels]
            except AttributeError:
                level_span = [level]

            for level in level_span:
                self.__geodesy_polygons.append({"id": id,
                                                "level": level,
                                                "polygon": geo_poly,
                                                "tags": properties})

                self.polygons.append(Polygon(id,
                                             level,
                                             self.graph_name,
                                             vertices,
                                             NE,
                                             SW,
                                             properties))

    def parse_rooms(self, nodes: List[PathNode]):
        """
            Give each node a name that corresponds
            to the room that it is located in

            Reads from Rooms.json and Access.json to assign room names
            tags each accordingly (room vs access) for routing later.
        """
        self.log.debug("Parsing rooms")
        return [self.parse_room(node)
                for node in nodes]

    def parse_room(self, node: PathNode):
        """
            Find the room that a node is in

            Args: node (dict): As defined in parse_nodes
        """
        node_coords = shapely.geometry.Point(node.lat, node.lon)
        room = self.in_poly(node_coords, node.level)

        if room is not None:
            node.poly_id = room.id

        return node

    async def create_room_paths(self, nodes: List[PathNode], pois: List[PoI]):
        """
            This method loops through all existing polygons
            and create paths in them based on:
                - Existing paths
                - Existing points

            In the case of hallways:
                - Skeletonise
                - Fix junctions using Haunert & Sesner
            In the case of 'areas':
                - Create a visibility matrix
                    - To all points in the polygon AND nodes in paths and PoIs
                - Create node at intersections in visibilty matrix
        """
        self.log.debug("Creating room paths")
        tasks = []
        for poly in self.__geodesy_polygons:
            properties = poly["properties"]
            if "indoor" in properties:
                if properties["indoor"] == "hallway":
                    tasks.append(asyncio.create_task(
                        self.create_hallway_paths(poly)))
                elif properties["indoor"] == "area":
                    tasks.append(asyncio.create_task(
                        self.create_area_paths(poly, nodes, pois)))

        nodes, edges = asyncio.wait(tasks)

    async def create_area_paths(self, poly: dict,
                                nodes: List[PathNode], pois: List[PoI]):
        """
            Creates a visibility matrix including all of the nodes and pois
            in the arguments, should make nodes at intersections of each

            Returns:
                List of nodes (newly created), and edges between them
                and existing nodes
        """
        self.log.debug("Creating area path for %s", poly.id)
        return [], []

    async def create_hallway_paths(self, poly: dict):
        """
            Skeletonises hallway and uses H&S algorithm to fix juntions

            Returns:
                List of nodes (newly created), edges between them
        """
        self.log.debug("Creating hallway path for %s", poly.id)
        return [], []
