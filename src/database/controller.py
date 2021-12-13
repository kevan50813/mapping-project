""" Redis DB controller using RedisGraph """
import logging
import redis
from redisgraph import Node, Edge, Graph
from redisearch import Client, IndexDefinition, TextField


class Controller():
    """
        Redis database controller

        Redis database must have Graph and Search modules
    """
    def __init__(self, host, port):
        self.log = logging.getLogger(__name__)
        self.db = redis.Redis(host=host, port=port)

        # FIXME debug -> remove for db persistence
        self.log.warning("CLEARING WHOLE DB, REMOVE BEFORE REAL USE")
        self.db.execute_command("FLUSHALL")
        # FIXME

        self.search_client = Client("points_of_interest", conn=self.db)
        definition = IndexDefinition(prefix=["poi:"])
        # TODO index the graph room name
        schema = (TextField("name"))

        # Check to see if index is already in db
        try:
            self.search_client.info()
        except redis.ResponseError:
            self.log.debug("Index does not exist, creating index")
            self.search_client.create_index(schema, definition=definition)

    def save_graph(self, graph_name, nodes, edges):
        """
            Save a graph given the nodes and edges to the database,
            breadth-first traversal

            Args:
                graph_name  (str): Name of the graph to save
                nodes (list): A list of nodes (dicts in format specified
                       by graph_parser)
                edges (list): A list of tuples mapping node id to node id
                       (sparse adjacency matrix)
        """
        graph = Graph(graph_name, self.db)
        # clean None from dict, redis doesn't understand it
        nodes = [{k: ('' if v is None else v)
                  for k, v in d.items()} for d in nodes]

        queue = []
        visited = []

        queue.append(nodes[0])
        visited.append(nodes[0])
        while len(queue) != 0:
            u = queue.pop(0)

            # the alias is there to stop duplication, it needs to start with
            # a letter for some reason
            node1 = Node(label='node',
                         properties=u,
                         alias="n"+str(u["id"]))
            graph.add_node(node1)

            # TODO I'm sure there's a better way of doing this, ensure
            # bi-directonality
            adjacent = []
            for e in edges:
                if u["id"] == e[0]:
                    adjacent.append(e[1])
                elif u["id"] == e[1]:
                    adjacent.append(e[0])

            adjn = [n for n in nodes if n["id"] in adjacent]
            for n in adjn:
                if n not in visited:
                    node2 = Node(label='node',
                                 properties=n,
                                 alias="n"+str(n["id"]))
                    edge = Edge(node1, 'path', node2)

                    graph.add_node(node2)
                    graph.add_edge(edge)

                    visited.append(n)
                    queue.append(n)

        self.log.debug(f"commiting graph {graph_name}")
        graph.commit()

    def add_poi(self, graph_name, poi):
        """
            Add a POI to a given graph_name

            Args:
                graph_name (str): name of the graph this PoI is identified with
                poi (dict): poi dictionary (from parser)

        """
        poi = {k: ('' if v is None else v)
               for k, v in poi.items()}

        poi_id = f"poi:{graph_name}:{str(poi.pop('id'))}"

        self.log.debug(f"Adding POI: {poi_id}")
        self.search_client.redis.hset(poi_id, mapping=poi)

    def get_poi_from_name(self, poi_name):
        """
            Search for a POI using Redisearch

            Args:
                poi_name (str): Search string for the POI

            Returns:
                Dictionary of POIs that match poi_name search string
        """
        res = self.search_client.search(poi_name)
        pois = []

        for doc in res.docs:
            # transform back to the standard form
            d = doc.__dict__
            d.pop("payload")
            d["id"] = int(d["id"].split(":")[-1])
            d["nearest_path_node"] = int(d["nearest_path_node"])

            pois.append(d)

        return pois
