"""
    Python class for parsing json files into nodes and edges
    for path finding.

    Requirements:   $ pip install pygeodesy

    To use this class:
        from Parser import Parser
        parser = Parser(<<path to directory containing json files>>)
"""
import logging
import shapely.geometry
from src.parser.polygon_parser import PolygonParser
from src.types.map_types import PathNode, PoI


class Parser:
    """Parser for GeoJSON maps"""

    def __init__(self, graph_name, polygons, linestring, points):
        """
        Call this to create the object
        """
        self.log = logging.getLogger(__name__)
        self.graph_name = graph_name
        self.poly_parser = PolygonParser(graph_name, polygons)
        self.json_linestring = linestring
        self.json_points = points

        # This in theory might take a while so maybe async?
        self.poly_parser.load_polygons()

        self.edges = []
        self.nodes = []
        self.pois = []
        self.polygons = self.poly_parser.polygons

        # polygons dictionary that has Pygeodesy object
        self.__node_hashes = {}

        self.parse_nodes()
        self.nodes = self.poly_parser.parse_rooms(self.nodes)
        self.parse_pois()
        self.edges += self.poly_parser.connect_stairways(self.nodes)

    @staticmethod
    def _nearest_node(point, nodes: list) -> int:
        """
        Finds the nearest node's ID in a list of nodes

        Args:
            point_lat_lon (LatLon): This should be a pygeodesy LatLon of
                                    the point you wish to find the closest
                                    node to
            nodes (list[dict]): List of nodes that are to be checked
        """
        # if there's only one node, don't bother checking distances
        if len(nodes) == 1:
            return nodes[0].id

        if len(nodes) == 0:
            return None

        nearest = None
        min_distance = float("inf")

        for node in nodes:
            node_point = shapely.geometry.Point(node.lat, node.lon)
            distance = point.distance(node_point)

            if distance < min_distance:
                nearest = node
                min_distance = distance

        return nearest.id

    def parse_nodes(self):
        """
        Parse nodes from the Ways.json layer of a given map
        Ways.json should be GEOJson file containing only LineString
        features (no MultiLineString).

        Also assigns to edges (sparse adajcency matrix)

        Edges are tuples of 2 ids (in self.nodes)
        """
        return [
            self.parse_node_feature(feature)
            for feature in self.json_linestring["features"]
        ]

    def parse_node_feature(self, feature):
        """
        Parse a single feature from the Ways.json file

        Args:
            feature (dict): A geojson format dict describing a single
            feature
        """
        prev_id = -1

        # qgis bug? some weird things with no geometry sometimes?
        if feature["geometry"] is None:
            return

        for point in feature["geometry"]["coordinates"]:
            point = (point[0], point[1])
            point_level = feature["properties"]["level"]
            # is p already in self.nodes ?
            if (
                point in self.__node_hashes
                and self.__node_hashes[point]["level"] == point_level
            ):
                node_id = self.__node_hashes[point]["id"]
            else:
                # Id for the current node
                node_id = len(self.nodes)

                # Append a new node
                self.nodes.append(
                    PathNode(
                        node_id,
                        self.graph_name,
                        point_level,
                        point[1],
                        point[0],
                        -1,
                        feature["properties"],
                    )
                )

                self.__node_hashes[point] = {"level": point_level, "id": node_id}

            # Append a new edge
            if prev_id != -1:
                self.edges.append((prev_id, node_id))

            # Store id
            prev_id = node_id

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
        """
        return [self.parse_poi(poi) for poi in self.json_points["features"]]

    def parse_poi(self, poi):
        """
        Parses a single PoI, finds nearest path node to it

        Args:
            poi (dict): GeoJSON PoI object
        """
        poi_id = len(self.pois)
        point = poi["geometry"]["coordinates"]
        poi_lat_lon = shapely.geometry.Point(point[1], point[0])

        room = self.poly_parser.in_poly(poi_lat_lon, float(poi["properties"]["level"]))

        if room is not None:
            poly_id = room.id

            # Get only the path nodes that are in the current room
            room_nodes = [n for n in self.nodes if n.poly_id == poly_id]
            nearest_path_node = self._nearest_node(poi_lat_lon, room_nodes)
        else:
            nearest_path_node = None

        self.pois.append(
            PoI(
                poi_id,
                self.graph_name,
                poi["properties"]["level"],
                point[0],
                point[1],
                nearest_path_node,
                poi["properties"],
            )
        )
