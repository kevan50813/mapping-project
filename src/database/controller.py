""" Redis DB controller using RedisGraph """
import redis
from redisgraph import Node, Edge, Graph


class Controller():
    def __init__(self, host, port):
        db = redis.Redis(host=host, port=port)
        # TODO remove this for persistence
        db.execute_command("FLUSHALL")
        self.graph = Graph('nodes', db)

    def save_graph(self, nodes, edges):
        # clean None from dict
        nodes = [{k: ('' if v is None else v)
                  for k, v in d.items()} for d in nodes]

        queue = []
        visited = []

        queue.append(nodes[0])
        while len(queue) != 0:
            u = queue[0]
            queue.pop(0)

            if "coordinates" in u.keys():
                u["lat"] = u["coordinates"][0]
                u["lon"] = u["coordinates"][1]
                u.pop("coordinates", None)
            node1 = Node(label='node', properties=u)
            self.graph.add_node(node1)

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

                    node2 = Node(label='node', properties=n)
                    edge = Edge(node1, 'path', node2)
                    self.graph.add_node(node2)
                    self.graph.add_edge(edge)

                    visited.append(n)
                    queue.append(n)
        self.graph.commit()
