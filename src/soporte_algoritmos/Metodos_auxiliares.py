from src.soporte_algoritmos.Nodo import Nodo


class Metodos_auxiliares:

    # -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def generar_arbol(nodo_padre: Nodo, lista_nodos: [], n_tarea: int, n_recurso: int, duraciones: [int], recursos: [int], dependencias)-> []:
        duracion_maxima = sum(duraciones)  # Duración máxima que puede tomar la ejecución en el peor caso.

        lista_no_nula = filter(lambda x: x != None, nodo_padre.t_inicio)  # Eliminamos los elementos None

        valor_maximo = max(lista_no_nula,
                           default=None) if lista_no_nula else None  # Calculamos el valor_maximo de lista, si la lista existe si no, será None

        if valor_maximo == None:
            for i in range(n_tarea):
                nuevo_nodo = Nodo(nodo_padre.obtener_copia())  # Copiamos la lista de t_inicio del padre
                nuevo_nodo.t_inicio[i] = 0

                if (Metodos_auxiliares.comprobar_dependencias_y_recursos(nuevo_nodo, n_recurso, duraciones, recursos, dependencias)):
                    lista_nodos.append(nuevo_nodo)  # Añadimos a la lista el nuevo nodo

        elif valor_maximo < duracion_maxima:

            for i in range(duracion_maxima):

                j = 0
                salir_algoritmo = False

                while j < n_tarea and not salir_algoritmo:

                    if nodo_padre.t_inicio[j] == None:
                        nuevo_nodo = Nodo(nodo_padre.obtener_copia())
                        nuevo_nodo.t_inicio[j] = valor_maximo + i

                        if (Metodos_auxiliares.comprobar_dependencias_y_recursos(nuevo_nodo, n_recurso, duraciones, recursos, dependencias)):
                            lista_nodos.append(nuevo_nodo)
                            salir_algoritmo = True  # Tenemos una opción viable, podemos salir totalmente y seguir con la ejecución.

                    j += 1

                if salir_algoritmo:
                    break

        return lista_nodos

    # -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def comprobar_dependencias_y_recursos(nodo: Nodo, n_recurso: int, duraciones: [int], recursos: [int], dependencias: [(int,int)]) -> bool:
        return Metodos_auxiliares.comprobar_dependencias(nodo, dependencias, duraciones) and Metodos_auxiliares.comprobar_recursos(nodo, duraciones, recursos, n_recurso)

    # -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def comprobar_dependencias(nodo: Nodo, dependencias: [(int,int)], duraciones: [int]) -> bool:

        for i in range(len(duraciones)):
            if nodo.t_inicio[i] != None:
                for j in range(len(dependencias)):
                    if dependencias[j][1] == i + 1:
                        if nodo.t_inicio[dependencias[j][0] - 1] != None and nodo.t_inicio[dependencias[j][0] - 1] + \
                                duraciones[dependencias[j][0] - 1] > nodo.t_inicio[i] or nodo.t_inicio[
                            dependencias[j][0] - 1] == None:
                            return False
        return True

    # -----------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def comprobar_recursos(nodo: Nodo, duraciones, recursos, n_recursos) -> bool:

        t_inicio = nodo.t_inicio
        t_finales = nodo.calcular_t_final(duraciones)

        n = len(t_inicio)
        for i in range(n):
            for j in range(i + 1, n):
                if (t_inicio[i] != None and t_finales[j] != None) and (t_inicio[j] != None and t_finales[i] != None):
                    if (t_inicio[i] < t_finales[j]) and (t_inicio[j] < t_finales[i]):
                        tareas_simultaneas = [i + 1, j + 1]
                        for k in range(j + 1, n):
                            if (t_inicio[k] != None and t_finales[i] != None) and (
                                    t_inicio[i] != None and t_finales[k] != None):
                                if (t_inicio[k] < t_finales[i]) and (t_inicio[i] < t_finales[k]):
                                    tareas_simultaneas.append(k + 1)
                        recursos_usados = sum(recursos[i - 1] for i in tareas_simultaneas)
                        if recursos_usados > n_recursos:
                            return False
        return True

    # -----------------------------------------------------------------------------------------------------------------------
