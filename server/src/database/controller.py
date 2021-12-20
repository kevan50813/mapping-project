""" Redis DB controller using RedisGraph & Redisearch """
import logging
import asyncio
from typing import List
import redis
from redisgraph import Node, Edge, Graph
from redisearch import Client, IndexDefinition, TextField


class Controller():
    """
        Redis database controller

        Redis database must have Graph and Search modules
    """

    def __init__(self, host="127.0.0.1", port="6379"):
        self.log = logging.getLogger(__name__)

        self.redis_db = redis.Redis(host=host, port=port)

        self.search_client = Client("points_of_interest", conn=self.redis_db)
        definition = IndexDefinition(prefix=["poi:"])
        schema = (TextField("name"))

        # Check to see if index is already in db
        try:
            self.search_client.info()
        except redis.ResponseError:
            self.log.debug("Index does not exist, creating index")
            asyncio.create_task(
                self.search_client.create_index(
                    schema, definition=definition))

    async def save_graph(self, graph_name: str,
                         nodes: List[dict], edges: List[tuple]) -> None:
        """
            Save a graph given the nodes and edges to the database,
            breadth-first traversal

            This clears the whole graph at a given name!

            Args:
                graph_name  (str): Name of the graph to save
                nodes (list): A list of nodes (dicts in format specified
                       by graph_parser)
                edges (list): A list of tuples mapping node id to node id
                       (sparse adjacency matrix)
        """
        graph = Graph(graph_name, self.redis_db)

        # For full-text search in the graph we need to create an index
        # Since we delete the graph before adding this needs to be done every
        # time.
        asyncio.create_task(graph.query("""CALL db.idx.fulltext.createNodeIndex
                    ('node', 'name', 'number')"""))

        # clean None from dict, redis doesn't understand it
        nodes = [{k: ('' if v is None else v)
                  for k, v in d.items()} for d in nodes]

        # Breadth-first traversal to discover and save nodes
        queue = []
        visited = []
        queue.append(nodes[0])
        visited.append(nodes[0])
        while len(queue) != 0:
            outer_node = queue.pop(0)

            # the alias is there to stop duplication, it needs to start with
            # a letter for some reason, NB this assumes there are no self-
            # connected nodes (why would there be?)
            node1 = Node(label='node',
                         properties=outer_node,
                         alias="n"+str(outer_node["id"]))
            asyncio.create_task(graph.add_node(node1))

            # gets the opposite value of the edges tuple
            adjacent = []
            for edg in edges:
                if outer_node["id"] == edg[0]:
                    adjacent.append(edg[1])
                elif outer_node["id"] == edg[1]:
                    adjacent.append(edg[0])

            adjn = [n for n in nodes if n["id"] in adjacent]
            for inner_node in adjn:
                if inner_node not in visited:
                    visited.append(inner_node)
                    queue.append(inner_node)

                node2 = Node(label='node',
                             properties=inner_node,
                             alias="n"+str(inner_node["id"]))
                edge = Edge(node1, 'path', node2)

                asyncio.create_task(graph.add_node(node2))
                asyncio.create_task(graph.add_edge(edge))

        self.log.debug("commiting graph %s", graph_name)
        graph.commit()

    def load_graph(self, graph_name: str) -> (List[dict], List[tuple]):
        """
            Returns the whole graph nodes, edges

            Args:
                graph_name: graph of which to return nodes and edges from

            Returns:
                tuple with two lists, first element is nodes, second is edges
        """
        nodes, edges = asyncio.gather(self.load_nodes(graph_name),
                                      self.load_edges(graph_name))

        return (nodes, edges)

    async def load_nodes(self, graph_name: str) -> List[dict]:
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

    async def load_edges(self, graph_name: str) -> List[tuple]:
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

    def load_pois(self, graph_name: str) -> List[dict]:
        """
            Returns all Pois in a building
            Try to use this sparingly as it currently is blocking on the db

            Args:
                graph_name (str): Name of graph you want PoIs for

            Returns:
                list of PoI objects for a given graph
        """
        # FIXME this is NOT a good implementation (keys is blocking)
        # TODO this can be async I think
        # format string in query?
        keys = self.redis_db.keys(f"poi:{graph_name}:*")
        pois = asyncio.gather(*[self.load_poi(key) for key in keys])
        return pois

    async def load_poi(self, key: str) -> dict:
        """
            Load a single PoI given a key

            Args:
                key (str): Key that corresponds to the PoI

            Returns:
                Key properties dict
        """
        poi = self.redis_db.hgetall(key)

        # decode binary strings (utf-8) -> python string
        poi = {k.decode('utf-8'): v.decode('utf-8')
               for k, v in poi.items()}

        # parse these again they are all strings
        # TODO write a better parser than this. Redis doesn't save type
        # hints...
        poi["id"] = int(poi["id"])
        poi["floor"] = float(poi["floor"])
        poi["lat"] = float(poi["lat"])
        poi["lon"] = float(poi["lon"])
        poi["nearest_path_node"] = int(poi["nearest_path_node"])

        return poi

    async def add_pois(self, building_name: str, pois: list) -> None:
        """
            Add a POIs to a given graph_name

            Args:
                building_name (str): name of the graph this PoI is identified
                                     with
                poi (dict): poi dictionary (from parser)

        """
        asyncio.gather(*[self.add_poi(building_name, poi) for poi in pois])

    async def add_poi(self, building_name: str, poi: dict) -> None:
        """
            Add a POI to a given graph_name

            Args:
                building_name (str): name of the graph this PoI is identified
                                     with
                poi (dict): poi dictionary (from parser)

        """
        poi = {k: ('' if v is None else v)
               for k, v in poi.items()}
        poi_id = f"poi:{building_name}:{str(poi['id'])}"
        asyncio.create_task(self.search_client.redis.hset(poi_id, mapping=poi))

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

            poi["id"] = int(poi["id"])
            poi["floor"] = float(poi["floor"])
            poi["lat"] = float(poi["lat"])
            poi["lon"] = float(poi["lon"])
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

    def get_node_neighbours(self, graph_name: str, node_id: int) -> list:
        """
            Returns list of neighbouring nodes to an ID

            Args:
                graph_name (str): name of graph to query
                node_id (int): ID of node you want neighbours of

            Returns:
                List of neighbouring node objects
        """
        graph = Graph(graph_name, self.redis_db)

        query = """MATCH (:node {id: $id})-->(m:node) RETURN m"""
        res = graph.query(query, {"id": node_id})

        nodes = []
        for node in res.result_set:
            # transform back to nodes we use, grab it's properties
            nodes.append(node[0].properties)

        return nodes
