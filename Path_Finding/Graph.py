class Graph:

    # create an edge between the start node and the end node
    def add_edge(self, adj, start, end):
        adj[start].append(end)
        adj[start].append(start)

    def breath_first_search(self, adj, start, end, vertex, previous, distance):
        queue = []

        visited = [False for i in range(vertex)]

        for i in range(vertex):
            distance[i] = 10000
            previous[i] = -1

        visited[start] = True
        distance[start] = 0
        queue.append(start)

        while (len(queue) != 0):
            u = queue[0]
            queue.pop(0)
            for i in range(len(adj[u])):

                if not visited[adj[u][i]]:
                    visited[adj[u][i]] = True
                    distance[adj[u][i]] = distance[u] + 1
                    previous[adj[u][i]] = u
                    queue.append(adj[u][i])

                    if (adj[u][i] == end):
                        return True
        return False

    def print_path(self, adj, start, end, vertex):

        previous = [0 for i in range(vertex)]
        distance = [0 for i in range(vertex)]
        if self.breath_first_search(adj, start, end, vertex, previous, distance) == False:
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
    v = 8
    adj = [[] for i in range(v)]
    Graph.add_edge(g, adj, 0, 1)
    Graph.add_edge(g, adj, 0, 3)
    Graph.add_edge(g, adj, 1, 2)
    Graph.add_edge(g, adj, 3, 4)
    Graph.add_edge(g, adj, 3, 7)
    Graph.add_edge(g, adj, 4, 5)
    Graph.add_edge(g, adj, 4, 6)
    Graph.add_edge(g, adj, 4, 7)
    Graph.add_edge(g, adj, 5, 6)
    Graph.add_edge(g, adj, 6, 7)
    start = 0
    end = 7

    Graph.print_path(g, adj, start, end, v)
