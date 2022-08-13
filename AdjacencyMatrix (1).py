import numpy as np

class Graph:
    def __init__(self, qtVertices, directed=False, weighted=False):
        self.size = 0
        self.order = qtVertices
        self.reachability_matrix = None
        self.directed = directed
        self.weighted = weighted
        self.adjancency_matrix = np.ones((qtVertices, qtVertices)) * np.inf if self.weighted else np.zeros((qtVertices, qtVertices))

    def add_edge(self, u, v, weight=1):
        assert u < self.adjancency_matrix.shape[0] and \
               v < self.adjancency_matrix.shape[1], "Index u or v out of matrix"
        self.adjancency_matrix[u,v] = weight
        if not self.directed:
            self.adjancency_matrix[v,u] = weight
        if not self.has_egde(u, v):
            self.size += 1

    def remove_edge(self, u, v):
        assert u < self.adjancency_matrix.shape[0] and \
               v < self.adjancency_matrix.shape[1], "Index u or v out of matrix"
        if self.has_edge(u, v):
            self.size -= 1

        new_value = 0 if not self.weighted else np.inf
        self.adjancency_matrix[u,v] = new_value
        if not self.directed:
            self.adjancency_matrix[v,u] = new_value

    def has_edge(self, u, v):
        assert u < self.adjancency_matrix.shape[0] and \
               v < self.adjancency_matrix.shape[1], "Index u or v out of matrix"
        if self.weighted:
            return self.adjancency_matrix[u,v] != np.inf
        return self.adjancency_matrix[u,v] != 0

    def input_degree(self, u):
        assert u < self.adjancency_matrix.shape[0], "Index u out of matrix"
        input_degree = 0
        null_value = 0 if not self.weighted else np.inf
        for i in range(self.order):
            if self.adjancency_matrix[i][u] != null_value:
                input_degree += 1
        return input_degree

    def output_degree(self, u):
        assert u < self.adjancency_matrix.shape[0], "Index u out of matrix"
        output_degree = 0
        null_value = 0 if not self.weighted else np.inf
        for i in range(self.order):
            if self.adjancency_matrix[u][i] != null_value:
                output_degree += 1
        return output_degree

    def degree(self, u):
        assert u < self.adjancency_matrix.shape[0], "Index u out of matrix"
        degree = 0
        null_value = 0 if not self.weighted else np.inf
        for i in range(self.order):
            if self.adjancency_matrix[i][u] != null_value:
                degree += 1
            if self.weighted:
                if self.adjancency_matrix[u][i] != null_value:
                    degree += 1
        return degree

    def return_adjacents(self, u):
        assert u < self.adjancency_matrix.shape[0], "Index u out of matrix"
        null_value = 0 if not self.weighted else np.inf
        return [i for i,v in enumerate(self.adjancency_matrix[u]) if v != null_value]

    def print_adjacency_matrix(self):
        for row in self.adjancency_matrix:
            print(row)

    def warshall_algorithm(self):
        if self.directed:
            self.reachability_matrix = (self.adjancency_matrix != np.inf).astype(int)
        else:
            self.reachability_matrix = self.adjancency_matrix.copy()
        n = self.adjancency_matrix.shape[0]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    self.reachability_matrix[i][j] = self.reachability_matrix[i][j] or \
                                                    (self.reachability_matrix[i][k] and self.reachability_matrix[k][j])

    def has_path(self, u, v):
        assert u < self.adjancency_matrix.shape[0] and \
               v < self.adjancency_matrix.shape[1], "Index u or v out of matrix"
        if self.reachability_matrix is None:
            self.warshall_algorithm()

        return self.reachability_matrix[u][v]

    def is_Eulerian(self):
        if self.reachability_matrix is None:
            self.warshall_algorithm()

        if not np.all((self.reachability_matrix == 1)):
            print("Non-Eulerian")
            return 0

        odd_count = 0
        for u in range(self.order):
            if self.directed:
                print(f"Diff: {abs(self.input_degree(u) - self.output_degree(u))}")
                if abs(self.input_degree(u) - self.output_degree(u)) == 1:
                    odd_count += 1
                elif abs(self.input_degree(u) - self.output_degree(u)) > 1:
                    print("Non-Eulerian")
                    return 0
            else:
                print(f"degree: {self.degree(u)}")
                if self.degree(u) % 2 != 0:
                    odd_count += 1
            if odd_count > 2:
                print("Non-Eulerian")
                return 0

        print(odd_count)
        if odd_count == 0:
            print("Eulerian")
            return 1
        elif odd_count == 2:
            print("Semi-Eulerian")
            return 2
        else:
            print("Non-Eulerian")
            return 0

G = Graph(4, directed=True)
G.add_edge(0,1)
G.add_edge(1,3)
G.add_edge(2,1)
G.add_edge(0,2)
G.add_edge(3,0)
G.add_edge(1,2)
G.add_edge(3,2)

for i in range(4):
    for j in range(4):
        print(f"It has path between {i} e {j}: {G.has_path(i,j)}")

print(G.input_degree(3))
print(G.input_degree(3))
print(G.degree(3))
print(G.reachability_matrix)
G.print_adjacency_matrix()
print(G.is_Eulerian())