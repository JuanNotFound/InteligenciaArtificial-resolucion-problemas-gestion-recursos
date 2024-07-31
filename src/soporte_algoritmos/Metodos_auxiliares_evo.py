import numpy as np
from numpy.random import random

from src.soporte_algoritmos.Metodos_auxiliares import Metodos_auxiliares
from src.soporte_algoritmos.Nodo import Nodo


class Metodos_auxiliares_evo(Metodos_auxiliares):

# -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def seleccion_por_ruleta_de_la_fortuna(poblacion_nodos, n_recurso: int, recursos: [int], dependencias: [(int, int)],
                                           duraciones: [int]):
        fitnesstotal = 0
        fitnessparciales = []
        probabilidades = []
        soluciones = []
        for i in range(len(poblacion_nodos)):
            fitnessparciales.append(
                Metodos_auxiliares_evo.fitness(poblacion_nodos[i], n_recurso, recursos, dependencias, duraciones))
            fitnesstotal += fitnessparciales[i]
        if fitnesstotal == 0:
            for i in range(len(poblacion_nodos)):
                nodo = np.random.choice(poblacion_nodos)
                soluciones.append(nodo)
        else:
            for i in range(len(poblacion_nodos)):
                probabilidades.append(fitnessparciales[i] / fitnesstotal)
            for i in range(len(poblacion_nodos)):
                soluciones.append(np.random.choice(poblacion_nodos, p=probabilidades, replace=True))
        return soluciones

# -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def cruce_punto(individuo_nodo1, individuo_nodo2, n_tareas, p_cruz):
        soluciones = []
        if random() < p_cruz:
            Array1 = individuo_nodo1.t_inicio.copy()
            Array2 = individuo_nodo2.t_inicio.copy()
            child1 = Nodo(Array1)
            child2 = Nodo(Array2)
            punto_cruce = np.random.randint(1, n_tareas)
            for i in range(punto_cruce):
                child1.t_inicio[i] = individuo_nodo2.t_inicio[i]
                child2.t_inicio[i] = individuo_nodo1.t_inicio[i]
            soluciones.append(child1)
            soluciones.append(child2)
            return soluciones
        else:
            soluciones.append(individuo_nodo1)
            soluciones.append(individuo_nodo2)
            return soluciones

# -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def mutacion(individuo_nodo: Nodo, n_tarea, alphabet, p_mut):
        if random() < p_mut:
            child = Nodo(individuo_nodo.t_inicio)
            punto_mutacion = np.random.randint(0, n_tarea)
            child.t_inicio[punto_mutacion] = np.random.choice(alphabet)
            return child
        else:
            return individuo_nodo

# -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def fitness(individuo_nodo: Nodo, n_recurso: int, recursos: [int], dependencias: [(int, int)], duraciones: [int]):
        resultado = 0
        if (Metodos_auxiliares.comprobar_dependencias_y_recursos(individuo_nodo, n_recurso, duraciones, recursos, dependencias)):
            return  1 / individuo_nodo.calcular_makespan(duraciones)


        else:
            return resultado

# -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def mejor_individuo(poblacion_nodos, n_recurso, recursos, dependencias: [(int, int)], duraciones: [int]) -> Nodo:
        mejor = 0
        for i in range(len(poblacion_nodos)):
            if (Metodos_auxiliares.comprobar_dependencias_y_recursos(poblacion_nodos[i], n_recurso, duraciones, recursos,
                                                                    dependencias)):
                if Metodos_auxiliares_evo.fitness(poblacion_nodos[i], n_recurso, recursos, dependencias, duraciones) > Metodos_auxiliares_evo.fitness(
                        poblacion_nodos[mejor], n_recurso, recursos, dependencias, duraciones):
                    mejor = i
        return poblacion_nodos[mejor]

# -----------------------------------------------------------------------------------------------------------------------

