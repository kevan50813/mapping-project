""" Redis DB controller using RedisGraph """
import logging
import redis
from redisgraph import Node, Edge, Graph
from redisearch import Client, IndexDefinition, TextField


class Controller():
    def __init__(self, host, port):
        self.log = logging.getLogger(__name__)
        self.db = redis.Redis(host=host, port=port)
        # FIXME debug -> remove for db persistence
        self.db.execute_command("FLUSHALL")

        self.search_client = Client("points_of_interest", conn=self.db)
        definition = IndexDefinition(prefix=["poi:"])
        schema = (TextField("name"))

        try:
            self.search_client.info()
        except redis.ResponseError:
            self.log.debug("Index does not exist, creating index")
            # Index does not exist. We need to create it!
            self.search_client.create_index(schema, definition=definition)

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

        self.log.debug(f"commiting graph {graph_name}")
        graph.commit()

    def add_poi(self, graph_name, poi):
        """
            Add a POI to a given graph_name

            TODO: Should this be a seperate table for every POI
                  TAGGED with the graph_name you can find it on
        """
        poi = {k: ('' if v is None else v)
               for k, v in poi.items()}
        poi["lat"] = poi["coordinates"][0]
        poi["lon"] = poi["coordinates"][1]
        poi["graph"] = graph_name
        poi.pop("coordinates", None)

        poi_id = f"poi:{graph_name}:{str(poi.pop('id'))}"
        self.log.debug(f"Adding POI: {poi_id}")
        self.search_client.redis.hset(poi_id, mapping=poi)

    def get_pois_from_name(self, poi_name):
        pass
