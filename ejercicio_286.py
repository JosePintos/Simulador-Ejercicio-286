from random import random
import functools

estados = ["buena", "regular", "critica", "alta"]
estado_siguiente = {"0": "buena", "1": "regular", "2": "critica", "3": "alta"}
estados_alta = ["mejorada", "no_mejorada", "muerto"]


def definir_condicion(rnd, probabilidades, sig_estado=None):
    pr_acc = 0
    total_iterations = len(probabilidades)
    if not sig_estado or sig_estado == "alta":
        j = 0
        for key, val in probabilidades.items():
            j += 1
            for i in range(4):
                pr_acc += val[i]
                if rnd < pr_acc:
                    return key, estado_siguiente[str(i)]
            if j == total_iterations:
                return key, estado_siguiente[str(i)]

    for i in range(4):
        pr_acc += probabilidades[sig_estado][i]
        if rnd < pr_acc:
            return sig_estado, estado_siguiente[str(i)]
        if i == 3:
            return sig_estado, estado_siguiente[str(i)]


def definir_condicion_alta(rnd, probabilidades):
    pr_acc = 0
    total_iterations = len(probabilidades)
    j = 0
    for key, val in probabilidades.items():
        for i in range(3):
            pr_acc += val[i]
            if rnd < pr_acc:
                return estado_siguiente[str(i)]
        if j == total_iterations:
            return estado_siguiente[str(i)]


def start_simulation(pr_en_hospital, pr_cond_alta, iter):
    vector_estado = [0, 0, "", "", 0, ""]
    ingreso_regular = False
    rnd2 = 0
    condicion_alta = ""
    tabla_final = list()

    dict_probabilidades_condiciones = {
        est: pr for est, pr in zip(estados[:3], pr_en_hospital)
    }
    dict_probabilidades_cond_alta = {
        est: pr for est, pr in zip(estados_alta, pr_cond_alta)
    }

    # Calcular promedio
    cant_pacientes, dias_en_hospital = 0, 0
    for _ in range(iter):
        rnd1 = random()
        estado1, estado2 = definir_condicion(
            rnd1,
            probabilidades=dict_probabilidades_condiciones,
            sig_estado=vector_estado[3],
        )
        dias_en_hospital += 1 if ingreso_regular else 0
        if (estado1 == "regular") and (
            vector_estado[3] == "alta" or vector_estado[3] == ""
        ):
            ingreso_regular = True
            cant_pacientes += 1
        if estado2 == "alta":
            rnd2 = random()
            condicion_alta = definir_condicion_alta(
                rnd2, probabilidades=dict_probabilidades_cond_alta
            )
            ingreso_regular = False
        tabla_final.append(vector_estado)
        vector_estado = [
            vector_estado[0] + 1,
            "%.3f" % (rnd1),
            estado1,
            estado2,
            "%.3f" % (rnd2) if rnd2 else "-",
            condicion_alta,
        ]
    res = tuple(tuple(lst) for lst in tabla_final)
    return res


if __name__ == "__main__":
    start_simulation()
