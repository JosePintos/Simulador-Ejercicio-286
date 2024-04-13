from random import random
import functools
import numpy as np


estados = [
    ("buena", "buena"),
    ("buena", "regular"),
    ("buena", "critica"),
    ("buena", "alta"),
    ("regular", "buena"),
    ("regular", "regular"),
    ("regular", "critica"),
    ("regular", "alta"),
    ("critica", "buena"),
    ("critica", "regular"),
    ("critica", "critica"),
    ("critica", "alta"),
]
estado_siguiente = {"buena": 0, "regular": 1, "critica": 2, "alta": 3}
estados_alta = ["mejorada", "no_mejorada", "muerto"]


def definir_condicion(rnd, probabilidades, sig_estado=None):
    probabilidades = (
        probabilidades[0]
        if (sig_estado == "" or sig_estado == "alta")
        else probabilidades[estado_siguiente[sig_estado] + 1]
    )

    for i in range(len(probabilidades[0])):
        if rnd < probabilidades[0][i]:
            return probabilidades[1][i]
    return probabilidades[1][len(probabilidades) - 1]


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

    probabilidades = (
        [x for arr in probabilidades for x in arr]
        if (not sig_estado or sig_estado == "alta")
        else probabilidades[estado_siguiente[sig_estado]]
    )

    probabilidades.sort(reverse=True)
    for i, n in enumerate(probabilidades):
        pr_acc += n
        if rnd < pr_acc:
            return estados[i]
    return estados[len(probabilidades) - 1]


def start_simulation(pr_en_hospital, pr_cond_alta, iter):
    vector_estado = [0, 0, "", "", 0, ""]
    ingreso_regular = False
    rnd2 = 0
    condicion_alta = ""
    tabla_final = list()

    to_np_arr = np.array(pr_en_hospital)
    all_acc = (np.cumsum(to_np_arr), estados[:])
    buena_acc = (all_acc[0][0:4], estados[0:4])
    regular_acc = (all_acc[0][4:8], estados[4:8])
    critico_acc = (all_acc[0][8:], estados[8:])

    # Calcular promedio
    cant_pacientes, dias_en_hospital = 0, 0
    for _ in range(iter):
        rnd1 = random()
        estado1, estado2 = definir_condicion(
            rnd1,
            probabilidades=[all_acc, buena_acc, regular_acc, critico_acc],
            sig_estado=vector_estado[3],
        )
        dias_en_hospital += 1 if ingreso_regular else 0
        if (estado1 == "regular") and (
            vector_estado[3] == "alta" or vector_estado[3] == ""
        ):
            ingreso_regular = True
            cant_pacientes += 1
        if estado2 == "alta":
            # rnd2 = random()
            # condicion_alta = definir_condicion_alta(
            #     rnd2, probabilidades=dict_probabilidades_cond_alta
            # )
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
