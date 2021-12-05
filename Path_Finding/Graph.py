from Parser import Parser


class Graph:

    # create an edge between the start node and the end node
    def add_edge(self, adj, start, end):
        adj[start].append(end)
        adj[start].append(start)

    # Do a breath first search algorithm to find a route that goes though the least number of nodes
    # TODO change to include weights, this will be done later
    def breath_first_search(self, adj, start, end, vertex, previous, distance):

        # make an empty list that will que up all nodes to search
        queue = []

        visited = [False for i in range(vertex)]

        # fill distance nad previous will arbitrary values distance refers to the number of nodes and previous
        # refers to the nodes already searched
        for i in range(vertex):
            distance[i] = 0
            previous[i] = -1
        # add the start node to the visited path to prevent the path finder form including it in the results
        visited[start] = True
        distance[start] = 0
        queue.append(start)
        # while ever there is stuff in the queue continue to search though it
        while (len(queue) != 0):
            u = queue[0]
            queue.pop(0)
            # check all the neighbors to the current node and visit them
            for i in range(len(adj[u])):
                # if a path is found return ture indicating there was a path that could be found else return false
                if not visited[adj[u][i]]:
                    visited[adj[u][i]] = True
                    distance[adj[u][i]] = distance[u] + 1
                    previous[adj[u][i]] = u
                    queue.append(adj[u][i])

                    if (adj[u][i] == end):
                        return True
        return False

    # used for printing the path, this will be removed when we have an actual GUI for testing purposes
    def print_path(self, adj, start, end, vertex):

        previous = [0 for i in range(vertex)]
        distance = [0 for i in range(vertex)]
        if self.breath_first_search(adj, start, end, vertex, previous, distance) is False:
            print("No path could be found")

        path = []
        crawl = end
        path.append(crawl)

        while previous[crawl] != -1:
            path.append(previous[crawl])
            crawl = previous[crawl]

        print("Shortest Path is " + str(distance[end]))
        print("\nPath is: ")
        for i in range(len(path) - 1, -1, -1):
            print(path[i])


if __name__ == '__main__':
    g = Graph()
    p = Parser("/home/kevan/Documents/Uni/comp5530m/comp5530m_mapping_project/Json/simple-house")
    start = 0
    end = 18
    v = len(p.nodes)  # the number of vertices is the number of nodes found by the parser
    # create the edges of the graph based on the adjacency's table and the neighboring nodes
    adj = [[] for i in range(v)]
    # loop though the list of edges and created edges on the graph.
    for i in p.edges:
        Graph.add_edge(g, adj, i[0], i[1])

    Graph.print_path(g, adj, start, end, v)
