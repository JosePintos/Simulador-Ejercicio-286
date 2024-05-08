import numpy as np
from time import perf_counter


arr = np.array(
    [
        [0.2, 0.2, 0.05, 0.1],
        [0.7, 0.5, 0.6, 0.4],
        [0.2, 0.25, 0.2, 0.04],
    ]
)
start = perf_counter()
acc = np.cumsum(arr)
end = perf_counter()

print(f"Acc list: {acc} - and it took {end-start} seconds")
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
    if not sig_estado or sig_estado == "alta":
        probabilidades = [x for arr in probabilidades for x in arr]
        res_estados = estados[:]
    else:
        est_idx = estado_siguiente[sig_estado]
        probabilidades = probabilidades[est_idx]
        if est_idx == 0:
            res_estados = estados[:4]
        elif est_idx == 1:
            res_estados = estados[4:8]
        else:
            res_estados = estados[8:12]

    # probabilidades.sort(reverse=True)
    to_np_arr = np.array(probabilidades)
    pr_acc = np.cumsum(to_np_arr)

    for i in range(len(pr_acc)):
        if rnd < pr_acc:
            return res_estados[i]
    return res_estados[len(probabilidades) - 1]
