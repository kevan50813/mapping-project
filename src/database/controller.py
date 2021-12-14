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

    def save_graph(self, graph_name, nodes, edges) -> None:
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
            outer_node = queue.pop(0)

            # the alias is there to stop duplication, it needs to start with
            # a letter for some reason
            node1 = Node(label='node',
                         properties=outer_node,
                         alias="n"+str(outer_node["id"]))
            graph.add_node(node1)

            # TODO I'm sure there's a better way of doing this, ensure
            # bi-directonality
            adjacent = []
            for edge in edges:
                if outer_node["id"] == edge[0]:
                    adjacent.append(edge[1])
                elif outer_node["id"] == edge[1]:
                    adjacent.append(edge[0])

            adjn = [n for n in nodes if n["id"] in adjacent]
            for node in adjn:
                if node not in visited:
                    node2 = Node(label='node',
                                 properties=node,
                                 alias="n"+str(node["id"]))
                    edge = Edge(node1, 'path', node2)

                    graph.add_node(node2)
                    graph.add_edge(edge)

                    visited.append(node)
                    queue.append(node)

        self.log.debug("commiting graph %s", graph_name)
        graph.commit()

    def add_poi(self, graph_name, poi) -> None:
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

    def search_poi_by_name(self, poi_name) -> list:
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

    def search_room_nodes(self, search_string) -> list:
        """
            Search for room nodes by name
        """
        return []
