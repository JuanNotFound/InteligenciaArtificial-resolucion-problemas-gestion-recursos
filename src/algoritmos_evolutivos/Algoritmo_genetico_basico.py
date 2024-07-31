import numpy as np

from src.soporte_algoritmos.Metodos_auxiliares_evo import Metodos_auxiliares_evo
from src.soporte_algoritmos.Nodo import Nodo


class Algoritmo_genetico_basico:

# -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def iniciar(semilla: int, n_tarea: int, n_recurso: int, duraciones: [int], recursos: [int], dependencias: [(int,int)]) -> [int]:
        np.random.seed(semilla)
        t_maximo_posible = sum(duraciones)

        N = 100
        G = 100
        Pcross = 0.9
        mut = 0.1
        alphabet = []

        for i in range(t_maximo_posible):
            alphabet.append(i + 1)
        solucion: Nodo = Metodos_auxiliares_evo.mejor_individuo(
            Algoritmo_genetico_basico.algoritmo(n_tarea, n_recurso, duraciones, recursos, dependencias, N, G, Pcross,
                                                mut, alphabet), n_recurso, recursos, dependencias, duraciones)

        if np.sum(np.equal(solucion, None)) == 0:
            print(solucion.calcular_makespan(duraciones))
            print(solucion.t_inicio)
            return solucion.t_inicio
        else:
            return []

# -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def algoritmo(n_tarea: int, n_recursos: int, duraciones: [int], recursos: [int], dependencias: [(int,int)], N: int, G: int, p_cruce:float, p_mut:float, alphabet: []) -> [Nodo]:

        poblacion_nodos = []  # array vacio de poblacion

        # Generación de población
        for i in range(N):
            poblacion_nodos.append(Nodo(np.random.choice(alphabet, size=n_tarea, replace=True)))

        for i in range(G):
            poblacion_nodos = Metodos_auxiliares_evo.seleccion_por_ruleta_de_la_fortuna(poblacion_nodos, n_recursos,
                                                                                        recursos, dependencias,
                                                                                        duraciones)

            if len(poblacion_nodos) % 2 == 0:
                poblacion_cruzada = []

                for j in range(int(len(poblacion_nodos) / 2)):
                    cruce = Metodos_auxiliares_evo.cruce_punto(poblacion_nodos[j], poblacion_nodos[j + 1], n_tarea, p_cruce)
                    poblacion_cruzada.append(cruce[0])
                    poblacion_cruzada.append(cruce[1])
            else:

                poblacion_cruzada = []
                for j in range(int(len(poblacion_nodos) / 2)):
                    cruce = Metodos_auxiliares_evo.cruce_punto(poblacion_nodos[j], poblacion_nodos[j + 1], n_tarea, p_cruce)
                    poblacion_cruzada.append(cruce[0])
                    poblacion_cruzada.append(cruce[1])

            proxima_poblacion = []
            for j in range(len(poblacion_cruzada)):
                mutado = Metodos_auxiliares_evo.mutacion(poblacion_cruzada[j], n_tarea, alphabet, p_mut)
                proxima_poblacion.append(mutado)
            poblacion_nodos = proxima_poblacion

        return poblacion_nodos

# -----------------------------------------------------------------------------------------------------------------------

