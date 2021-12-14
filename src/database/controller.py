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

    def __init__(self, host: str, port: str):
        self.log = logging.getLogger(__name__)
        self.redis_db = redis.Redis(host=host, port=port)

        # FIXME debug -> remove for db persistence
        self.log.warning("CLEARING WHOLE DB, REMOVE BEFORE REAL USE")
        self.redis_db.execute_command("FLUSHALL")
        # FIXME

        self.search_client = Client("points_of_interest", conn=self.redis_db)
        definition = IndexDefinition(prefix=["poi:"])
        # TODO index the graph room name
        schema = (TextField("name"))

        # Check to see if index is already in db
        try:
            self.search_client.info()
        except redis.ResponseError:
            self.log.debug("Index does not exist, creating index")
            self.search_client.create_index(schema, definition=definition)

    def save_graph(self, graph_name: str, nodes: list, edges: list) -> None:
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
        # TODO: should we make sure the graph is clear first
        graph = Graph(graph_name, self.redis_db)

        # For full-text search in the graph we need to create an index
        index_query = """CALL db.idx.fulltext.createNodeIndex
                         ('node', 'name', 'number')"""
        graph.query(index_query)

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

        self.log.debug("commiting graph %s", graph_name)
        graph.commit()

    def add_poi(self, graph_name: str, poi: dict) -> None:
        """
            Add a POI to a given graph_name

            Args:
                graph_name (str): name of the graph this PoI is identified with
                poi (dict): poi dictionary (from parser)

        """
        poi = {k: ('' if v is None else v)
               for k, v in poi.items()}

        poi_id = f"poi:{graph_name}:{str(poi.pop('id'))}"

        self.log.debug("Adding POI: %s", poi_id)
        self.search_client.redis.hset(poi_id, mapping=poi)

    def search_poi_by_name(self, poi_name: str) -> list:
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
            poi = doc.__dict__
            poi.pop("payload")
            poi["id"] = int(poi["id"].split(":")[-1])
            poi["nearest_path_node"] = int(poi["nearest_path_node"])

            pois.append(poi)

        return pois

    def search_room_nodes(self, graph_name: str, search_string: str) -> list:
        """
            Search for room nodes by name
        """
        graph = Graph(graph_name, self.redis_db)

        # We should query the graph for two things, both the name and the
        # room number
        query = """CALL db.idx.fulltext.queryNodes(node, $search_string)
                   YIELD node RETURN node.title, node.score"""
        res = graph.query(query, {"search_string": search_string})

        return res.result_set
