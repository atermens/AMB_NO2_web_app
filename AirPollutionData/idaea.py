# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd

# Dades de les estacions que s'han treballat abans amb QGIS.
# Periode de dates: [2019, 2022, 2023]
# Te la següent estructura:
# codi_eoi: {
#       yr: [0, mean,],
#       yr: [1, mean, max, min, d20, d50,],
# },
#

EOI_NO2 = {
    '08015021': {
            2019: [0, 33.0],
            2022: [1, 29.83, 60.25, 4.63, 243, 18],
            2023: [1, 26.22, 86.11, 5.63, 240, 10],
    },
    '08019004': {
            2019: [0, 37.0],
            2022: [1, 27.46, 59.63, 6.79, 255, 14],
            2023: [1, 24.30, 62.17, 4.46, 225,  9],
    },
    '08019042': {
            2019: [0, 31.0],
            2022: [1, 25.77, 59.71, 6.96, 235, 11],
            2023: [1, 20.34, 61.04, 6.33, 151,  5],
    },
    '08019043': {
            2019: [0, 50.0],
            2022: [1, 42.29, 84.50, 13.68, 345, 96],
            2023: [1, 34.59, 83.00, 14.13, 334, 37],
    },
    '08019044': {
            2019: [0, 44.0],
            2022: [1, 34.87,  79.00, 10.83, 317, 47],
            2023: [1, 29.11, 110.23,  8.29, 266, 25],
    },
    '08019050': {
            2019: [0, 32.0],
            2022: [1, 31.21, 72.50, 5.79, 291, 39],
            2023: [1, 27.14, 70.92, 4.08, 240, 27],
    },
    '08019054': {
            2019: [0, 29.0],
            2022: [1, 21.86, 56.33, 5.58, 184, 5],
            2023: [1, 18.92, 57.29, 4.04, 130, 4],
    },
    '08019057': {
            2019: [0, 28.0],
            2022: [1, 21.00, 51.83, 4.21, 167, 2],
            2023: [1, 16.79, 47.63, 5.29, 100, 0],
    },
    '08019058': {
            2022: [1, 8.86, 28.75, 1.67, 8, 0],
            2023: [1, 8.76, 29.50, 1.50, 6, 0]
    },
    '08089005': {
            2019: [0, 15.0],
            2022: [1, 12.05, 27.25, 2.42, 16, 0],
            2023: [1,  9.76, 28.38, 3.04, 10, 0],
    },
    '08101001': {
            2019: [0, 33.0],
            2022: [1, 24.88, 58.88, 6.25, 211, 7],
            2023: [1, 22.99, 55.63, 6.58, 196, 5],
    },
    '08125002': {
            2019: [0, 35.0],
            2023: [1, 31.54, 66.13, 9.71, 318, 25],
    },
    '08169008': {
            2019: [0, 33.0],
            2022: [1, 28.73, 55.29, 7.70, 288, 4],
            2023: [1, 25.06, 61.92, 8.25, 214, 3],
    },
    '08169009': {
            2019: [0, 32.0],
            2022: [1, 28.52, 57.88, 7.04, 298, 2],
            2023: [1, 24.73, 52.00, 6.75, 238, 2],
    },
    '08157003': {
            2022: [1, 17.92, 38.79, 2.58, 136, 0],
            2023: [1, 16.01, 53.17, 1.33,  96, 2],
    },
    '08194008': {
            2019: [0, 37.0],
            2022: [1, 29.58, 61.71, 3.04, 288, 23],
            2023: [1, 27.33, 63.75, 3.38, 259, 14],
    },
    '08196001': {
            2019: [0, 38.0],
            2022: [1, 31.24, 57.75, 6.54, 305,19],
            2023: [1, 28.08, 56.19, 6.67, 273,10],
    },
    '08205002': {
            2019: [0, 25.0],
            2022: [1, 20.97, 48.13, 7.25, 174, 0],
            2023: [1, 19.07, 50.17, 5.67, 138, 1],
    },
    '08245012': {
            2019: [0, 33.0],
            2022: [1, 29.37, 63.50, 8.63, 283, 16],
            2023: [1, 25.63, 62.88, 3.58, 221, 13],
    },
    '08252006': {
            2019: [0, 34.0],
            2022: [1, 26.94, 62.83, 6.04, 249, 10],
            2023: [1, 24.57, 64.17, 2.96, 214, 17],
    },
    '08263001': {
            2019: [0, 32.0],
            2022: [1, 28.36, 57.96, 8.25, 267, 13],
            2023: [1, 24.74, 62.00, 4.04, 232,  9],
    },
    '08263007': {
            2019: [0, 28.0],
            2022: [1, 23.63, 50.17, 6.79, 218, 1],
            2023: [1, 20.59, 58.79, 1.71, 162, 3],
    },
    '08301004': {
            2019: [0, 25.0],
            2022: [1, 21.77, 48.79, 6.83, 197, 0],
            2023: [1, 18.59, 48.79, 3.54, 127, 0],
    },
}


def get_NO2_data(eoi_code: str, yr: int) -> list:
    dicc = EOI_NO2.get(eoi_code, {})   # {yr: [0, mean,], yr: [1, mean, max, min, d20, d50,],}
    return dicc.get(yr, [])


def get_NO2_mean(eoi_code: str, yr: int) -> float:
    llista = get_NO2_data(eoi_code, yr)
    v = llista[0]
    if v in [0, 1]:
        return float(llista[1])
    else:
        return np.nan


# deprecated function ---
def get_NO2_2019(eoi_code: str) -> float:
    return get_NO2_mean(eoi_code, 2019)

