""" Routing using sparse adjacency matrix """
import networkx as nx
from pygeodesy.sphericalNvector import LatLon


class Router:
    """ Class that provides methods to generate routes through a graph """

    def __init__(self, graph_name, nodes, edges):
        self.graph_name = graph_name
        self.nodes = nodes
        self.edges = edges

        self.graph = nx.Graph()

        nodes_tuples = [(x["id"], x) for x in nodes]
        self.graph.add_nodes_from(nodes_tuples)
        self.graph.add_edges_from(edges)

    def __heuristic(self, n, m):
        """
            Heuristic function that should take into account:
                - Distance
                - Room -> Room traversal where rooms are different
                - Simplicity of route?

            Returns:
                Integer that is weighted by the above (higher is worse)
        """
        n_lat_lon = LatLon(self.graph.nodes[n]["lat"],
                           self.graph.nodes[n]["lon"])
        m_lat_lon = LatLon(self.graph.nodes[m]["lat"],
                           self.graph.nodes[m]["lon"])

        return n_lat_lon.distanceTo(m_lat_lon)

    def generate_route(self, start_node, end_node):
        """
            This should generate a route with instructions attached to each
            edges. Further this should path PoI to the nearest path node.
        """
        return self.find_path(start_node, end_node)

    def find_path(self, start_node, end_node):
        """
            Find and returns a path through path nodes.

            Args:
                start_node (int): Node ID
                start_node (int): Node ID
            Returns:
                Path from node ID to node ID with heuristic
        """
        return nx.algorithms.astar_path(
            self.graph, start_node, end_node, heuristic=self.__heuristic)

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
            nodes.append(self.graph.nodes[node])

        return nodes
