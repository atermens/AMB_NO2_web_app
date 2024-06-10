# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd



# Dades de les estacions que s'han treballat abans amb QGIS.
# Periode de dates: [2019, 2022, 2023]
# Te la següent estructura:
# codi_eoi: {
#       0: [LCZ_1_m2, LCZ_2_m2, LCZ_3_m2, LCZ_4_m2, LCZ_5_m2, LCZ_6_m2, LCZ_7_m2, LCZ_8_m2, LCZ_9_m2, LCZ_10_m2, LCZ_A_m2, LCZ_B_m2, LCZ_C_m2, LCZ_D_m2, LCZ_E_m2, LCZ_F_m2, LCZ_G_m2, T_LCZ_m2,],
#       1: [%LCZ_1, %LCZ_2, %LCZ_3, %LCZ_4, %LCZ_5, %LCZ_6, %LCZ_7, %LCZ_8, %LCZ_9,% LCZ_10, %LCZ_A, %LCZ_B, %LCZ_C, %LCZ_D, %LCZ_E, %LCZ_F, %LCZ_G,],
# },
#

EOI_LCZ = {
    '08015021': {
            0: [0.0, 278442.682, 214240.505, 0.0, 7002.86, 2.0, 0.0, 69726.274, 0.0, 0.0, 0.0, 48304.1669, 0.0, 0.0, 158.911, 0.0, 0.0, 617877.3989],
            1: [1.33,    36.33,      27.59,  0.0,    0.89, 0.0, 0.0,    10.89,  0.0, 0.0, 0.0,     6.33,   0.0, 0.0,  16.64,  0.0, 0.0 ],
    },
    '08019004': {
            0: [0.0, 379257.4914, 61800.52, 0.0, 16716.5,  6.0, 0.0, 70664.86674, 0.0, 0.0, 0.0, 67516.108, 0.0, 0.0, 435.597715, 3072.14, 0.0, 599469.2238],
            1: [7.75,    49.18,       7.99, 0.0,     2.13, 0.0, 0.0,     9.17,    0.0, 0.0, 0.0,     8.88,  0.0, 0.0,  14.49,        0.41, 0.0],
    },
    '08019042': {
            0: [0.0, 295977.6811, 68365.27626, 0.0, 0.0, 0.0, 0.0, 15903.45779, 0.0, 0.0, 0.0, 39170.90248, 0.0, 0.0,  0.0,  0.0, 0.0, 419417.3177],
            1: [9.91,    55.10,       8.77,    0.0, 0.0, 0.0, 0.0,     2.16,    0.0, 0.0, 0.0,     5.01,    0.0, 0.0, 19.05, 0.0, 0.0],
    },
    '08019043': {
            0: [ 0.0, 433988.0194, 520.608, 0.0, 2149.944, 0.0, 0.0, 46428.8,  0.0, 0.0, 0.0, 12641.62826, 0.0, 0.0, 855.62, 0.0, 0.0, 496584.6197],
            1: [20.13,    56.15,     0.11,  0.0,    0.29,  0.0, 0.0,     6.09, 0.0, 0.0, 0.0,     1.60,    0.0, 0.0,  15.62, 0.0, 0.0],
    },
    '08019044': {
            0: [ 0.0, 442401.9501, 45416.734, 0.0, 0.0, 0.0, 0.0, 21029.49, 0.0, 0.0, 0.0, 31025.46, 0.0, 0.0, 795.78299, 0.0, 0.0, 540669.4171],
            1: [11.02,    57.19,       5.82,  0.0, 0.0, 0.0, 0.0,     2.71, 0.0, 0.0, 0.0,     4.02, 0.0, 0.0,  19.23,    0.0, 0.0],
    },
    '08019050': {
            0: [0.0, 167495.894, 8930.168899, 0.0, 0.0, 334.54, 0.0, 179017.273, 0.0, 0.0, 0.0, 293779.5748, 10873.1,  0.0, 1365.395929, 0.0, 0.0, 661795.9466],
            1: [1.64,    21.93,     1.21,     0.0, 0.0,   0.05, 0.0,     23.01,  0.0, 0.0, 0.0,     37.78,       1.38, 0.0,   13.00,     0.0, 0.0],
    },
    '08019054': {
            0: [0.0, 151658.5413, 93845.30353, 0.0, 48671.26, 34105.44, 0.0, 222573.6532, 0.0, 0.0, 0.0, 118144.3149, 0.0, 0.0, 5725.805621, 0.0, 0.0, 674724.3185],
            1: [0.36,    19.73,      12.21,    0.0,     6.20,     4.47, 0.0,     28.75,   0.0, 0.0, 0.0,     15.13,   0.0, 0.0,   13.16,     0.0, 0.0],
    },
    '08019057': {
            0: [0.0,  13.0, 0.0, 0.0, 89143.30096, 56067.98453, 0.0, 336927.1054, 0.0, 0.0, 0.0, 215985.4996, 0.0, 0.0, 5118.621515, 0.0, 0.0, 703255.512],
            1: [0.58,  0.0, 0.0, 0.08,   11.81,        7.30,    0.0,     43.69,   0.0, 0.0, 0.0,     27.55,   0.0, 0.0,    9.00,     0.0, 0.0],
    },
    '08019058': {
            1: [ 0.0, 0.0, 0.0, 0.0, 1.09, 2.16, 0.0, 2.71, 1.11, 0.0, 72.39, 3.33, 11.25, 0.12, 5.81, 0.01, 0.0],
    },
    '08089005': {
            0: [0.0, 75572.7271, 1735.280829, 0.0, 22791.12, 3820.795, 0.0, 68230.32611, 2.87525, 0.0, 234707.1335, 196553.3877, 98112.49791, 11670.322, 6139.396753, 5463.61726, 265.125929, 725064.6053],
            1: [0.0,     9.71,      0.31,     0.0,     2.91,    0.52,  0.0,     8.84,    0.0,     0.0,     30.48,       25.30,      12.76,        1.50,     6.92,        0.71,      0.05],
    },
    '08101001': {
            0: [0.0, 409162.6443, 99192.50982, 0.0, 1190.02, 0.0, 0.0, 99502.416, 0.0, 0.0, 0.0, 35832.88324, 18.94399, 0.0, 37.86917, 230.644, 0.0, 645167.9305],
            1: [0.37,    52.71,      12.73,    0.0,    0.16, 0.0, 0.0,    13.01,  0.0, 0.0, 0.0,     4.82,     0.0,     0.0, 16.17,      0.02,  0.0],
    },
    '08125002': {
            0: [0.0, 139042.2891, 142262.5054, 0.0, 0.0, 16211.52189, 0.0, 48648.227, 3648.6822, 0.0, 40269.78746, 36249.8466, 93280.3618, 0.0, 36435.66925, 72951.7795, 22360.8, 651361.4702],
            1: [0.0,     17.95,       18.27,   0.0, 0.0,     2.18,    0.0,     9.91,     0.47,   0.0,     5.40,        4.69,      12.12,   0.0,    16.69,        9.45,       2.88],
    },
    '08169008': {
            0: [0.0, 251897.516, 104756.9656, 0.0, 0.0, 2967.589, 0.0, 94872.74, 1696.5447, 0.0, 0.0, 74744.573, 37506.342, 32746.328, 465.081429, 63118.90843, 0.0, 664772.5881],
            1: [0.0,     32.60,      13.67,   0.0, 0.0,    0.37,  0.0,    12.25,    0.22,   0.0, 0.0,     9.64,      4.86,      4.35,   13.87,         8.18,    0.0],
    },
    '08169009': {
            0: [0.0, 84308.417, 26897.43, 0.0, 956.642, 0.0, 0.0, 478955.3847, 0.0, 0.0, 0.0, 136823.0241, 0.0, 0.0, 3038.8338, 792.7659, 0.0, 731772.4975],
            1: [0.0,    10.97,      3.57, 0.0,   0.14,  0.0, 0.0,     61.94,   0.0, 0.0, 0.0,     17.60,   0.0, 0.0,    5.68,     0.10,   0.0],
    },
    '08157003': {
            1: [ 0.0, 0.21, 0.75, 0.0, 0.86, 8.71, 0.0, 0.18, 0.77, 0.0, 52.79, 7.75, 16.86, 1.49, 5.82, 3.43, 0.38],
    },
    '08194008': {
            0: [0.0, 139614.7481, 58082.50993, 0.0, 0.0, 17586.5,  0.0, 60690.838, 22065.0,  0.0, 0.0, 238615.7406, 2518.57, 0.0, 105.194249, 6141.888, 37134.63, 582555.6189],
            1: [1.36,    17.86,       7.60,    0.0, 0.0,     2.34, 0.0,     8.02,      2.79, 0.0, 0.0,     30.87,      0.33, 0.0,  23.26,        0.80,      4.78],
    },
    '08196001': {
            0: [0.0, 183432.5837, 27223.95122, 0.0, 0.0, 227.732, 0.0, 185921.945, 0.0, 0.0, 0.0, 132195.8166, 62383.72, 0.0, 1551.705, 677.312, 33130.44062, 626745.2061],
            1: [0.0,     23.52,       3.55,    0.0, 0.0,   0.03,  0.0,     24.52,  0.0, 0.0, 0.0,     16.95,       8.05, 0.0,   19.02,    0.10,      4.26],
    },
    '08205002': {
            0: [0.0, 152593.6757, 86706.70063, 0.0, 99117.18749, 35674.99762, 0.0, 149924.6302, 0.0, 0.0, 0.0, 152673.3165, 0.0, 0.0, 3227.236843, 13.6275, 0.0, 679931.3724],
            1: [0.0,     19.70,      11.02,    0.0,    12.93,        4.52,    0.0,     19.39,   0.0, 0.0, 0.0,     19.90,   0.0, 0.0,   12.53,      0.01,   0.0],
    },
    '08245012': {
            0: [0.0, 416177.8914, 68168.42893, 0.0, 0.0, 0.0, 0.0, 41617.72683, 0.0, 0.0, 0.0, 85045.298, 3342.108, 0.0, 1297.4199, 0.0, 22270.9, 637919.773],
            1: [1.17,    53.84,       8.82,    0.0, 0.0, 0.0, 0.0,     5.40,    0.0, 0.0, 0.0,    11.12,     0.44,  0.0,   16.36,   0.0,     2.86],
    },
    '08252006': {
            0: [0.0, 120351.4992, 345920.3427, 0.0, 0.0, 467.68217, 0.0, 118881.4871, 0.0, 0.0, 0.0, 70083.01928, 0.0, 0.0, 911.12522, 3957.14, 0.0, 660572.2957],
            1: [0.0,     15.60,       44.69,   0.0, 0.0,   0.06,    0.0,     15.43,   0.0, 0.0, 0.0,     9.12,    0.0, 0.0,  14.55,       0.55, 0.0],
    },
    '08263001': {
            0: [0.0, 128839.3854, 234603.9914, 0.0, 3475.75, 14725.42929, 0.0, 81184.4439, 0.0, 0.0, 4782.75, 30171.26, 63935.11, 66368.695, 47.0, 10795.5019, 0.0, 638929.3168],
            1: [0.0,     16.67,       30.18,   0.0,    0.44,     1.96,    0.0,    10.64,   0.0, 2.09,   0.62,     4.11,     8.39,     8.56,  14.94,    1.39,   0.0],
    },
    '08263007': {
            0: [0.0, 29940.94379, 207422.3694, 0.0, 0.0, 28879.66166, 0.0, 96649.75826, 613.395, 0.0, 2006.72, 6429.096263, 174422.8714, 6416.98, 66.411027, 6817.3, 431.0227, 560096.5295],
            1: [0.0,     3.95,        26.64,   0.0, 0.0,     3.74,    0.0,    12.45,      0.08, 17.36,   0.26,    0.91,         22.62,      0.82, 10.26,        0.86,  0.06],
    },
    '08301004': {
            0: [0.0, 202100.0078, 116802.6309, 0.0, 23803.4, 2627.564, 0.0, 229160.5089, 0.0, 0.0, 0.0, 93119.0132, 0.0, 0.0, 1731.854945, 0.0, 0.0, 669344.9798],
            1: [0.0,     26.40,       14.95,   0.0,     3.0,    0.33,  0.0,     29.74,   0.0, 0.0, 0.0,    11.97,   0.0, 0.0,   13.6,      0.0, 0.0],
    },
}

LCZ_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'B', 'C', 'D', 'E', 'F', 'G']

nom1 = [
    'compact high-rise',
    'compact midrise',
    'compact low-rise',
    'open high-rise',
    'open midrise',
    'open low-rise',
    'lightweight low-rise',
    'large low-rise',
    'sparsely built',
    'heavy industry',
    'dense trees',
    'scattered trees',
    'bush, scrub',
    'low plants',
    'bare rock or paved',
    'bare soil or sand',
    'water',
]
LCZ_NAME = { k:n for k,n in zip(LCZ_KEYS, nom1) }

nom2 = [
    'Dense mix of tall buildings to tens of stories. Few or no trees. Land cover mostly paved. Concrete, steel, stone and glass construction materials.',
    'Dense mix of midrise buildings (3–9 stories). Few or no trees. Land cover mostly paved. Stone, brick, tile, and concrete construction materials.',
    'Dense mix of low-rise buildings (1–3 stories). Few or no trees. Land cover mostly paved. Stone, brick, tile, and concrete construction materials.',
    'Open arrangement of tall buildings to tens of stories. Abundance of pervious land cover (low plants, scattered trees). Concrete, steel, stone, and glass construction materials.',
    'Open arrangement of midrise buildings (3–9 stories). Abundance of pervious land cover (low plants, scattered trees). Concrete, steel, stone, and glass construction materials.',
    'Open arrangement of low-rise buildings (1–3 stories). Abundance of pervious land cover (low plants, scattered trees). Wood, brick, stone, tile, and concrete construction materials.',
    'Dense mix of single-story buildings. Few or no trees. Land cover mostly hard-packed. Lightweight construction materials (e.g., wood, thatch, corrugated metal).',
    'Open arrangement of large low-rise buildings (1–3 stories). Few or no trees. Land cover mostly paved. Steel, concrete, metal, and stone construction materials.',
    'Sparse arrangement of small or medium-sized buildings in a natural setting. Abundance of pervious land cover (low plants, scattered trees).',
    'Low-rise and midrise industrial structures (towers, tanks, stacks). Few or no trees. Land cover mostly paved or hard-packed. Metal, steel, and concrete construction materials.',
    'Heavily wooded landscape of deciduous and/or evergreen trees. Land cover mostly pervious (low plants). Zone function is natural forest, tree cultivation, or urban park.',
    'Lightly wooded landscape of deciduous and/or evergreen trees. Land cover mostly pervious (low plants). Zone function is natural forest, tree cultivation, or urban park.',
    'Open arrangement of bushes, shrubs, and short, woody trees. Land cover mostly pervious (bare soil or sand). Zone function is natural scrubland or agriculture.',
    'Featureless landscape of grass or herbaceous plants/crops. Few or no trees. Zone function is natural grassland, agriculture, or urban park.',
    'Featureless landscape of rock or paved cover. Few or no trees or plants. Zone function is natural desert (rock) or urban transportation.',
    'Featureless landscape of soil or sand cover. Few or no trees or plants. Zone function is natural desert or agriculture.',
    'Large, open water bodies such as seas and lakes, or small bodies such as rivers, reservoirs, and lagoons.',
]
LCZ_DEFINITION = { k:n for k,n in zip(LCZ_KEYS, nom2) }

# Valores de propiedades geometricas y de cobertura de superficie para zonas climaticas locales.
# Todas las propiedades no tienen unidades, excepto la altura de los elementos de rugosidad (m).
# LCZ_PROPERTIES = {
#   'lcz': [
#       'Sky view factor',
#       'Espaciado entre edificios/arboles',
#       'Fraccion edificios',
#       'Fraccion impermeable',
#       'Fraccion permeable',
#       'Altitud edificios',
#       'Rugosidad del terreno (m)'
#   ]
# }
#
#
# LCZ_PROPERTIES = {
#    '1': ['0.2-0.4',  '>2.0',      '40-60', '40-60', '<10',   '>25',   '8'],
#    '2': ['0.3-0.6',  '0.75-2.0',  '40-70', '40-70', '<20',   '10-25', '6-7'],
#    '3': ['0.2-0.6',  '0.75-1.5',  '40-70', '40-70', '<30',   '3-10',  '6'],
#    '4': ['0.5-0.7',  '0.75-1.25', '20-40', '20-40', '30-40', '>25',   '7-8'],
#    '5': ['0.5-0.8',  '0.3-0.75',  '20-40', '20-40', '20-40', '10-25', '5-6'],
#    '6': ['0.6-0.9',  '0.3-0.75',  '20-40', '20-40', '30-60', '3-10',  '5-6'],
#    '7': ['0.2-0.5',  '1.0-2.0',   '60-90', '60-90', '<30',   '2-4',   '4-5'],
#    '8': ['>0.7',     '0.1-0.3',   '30-50', '30-50', '<20',   '3-10',  '5'],
#    '9': ['>0.8',     '0.1-0.25',  '10-20', '10-20', '60-80', '3-10',  '5-6'],
#    '10': ['0.6-0.9', '0.2-0.5',   '20-30', '20-30', '40-50', '5-15',  '5-6'],
#    'A': ['<0.4',     '<0.1',      '<10',   '<10',   '>90',   '3-30',  '8'],
#    'B': ['0.5-0.8',  '0.25-0.75', '<10',   '<10',   '>90',   '3-15',  '5-6'],
#    'C': ['0.7-0.9',  '0.25-1.0',  '<10',   '<10',   '>90',   '<2',    '4-5'],
#    'D': ['>0.9',     '<0.1',      '<10',   '>90',   '>90',   '<1',    '3-4'],
#    'E': ['>0.9',     '<0.1',      '<10',   '<10',   '<10',   '<0.25', '1-2'],
#    'F': ['>0.9',     '<0.1',      '<10',   '<10',   '>90',   '<0.25', '1-2'],
#    'G': ['>0.9',     '<0.1',      '<10',   '<10',   '>90',   '-',     '1']
#    }
# ---------------------------------------------------------------------------------------------------------------------


def get_LCZmax(eoi_code: str, tipo: int) -> tuple:
    dicc0 = { value: round(0.0, 2) for i,value in enumerate(LCZ_KEYS) }
    # anem a obtenir la informacio associada a les LCZs dins d'un buffer de 500m de l'estacio
    dicc = EOI_LCZ.get(eoi_code, {})  # { 0: [LCZ_1_m2, LCZ_2_m2, LCZ_3_m2, LCZ_4_m2, LCZ_5_m2, LCZ_6_m2, LCZ_7_m2, LCZ_8_m2, LCZ_9_m2, LCZ_10_m2, LCZ_A_m2, LCZ_B_m2, LCZ_C_m2, LCZ_D_m2, LCZ_E_m2, LCZ_F_m2, LCZ_G_m2, T_LCZ_m2,], 1: [%LCZ_1, %LCZ_2, %LCZ_3, %LCZ_4, %LCZ_5, %LCZ_6, %LCZ_7, %LCZ_8, %LCZ_9,% LCZ_10, %LCZ_A, %LCZ_B, %LCZ_C, %LCZ_D, %LCZ_E, %LCZ_F, %LCZ_G,], },
    llista = dicc.get(tipo, [])
    if not llista: return(dicc0, "")

    if tipo == 0:
        #         0         1         2         3         4         5         6         7         8          9         10        11        12        13        14        15        16      17
        # 0: [LCZ_1_m2, LCZ_2_m2, LCZ_3_m2, LCZ_4_m2, LCZ_5_m2, LCZ_6_m2, LCZ_7_m2, LCZ_8_m2, LCZ_9_m2, LCZ_10_m2, LCZ_A_m2, LCZ_B_m2, LCZ_C_m2, LCZ_D_m2, LCZ_E_m2, LCZ_F_m2, LCZ_G_m2, T_LCZ_m2,]
        total = float(llista[17])
        dicc = { value: round(100*float(llista[i])/total, 2) for i, value in enumerate(LCZ_KEYS) }
        # retornem la key (LCZ) associada que ocupa mes area en el buffer...
        return (dicc, max(dicc, key=dicc.get))
    elif tipo == 1:
        #          0       1       2       3       4       5       6       7       8       9       10      11      12      13      14      15      16
        # 1: [%LCZ_1, %LCZ_2, %LCZ_3, %LCZ_4, %LCZ_5, %LCZ_6, %LCZ_7, %LCZ_8, %LCZ_9,% LCZ_10, %LCZ_A, %LCZ_B, %LCZ_C, %LCZ_D, %LCZ_E, %LCZ_F, %LCZ_G,], },
        dicc = { value: round(float(llista[i]), 2) for i, value in enumerate(LCZ_KEYS) }
        return (dicc, max(dicc, key=dicc.get))
    else:
        return (dicc0, "")


def get_LCZ_image(lcz: str) -> str:
    return os.path.join(os.getcwd(),f'lcz_img/LCZ{lcz}.png')


def get_LCZ_station_image(eoi_code: str, v: int) -> str:
    # versio 0 (Mariela) / versio 1 (Wenyu)
    if v == 0:
        return os.path.join(os.getcwd(), f'lcz_bf_v{v}/{eoi_code}_lcz.jpg')
    elif v == 1:
        return os.path.join(os.getcwd(), f'lcz_bf_v{v}/LCZ_{int(eoi_code)}.jpg')
    else:
        return ''


def get_VUCI(lcz: str) -> float:
    # Vulnerability Urban Climate Index (taula Joan Gilabert).
    # Diccionari del tipus lcz:vuci
    #         1    2   3   4   5   6   7   8   9   10  A   B   C   D   E   F   G
    valors = [100, 80, 70, 70, 60, 50, 60, 50, 30, 70, 50, 30, 30, 20, 40, 10, 20 ]
    vuci = { k:v for k,v in zip(LCZ_KEYS, valors) }
    return vuci.get(lcz, 0)


# ---------------------------------------------------------------------------------------------------------------------
# VUCI_CVP scenarios
#
# A1 ... Extremadamente vulnerable
# A2 ... Muy vulnerable
# B  ... Vulnerable
# C1 ... Vulnerable VUCI, poco vulnerable CVP
# C2 ... Poco vulnerable VUCI, vulnerable CVP
# D  ... Poco vulnerable
#
#            | vuci<50 | 50<vuci<60 | 60<vuci<70 | 70<vuci |
#-----------------------------------------------------------
# cvpi<50    |   D     |   C1       |   C1       |   C1    |
# 50<cvpi<60 |   C2    |   B        |   B        |   B     |
# 60<cvpi<70 |   C2    |   B        |   A2       |   A2    |
# 70<cvpi    |   C2    |   B        |   A2       |   A1    |
#-----------------------------------------------------------
def getcr(dato: float) -> int:
    if dato < 50.0:
        return 1
    elif dato < 60.0:
        return 2
    elif dato < 70.0:
        return 3
    else:
        return 4


#-----------------------------------------------------------
def get_scenario(vuci: float, cvpi: float) -> tuple:
    # vuci i cvpi son percentatges 

    scenarios_dict = {
        "A1": "Extremadamente vulnerable",
        "A2": "Muy vulnerable",
        "B":  "Vulnerable",
        "C1": "Vulnerable VUCI, poco vulnerable CVP",
        "C2": "Poco vulnerable VUCI, vulnerable CVP",
        "D":  "Poco vulnerable",
    }

    # columnwise storage
    scenario_matrix = [ 'D', 'C2', 'C2', 'C2', 'C1', 'B', 'B', 'B', 'C1', 'B', 'A2', 'A2', 'C1', 'B', 'A2', 'A1' ]

    scenario_key = scenario_matrix[4*(getcr(vuci)-1)+getcr(cvpi)]
    
    return (scenario_key, scenarios_dict.get(scenario_key, "none"))

# ---------------------------------------------------------------------------------------------------------------------
# Conversión Urban Atlas a LCZ urbanas. (taula 6.1 tesis JGilabert)
# Urban Atlas <-> LCZ
# 'Tejido urbano continuo': ['1', '2', '3']
# 'Tejido urbano denso discontinuo': ['4', '5', '6']
# 'Tejido urbano discontinuo de densidad media': ['5', '6']
# 'Tejido urbano discontinuo de baja densidad': ['6']
# 'Tejido urbano discontinuo de muy baja densidad': ['6']
# 'Estructuras aisladas': ['9']
# 'Unidades industriales, comerciales, públicas y privadas': ['1', '2', '3', '4', '5', '6']
# 'Carreteras y calles': ['E']
# 'Otros caminos y terrenos asociados': ['E']
# 'Ferrocarriles': ['E']
# 'Zona portuaria': ['E']
# 'Aeropuerto': ['E']
# 'Extracción de minerales': ['E']
# 'Sitios de construcción': ['E']
# 'Terreno sin uso actual': ['F']
# 'Verde Urbano': ['B','D']
# 'Instalaciones deportivas': ['D']
# 'Huertos urbanos': ['B']
# 'Zonas de vegetación herbácea': ['B']
# ---------------------------------------------------------------------------------------------------------------------
