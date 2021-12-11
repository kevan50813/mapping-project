""" Redis DB controller using RedisGraph """
import redis
from redisgraph import Node, Edge, Graph


class Controller():
    def __init__(self, host, port):
        self.db = redis.Redis(host=host, port=port)

    def save_graph(self, graph_name, nodes, edges):
        """
            Save a graph given the nodes and edges to the database

            Args:
                graph_name  (str): Name of the graph to save
                nodes (list): A list of nodes (dicts in format specified
                       by graph_parser)
                edges (list): A list of tuples mapping node id to node id
                       (sparse adjacency matrix)
        """
        graph = Graph(graph_name, self.db)
        # clean None from dict
        nodes = [{k: ('' if v is None else v)
                  for k, v in d.items()} for d in nodes]

        queue = []
        visited = []

        queue.append(nodes[0])
        visited.append(nodes[0])
        while len(queue) != 0:
            u = queue.pop(0)

            if "coordinates" in u.keys():
                u["lat"] = u["coordinates"][0]
                u["lon"] = u["coordinates"][1]
                u.pop("coordinates", None)

            # the alias is there to stop duplication, it needs to start with
            # a letter for some reason
            node1 = Node(label='node',
                         properties=u,
                         alias="n"+str(u["id"]))
            graph.add_node(node1)

            adjacent = []
            for e in edges:
                if u["id"] == e[0]:
                    adjacent.append(e[1])
                elif u["id"] == e[1]:
                    adjacent.append(e[0])

            adjn = [n for n in nodes if n["id"] in adjacent]
            for n in adjn:
                if n not in visited:
                    if "coordinates" in n.keys():
                        n["lat"] = n["coordinates"][0]
                        n["lon"] = n["coordinates"][1]
                        n.pop("coordinates", None)

                    node2 = Node(label='node',
                                 properties=n,
                                 alias="n"+str(n["id"]))
                    graph.add_node(node2)

                    edge = Edge(node1, 'path', node2)
                    graph.add_edge(edge)

                    visited.append(n)
                    queue.append(n)

        graph.commit()

    def add_poi(self, graph_name, poi):
        """
            Add a POI to a given graph_name
        """
        graph = Graph(graph_name, self.db)

        poi = {k: ('' if v is None else v)
               for k, v in poi.items()}
        poi["lat"] = poi["coordinates"][0]
        poi["lon"] = poi["coordinates"][1]
        poi.pop("coordinates", None)

        poi_node = Node(label='poi', properties=poi)
        graph.add_node(poi_node)
        graph.commit()

        # Now find path node it is associated with, and create edge
        query = """MATCH (n:node {id: $id}), (p:poi {id:$poi_id})
                   CREATE (p)-[:poi_nearest]->(n)"""
        graph.query(query, {"id": poi["nearest_path_node"],
                            "poi_id": poi["id"]})

    def get_poi(self, graph_name, poi):
        pass
