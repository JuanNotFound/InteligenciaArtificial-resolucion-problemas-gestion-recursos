import numpy as np

from src.soporte_algoritmos.Metodos_auxiliares_evo_adv import Metodos_auxiliares_evo_adv
from src.soporte_algoritmos.Nodo import Nodo


class Algoritmo_genetico_avanzado:

    # -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def iniciar(semilla: int, n_tarea: int, n_recurso: int, duraciones: [int], recursos: [int], dependencias: [(int,int)]) -> [int]:
        np.random.seed(semilla)

        N = 150
        G = 50
        p_cruce = 0.9
        p_mut = 0.1

        solucion = Metodos_auxiliares_evo_adv.mejor_individuo(
            Algoritmo_genetico_avanzado.algoritmo(n_tarea, n_recurso, duraciones, recursos, dependencias, N, G, p_cruce, p_mut), n_recurso, recursos, dependencias, duraciones).t_inicio
        if solucion.count(None) == 0:
            nodo_solucion = Nodo(solucion)
            print(nodo_solucion.calcular_makespan(duraciones))
            print(solucion)
            return solucion
        else:
            return []

    # -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def algoritmo(n_tarea: int, n_recurso: int, duraciones: [int], recursos: [int], dependencias: [int], N: int, G: int, p_cruz: float, p_mut: float) -> [Nodo]:

        poblacion_nodos = []
        for i in range(N):
            poblacion_nodos.append(Metodos_auxiliares_evo_adv.generar_individuo(n_tarea, dependencias, duraciones, recursos, n_recurso))

        for i in range(G):
            poblacion_nodos = Metodos_auxiliares_evo_adv.selecion_torneo(poblacion_nodos, n_recurso, recursos, dependencias, duraciones)
            poblacion_cruzada = []
            for j in range(int(len(poblacion_nodos) / 2)):
                cruzados = Metodos_auxiliares_evo_adv.cruce_intercambio(poblacion_nodos[j], poblacion_nodos[j + 1],
                                                                        n_tarea, p_cruz)
                poblacion_cruzada.append(cruzados[0])
                poblacion_cruzada.append(cruzados[1])
            proxima_generacion = []
            for j in range(len(poblacion_cruzada)):
                mutado = Metodos_auxiliares_evo_adv.mutacion_intercambio(poblacion_cruzada[j], n_tarea, p_mut)
                proxima_generacion.append(mutado)
            poblacion_nodos = proxima_generacion
        return poblacion_nodos

    # -----------------------------------------------------------------------------------------------------------------------
