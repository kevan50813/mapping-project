"""
    Class that deals with polygon parsing and generating paths through them
"""
import logging
import asyncio
from typing import List, Tuple
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

    @staticmethod
    def nodes_between_adj_levels(nodes: List[PathNode]) -> List[Tuple[int, int]]:
        """
        Connects nodes in the list together to the nodes exactly one floor
        above and below it. Generate a spanning list of floors for this.

        e.g. floors in the list are 0, 0.5, 1, 2
        Nodes on 0 will be connected to 0.5, and 0.5 to 0 and 1

        Use for stairs (where pathing needs to be done to every floor)

        Args:
            nodes (List[Pathnode]): List of pathnodes to connect
        Returns:
            List of tuples containing the edges created between node IDs
        """
        # sorted list of unique levels
        levels = sorted({n.level for n in nodes})
        edges = []

        for node in nodes:
            level_index = levels.index(node.level)

            above_nodes = below_nodes = []
            if level_index - 1 > 0:
                below = levels[level_index - 1]
                below_nodes = filter(lambda n, b=below: n.level == b, nodes)

            if level_index + 1 < len(levels):
                above = levels[level_index + 1]
                above_nodes = filter(lambda n, a=above: n.level == a, nodes)

            adjacent_nodes = list(above_nodes) + list(below_nodes)

            for adj in adjacent_nodes:
                edges.append((node.id, adj.id))

            # we have exhausted this node's neighbours, since it's
            # bidirectional we can just remove it to save iterations
            nodes.remove(node)

        return edges

    @staticmethod
    def nodes_between_levels(nodes: List[PathNode]) -> List[Tuple[int, int]]:
        """
        Connects nodes in the list together with all nodes on all floors
        (Generate a fully-connected graph.)

        e.g. floors in the list are 0, 0.5, 1, 2
        Nodes on 0 will be connected to 0.5, 1, and 2

        Use for lifts

        Args:
            nodes (List[Pathnode]): List of pathnodes to connect
        Returns:
            List of tuples containing the edges created between node IDs
        """
        edges = []

        for node in nodes:
            # don't join if they are on same level, probably these edges
            # already exist, or if they dont they dont for a reason
            for adj in nodes:
                if adj.level != node.level:
                    edges.append((node.id, adj.id))
            # we have exhausted this node's neighbours, since it's
            # bidirectional we can just remove it to save iterations
            nodes.remove(node)

        return edges

    def in_poly(self, node: shapely.geometry.Point, level: float):
        """
        Checks if a node is in a given room
        first by bounding box then by isEnclosedBy
        """
        lookup_polys = {}
        for poly in self.polygons:
            lookup_polys[poly.id] = poly

        rooms_on_level = filter(lambda x: x["level"] == level, self.__geodesy_polygons)

        for room in rooms_on_level:
            if room["polygon"].contains(node):
                return lookup_polys[room["id"]]

        return None

    def load_polygons(self):
        """
        Loads and pre-computes properties about the rooms
        """
        self.log.debug("Loading polygons")

        level_range = {str(n["properties"]["level"])
                       for n in self.json_polygons["features"]}
        level_range = sorted([level for level in level_range
                              if ";" not in level])

        for feature in self.json_polygons["features"]:
            id = len(self.polygons)
            room = feature["geometry"]["coordinates"][0]
            # Important note: this means that the API returns the range
            # and the server expands it below, this might be quite confusing
            # when returning nodes vs polygons...
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
                lower = int(levels[0])
                upper = int(levels[1])

                level_span = [float(level) for level in level_range[lower:upper]]
            except (AttributeError, IndexError):
                level_span = [float(level)]

            for span in level_span:
                self.__geodesy_polygons.append(
                    {"id": id, "level": span, "polygon": geo_poly, "tags": properties}
                )

                self.polygons.append(
                    Polygon(id, self.graph_name, span, vertices, NE, SW, properties)
                )

    def parse_rooms(self, nodes: List[PathNode]):
        """
        Give each node a name that corresponds
        to the room that it is located in

        Reads from Rooms.json and Access.json to assign room names
        tags each accordingly (room vs access) for routing later.
        """
        self.log.debug("Parsing rooms")
        return [self.parse_room(node) for node in nodes]

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

    def connect_stairways(self, nodes: List[PathNode]):
        """
        Method to call to connect staircases in a list of nodes
        """
        # TODO fix this to not work on wall edges
        self.log.debug("Generating stairway edges")
        total_edges = []

        way_nodes = list(filter(lambda n: n.tags["indoor"] == "way", nodes))

        for node in way_nodes:
            if "indoor" in node.tags:
                if node.tags["indoor"] == "wall":
                    continue

            self.log.debug("Adding edges for node: %s", node)

            room = None

            for poly in self.__geodesy_polygons:
                if poly["id"] == node.poly_id:
                    self.log.debug("Found room: %s", poly["id"])
                    room = poly
                    break

            # Can't find the room for whatever reason, return none
            if room is None:
                self.log.debug("Couldn't find room")
                continue

            tags = room["tags"]
            self.log.debug("Tags: %s", tags)

            # Ideally we'd be able to not rely on tags here but, given this
            # will do nothing for buildings that don't have these it's fine
            if "stairs" not in tags and "highway" not in tags:
                self.log.debug("%s, not a staircase or elevator", room)
                continue

            same_room = list(
                filter(lambda n, node=node: node.poly_id == n.poly_id, way_nodes)
            )

            self.log.debug("Nodes in the same room: %s", same_room)

            if "stairs" in tags and tags["stairs"] is not None:
                self.log.debug("%s is staircase", room["id"])
                edges = self.nodes_between_adj_levels(same_room)
            elif "highway" in tags and tags["highway"] == "elevator":
                self.log.debug("%s is elevator", room["id"])
                edges = self.nodes_between_levels(same_room)
            else:
                # This is a for rooms that have highway tag but aren't lifts
                edges = []

            total_edges += edges

        if total_edges:
            self.log.debug(total_edges)

        return total_edges

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
                    tasks.append(asyncio.create_task(self.create_hallway_paths(poly)))
                elif properties["indoor"] == "area":
                    tasks.append(
                        asyncio.create_task(self.create_area_paths(poly, nodes, pois))
                    )

        nodes, edges = asyncio.wait(tasks)

    async def create_area_paths(
        self, poly: dict, nodes: List[PathNode], pois: List[PoI]
    ):
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
