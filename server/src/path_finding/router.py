""" Routing using sparse adjacency matrix """
import math
import json
import dataclasses
from typing import List, Type
import networkx as nx
import shapely.geometry
from src.types.map_types import PathNode


class Router:
    """Class that provides methods to generate routes through a graph"""

    def __init__(self, nodes, edges, polys):
        """
        Initialise the networkx graph

        Args:
            nodes (List[PathNode]): Nodes to find path in
            edges (List[Tuple[int, int]]): Edges between nodes
            polys (List[Polygon]): Room polygons
        """
        self.nodes = nodes
        self.edges = edges

        # create a lookup map for the polygons
        self.lookup_polys = {}
        for poly in polys:
            self.lookup_polys[poly.id] = poly

        self.graph = nx.Graph()

        nodes_tuples = []
        for node in nodes:
            node_as_dict = dataclasses.asdict(
                node, dict_factory=self.__dataclass_to_flat_dict
            )
            nodes_tuples.append((node.id, node_as_dict))

        self.graph.add_nodes_from(nodes_tuples)
        self.graph.add_edges_from(edges)

    @staticmethod
    def __serialise_list(ser_list):
        """
        Serialise a list, for use in the database
        """
        return "serialised:" + json.dumps(ser_list)

    @staticmethod
    def __deserialise_list(ser_list):
        """
        Deserialise a list
        """
        return json.loads(ser_list.split(":", 1)[1])

    def __dataclass_to_flat_dict(self, dataclass):
        """
        Prepares dataclass to a flat dict object
        """
        flat_dict = {}
        for key, value in dataclass:
            if key == "tags":
                flat_dict.update(value)
            elif isinstance(value, (list, tuple)):
                flat_dict[key] = self.__serialise_list(value)
            elif value is None:
                flat_dict[key] = ""
            else:
                flat_dict[key] = value

        return flat_dict

    def __flat_dict_to_dataclass(self, dictionary: dict, target_class: Type) -> Type:
        """
        Attempts to turn a dict into an instance of the given dataclass
        """
        fields = [field.name for field in dataclasses.fields(target_class)]
        fields.remove("tags")
        kwargs = {field: dictionary[field] for field in fields}

        tags = {k: dictionary[k] for k in fields ^ dictionary.keys()}
        kwargs["tags"] = tags

        # Transform empty strings back to 'None' had to be changed when loading
        for key, value in kwargs.items():
            if isinstance(value, str) and value.startswith("serialised:"):
                kwargs[key] = self.__deserialise_list(value)
            elif value == "":
                kwargs[key] = None

        return target_class(**kwargs)

    def __heuristic(self, n, m):
        """
        Heuristic function that should take into account:
            - Distance
            - Room -> Room traversal where rooms are different
            - Simplicity of route?

        Returns:
            Integer that is weighted by the above (higher is worse)
        """
        n_node = self.__flat_dict_to_dataclass(self.graph.nodes[n], PathNode)
        m_node = self.__flat_dict_to_dataclass(self.graph.nodes[m], PathNode)

        n_lat_lon = shapely.geometry.Point(n_node.lat, n_node.lon)
        m_lat_lon = shapely.geometry.Point(m_node.lat, m_node.lon)

        weight = n_lat_lon.distance(m_lat_lon)

        # Try except as there might be no polygons or broken map, shouldn't
        # break routing if it can be avoided (since this is optional)
        try:
            n_poly = self.lookup_polys[n_node.poly_id]
            m_poly = self.lookup_polys[m_node.poly_id]

            if n_poly.tags["indoor"] == "room" or m_poly.tags["indoor"] == "room":
                # tune this
                weight += 10000
        except KeyError:
            pass

        return weight

    def __angle_to(self, n, m, o):
        """n, m, o are path nodes"""
        n_node = self.__flat_dict_to_dataclass(self.graph.nodes[n], PathNode)
        m_node = self.__flat_dict_to_dataclass(self.graph.nodes[m], PathNode)
        o_node = self.__flat_dict_to_dataclass(self.graph.nodes[o], PathNode)

        n_lat_lon = (n_node.lat, n_node.lon)
        m_lat_lon = (m_node.lat, m_node.lon)
        o_lat_lon = (o_node.lat, o_node.lon)

        v1 = (n_lat_lon[0] - m_lat_lon[0], n_lat_lon[1] - m_lat_lon[1])
        v2 = (m_lat_lon[0] - o_lat_lon[0], m_lat_lon[1] - o_lat_lon[1])

        dot_product = (v1[0] * v2[0]) + (v1[1] * v2[1])
        r_angle = math.acos(dot_product / (math.hypot(*v1) * math.hypot(*v2)))

        angle = math.degrees(r_angle)

        return angle

    def __direction_to(self, n, m, o):
        angle = self.__angle_to(n, m, o)

        if 135 <= angle <= 225:
            return "Forward"

        if 45 <= angle <= 225:
            return "Left"

        if 225 <= angle <= 315:
            return "Right"

        return "Reverse"

    def generate_instructions(self, path):
        """
        This should generate a route with instructions attached to each
        edges. Further this should path PoI to the nearest path node.
        """
        if len(path) < 3:
            return ["Forwards"]

        n = path.pop(0)
        m = path.pop(0)
        o = path.pop(0)

        # Start with forward instruction until we can do bearings
        instructions = ["Forward"]
        instructions.append(self.__direction_to(n, m, o))

        for _ in path:
            if len(path) < 3:
                break

            n = path.pop(0)
            m = path.pop(0)
            o = path.pop(0)

            instructions.append(self.__direction_to(n, m, o))

        return instructions

    def find_path(self, start_node, end_node) -> List[int]:
        """
        Find and returns a path through path nodes.

        Args:
            start_node (int): Node ID
            end_node (int): Node ID
        Returns:
            Path from node ID to node ID with heuristic
        """
        return nx.algorithms.astar_path(
            self.graph, start_node, end_node, heuristic=self.__heuristic
        )

    def get_path_nodes(self, path):
        """
        Returns all of the node objects in a path

        Args:
            path (list): list of ints that describe a path through
                         path nodes

        Returns:
            A list of node objects corresponding to the path
        """
        nodes = []
        for node in path:
            node_dataclass = self.__flat_dict_to_dataclass(
                self.graph.nodes[node], PathNode
            )
            nodes.append(
                node_dataclass,
            )

        return nodes
