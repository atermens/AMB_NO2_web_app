# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


def get_lczmax(eoi_code: str, tipo: int) -> tuple:
    from air_pollution_data.datos import LCZ_KEYS, EOI_LCZ
    dicc0 = {value: round(0.0, 2) for i, value in enumerate(LCZ_KEYS)}
    # anem a obtenir la informacio associada a les LCZs dins d'un buffer de 500m de l'estacio
    dicc = EOI_LCZ.get(eoi_code, {})
    llista = dicc.get(tipo, [])
    if not llista:
        return dicc0, ""
    else:
        match tipo:
            case 0:
                #         0         1         2         3         4         5         6         7         8
                #         9         10        11        12        13        14        15        16      17
                # 0: [LCZ_1_m2, LCZ_2_m2, LCZ_3_m2, LCZ_4_m2, LCZ_5_m2, LCZ_6_m2, LCZ_7_m2, LCZ_8_m2, LCZ_9_m2,
                #    LCZ_10_m2, LCZ_A_m2, LCZ_B_m2, LCZ_C_m2, LCZ_D_m2, LCZ_E_m2, LCZ_F_m2, LCZ_G_m2, T_LCZ_m2,]
                total = float(llista[17])
                dicc = {value: round(100*float(llista[i])/total, 2) for i, value in enumerate(LCZ_KEYS)}
                # retornem la key (LCZ) associada que ocupa mes area en el buffer...
                return dicc, max(dicc, key=dicc.get)
            case 1:
                #          0       1       2       3       4       5       6       7       8       9       10
                #          11      12      13      14      15      16
                # 1: [%LCZ_1, %LCZ_2, %LCZ_3, %LCZ_4, %LCZ_5, %LCZ_6, %LCZ_7, %LCZ_8, %LCZ_9,% LCZ_10, %LCZ_A,
                #     %LCZ_B, %LCZ_C, %LCZ_D, %LCZ_E, %LCZ_F, %LCZ_G,], },
                dicc = {value: round(float(llista[i]), 2) for i, value in enumerate(LCZ_KEYS)}
                return dicc, max(dicc, key=dicc.get)
            case _:
                return dicc0, ""


def get_lcz_image(lcz: str) -> str:
    import os
    return os.path.join(os.getcwd(), f'lcz_img/lcz{lcz}.png')


def get_lcz_station_image(eoi_code: str, v: int) -> str:
    import os
    # versio 0 (Mariela) / versio 1 (Wenyu)
    match v:
        case 0:
            return os.path.join(os.getcwd(), f'lcz_bf_v{v}/{eoi_code}_lcz.jpg')
        case 1:
            return os.path.join(os.getcwd(), f'lcz_bf_v{v}/LCZ_{int(eoi_code)}.jpg')
        case _:
            return ''


def get_vuci(lcz: str) -> float:
    from air_pollution_data.datos import LCZ_KEYS
    # Vulnerability Urban Climate Index (taula Joan Gilabert).
    # Diccionari del tipus lcz:vuci
    #         1    2   3   4   5   6   7   8   9   10  A   B   C   D   E   F   G
    valors = [100, 80, 70, 70, 60, 50, 60, 50, 30, 70, 50, 30, 30, 20, 40, 10, 20]
    vuci = {k: v for k, v in zip(LCZ_KEYS, valors)}

    return vuci.get(lcz, 0)


def get_vuci_ponderado(eoi_code: str, tipo: int) -> float:
    from air_pollution_data.datos import LCZ_KEYS
    lcz_dict, lcz_max = get_lczmax(eoi_code, tipo)
    # vamos a calcular el VUCI ponderado
    suma = 0.0
    for i, k in enumerate(LCZ_KEYS):
        suma += lcz_dict.get(k, 0.0) * get_vuci(k)
    return suma / 100.0


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
# -----------------------------------------------------------
# cvpi<50    |   D     |   C1       |   C1       |   C1    |
# 50<cvpi<60 |   C2    |   B        |   B        |   B     |
# 60<cvpi<70 |   C2    |   B        |   A2       |   A2    |
# 70<cvpi    |   C2    |   B        |   A2       |   A1    |
# -----------------------------------------------------------
def getcr(dato: float) -> int:
    limits = [50.0, 60.0, 70.0]
    cc = [dato < limit for limit in limits]  # [True|False, True|False, True|False]
    try:
        return cc.index(True) + 1
    except ValueError:
        return len(limits) + 1


# -----------------------------------------------------------
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
    scenario_matrix = ['D', 'C2', 'C2', 'C2', 'C1', 'B', 'B', 'B', 'C1', 'B', 'A2', 'A2', 'C1', 'B', 'A2', 'A1']

    scenario_key = scenario_matrix[4 * (getcr(vuci) - 1) + getcr(cvpi)]
    
    return scenario_key, scenarios_dict.get(scenario_key, "none")


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
def get_hazard_daily_data(df: pd.DataFrame) -> float:
    from air_pollution_data.datos import HORES_DIA
    # df es el registre que conte els valors horaris d'un dia del contaminant.
    # Aixo vol dir que df.shape[0] == 1
    value_list = [df[h].iloc[0] if h in df.columns else np.nan for h in HORES_DIA]
    return round(np.nanmedian(np.array(value_list)), 2)
