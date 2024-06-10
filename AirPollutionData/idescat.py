# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
# Indicador: Indice de envejecimiento
# Definicion: Expresa la relacion entre la cantidad de personas adultas mayores y la cantidad de menores.
# Calculo: Cociente entre personas de 65 y mas con respecto a las personas menores de 15, multiplicado por 100.
#
#          100 * (P_65_I_MES / P_0_14)
#
# Interpretacion estadistica: Un valor de 10 significa que hay 10 adultos mayores (de 65 y más) por cada 100 menores de 15.
#
# Interpretacion contextual y pertinencia: En la sociedad occidental, si bien se reconoce que la vejez es un fenomeno multidimensional,
# suele estar definida por límites de edad. En los pueblos indígenas, lo que distingue la vejez es el cambio de etapa en el ciclo vital
# y el limite cronologico pierde sentido; a lo sumo puede establecerse una frontera asociada a la perdida de capacidades fisiologicas
# o cuando no pueden realizar tareas para la reproduccion material de la familia y comunidad. Asimismo, el estatus y el rol social
# puede aumentar en la medida en que se "envejece", ya que se trata de las personas que atesoran la sabiduria y la memoria colectiva
# que debe ser transmitida a los jovenes para asegurar la reproduccion cultural del grupo o pueblo. Por lo tanto, no cabe una
# interpretacion "negativa", sino de continuidad cultural.
#
# Observaciones: Segun su interpretacion convencional, se trata de un indicador asociado a las transferencias intergeneracionales
# y su aumento sistematico implica para los estados una mayor inversion en salud y seguridad social orientada a las personas de edad,
# beneficios de los cuales no deberian estar exentos los pueblos indígenas.
#
# En Espanya el indice de envejecimiento con las cifras de 2021 se situaba en el 129.1% segun apunta el INE.
# Siendo bastante superior (casi por un 30%) el numero de personas mayores de 65 años que el de adolescentes, podemos ver como el
# envejecimiento de la poblacion es un hecho. Con el avance de la esperanza de vida y la disminucion de la natalidad, la piramide
# demografica se va invirtiendo, teniendo cada vez una base mas estrecha.
#
# Ademas, analizando los datos que nos ofrece el INE podemos definir este aumento como progresivo y sostenido en el tiempo.
# El indice de envejecimiento lleva subiendo sin parar en los ultimos años. En 2020 el indice de envejecimiento era del 125.75%.
# En 2018, el indice de envejecimiento se situaba en el 120.46%. En 2017 este indice no superaba el 120%.
#
# Como vemos, el indicador de envejecimiento crece anyo tras anyo debido a un envejecimiento de la poblacion y a un descenso en la
# natalidad. En enero de 2021, se calculaba que las personas mayores de 65 anyos eran mas de 9 millones.
# Esto se traduce en que alrededor del 19% de la población española son personas mayores.  Conviene recordar que las personas
# mayores de 65 suponen mas o menos una quinta parte de los españoles para poder darles la importancia demografica que se merecen.
#
# Para hacernos una mayor idea del volumen de personas mayores podemos compararlos con otros grupos en Espanya para relativizar
# su importancia. En 2021, mismo anyo en el que se calculaban 9 millones de personas mayores de 65 años, se registraban 2.7 millones
# de empleados publicos. Siendo los funcionarios un volumen de la poblacion activa importante, conviene recordar que las personas
# mayores son un grupo de poblacion tres veces más numeroso.
#
# Si incluimos en estos calculos tanto al sector publico como al privado, se contabiliza que en 2022 hay 19 millones de personas
# trabajando en nuestro pais. Este volumen de trabajadores es poco mas del doble que el de personas mayores de 65 anyos.
# Hay que tener en cuenta que en estas cifras se contabiliza a todas las personas que estan cotizando, sin importar el tipo de contrato.
# Trabajadores con media jornada, contratos de practicas o sueldos precarios tambien entran en esos 19 millones.
# Estas cifras muestran un equilibrio delicado, ya que la cotizacion de estos trabajadores es un pilar fundamental del que dependen las pensiones.
#
# El indice de envejecimiento creciente es una realidad que se debe tener en cuenta desde la administracion publica para crear una
# sociedad inclusiva e igualitaria.
# El cambio demografico que estamos viviendo ofrece una oportunidad para adaptarnos como sociedad si sabemos como.
#

import numpy as np


# Dades de població a partir de dades IDESCAT
# Periode de dates: [2019, 2022, 2023]
# Te la següent estructura:
#
# codi_eoi: {
#     yr: [0, TOTAL, HOMES, DONES, P_0_14, P_15_64, P_65_I_MES, P_ESPANYOL, P_ESTRANGE, P_NASC_CAT, P_NASC_RES, P_NASC_EST,],
#     yr: [1, P_H_0_14, P_H_15_64, P_H_65_I_MES, P_D_0_14, P_D_15_64, P_D_65_I_MES,],
# }
#

EOI_POB = {
    '08015021': {
            2019: [0, 19106, 9267, 9839, 2770, 12694, 3346, 12920, 1576, 13336, 2812, 2113],
            2022: [1, 2237, 9205, 2381, 2007, 9342, 3133],
            2023: [1, 2206, 9284, 2435, 2022, 9434, 3205],
    },
    '08019004': {
            2019: [0, 28094, 13681, 14413, 3990, 19065, 4345, 22195, 4489, 18486, 3701, 5467],
            2022: [1, 3595, 14244, 2610, 3382, 14519, 3740],
            2023: [1, 3503, 14477, 2706, 3271, 14976, 3838],
    },
    '08019042': {
            2019: [0, 39605, 18560, 21027, 4248, 25704, 9278, 32287, 5229, 25297, 6648, 7354],
            2022: [1, 3332, 16705, 5340, 3191, 18081, 7925],
            2023: [1, 3620, 19460, 5474, 3438, 20052, 8068],
    },
    '08019043': {
            2019: [0, 37590, 17476, 20114, 3776, 25335, 8176, 30329, 6789, 22722, 5489, 9224],
            2022: [1, 2723, 17094, 4427, 2557, 17683, 6857],
            2023: [1, 2646, 17494, 4487, 2527, 18124, 6978],
    },
    '08019044': {
            2019: [0, 26018, 11833, 14163, 3188, 17705, 4707, 19932, 4824, 16491, 3154, 6043],
            2022: [1, 2694, 12817, 2959, 2494, 14499, 4891],
            2023: [1, 2690, 13265, 2978, 2492, 15160, 4901],
    },
    '08019050': {
            2019: [0, 7190, 3460, 3730, 590, 5061, 1178, 4913, 1998, 3528, 1107, 2333],
            2022: [1, 1037, 7151, 1429, 979, 6916, 2089],
            2023: [1, 1038, 7372, 1458, 971, 7092, 2082],
    },
    '08019054': {
            2019: [0, 16507, 7954, 8505, 2005, 10755, 3516, 13571, 1953, 8869, 4616, 2832],
            2022: [1, 1563, 7473, 2081, 1485, 7684, 3199],
            2023: [1, 1621, 7735, 2093, 1487, 7968, 3236],
    },
    '08019057': {
            2019: [0, 2845, 1369, 1476, 352, 1841, 528, 1840, 621, 1578, 369, 699],
            2022: [1, 864, 3114, 1105, 871, 3392, 1577],
            2023: [1, 923, 3286, 1138, 911, 3635, 1590],
    },
    '08019058': {
            2022: [1, 672, 2169, 660, 619, 2334, 942],
            2023: [1, 684, 2234, 667, 618, 2425, 969],
    },
    '08089005': {
            2019: [0, 4302, 2138, 2147, 612, 3009, 241, 2161, 139, 3217, 485, 251],
            2022: [1, 1308, 5008, 1009, 1231, 4950, 1267],
            2023: [1, 1278, 5068, 1027, 1222, 5062, 1299],
    },
    '08101001': {
            2019: [0, 52579, 25616, 26940, 7585, 35542, 9280, 36791, 15545, 19944, 10495, 21981],
            2022: [1, 5674, 23543, 4566, 5312, 23778, 6646],
            2023: [1, 5809, 25038, 4539, 5483, 24976, 6713],
    },
    '08125002': {
            2019: [0, 8759, 4202, 4510, 1188, 5799, 1523, 5663, 944, 5408, 1736, 1387],
            2022: [1, 804, 3506, 883, 776, 3537, 1229],
            2023: [1, 815, 3562, 889, 766, 3602, 1248],
    },
    '08169008': {
            2019: [0, 21556, 10575, 10964, 3028, 14066, 4117, 15310, 1695, 12689, 5372, 2440],
            2022: [1, 2549, 10674, 3137, 2461, 10619, 4043],
            2023: [1, 2537, 10768, 3181, 2427, 10668, 4149],
    },
    '08169009': {
            2019: [0, 5528, 2732, 2796, 867, 3728, 549, 3449, 197, 3857, 915, 368],
            2022: [1, 901, 3174, 638, 905, 3133, 898],
            2023: [1, 879, 3170, 652, 861, 3146, 931],
    },
    '08157003': {
            2022: [1, 549, 2087, 563, 493, 2041, 735],
            2023: [1, 555, 2117, 572, 470, 2059, 754],
    },
    '08194008': {
            2019: [0, 9548, 4658, 4873, 1316, 6396, 1481, 6811, 818, 6467, 1545, 1086],
            2022: [1, 1568, 5977, 1366, 1461, 6017, 1854],
            2023: [1, 1559, 6227, 1410, 1471, 6179, 1931],
    },
    '08196001': {
            2019: [0, 9552, 4800, 4752, 1782, 6455, 1126, 6913, 1340, 5722, 1781, 1785],
            2022: [1, 1632, 6124, 1084, 1615, 5925, 1506],
            2023: [1, 1563, 6117, 1096, 1564, 5937, 1565],
    },
    '08205002': {
            2019: [0, 13187, 6249, 6938, 1933, 8749, 1891, 9144, 1675, 8360, 2066, 2293],
            2022: [1, 1864, 6468, 1297, 1803, 6904, 1849],
            2023: [1, 1861, 6516, 1361, 1742, 6983, 1895],
    },
    '08245012': {
            2019: [0, 33771, 16636, 17135, 4766, 21497, 7274, 26391, 5926, 16321, 9561, 7688],
            2022: [1, 3898, 15832, 4334, 3769, 15505, 6084],
            2023: [1, 3954, 16254, 4330, 3763, 15868, 6093],
    },
    '08252006': {
            2019: [0, 12376, 6009, 6350, 1676, 8381, 1878, 8525, 908, 7790, 2639, 1186],
            2022: [1, 1516, 6302, 1762, 1476, 6274, 2279],
            2023: [1, 1471, 6306, 1810, 1424, 6317, 2351],
    },
    '08263001': {
            2019: [0, 9635, 4747, 4852, 1190, 6516, 1229, 6433, 448, 6808, 1439, 652],
            2022: [1, 1259, 5028, 1141, 1159, 4874, 1495],
            2023: [1, 1233, 5092, 1195, 1131, 4910, 1528],
    },
    '08263007': {
            2019: [0, 5452, 2754, 2681, 773, 3642, 732, 3413, 381, 3446, 1032, 542],
            2022: [1, 709, 2956, 615, 681, 2789, 764],
            2023: [1, 711, 3007, 616, 662, 2832, 784],
    },
    '08301004': {
            2019: [0, 12440, 6152, 6288, 1763, 8236, 2028, 7977, 817, 7757, 2499, 1168],
            2022: [1, 1732, 7269, 1716, 1665, 7137, 2271],
            2023: [1, 1683, 7265, 1734, 1630, 7155,	2322],
    },
}


def get_pob_data(eoi_code: str, yr: int) -> tuple:
    # output: [p_0_14, p_15_64, p_65]

    dicc = EOI_POB.get(eoi_code, {}) # { yr: [0, ...], yr: [1, ...]}
    llista = dicc.get(yr, [])
    if not llista: return (0, [])

    # tenemos que ver cual es la version: si es de tipo 0 o tipo 1...
    v = llista[0]

    if v == 0:
        #  0  1      2      3      4       5        6           7           8           9           10          11
        # [0, TOTAL, HOMES, DONES, P_0_14, P_15_64, P_65_I_MES, P_ESPANYOL, P_ESTRANGE, P_NASC_CAT, P_NASC_RES, P_NASC_EST,],
        return (3, llista[4:7])
    elif v == 1:
        #  0   1          2             3         4          5          6
        # [1, P_H_0_14, P_H_15_64, P_H_65_I_MES, P_D_0_14, P_D_15_64, P_D_65_I_MES,],
        return (3, [ llista[i+1] + llista[i+4] for i in range(3) ])
    else:
        return (0, [])


def get_CVP(eoi_code: str, yr: int, iP: int) -> float:
    # iP: num. indice o tasa
    #
    # 0. El indice o mal llamada «tasa» de envejecimiento (por que no es una tasa),
    #    en realidad es simplemente la proporcion de mayores de 64 anyos
    #    = ((Poblacion >64 anyos / Poblacion total) x100) (proporcion de individuos
    #    mayores de 64 anyos sobre el total de la poblacion. Se suele expresar como porcentaje).
    #
    # 1. 100* (P_0_14 + P_65_I_MES) / TOTAL  que es la poblacio vulnerable (= docs Joan)
    #
    # 2. Index d'envelliment (IDESCAT). Poblacio de 65 anys i mes per cada 100 habitants de menys de 15 anys.
    #    https://www.idescat.cat/pub/?id=inddt&m=m
    #    A REVISAR !!!!
    
    n, datos = get_pob_data(eoi_code, yr)   # [p_0_14, p_15_64, p_65]
    # check if datos is empty
    if n == 0: return np.nan

    total = float(sum(datos))

    if iP == 0:
        return round(100.0 * float(datos[2]) / total, 2)
    elif iP == 1:
        return round(100.0 * float(datos[0] + datos[2]) / total, 2)
    elif iP == 2:
        return round(100.0 * float(datos[2]) / float(datos[0]), 2)
    else:
        return np.nan

