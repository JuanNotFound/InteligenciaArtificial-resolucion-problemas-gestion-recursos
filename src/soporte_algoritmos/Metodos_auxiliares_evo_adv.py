import numpy as np
from numpy.random import random

from src.soporte_algoritmos.Metodos_auxiliares import Metodos_auxiliares
from src.soporte_algoritmos.Metodos_auxiliares_evo import Metodos_auxiliares_evo
from src.soporte_algoritmos.Nodo import Nodo


class Metodos_auxiliares_evo_adv(Metodos_auxiliares_evo):

    # -----------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def generar_individuo(n_tarea: int, dependencias: [(int,int)], duraciones:[int], recursos: [int], n_recurso: int) -> Nodo:
        nodo_actual = Nodo([None] * n_tarea)
        duracion_maxima = sum(duraciones)
        lista = []

        while nodo_actual.t_inicio.count(None) > 0:
            lista = []
            lista_no_None = filter(lambda x: x is not None, nodo_actual.t_inicio)
            valor_maximo = max(lista_no_None, default=None) if lista_no_None else None

            if valor_maximo is None:
                for i in range(len(nodo_actual.t_inicio)):
                    nodo = Nodo(nodo_actual.t_inicio.copy())
                    nodo.t_inicio[i] = 0
                    if Metodos_auxiliares.comprobar_dependencias_y_recursos(nodo, n_recurso, duraciones, recursos,dependencias):
                        lista.append(nodo)
            else:
                salir = False
                for i in range(duracion_maxima):
                    for j in range(len(nodo_actual.t_inicio)):
                        if nodo_actual.t_inicio[j] == None:
                            nodo = Nodo(nodo_actual.t_inicio.copy())
                            nodo.t_inicio[j] = valor_maximo + i

                            if Metodos_auxiliares.comprobar_dependencias_y_recursos(nodo, n_recurso, duraciones, recursos, dependencias):
                                lista.append(nodo)
                                salir = True
                    if salir:
                        break
            nodo_actual = Metodos_auxiliares_evo_adv.escoger_ruleta_de_la_fortuna(lista, n_recurso, recursos, dependencias, duraciones)
        nodo_actual = max(lista, key=lambda x: Metodos_auxiliares_evo_adv.fitness(x, n_recurso, recursos, dependencias, duraciones))
        return nodo_actual

    # -----------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def escoger_ruleta_de_la_fortuna(poblacion_nodos: [Nodo], n_recurso: int, recursos: [int], dependencias: [(int,int)], duraciones: [int]) -> Nodo:
        fitness_total = 0
        fitness_parcial = []
        probabilidades = []

        for i in range(len(poblacion_nodos)):
            fitness_parcial.append(
                Metodos_auxiliares_evo_adv.fitness(poblacion_nodos[i], n_recurso, recursos, dependencias, duraciones))
            fitness_total += fitness_parcial[i]
        if fitness_total == 0:
            nodo = np.random.choice(poblacion_nodos)
            return nodo
        else:
            for i in range(len(poblacion_nodos)):
                probabilidades.append(fitness_parcial[i] / fitness_total)
            return np.random.choice(poblacion_nodos, p=probabilidades, replace=True)

    # -----------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def selecion_torneo(poblacion_nodos: [Nodo], n_recurso: int, recursos: [int], dependencias: [(int, int)], duraciones: [int]) -> []:
        resultado_seleccion = []
        for i in range(len(poblacion_nodos)):
            seleccionados = []
            for j in range(2):
                seleccionados.append(np.random.choice(poblacion_nodos))
            resultado_seleccion.append(max(seleccionados, key=lambda x: Metodos_auxiliares_evo_adv.fitness(x, n_recurso, recursos, dependencias, duraciones)))
        return resultado_seleccion

    # -----------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def cruce_intercambio(nodo_padre1: Nodo, nodo_padre2: Nodo, n_tarea: int, p_cruce: float) -> []:
        resultado_cruce = []
        if random() < p_cruce:
            t_inicio1 = nodo_padre1.obtener_copia()
            t_inicio2 = nodo_padre2.obtener_copia()

            descendiente1 = Nodo(t_inicio1)
            descendiente2 = Nodo(t_inicio2)
            punto_c1 = np.random.randint(1, n_tarea)
            punto_c2 = np.random.randint(1, n_tarea)
            if punto_c1 > punto_c2:
                punto_c1 = punto_c2
                punto_c2 = punto_c1
            for i in range(punto_c1, punto_c2):
                descendiente1.t_inicio[i] = nodo_padre2.t_inicio[i]
                descendiente2.t_inicio[i] = nodo_padre1.t_inicio[i]
            resultado_cruce.append(descendiente1)
            resultado_cruce.append(descendiente2)
            return resultado_cruce
        else:
            resultado_cruce.append(nodo_padre1)
            resultado_cruce.append(nodo_padre2)
            return resultado_cruce

    # -----------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def mutacion_intercambio(nodo: Nodo, n_tarea: int, p_mut: float) -> Nodo:
        if random() < p_mut:
            descendiente = Nodo(nodo.t_inicio)

            p_mut1 = np.random.randint(0, n_tarea)
            p_mut2 = np.random.randint(0, n_tarea)

            descendiente.t_inicio[p_mut1] = descendiente.t_inicio[p_mut2]
            descendiente.t_inicio[p_mut2] = descendiente.t_inicio[p_mut1]
            return descendiente
        else:
            return nodo


    # -----------------------------------------------------------------------------------------------------------------------

