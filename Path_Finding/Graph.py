class Graph:

    # create an edge between the start node and the end node
    def add_edge(self, adj, start, end):
        adj[start].append(end)
        adj[start].append(start)

    #Do a breth first seach algorithm to find a route that gose though the least number of nodes, will chage laster to inldue weigts
    def breath_first_search(self, adj, start, end, vertex, previous, distance):

        #make an emty list that will que up all nodes to search
        queue = []

        visited = [False for i in range(vertex)]

        #fill distace nad previous will arbity values distace refexrs to the umebr of nodes and previous refers to the nodes alreay seached
        for i in range(vertex):
            distance[i] = 10000
            previous[i] = -1
        #add the start node to the visted path to prevet the path finder form inclueing it in the reults
        visited[start] = True
        distance[start] = 0
        queue.append(start)

        #whilever there is stuff in the queue coninue to seach though it
        while (len(queue) != 0):
            u = queue[0]
            queue.pop(0)
            #check all the neighbors to the currnat node and visit them
            for i in range(len(adj[u])):
                #if a path is found return ture indicating there was a path that could be found else retun flase as there is no path
                if not visited[adj[u][i]]:
                    visited[adj[u][i]] = True
                    distance[adj[u][i]] = distance[u] + 1
                    previous[adj[u][i]] = u
                    queue.append(adj[u][i])

                    if (adj[u][i] == end):
                        return True
        return False

    #literly used for prting the path, this will be removed when we have an actual GUI ,this is purely for testing purposes
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
    start = 0
    end = 7
    v = 8
    adj = [[] for i in range(v)]
    #cretae the edges of the grpah based on the ajacency table and the naighboring nodes
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

    Graph.print_path(g, adj, start, end, v)
