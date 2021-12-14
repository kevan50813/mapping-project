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

    def load_graph(self, graph_name) -> (list, list):
        """
            Returns the whole graph nodes, edges

            Args:
                graph_name: graph of which to return nodes and edges from

            Returns:
                tuple with two lists, first element is nodes, second is edges
        """
        nodes = self.load_nodes(graph_name)
        edges = self.load_edges(graph_name)

        return (nodes, edges)

    def load_nodes(self, graph_name) -> list:
        """
            Return all nodes in a given graph

            Args:
                graph_name: graph of which to return nodes from

            Returns:
                List of nodes (see graph_parser for definition of their format)
        """
        graph = Graph(graph_name, self.redis_db)
        query = """MATCH (n:node) RETURN n"""
        result = graph.query(query)

        nodes = []
        for res in result.result_set:
            nodes.append(res[0].properties)

        nodes = [{k: (None if v == '' else v)
                  for k, v in d.items()} for d in nodes]

        return nodes

    def load_edges(self, graph_name) -> list:
        """
            Returns all edges in a given graph

            Args:
                graph_name: graph of which to return edges from

            Returns:
                list of tuples that contain two node ids that are connected
        """
        graph = Graph(graph_name, self.redis_db)
        query = """MATCH (n:node)-->(m:node) RETURN n.id, m.id"""
        result = graph.query(query)

        edges = []
        for res in result.result_set:
            edges.append((res[0], res[1]))

        return edges

    def load_pois(self, graph_name) -> list:
        """
            Returns all Pois in a building
            Try to use this sparingly
        """
        # FIXME this is NOT a good implementation (keys is blocking)
        pois = []
        for key in self.redis_db.keys(f"poi:{graph_name}:*"):
            vals = self.redis_db.hgetall(key)
            # TODO parse these again they are all binary strings
            pois.append(vals)
        # query = """SCAN 0 MATCH poi:$name:"""
        # for key in self.redis_db.hscan_iter(f"poi:{building_name}"):
        #     print(key)
        return pois

    def add_poi(self, building_name: str, poi: dict) -> None:
        """
            Add a POI to a given graph_name

            Args:
                graph_name (str): name of the graph this PoI is identified with
                poi (dict): poi dictionary (from parser)

        """
        poi = {k: ('' if v is None else v)
               for k, v in poi.items()}

        poi_id = f"poi:{building_name}:{str(poi['id'])}"

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

            Args:
                graph_name (str): name of the graph to search in
                search_string (str): search string

            Returns:
                List of path nodes that match search_string
        """
        graph = Graph(graph_name, self.redis_db)

        # redisearch fulltext search makes this mad easy
        query = """CALL db.idx.fulltext.queryNodes('node', $search_string)
                   YIELD node RETURN node"""
        res = graph.query(query, {"search_string": search_string})

        nodes = []
        for node in res.result_set:
            # transform back to nodes we use, grab it's properties
            nodes.append(node[0].properties)

        return nodes
