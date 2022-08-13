class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, u):
        if u not in self.adjacency_list.keys():
            self.adjacency_list[u] = []

    def add_edge(self, u, v, weight):
        assert u in self.adjacency_list.keys() and v in self.adjacency_list.keys(), "Some of the nodes have not been" \
                                                                                    "added on the graph."
        self.adjacency_list[u].append((v, weight))

    def remove_edge(self, u, v):
        assert u in self.adjacency_list.keys(), "the node U have not been added on the graph."
        for edge in self.adjacency_list[u]:
            if edge[0] == v:
                self.adjacency_list[u].remove(edge)
                break

    def remove_vertex(self, u):
        assert u in self.adjacency_list.keys(), "The node U did not exist on the graph."
        del self.adjacency_list[u]
        for key in self.adjacency_list.keys():
            for edge in self.adjacency_list[key]:
                if edge[0] == u:
                    self.adjacency_list[key].remove(edge)
                    break

    def has_edge(self, u, v):
        assert u in self.adjacency_list.keys(), "The node U has not been added on the graph."
        for edge in self.adjacency_list[u]:
            if edge[0] == v:
                return True
        return False

    def degree(self, u):
        assert u in self.adjacency_list.keys(), "The node U has not been added on the graph."
        outdegree = len(self.adjacency_list[u])
        indegree = 0
        for key in self.adjacency_list.keys():
            if key != u:
                for edge in self.adjacency_list[u]:
                    if edge[0] == u:
                        indegree += 1
                        break

        return outdegree + indegree

    def weight(self, u, v):
        if self.has_edge(u, v):
            for edge in self.adjacency_list[u]:
                if edge[0] == v:
                    return edge[1]

    def print_adjacent_list(self):
        for key in self.adjacency_list.keys():
            print(key, end=": ")
            for relation in self.adjacency_list[key]:
                print(str(relation) + " -> ", end="")
            print()

    def dijkstra(self, start):
        if start not in self.adjacency_list.keys():
            print("The matrix does not have the key passed as the beginning.")
            return

        visited = {}

        current_node = start
        current_distance = 0
        unvisited = {node: (None, None) for node in self.adjacency_list.keys()}
        unvisited[current_node] = (None, current_distance)

        while True:
            for neighbour, distance in self.adjacency_list[current_node]:

                if neighbour not in unvisited:
                    continue

                new_distance = current_distance + distance

                if unvisited[neighbour][1] is None or unvisited[neighbour][1] > new_distance:
                    unvisited[neighbour] = (current_node, new_distance)

            del unvisited[current_node]
            if not unvisited:
                break

            keys = [node for node in unvisited.items() if node[1][1] != None]

            new_node = sorted(keys, key=lambda tup: tup[1][1])[0]
            visited[new_node[0]] = (current_node, new_node[1][1])
            current_node = new_node[0]
            current_distance = new_node[1][1]

        print(visited)



G = Graph()
G.add_vertex("A")
G.add_vertex("B")
G.add_vertex("C")
G.add_vertex("D")
G.add_vertex("E")
G.add_vertex("F")
G.add_edge("A", "B", 4)
G.add_edge("A", "C", 2)
G.add_edge("C", "B", 1)
G.add_edge("C", "D", 8)
G.add_edge("C", "E", 10)
G.add_edge("B", "D", 5)
G.add_edge("D", "F", 6)
G.add_edge("D", "E", 2)
G.add_edge("E", "F", 2)
G.dijkstra("A")