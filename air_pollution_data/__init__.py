# -*- coding: utf-8 -*-
from .auxiliar import AirPollutionIndex, AirPollutionRisk
from .auxiliar import get_df_histograma_hores, get_information_about_data, get_station_map_data
from .dades_obertes import get_eoi_data_contaminant, get_cm
from .icgc import get_lczmax, get_lcz_image, get_lcz_station_image, get_vuci_ponderado, get_hazard_daily_data
from .idaea import get_no2_mean
from .idescat import get_cvp
from .stations import get_codi_eoi, get_nom_eoi

__all__ = [
    'get_last_day',
    'AirPollutionIndex', 'AirPollutionRisk',
    'get_df_histograma_hores', 'get_information_about_data', 'get_station_map_data',
    'get_eoi_data_contaminant', 'get_cm',
    'get_lczmax', 'get_lcz_image', 'get_lcz_station_image', 'get_vuci_ponderado', 'get_hazard_daily_data',
    'get_no2_mean',
    'get_cvp',
    'get_codi_eoi', 'get_nom_eoi',
]


def get_last_day(yr: int, mes: int) -> int:
    match mes:
        case 1 | 3 | 5 | 7 | 8 | 10 | 12:
            return 31
        case 4 | 6 | 9 | 11:
            return 30
        case 2:
            return 29 if ((yr % 4 == 0 and yr % 100 != 0) or (yr % 400 == 0)) else 28
        case _:
            return -1
