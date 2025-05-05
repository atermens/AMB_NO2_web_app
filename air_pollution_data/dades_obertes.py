
import numpy as np
import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------
# dades associades al set de dades obertes
# ----------------------------------------------------------------------------------------------------------------------
#
DATASET_ID = "tasf-thgu"
DATASET_DOMAIN = "analisi.transparenciacatalunya.cat"
DATASET_LIMIT = 50000

URL_DATA = f"https://{DATASET_DOMAIN}/resource/{DATASET_ID}.json?"
# "https://analisi.transparenciacatalunya.cat/resource/tasf-thgu.json?"
# ----------------------------------------------------------------------------------------------------------------------


def get_all_eoi_data(ymd: str) -> pd.DataFrame:
    from air_pollution_data.datos import ESTACIONS

    # obtenim les dades en format JSON de tots els contaminants i de totes les estacions
    # per una data determinada (format 'yyyy-mm-dd')
    df = pd.read_json(f"{URL_DATA}$where=data='{ymd}T00:00:00.000'", orient='records')
    if df.empty:
        return df
    else:
        # abans de res li canviem les columnes de longitud i latitud per si s'han de mapejar despres...
        df.rename(columns={'latitud': 'lat', 'longitud': 'lon'}, inplace=True)
        # ara filtrem per a totes les estacions de l'estudi, segons ESTACIONS["nom_eoi"]:
        return df[df.nom_estacio.isin(ESTACIONS["nom_eoi"])]


def get_all_eoi_data_contaminant(ymd: str, contaminante: str) -> pd.DataFrame:
    # obtenim les dades de totes les les estacions del projecte en una data determinada
    df = get_all_eoi_data(ymd)
    if df.empty:
        return df
    else:
        # filtrem ara pel contaminant que ens interessa:
        return df[df.contaminant.eq(contaminante)]


def get_eoi_data_contaminant(ymd: str, nom_eoi: str, contaminante: str) -> pd.DataFrame:
    # obtenim les dades de totes les estacions del projecte per un contaminant en una data determinada
    df = get_all_eoi_data_contaminant(ymd, contaminante)
    if df.empty:
        return df
    else:
        # filtrem ara per l'estacio que ens interessa
        return df[df.nom_estacio.eq(nom_eoi)]


def get_cm(df: pd.DataFrame) -> tuple:
    # df conte uns camps lon, lat. Aixi d'un conjunt de posicions, calculem el seu centroide:
    if df.empty:
        # retornem el centre del BBOX que defineix Catalunya lon [0,3] i lat [40.0 43.0]
        return 1.75, 41.5
    else:
        # obtenim el centre de masses definit per (lon,lat):
        return df.lon.mean(), df.lat.mean()


def get_no2_annual_mean(nom_eoi: str, yr: int) -> float:
    from . import get_last_day, get_hazard_daily_data
    val_list = []
    for mes in range(1, 13):
        for dia in range(1, get_last_day(yr, mes) + 1):
            ymd = f"{yr:0>4}-{mes:0>2}-{dia:0>2}"
            df = get_eoi_data_contaminant(ymd, nom_eoi, 'NO2')
            if not df.empty:
                val_list.append(get_hazard_daily_data(df))
    return round(np.nanmedian(np.array(val_list)), 2)
