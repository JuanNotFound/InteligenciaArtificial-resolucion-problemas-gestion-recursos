
class Nodo:

    # -----------------------------------------------------------------------------------------------------------------------

    def __init__(self, t_inicio):
        self.t_inicio = t_inicio

    # -----------------------------------------------------------------------------------------------------------------------

    def calcular_t_final(self, duraciones: int) -> [int]:
        finales = self.obtener_copia()

        for i in range(len(finales)):
            if finales[i] is not None:
                finales[i] += duraciones[i]
        return finales

    # -----------------------------------------------------------------------------------------------------------------------

    def calcular_makespan(self, duraciones: [int]) -> int:
        t_finales = self.calcular_t_final(duraciones)
        e_mayor = 0
        for elemento in t_finales:
            if(elemento != None) and (elemento > e_mayor):
                e_mayor = elemento

        return e_mayor

    # -----------------------------------------------------------------------------------------------------------------------

    def obtener_copia(self) ->[int]:
        return self.t_inicio.copy()

    # -----------------------------------------------------------------------------------------------------------------------

    def suma_t_inicio(self, task_duration: [int]) -> int:
        finales = self.calcular_t_final(task_duration)
        suma = 0
        for i in range(len(finales)):
            if finales[i] is not None:
                suma += task_duration[i]
        return suma

    # -----------------------------------------------------------------------------------------------------------------------

    def favorecer_inicio_recursos(self) -> float:
        return 1.5 * self.t_inicio.count(None)

    # -----------------------------------------------------------------------------------------------------------------------

    def recursos_no_utilizados(self, duraciones: [int], n_recurso:[int], recursos:[int]) -> int:
        recursos_no_usados = 0
        for i in range(len(self.t_inicio)):
            if self.t_inicio[i] is not None:
                recursos_no_usados += duraciones[i] * (n_recurso - recursos[i])
        return recursos_no_usados

    # -----------------------------------------------------------------------------------------------------------------------
