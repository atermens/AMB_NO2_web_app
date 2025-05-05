# -*- coding: utf-8 -*-
def get_no2_data(eoi_code: str, yr: int) -> list:
    from air_pollution_data.datos import EOI_NO2

    dicc = EOI_NO2.get(eoi_code, {})  # {yr: [0, mean,], yr: [1, mean, max, min, d20, d50,],}

    return dicc.get(yr, [])


def get_no2_mean(eoi_code: str, yr: int) -> float:
    import numpy as np

    lst = get_no2_data(eoi_code, yr)

    if not lst:
        return np.nan
    else:
        match lst[0]:
            case 0 | 1:
                return float(lst[1])
            case _:
                return np.nan


# deprecated function ---
def get_no2_2019(eoi_code: str) -> float:
    return get_no2_mean(eoi_code, 2019)
