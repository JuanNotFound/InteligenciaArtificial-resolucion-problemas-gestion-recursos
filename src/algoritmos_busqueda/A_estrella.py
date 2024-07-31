from src.soporte_algoritmos.Metodos_auxiliares import Metodos_auxiliares
from src.soporte_algoritmos.Nodo import Nodo

class A_estrella:

    # -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def iniciar(n_tarea: int, n_recurso: int, duraciones: [int], recursos: [int], dependencias) -> [int]:
        solucion = A_estrella.algoritmo(n_tarea, n_recurso, duraciones, recursos, dependencias)
        if solucion.t_inicio.count(None) == 0:
            print(solucion.calcular_makespan(duraciones))
            print(solucion.t_inicio)
            return solucion
        else:
            return []

    # -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def algoritmo(n_tarea: int, n_recurso: int, duraciones: [int], recursos: [int], dependencias) -> Nodo:
        salir = False
        nodo: Nodo = Nodo([])
        lista_nodos: [] = [(Nodo([None] * n_tarea))] # creamos una lista de nodos, con u nodo vacio preexistente

        while not salir:
            nodo = lista_nodos.pop()
            lista_nodos = Metodos_auxiliares.generar_arbol(nodo, lista_nodos, n_tarea, n_recurso, duraciones, recursos, dependencias)

            lista_nodos = sorted(lista_nodos, key=lambda x: x.calcular_makespan(duraciones) + x.favorecer_inicio_recursos(), reverse=True)
            if len(lista_nodos) == 0 or nodo.t_inicio.count(None) == 0:
                salir = True


        return nodo

    # -----------------------------------------------------------------------------------------------------------------------
