""" Redis DB controller using RedisGraph & Redisearch """
import logging
import warnings
import asyncio
import json
from typing import List, Type, Tuple
import dataclasses
import redis
from redisgraph import Node, Edge, Graph
from redisearch import Client, IndexDefinition, TextField
from src.types.map_types import PathNode, PoI, Polygon


class Controller:
    """
    Redis database controller

    Redis database must have Graph and Search modules
    """

    def __init__(self, host="127.0.0.1", port="6379"):
        self.log = logging.getLogger(__name__)
        self.redis_db = redis.Redis(host=host, port=port)

        # define a search client and index fields for poi
        self.log.debug("Creating PoI search client")
        self.poi_search_client = Client("points_of_interest", conn=self.redis_db)
        poi_definition = IndexDefinition(prefix=["PoI:"])
        poi_schema = TextField("amenity")

        self.log.debug("Creating rooms search client")
        self.room_search_client = Client("rooms", conn=self.redis_db)
        room_definition = IndexDefinition(prefix=["Polygon:"])
        room_schema = (
            TextField("room-name"),
            TextField("room-no"),
        )

        # Check to see if index is already in db, otherwise create it
        try:
            self.log.debug("Seeing if PoI search indicies exist")
            self.poi_search_client.info()
            self.log.debug("PoI search indicies exist")
        except redis.ResponseError:
            self.log.debug("PoI index does not exist, creating index")
            self.poi_search_client.create_index(poi_schema, definition=poi_definition)

        try:
            self.log.debug("Seeing if room search indicies exist")
            self.room_search_client.info()
            self.log.debug("Room search indicies exist")
        except redis.ResponseError:
            self.log.debug("Index does not exist, creating index")
            self.room_search_client.create_index(
                room_schema, definition=room_definition
            )

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
        # See how to make this faster
        flat_dict = {}

        for key, value in dataclass:
            if key == "tags":
                flat_dict.update(value)

            if isinstance(value, (list, tuple)):
                flat_dict[key] = self.__serialise_list(value)
            elif key != "tags":
                flat_dict[key] = value

        flat_dict = {k: ("" if v is None else v) for k, v in flat_dict.items()}

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

    def __redisgraph_result_to_node(self, res) -> List[PathNode]:
        """
        Transforms a redisgraph result into a list of PathNode objects
        """
        nodes = []
        for node in res.result_set:
            node_dict = node[0].properties
            node_object = self.__flat_dict_to_dataclass(node_dict, PathNode)
            nodes.append(node_object)
        return nodes

    async def save_graph(
        self, graph_name: str, nodes: List[PathNode], edges: List[tuple]
    ) -> None:
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

        # first I want to be able to look up nodes by ID
        lookup_nodes = {}
        for node in nodes:
            lookup_nodes[node.id] = node

        # loop through edges, add nodes from that
        for node_ids in edges:
            nodes = (lookup_nodes[node_ids[0]], lookup_nodes[node_ids[1]])

            node_objs = []
            node_label = "node"
            for index, node in enumerate(nodes):
                if "indoor" in node.tags:
                    node_label = node.tags["indoor"]

                node_alias = "n" + str(node_ids[index])

                if node_alias not in graph.nodes:
                    node_properties = dataclasses.asdict(
                        node, dict_factory=self.__dataclass_to_flat_dict
                    )

                    node_obj = Node(
                        label=node_label, properties=node_properties, alias=node_alias
                    )

                    node_objs.append(node_obj)
                    graph.add_node(node_obj)
                else:
                    node_objs.append(graph.nodes[node_alias])

            # Edges are labelled with whatever the latter node's label is
            # Given the rest of the program there's no place where these differ
            # But maybe this is something to look at later for flexibility
            edge = Edge(node_objs[0], node_label, node_objs[1])
            graph.add_edge(edge)

        self.log.debug("Commiting graph %s", graph_name)
        graph.commit()

    async def load_graph(
        self, graph_name: str
    ) -> (List[PathNode], List[tuple]):  # noqa: E501
        """
        Returns the whole graph nodes, edges

        Args:
            graph_name: graph of which to return nodes and edges from

        Returns:
            tuple with two lists, first element is nodes, second is edges
        """
        nodes, edges = await asyncio.gather(
            self.load_nodes(graph_name), self.load_edges(graph_name)
        )

        return (nodes, edges)

    async def load_nodes(self, graph_name: str) -> List[PathNode]:
        """
        Return all nodes in a given graph

        Args:
            graph_name: graph of which to return nodes from

        Returns:
            List of nodes (see graph_parser for definition of their format)
        """
        graph = Graph(graph_name, self.redis_db)
        query = """MATCH (n:way) RETURN n"""
        result = graph.query(query)

        nodes = []
        for res in result.result_set:
            nodes.append(res[0].properties)

        node_objects = []
        for node in nodes:
            node_objects.append(self.__flat_dict_to_dataclass(node, PathNode))

        return node_objects

    async def load_walls(self, graph_name: str) -> List[PathNode]:
        """
        Return all walls in a given graph

        Args:
            graph_name: graph of which to return nodes from

        Returns:
            List of nodes (see graph_parser for definition of their format)


        This way of doing things could probably just be return every node?
        """
        graph = Graph(graph_name, self.redis_db)
        query = """MATCH (n:wall) RETURN n"""
        result = graph.query(query)

        nodes = []
        for res in result.result_set:
            nodes.append(res[0].properties)

        node_objects = []
        for node in nodes:
            node_objects.append(self.__flat_dict_to_dataclass(node, PathNode))

        return node_objects

    async def load_edges(self, graph_name: str) -> List[tuple]:
        """
        Returns all edges in a given graph

        Args:
            graph_name: graph of which to return edges from

        Returns:
            list of tuples that contain two node ids that are connected
        """
        graph = Graph(graph_name, self.redis_db)
        query = """MATCH (n:way)-->(m:way) RETURN n.id, m.id"""
        result = graph.query(query)

        edges = []
        for res in result.result_set:
            edges.append((res[0], res[1]))

        return edges

    async def load_entries(
        self, graph_name: str, entry_type: Type
    ) -> List[Type]:  # noqa: E501
        """
        Returns all entries in a building matching a dataclass

        Args:
            graph_name (str): Name of graph you want PoIs for
            dataclass (Type): Dataclass to fetch from the DB

        Returns:
            list of dataclass entries for a given graph
        """
        keys = self.redis_db.scan_iter(f"{entry_type.__name__}:{graph_name}:*")
        entries = await asyncio.gather(
            *[self.load_entry(key, entry_type) for key in keys]
        )
        return entries

    async def load_entry(self, key: str, entry_type: Type) -> Type:
        """
        Load a single PoI given a key

        Args:
            key (str): Key that corresponds to the entry
            entry_type (Type): Dataclass of key

        Returns:
            dataclass object of entry
        """
        entry = self.redis_db.hgetall(key)
        entry.pop("ID")

        # decode binary strings (utf-8) -> python string
        entry = {k.decode("utf-8"): v.decode("utf-8") for k, v in entry.items()}

        return self.__flat_dict_to_dataclass(entry, entry_type)

    async def load_entry_by_id(
        self, graph_name: str, entry_id: int, entry_type: Type
    ) -> Type:  # noqa: E501
        """
        Builds key for entry and uses load_entry to load it

        Args:
            graph_name (str): Name of graph entry is in
            entry_id (int): ID of entry to find
            entry_type (Type): Dataclass of key

        Returns:
            dataclass object of entry
        """
        key = f"{entry_type.__name__}:{graph_name}:{str(entry_id)}"
        return await self.load_entry(key, entry_type)

    async def add_entries(self, graph_name: str, entries: List[Type]) -> None:
        """
        Adds a generic record from a list of dataclasses

        Args:
            graph_name (str): name of the graph this PoI is identified
                              with
            entries (List[Type]): list of dataclass objects to add to db
                                  dataclass must have 'id' field
        """
        await asyncio.gather(*[self.add_entry(graph_name, entry) for entry in entries])

    async def add_entry(self, graph_name: str, entry: Type) -> None:
        """
        Add a record to a given graph_name

        Args:
            graph_name (str): name of the graph this room is in
            entry (Type): Generic dataclass object
                          dataclass must have 'id' field
        """
        entry_id = f"{type(entry).__name__}:{graph_name}:{str(entry.id)}"
        mapping = dataclasses.asdict(entry, dict_factory=self.__dataclass_to_flat_dict)
        self.redis_db.hset(entry_id, mapping=mapping)

    async def search_poi_by_name(self, poi_name: str) -> List[PoI]:
        """
        Search for a POI using Redisearch

        Args:
            poi_name (str): Search string for the POI

        Returns:
            Dictionary of POIs that match poi_name search string
        """
        res = self.poi_search_client.search(poi_name)
        pois = []

        for doc in res.docs:
            # transform back to the standard form
            poi = doc.__dict__
            # remove payload object that search returns
            poi.pop("payload")
            poi.pop("ID")
            # remove prefix from redis db
            poi["id"] = poi["id"].rsplit(":", 1)[1]

            poi_object = self.__flat_dict_to_dataclass(poi, PoI)
            pois.append(poi_object)

        return pois

    async def search_poi_by_name_in_graph(self, graph: str, poi_name: str) -> List[PoI]:
        """
        Search then filter for the graph you are looking for
        probably a nicer way of doing this really lol
        """
        results = await self.search_poi_by_name(poi_name)
        return [r for r in results if r.graph == graph]

    async def search_rooms(
        self, graph_name: str, search_string: str
    ) -> Tuple[List[Polygon]]:
        """
        Search for room by name
        """
        # First search the rooms keys for the search string
        res = self.room_search_client.search(search_string)
        rooms = []

        for doc in res.docs:
            # transform back to the standard form
            room = doc.__dict__
            room.pop("payload")
            room.pop("ID")
            # remove prefix from redis db
            room["id"] = room["id"].rsplit(":", 1)[1]
            room_object = self.__flat_dict_to_dataclass(room, Polygon)
            rooms.append(room_object)

        return [r for r in rooms if r.graph == graph_name]

    async def search_room_nodes(
        self, graph_name: str, search_string: str
    ) -> Tuple[List[Polygon], List[PathNode]]:  # noqa: E501
        """
        Search for room nodes by name

        Args:
            graph_name (str): name of the graph to search in
            search_string (str): search string

        Returns:
            List of node objects
        """
        rooms = self.search_rooms(graph_name, search_string)
        if not rooms:
            # If there are no rooms in the search don't do anything
            return []

        nodes = []

        for room in rooms:
            poly_id = room.id
            # Then get the node ids that have that poly_id
            graph = Graph(graph_name, self.redis_db)

            query = """MATCH (n:way {poly_id: $poly_id}) RETURN n"""
            res = graph.query(query, {"poly_id": poly_id})
            nodes.append(self.__redisgraph_result_to_node(res))

        return nodes

    async def get_node_neighbours(
        self, graph_name: str, node_id: int
    ) -> List[PathNode]:
        """
        Returns list of neighbouring nodes to an ID

        Args:
            graph_name (str): name of graph to query
            node_id (int): ID of node you want neighbours of

        Returns:
            List of neighbouring node objects
        """
        graph = Graph(graph_name, self.redis_db)

        query = """MATCH (:way {id: $node_id})-->(m:way) RETURN m"""
        res = graph.query(query, {"node_id": node_id})
        nodes = self.__redisgraph_result_to_node(res)
        return nodes

    async def get_node_by_id(self, graph_name: str, node_id: int) -> PathNode:
        """
        Get one node by it's ID

        Args:
            graph_name (str): Name of the graph to find the node in
            node_id (str): Integer ID of the node
        """
        graph = Graph(graph_name, self.redis_db)

        query = """MATCH (n:way {id: $id}) RETURN n"""
        res = graph.query(query, {"id": node_id})

        if len(res.result_set) == 0:
            raise IndexError("No node with ID found in database")

        nodes = self.__redisgraph_result_to_node(res)

        if len(nodes) > 1:
            warnings.warn(
                "There appears to be more than one node with this ID"
                "Returning the first"
            )

        return nodes[0]
