import os
import numpy as np
import pandas as pd
import pydeck as pdk

from air_pollution_data.datos import DEFAULT_COLOR_TABLE, DEFAULT_CONTAMINANT


# np.nan tiene asociado el color 250_250_250.png
def get_color_table(tcolor: int = DEFAULT_COLOR_TABLE) -> dict:
    out_dict = {0: ["nodata", [250, 250, 250]]}

    match tcolor:
        case 3:
            out_dict[1] = ["low", [0, 200, 0]]
            out_dict[2] = ["medium", [255, 255, 0]]
            out_dict[3] = ["high", [255, 0, 0]]
        case 5:
            out_dict[1] = ["low", [0, 200, 0]]
            out_dict[2] = ["medium", [255, 255, 0]]
            out_dict[3] = ["high", [255, 150, 0]]
            out_dict[4] = ["very high", [255, 0, 0]]
            # out_dict[1] = ["low", [0, 0, 255]] # output[2] = ["medium", [0, 200, 0]]
            # out_dict[3] = ["high", [255, 255, 0]] # output[4] = ["very high", [255, 0, 0]]
        case _:
            out_dict[1] = ["low", [0, 255, 0]]
            out_dict[2] = ["low", [0, 200, 0]]
            out_dict[3] = ["medium", [255, 255, 0]]
            out_dict[4] = ["medium", [255, 150, 0]]
            out_dict[5] = ["medium", [255, 55, 0]]
            out_dict[6] = ["high", [255, 0, 0]]
            out_dict[7] = ["high", [150, 10, 50]]

    return out_dict


def get_color_caption(ncolor: int, tcolor: int = DEFAULT_COLOR_TABLE) -> tuple:
    paleta = get_color_table(tcolor)
    [caption, rgb] = paleta.get(ncolor, ["no data", [250, 250, 250]])
    color = os.path.join(os.getcwd(), f"rgb_img/{rgb[0]:03d}_{rgb[1]:03d}_{rgb[2]:03d}.png")
    return caption, color


# ---------------------------------------------------------------------------------------------------------------------
def get_df_histograma_hores(df: pd.DataFrame, contaminante: str = DEFAULT_CONTAMINANT) -> pd.DataFrame:
    from air_pollution_data.datos import HORES_DIA
    from . import get_hazard_daily_data

    # df es el registre que conte els valors horaris del contaminant
    # Aixo vol dir que df.shape[0] == 1
    # calculem el valor mig del contaminant...
    v_mean = get_hazard_daily_data(df)

    # ara creem la informacio que volem plotejar...
    value_dict = {
        "hora": [h + 1 for h in range(24)],
        f"{contaminante}": [df[h].iloc[0] if h in df.columns else 0.0 for h in HORES_DIA],
        "mean": [v_mean if h in df.columns else 0.0 for h in HORES_DIA],
        "good": [20.0 if h in df.columns else 0.0 for h in HORES_DIA],
        "moderate": [40.0 if h in df.columns else 0.0 for h in HORES_DIA],
        "bad": [60.0 if h in df.columns else 0.0 for h in HORES_DIA],
    }
    return pd.DataFrame(value_dict)


def get_information_about_data(df: pd.DataFrame, eoi_name: str, ymd: str, contamina: str = DEFAULT_CONTAMINANT) -> str:
    from air_pollution_data.datos import DEFAULT_YEAR
    from . import get_codi_eoi

    msg = f"{contamina} data for {eoi_name} ({get_codi_eoi(eoi_name)}) in {ymd}"
    if df.empty:
        return f"No {msg}. We use IDAEA's {DEFAULT_YEAR} mean value."
    elif df.shape[0] != 1:
        return f"Insconsistent {msg}."
    else:
        return f"{msg}."


def get_station_map_data(df: pd.DataFrame) -> tuple:
    from air_pollution_data.datos import EOI_DF
    from . import get_cm

    # obtenemos los datos necesarios de las estaciones del proyecto que estan almacenadas en ESTACIONS y EOI_DF
    # a partir de ellas calcularemos las capas que queremos mostrar en el mapa.
    llocs = EOI_DF[['lon', 'lat', 'etiqueta']]

    # calculamos el punto central del conjunto de estaciones.
    lon_cm, lat_cm = get_cm(llocs)

    # definimos la capa d'estaciones del proyecto
    layer_s = pdk.Layer("ScatterplotLayer",
                        data=llocs,
                        get_position=['lon', 'lat'],
                        auto_highlight=True,
                        get_radius=500,
                        get_color='[0,0,255,75]',
                        pickable=True)

    # definimos ahora la capa d'etiquetas (labels) de las estaciones
    layer_l = pdk.Layer("TextLayer",
                        data=llocs,
                        get_position=['lon', 'lat'],
                        get_text='etiqueta',
                        get_color='[0,0,255]',
                        get_size=12,
                        get_alignment_baseline="'bottom'")

    # ahora nos falta la capa de la estacion escogida, si es que hay datos asociados
    if df.empty:
        selected_layers = [layer_s, layer_l]
    else:
        layer_p = pdk.Layer("ScatterplotLayer",
                            data=df[['lon', 'lat', 'codi_eoi']],
                            get_position=['lon', 'lat'],
                            auto_highlight=True,
                            get_radius=500,
                            get_color='[255,0,255,150]',
                            pickable=True)

        selected_layers = [layer_s, layer_l, layer_p]

    # Una vez tenemos las capas que queremos poner en el mapa (selected_layers), vamos a definir el mapa base.
    # Cambiamos mapbox (default) per ICGC contextmaps:
    map_style = "mapbox://styles/mapbox/light-v9"
    # map_style = "https://geoserveis.icgc.cat/contextmaps/icgc_mapa_base_gris_simplificat.json"

    # Y ahora definimos la vista inicial:
    init_view_state = pdk.ViewState(latitude=lat_cm, longitude=lon_cm, zoom=10)

    return map_style, init_view_state, selected_layers


def get_color(hazard_value: float,
              hazard: float,
              vuci: float,
              cvpi: float,
              tcolor: int = DEFAULT_COLOR_TABLE,
              scene_key: str = '-',
              contamina: str = DEFAULT_CONTAMINANT
              ) -> tuple:
    match contamina:
        case 'NO2':
            match tcolor:
                case 7:
                    # tcolor = 7
                    # COLOR7TO3 = { 0:0, 1:1, 2:1, 3:2, 4:2, 5:2, 6:3, 7:3 }
                    # RISK_DF7 index=['<20', '20-30', '30-40', '40-50', '50-60', '>60']
                    risk_matrix = {
                        'D': [1, 2, 3, 4, 5, 5],  # poco vulnerable
                        'C2': [2, 3, 4, 5, 5, 5],  # VUCI poco vulnerable, CVP vulnerable
                        'C1': [2, 3, 4, 5, 5, 5],  # VUCI vulnerable, CVP poco vulnerable
                        'B': [3, 4, 5, 6, 6, 6],  # vulnerable
                        'A2': [3, 4, 5, 6, 6, 6],  # muy vulnerable
                        'A1': [3, 4, 5, 6, 6, 6]  # extremadamente vulnerable
                    }
                    # obtenemos el valor del COLOR7 definido por risk_matrix
                    llista = risk_matrix.get(scene_key, [])

                    if np.isnan(hazard) or not llista:
                        k2 = 0
                    else:
                        fhazard = hazard * (vuci + cvpi) / 100.0
                        rangos = {
                            (float("-inf"), 20.0): llista[0],
                            (20.0, 30.0): llista[1],
                            (30.0, 40.0): llista[2],
                            (40.0, 50.0): llista[3],
                            (50.0, 60.0): llista[4],
                            (60.0, float("inf")): llista[5],
                        }
                        k2 = next(v for (low, high), v in rangos.items() if low < fhazard <= high)

                    k1 = k2

                case 5:
                    # old get_no2_color5 on hazard, vuci i cvpi son normalitzats (hazard_norm, vuci_norm, cvpi_norm)
                    # risk = hazard x scenario_code
                    # vamos a modificar el hazard segun los valores de vuci i cvpi.
                    if np.isnan(hazard_value):
                        k1 = 0
                    else:
                        rangos = {
                            (float("-inf"), 20.0): 1,
                            (20.0, 40.0): 2,
                            (40.0, 60.0): 3,
                            (60.0, float("inf")): 4,
                        }
                        k1 = next(v for (low, high), v in rangos.items() if low < hazard_value <= high)

                    indice_compuesto = (vuci + cvpi + hazard) / 3.0
                    if np.isnan(indice_compuesto):
                        k2 = 0
                    else:
                        rangos = {
                            (float("-inf"), 0.9): 1,
                            (0.9, 1.0): 2,
                            (1.0, 1.1): 3,
                            (1.1, float("inf")): 4,
                        }
                        k2 = next(v for (low, high), v in rangos.items() if low < indice_compuesto <= high)

                case 3:
                    # tcolor = 3
                    # risk = hazard x scenario_code
                    # vamos a modificar el hazard segun los valores de vuci i cvpi.
                    if np.isnan(hazard):
                        k2 = 0
                    else:
                        fhazard = hazard * (vuci + cvpi) / 100.0
                        rangos = {
                            (float("-inf"), 30.0): 1,
                            (30.0, 40.0): 2,
                            (40.0, float("inf")): 3,
                        }
                        k2 = next(v for (low, high), v in rangos.items() if low < fhazard <= high)

                    k1 = k2

                case _:
                    k1 = 0
                    k2 = 0
        case _:
            k1 = 0
            k2 = 0

    # aplicamos la paleta de colors...
    caption1, color1 = get_color_caption(k1, tcolor)
    caption2, color2 = get_color_caption(k2, tcolor)
    return k1, color1, caption1, k2, color2, caption2


class AirPollutionIndex:
    def __init__(self, eoi_code: str):
        from air_pollution_data.datos import DEFAULT_VERSION, DEFAULT_YEAR, DEFAULT_CVP_INDEX
        from . import get_lczmax, get_vuci_ponderado, get_cvp, get_no2_mean

        # calculamos los porcentajes de cada LCZ, que se almacenan en un diccionario {lcz:%}
        # devolvemos tambien el codigo de LCZ maximo
        self.lcz_dict, self.lcz_max = get_lczmax(eoi_code, DEFAULT_VERSION)

        # vamos a calcular el self.vuci como VUCI ponderado
        self.vuci_ponderado = get_vuci_ponderado(eoi_code, DEFAULT_VERSION)

        self.cvpi = get_cvp(eoi_code, DEFAULT_YEAR, DEFAULT_CVP_INDEX)

        self.no2_mean = get_no2_mean(eoi_code, DEFAULT_YEAR)

    def write(self):
        print(f"LCZ %: {self.lcz_dict}")
        print(f"LCZ max: {self.lcz_max}")
        print(f"VUCI ponderado: {self.vuci_ponderado}")
        print(f"CVPI: {self.cvpi}")
        print(f"NO2 mean: {self.no2_mean}")


class AirPollutionRisk:
    def __init__(self, eoi_code: str, df: pd.DataFrame):
        from air_pollution_data.datos import EOI_DF
        from . import get_hazard_daily_data

        rdi = AirPollutionIndex(eoi_code)
        self.hazard_value = get_hazard_daily_data(df)

        # necesitamos calcular hazard_norm, vuci_norm y cvpi_norm

        no2_mean_list = []
        vuci_ponderado_list = []
        cvpi_list = []
        for estacion in EOI_DF["codi_eoi"]:
            datos = AirPollutionIndex(estacion)
            no2_mean_list.append(datos.no2_mean)
            vuci_ponderado_list.append(datos.vuci_ponderado)
            cvpi_list.append(datos.cvpi)

        # aproximacion ya que mezclamos datos dia con medias anuales
        hazard = self.hazard_value / np.nanmean(np.array(no2_mean_list))
        vuci = rdi.vuci_ponderado / np.nanmean(np.array(vuci_ponderado_list))
        cvpi = rdi.cvpi / np.nanmean(np.array(cvpi_list))

        k1, color1, caption1, k2, color2, caption2 = get_color(self.hazard_value, hazard, vuci, cvpi, 5)

        self.risk = k1
        self.risk_image = color1
        self.risk_caption = caption1
        self.vi = k2
        self.vi_image = color2
        self.vi_caption = caption2

    def write(self):
        print(f"Hazard value: {self.hazard_value}")
        print(f"Risk: {self.risk}")
        print(f"Risk Image: {self.risk_image}")
        print(f"Risk Caption: {self.risk_caption}")
        print(f"VI: {self.vi}")
        print(f"VI Image: {self.vi_image}")
        print(f"VI Caption: {self.vi_caption}")
