import numpy as np
import random

A = np.array([
    [0, 5, 4, 5, 6, 3, 20, np.inf, np.inf, np.inf, 10, np.inf, np.inf, np.inf],
    [5, 0, np.inf, 4, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],
    [4, np.inf, 0, 2, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],
    [5, 4, 2, 0, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],
    [6, np.inf, np.inf, np.inf, 0, 4, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],
    [3, np.inf, np.inf, np.inf, 4, 0, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],
    [20, np.inf, np.inf, np.inf, np.inf, np.inf, 0, 2, 5, 4, 25, np.inf, np.inf, np.inf],
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 2, 0, 4, np.inf, np.inf, np.inf, np.inf, np.inf],
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 5, 4, 0, 5, np.inf, np.inf, np.inf, np.inf],
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 4, np.inf, 5, 0, np.inf, np.inf, np.inf, np.inf],
    [10, np.inf, np.inf, np.inf, np.inf, np.inf, 25, np.inf, np.inf, np.inf, 0, 2, 3, 4],
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 2, 0, 4, 5],
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 3, 4, 0, 5],
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 4, 5, 5, 0]
])

pg = 1  # Primer nodo
ug = 14  # Último nodo

nc = len(A)  # Número de nodos
mejora = []  # Mejora de cada generación

class AG(object):
    def __init__(self, Npop, Nit, mu, xrat):
        self.Npop = Npop
        self.Nit = Nit
        self.mu = mu
        self.xrat = xrat
        self.Nkeep = int(np.ceil(xrat * Npop))  # Número de individuos a mantener

    def generate_random_path(self):
        path = [pg - 1]
        last_neighbour = []
        print(path)
        while path[-1] != ug - 1:
            neighbors = [i for i in range(nc) if A[path[-1], i] != np.inf and A[path[-1], i] != 0]
            if neighbors == last_neighbour and path[-1] != pg - 1:
                path.pop()
                if len(path) == 0:
                    path.append(pg - 1)
                continue
            last_neighbour = neighbors
            next_node = random.choice(neighbors)
            if next_node in path:  # Avoid loops
                continue
            path.append(next_node)
        return path

    def poblacion(self):
        # Genera individuos con longitud variable
        return [self.generate_random_path() for _ in range(self.Npop)]

    def probabilidad(self):
        p = np.array(range(1, self.Nkeep + 1))
        p = (self.Nkeep - p + 1) / sum(p)
        p = np.cumsum(p)
        return p

    def seleccion(self, p):
        u = random.random()
        for i in range(len(p)):
            if u <= p[i]:
                return i

    def cruce(self, A, B):
        # Cruce ordenado para rutas de longitud variable
        corte = random.randint(1, min(len(A), len(B)) - 1)
        hijo = A[:corte]
        hijo.extend(n for n in B if n not in hijo)
        return hijo

    def cruce_poblacion(self, pop, P):
        nuevos = []
        for _ in range(self.Nkeep, self.Npop):
            p1 = self.seleccion(P)
            p2 = self.seleccion(P)
            nuevos.append(self.cruce(pop[p1], pop[p2]))
        pop[self.Nkeep:] = nuevos
        return pop

    def mutacion(self, pop):
        for i in range(len(pop)):
            if random.random() < self.mu:
                if random.random() < 0.5 and len(pop[i]) > 2:
                    # Eliminar un nodo aleatorio
                    pop[i].pop(random.randint(1, len(pop[i]) - 2))
                else:
                    # Insertar un nodo aleatorio
                    nodo = random.randint(1, nc - 1)
                    if nodo not in pop[i]:
                        pos = random.randint(0, len(pop[i]))
                        pop[i].insert(pos, nodo)
        return pop

    def funcion_costo(self, x):
        d = 0
        for i in range(len(x) - 1):
            d += A[x[i], x[i + 1]]
            if d == np.inf:
                return np.inf
        return d

    def evolucion(self):
        pop = self.poblacion()
        P = self.probabilidad()
        for _ in range(self.Nit):
            costos = [self.funcion_costo(ind) for ind in pop]
            indices = np.argsort(costos)
            pop = [pop[i] for i in indices]
            mejora.append(costos[indices[0]])
            pop = self.cruce_poblacion(pop, P)
            pop = self.mutacion(pop)

        # Mejor solución final
        costos = [self.funcion_costo(ind) for ind in pop]
        mejor = pop[np.argmin(costos)]
        return {"solucion": mejor, "costo": self.funcion_costo(mejor)}

def main():
    ag = AG(180, 1000, 0.01, 0.6)
    sol = ag.evolucion()
    print(sol)

if __name__ == "__main__":
    main()
