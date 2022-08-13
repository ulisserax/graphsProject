import numpy as np

class Graph:
    def __init__(self, qtVertices, directed=False, weighted=False):
        self.tamanho = 0
        self.ordem = qtdVertices
        self.matriz_alcancabilidade = None
        self.direcionado = direcionado
        self.ponderado = ponderado
        self.matriz_adjacencias = np.ones((qtVertices, qtVertices)) * np.inf if self.ponderado else np.zeros((qtVertices, qtVertices))

    def adiciona_aresta(self, u, v, peso=1):
        assert u < self.matriz_adjacencias.shape[0] and \
               v < self.matriz_adjacencias.shape[1], "Índice u ou v fora da matriz"
        self.matriz_adjacencias[u,v] = peso
        if not self.direcionado:
            self.matriz_adjacencias[v,u] = peso
        if not self.tem_aresta(u, v):
            self.tamanho += 1

    def remove_aresta(self, u, v):
        assert u < self.matriz_adjacencias.shape[0] and \
               v < self.matriz_adjacencias.shape[1], "Índice u ou v fora da matriz"
        if self.tem_aresta(u, v):
            self.tamanho -= 1

        novo_valor = 0 if not self.ponderado else np.inf
        self.matriz_adjacencias[u,v] = novo_valor
        if not self.direcionado:
            self.matriz_adjacencias[v,u] = novo_valor

    def tem_aresta(self, u, v):
        assert u < self.matriz_adjacencias.shape[0] and \
               v < self.matriz_adjacencias.shape[1], "Índice u ou v fora da matriz"
        if self.ponderado:
            return self.matriz_adjacencias[u,v] != np.inf
        return self.matriz_adjacencias[u,v] != 0

    def grau_entrada(self, u):
        assert u < self.matriz_adjacencias.shape[0], "Índice u fora da matriz"
        grau_entrada = 0
        valor_nulo = 0 if not self.ponderado else np.inf
        for i in range(self.ordem):
            if self.matriz_adjacencias[i][u] != valor_nulo:
                grau_entrada += 1
        return grau_entrada

    def grau_saida(self, u):
        assert u < self.matriz_adjacencias.shape[0], "Índice u fora da matriz"
        grau_saida = 0
        valor_nulo = 0 if not self.ponderado else np.inf
        for i in range(self.ordem):
            if self.matriz_adjacencias[u][i] != valor_nulo:
                grau_saida += 1
        return grau_saida

    def grau(self, u):
        assert u < self.matriz_adjacencias.shape[0], "Índice u fora da matriz"
        grau = 0
        valor_nulo = 0 if not self.ponderado else np.inf
        for i in range(self.ordem):
            if self.matriz_adjacencias[i][u] != valor_nulo:
                grau += 1
            if self.ponderado:
                if self.matriz_adjacencias[u][i] != valor_nulo:
                    grau += 1
        return grau

    def retorna_adjacentes(self, u):
        assert u < self.matriz_adjacencias.shape[0], "Índice u fora da matriz"
        valor_nulo = 0 if not self.ponderado else np.inf
        return [i for i,v in enumerate(self.matriz_adjacencias[u]) if v != valor_nulo]

    def imprime_matriz_adjacencias(self):
        for row in self.matriz_adjacencias:
            print(row)

    def warshall_algorithm(self):
        if self.direcionado:
            self.matriz_alcancabilidade = (self.matriz_adjacencias != np.inf).astype(int)
        else:
            self.matriz_alcancabilidade = self.matriz_adjacencias.copy()
        n = self.matriz_adjacencias.shape[0]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    self.matriz_alcancabilidade[i][j] = self.matriz_alcancabilidade[i][j] or \
                                                    (self.matriz_alcancabilidade[i][k] and self.matriz_alcancabilidade[k][j])

    def possui_caminho(self, u, v):
        assert u < self.matriz_adjacencias.shape[0] and \
               v < self.matriz_adjacencias.shape[1], "Índice u ou v fora da matriz"
        if self.matriz_alcancabilidade is None:
            self.warshall_algorithm()

        return self.matriz_alcancabilidade[u][v]

    def is_Eulerian(self):
        if self.matriz_alcancabilidade is None:
            self.warshall_algorithm()

        if not np.all((self.matriz_alcancabilidade == 1)):
            print("Não Euleriano")
            return 0

        odd_count = 0
        for u in range(self.ordem):
            if self.direcionado:
                print(f"Diff: {abs(self.grau_entrada(u) - self.grau_saida(u))}")
                if abs(self.grau_entrada(u) - self.grau_saida(u)) == 1:
                    odd_count += 1
                elif abs(self.grau_entrada(u) - self.grau_saida(u)) > 1:
                    print("Não Euleriano")
                    return 0
            else:
                print(f"grau: {self.grau(u)}")
                if self.grau(u) % 2 != 0:
                    odd_count += 1
            if odd_count > 2:
                print("Não Euleriano")
                return 0

        print(odd_count)
        if odd_count == 0:
            print("Euleriano")
            return 1
        elif odd_count == 2:
            print("Semi-Euleriano")
            return 2
        else:
            print("Não Euleriano")
            return 0

G = Grafo(4, direcionado=True)
G.adiciona_aresta(0,1)
G.adiciona_aresta(1,3)
G.adiciona_aresta(2,1)
G.adiciona_aresta(0,2)
G.adiciona_aresta(3,0)
G.adiciona_aresta(1,2)
G.adiciona_aresta(3,2)

for i in range(4):
    for j in range(4):
        print(f"Possui caminho entre {i} e {j}: {G.possui_caminho(i,j)}")

print(G.grau_entrada(3))
print(G.grau_saida(3))
print(G.grau(3))
print(G.matriz_alcancabilidade)
G.imprime_matriz_adjacencias()
print(G.is_Eulerian())