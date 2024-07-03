# -*- coding: utf-8 -*-
# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.CO

import os
import numpy as np
import pandas as pd

import streamlit as st
import pydeck as pdk

import operator

from AirPollutionData import dades_obertes as od
from AirPollutionData import stations
from AirPollutionData import idescat
from AirPollutionData import icgc
from AirPollutionData import idaea


CWD = os.getcwd()

YEAR_OF_DATA = [2019, 2022, 2023] # conjunto datos anuales que tenemos

DEFAULT_YEAR = 2023

DEFAULT_VERSION = 1 # version 0: TFM Mariela | 1: TFM Wenyu

DEFAULT_CVP_INDEX = 1 # version datos poblacio, 0: Joan (TFM Mariela) | 1: idescat por seccion censal

DEFAULT_CONTAMINANT = 'NO2'

# np.nan tiene asociado el color 250_250_250.png
COLOR3 = {
    0: os.path.join(CWD, "rgb_img/250_250_250.png"),
    1: os.path.join(CWD, "rgb_img/000_200_000.png"),
    2: os.path.join(CWD, "rgb_img/255_255_000.png"),
    3: os.path.join(CWD, "rgb_img/255_000_000.png"),
}

CAPTION3 = {
    0: "no data",
    1: "low",
    2: "medium",
    3: "high",
}

COLOR5 = {
    0: os.path.join(CWD, "rgb_img/250_250_250.png"), # no data
    1: os.path.join(CWD, "rgb_img/000_200_000.png"), # verde - bueno (menor que 20)
    2: os.path.join(CWD, "rgb_img/255_255_000.png"), # amarillo - moderado (20-39)
    3: os.path.join(CWD, "rgb_img/255_150_000.png"), # naranja - malo (40-59)
    4: os.path.join(CWD, "rgb_img/255_000_000.png")  # rojo - muy malo (mayor que 60)
}

VCOLOR5 = {
    0: os.path.join(CWD, "rgb_img/250_250_250.png"), # no data
    1: os.path.join(CWD, "rgb_img/000_000_255.png"), # azul <= 0.9
    2: os.path.join(CWD, "rgb_img/000_200_000.png"), # verde - <=1
    3: os.path.join(CWD, "rgb_img/255_255_000.png"), # amarillo - <= 1.1
    4: os.path.join(CWD, "rgb_img/255_000_000.png")  # rojo - > 1.1
}

CAPTION5 = {
    0: "no data",
    1: "low",
    2: "medium",
    3: "high",
    4: "very high",
}
COLOR7 = {
    0: os.path.join(CWD, "rgb_img/250_250_250.png"),
    1: os.path.join(CWD, "rgb_img/000_255_000.png"),
    2: os.path.join(CWD, "rgb_img/000_200_000.png"),
    3: os.path.join(CWD, "rgb_img/255_255_000.png"),
    4: os.path.join(CWD, "rgb_img/255_150_000.png"),
    5: os.path.join(CWD, "rgb_img/255_055_000.png"),
    6: os.path.join(CWD, "rgb_img/255_000_000.png"),
    7: os.path.join(CWD, "rgb_img/150_010_050.png"),
}

CAPTION7 = {
    0: "no data",
    1: "low",
    2: "low",
    3: "medium",
    4: "medium",
    5: "medium",
    6: "high",
    7: "high",
}

# ---------------------------------------------------------------------------------------------------------------------
def get_hazard_data(df: pd.DataFrame) -> float:
    # df es el registre que conte els valors horaris del contaminant.
    # Aixo vol dir que df.shape[0] == 1
    value_list = [ df[h].iloc[0]  if h in df.columns  else np.nan  for h in od.HORES ]
    return round(np.nanmedian(np.array(value_list)), 2)


def get_df_histograma_hores(contaminante: str, df: pd.DataFrame) -> pd.DataFrame:
    # df es el registre que conte els valors horaris del contaminant.
    # Aixo vol dir que df.shape[0] == 1
    # calculem el valor mig del contaminant...
    v_mean = get_hazard_data(df)

    # ara creem la informacio que volem plotejar...
    value_dict = {
        "hora": [ h + 1 for h in range(24)],
        f"{contaminante}": [ df[h].iloc[0]  if h in df.columns  else 0.0  for h in od.HORES ],
        "mean": [v_mean if h in df.columns else 0.0 for h in od.HORES],
        "good": [ 20.0 if h in df.columns  else 0.0  for h in od.HORES ],
        "moderate": [40.0 if h in df.columns else 0.0 for h in od.HORES],
        "bad": [60.0 if h in df.columns else 0.0 for h in od.HORES],
        }
    return pd.DataFrame(value_dict)


def get_information_about_data(eoi_name: str, ymd: str, contaminante: str, df: pd.DataFrame) -> str:
    msg = f"{contaminante} data for {eoi_name} ({stations.get_codi_eoi(eoi_name)}) in {ymd}"
    if df.empty:
        return f"No {msg}. We use IDAEA's {DEFAULT_YEAR} mean value."
    elif df.shape[0] != 1:
        return f"Insconsistent {msg}."
    else:
        return msg


def get_station_map_data(df: pd.DataFrame) -> tuple:
    # obtenemos los datos necesarios de las estaciones del proyecto que estan almacenadas en ESTACIONS y EOI_DF
    # a partir de ellas calcularemos las capas que queremos mostrar en el mapa.
    llocs = stations.EOI_DF[['lon', 'lat', 'etiqueta']]
    
    # calculamos el punto central del conjunto de estaciones.
    lonCM, latCM = od.get_CM(llocs)

    # definimos la capa d'estaciones del proyecto
    layerS = pdk.Layer( "ScatterplotLayer",
        data = llocs, 
        get_position = ['lon', 'lat'],
        auto_highlight = True,
        get_radius = 500, 
        get_color = '[0, 0, 255, 75]',
        pickable = True )
    
    # definimos ahora la capa d'etiquetas (labels) de las estaciones
    layerL = pdk.Layer( "TextLayer",
        data = llocs, 
        get_position = ['lon', 'lat'],
        get_text = 'etiqueta', 
        get_color = '[0, 0, 255]',
        get_size = 12, 
        get_alignment_baseline = "'bottom'" )

    # ahora nos falta la capa de la estacion escogida, si es que hay datos asociados
    if df.empty:
        selected_layers = [layerS, layerL]
    else:
        layerP = pdk.Layer( "ScatterplotLayer",
            data =  df[['lon', 'lat', 'codi_eoi']],
            get_position = ['lon', 'lat'],
            auto_highlight = True,
            get_radius = 500, 
            get_color = '[255, 0, 255, 150]',
            pickable = True )

        selected_layers = [layerS, layerL, layerP]

    # Una vez tenemos las capas que queremos poner en el mapa (selected_layers), vamos a definir el mapa base. 
    # Cambiamos mapbox (default) per ICGC contextmaps: mapstyle = "mapbox://styles/mapbox/light-v9"
    map_style = "https://geoserveis.icgc.cat/contextmaps/icgc_mapa_base_gris_simplificat.json"
    
    # Y ahora definimos la vista inicial:
    init_view_state = pdk.ViewState(latitude=latCM, longitude=lonCM, zoom=10)
    
    return ( map_style, init_view_state, selected_layers )


def get_color7(scene_key: str, hazard: float, vuci: float, cvpi: float) -> tuple:
    # COLOR7TO3 = { 0:0, 1:1, 2:1, 3:2, 4:2, 5:2, 6:3, 7:3 }
    # RISK_DF7 index=['<20', '20-30', '30-40', '40-50', '50-60', '>60']
    risk_matrix = {
        'D':  [1,2,3,4,5,5], # poco vulnerable
        'C2': [2,3,4,5,5,5], # VUCI poco vulnerable, CVP vulnerable
        'C1': [2,3,4,5,5,5], # VUCI vulnerable, CVP poco vulnerable
        'B':  [3,4,5,6,6,6], # vulnerable
        'A2': [3,4,5,6,6,6], # muy vulnerable
        'A1': [3,4,5,6,6,6]  # extremadamente vulnerable
        }
    # obtenemos el valor del COLOR7 definido por risk_matrix
    llista = risk_matrix.get(scene_key, [])

    if np.isnan(hazard) or not llista:
        k = 0
    else:
        fhazard = hazard * (vuci + cvpi) / 100.0
        if fhazard < 20.0:
            k = llista[0]
        elif fhazard < 30.0:
            k = llista[1]
        elif fhazard < 40.0:
            k = llista[2]
        elif fhazard < 50.0:
            k = llista[3]
        elif fhazard < 60.0:
            k = llista[4]
        else:
            k = llista[5]

    # aplicamos la paleta de 7 colores
    return (k, COLOR7.get(k, ''), CAPTION7.get(k, ''))


def get_color3(scene_key: str, hazard: float, vuci: float, cvpi: float) -> tuple:
    # risk = hazard x scenario_code
    # vamos a modificar el hazard segun los valores de vuci i cvpi.
    if np.isnan(hazard):
        k = 0
    else:
        fhazard = hazard * (vuci + cvpi) / 100.0
        if fhazard < 30.0:
            k = 1
        elif fhazard < 40.0:
            k = 2
        else:
            k = 3

    return (k, COLOR3.get(k, ''), CAPTION3.get(k, ''))


def get_no2_color5(hazard: float, hazard_norm: float, vuci_norm: float, cvpi_norm: float) -> tuple:
    # risk = hazard x scenario_code
    # vamos a modificar el hazard segun los valores de vuci i cvpi.
    if np.isnan(hazard):
        k1 = 0
    else:
        if hazard < 20.0:
            k1 = 1
        elif hazard < 40.0:
            k1 = 2
        elif hazard < 60.0:
            k1 = 3
        else:
            k1 = 4

    indice_compuesto = (vuci_norm + cvpi_norm + hazard_norm ) / 3.0
    if np.isnan(indice_compuesto):
        k2 = 0
    else:
        if indice_compuesto <= 0.9:
            k2 = 1
        elif indice_compuesto <= 1.0:
            k2 = 2
        elif indice_compuesto <= 1.1:
            k2 = 3
        else:
            k2 = 4

    return (k1, COLOR5.get(k1, ''), CAPTION5.get(k1, ''), k2, VCOLOR5.get(k2, ''), CAPTION5.get(k2, ''))


class AirPollutionIndex:
    def __init__(self, eoi_code:str):
        # calculamos los porcentajes de cada LCZ, que se almacenan en un diccionario {lcz:%}
        # devolvemos tambien el codigo de LCZ maximo
        self.lcz_dict, self.lcz_max = icgc.get_LCZmax(eoi_code, DEFAULT_VERSION)

        # vamos a calcular el self.vuci como VUCI ponderado
        self.vuci_ponderado = icgc.get_VUCI_ponderado(eoi_code, DEFAULT_VERSION)

        self.cvpi = idescat.get_CVP(eoi_code, DEFAULT_YEAR, DEFAULT_CVP_INDEX)

        self.no2_mean = idaea.get_NO2_mean(eoi_code, DEFAULT_YEAR)


class AirPollutionRisk:
    def __init__(self, eoi_code: str, df: pd.DataFrame):
        rdi = AirPollutionIndex(eoi_code)
        self.hazard_value = get_hazard_data(df)

        # necesitamos calcular hazard_norm, vuci_norm y cvpi_norm

        no2_mean_list = [ ]
        vuci_ponderado_list = []
        cvpi_list = []
        for estacion in stations.EOI_DF["codi_eoi"]:
            datos = AirPollutionIndex(estacion)
            no2_mean_list.append(datos.no2_mean)
            vuci_ponderado_list.append(datos.vuci_ponderado)
            cvpi_list.append(datos.cvpi)

        hazard = self.hazard_value / np.nanmean(np.array(no2_mean_list)) # aproximacion ya que mezclamos datos dia con medias anuales
        vuci = rdi.vuci_ponderado / np.nanmean(np.array(vuci_ponderado_list))
        cvpi = rdi.cvpi / np.nanmean(np.array(cvpi_list))

        self.risk, self.risk_image, self.risk_caption, self.vi, self.vi_image, self.vi_caption = get_no2_color5(self.hazard_value, hazard, vuci, cvpi)




def streamlit_main():
    # SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON (1rst sentence Streamlit!!!)
    st.set_page_config(layout="wide", page_title="Air Quality Index", page_icon=":earth:")

    st.title("NO2 Air Pollution Data and Local Climate Zones in the AMB")

    with st.expander("About"):
        st.markdown("""
            Cities are growing fast and LCZs are a new way of classifying urban areas. 
            We know that air pollution is a factor that internally affects humans and their health. 
            It has direct repercussions on the human being and its analysis helps to know and understand what we must do to mitigate the damage.

            This viewer contains cross information between the classifications of the LCZs and air quality data, 
            with NO2 concentrations as target pollutant, at the Barcelona Metropolitan Area (AMB).

            We use NO2 values from the dataset <tasf-thgu> of dadesobertes.gencat.cat. 
            If there is not data, we use NO2 mean value of a year analized by IDAEA.
            """)
        # st.latex(r''' a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} = \sum_{k=0}^{n-1} ar^k = a \left(\frac{1-r^{n}}{1-r}\right) ''')

    # ======================================================
    row1_1, row1_2, row1_3 = st.columns((1, 1, 3))

    row1_1.subheader(f"Select...")
    # escogemos el nombre de la estacion de la cual queremos consultar los datos
    eoi_name = row1_1.selectbox("station", stations.EOI_DF)
    
    # escogemos la fecha que nos interesa, por defecto el dia de la consulta...
    row1_2.subheader(f" ")
    ymd = row1_2.date_input("one day")
    
    # Restringimos a los dos contaminantes descritos en el TFM, aunque por defecto trataremos siempre el NO2.
    # contaminante = row1_1.radio("pollutant:", ('NO2', 'PM2.5'))
    # contaminante = row1_1.selectbox("contaminant:", pd.DataFrame(CONTAMINANTS))
    contaminante = DEFAULT_CONTAMINANT

    # A partir de estos datos, obtenemos los datos (JSON) del dataset de dades obertes.
    # En principio nos tiene que devolver un DataFrame con solo una fila. En caso contrario el DataFrame estara vacio.
    df = od.get_data(ymd, eoi_name, contaminante)

    # Primero, vamos a pintar el mapa de situacion de las estaciones:
    mapstyle, initviewstate, selectedlayers = get_station_map_data(df)
    # row1_2.map(data=df, zoom=13, use_container_width=True)
    row1_3.pydeck_chart(pdk.Deck(map_style=mapstyle, initial_view_state=initviewstate, layers=selectedlayers))

    # buscamos el codigo de estacion asociado a eoi_name:
    eoi_code = stations.get_codi_eoi(eoi_name)

    # calculamos todos los datos del riesgo associado al contaminante:
    rd = AirPollutionRisk(eoi_code, df)

    row1_1.write(" ")
    row1_1.subheader(f" {contaminante} Daily Mean Concentration:")
    #row1_1.subheader(f" {contaminante} Air Quality Index ({DEFAULT_YEAR}):")
    # aqui pondremos el semaforo con el risk_data.risk
    semafor = rd.risk_image
    if os.path.isfile(semafor): row1_1.image(semafor, caption=rd.risk_caption, width=150)

    row1_2.write(" ")
    row1_2.subheader(f" Complex Vulnerability Index:")
    # aqui pondremos el semaforo con el risk_data.risk
    semafor = rd.vi_image
    if os.path.isfile(semafor): row1_2.image(semafor, caption=rd.vi_caption, width=150)

    # ======================================================
    # Vamos a comprovar si tenemos datos o no y calculamos todos los datos del riesgo asociado al contaminante:
    st.write(f" ")
    st.subheader(get_information_about_data(eoi_name, ymd, contaminante, df))
    #st.write(f"--- Year: DEFAULT_YEAR ---")
    #st.write(f"LCZ max: {rd.lcz_max.get(yr, '-')} | VUCI: {rd.vuci.get(yr, '-')} | CVP: {rd.cvpi.get(yr, '-')}")
    #    st.write(f"Hazard({contaminante}): {rd.hazard_value.get(yr, '-')} | NO2 mean: {rd.no2_mean.get(yr, '-')}")
    #    st.write(f" Scenario: {rd.scenario_code.get(yr, '-')} | Risk: {rd.risk.get(yr, '-')}")

    # ======================================================
    row2_1, row2_2 = st.columns((2, 3))
    # imagen del buffer de LCZ de la estacion escogida (eoi_code)
    row2_1.write(f"LCZ data in {eoi_name} area")
    img = icgc.get_LCZ_station_image(eoi_code, DEFAULT_VERSION)
    if os.path.isfile(img): row2_1.image(img)

    # pintamos ahora el histograma de valores del contaminante...
    if not df.empty:
        row2_2.write(f"{contaminante} data in {eoi_name} ({ymd})")
        cdf = get_df_histograma_hores(contaminante, df)
        row2_2.line_chart(cdf,
                          x="hora",
                          y=[f"{contaminante}","mean", "good", "moderate", "bad"],
                          color = ["#0033cc", "#ff0000", "#33cc33", "#66ccff", "#ff9900"])  # plot modo grafic linies no2-bad-good-mean-moderate

        # plot modo histograma. En aquest cas, es fa un histograma acumulat...
        #row2_2.write(f"{contaminante} data in {eoi_name} ({ymd}) - cumulative histogram")
        #row2_2.bar_chart(get_df_histograma_hores(contaminante, df))

    # ======================================================
    st.subheader(f"LCZ distribution:")
    # vamos a pintar la informacion asociada a cada LCZ, con la imagen associada
    # el procedimiento va a ser muy rudimentario y seguro que se puede optimizar mas...
    # partimos la columna en 10 subcolumnas (una para cada LCZ)
    #ck = [ ['1', 'A'], ['2', 'B'], ['3', 'C'], ['4', 'D'], ['5', 'E'], ['6', 'F'], ['7', 'G'], ['8'], ['9'], ['10'] ]
    ck = [ ['1', '6', 'A', 'F'], ['2', '7', 'B', 'G'], ['3', '8', 'C'], ['4', '9', 'D'], ['5', '10', 'E'] ]

    #for i, col in enumerate(st.columns(10)):
    for i, col in enumerate(st.columns(5)):
        for c in ck[i]:
            dicc = rd.lcz_dict.get(DEFAULT_YEAR, {})
            #col.metric(f"% LCZ {c}", dicc.get(c, -99.99))
            col.metric(f"", f"{dicc.get(c, -99.99)} %")
            col.image(icgc.get_LCZ_image(c))
            #col.metric(icgc.LCZ_NAME.get(c, ''), '')


def get_NO2_annual_mean (nom_eoi:str, yr: int) -> float:
    calendari = {
        2019: [(1,31), (2,28), (3,31), (4,30), (5,31), (6,30), (7,31), (8,31), (9,30), (10,31), (11,30), (12,31)],
        2020: [(1,31), (2,29), (3,31), (4,30), (5,31), (6,30), (7,31), (8,31), (9,30), (10,31), (11,30), (12,31)],
        2021: [(1,31), (2,28), (3,31), (4,30), (5,31), (6,30), (7,31), (8,31), (9,30), (10,31), (11,30), (12,31)],
        2022: [(1,31), (2,28), (3,31), (4,30), (5,31), (6,30), (7,31), (8,31), (9,30), (10,31), (11,30), (12,31)],
        2023: [(1,31), (2,28), (3,31), (4,30), (5,31), (6,30), (7,31), (8,31), (9,30), (10,31), (11,30), (12,31)]
    }
    val_list = []
    for mes, ld in calendari.get(yr, []):
        for dia in range(1,ld+1):
            ymd = f"{yr:0>4}-{mes:0>2}-{dia:0>2}"
            print(ymd)
            df = od.get_data (ymd, nom_eoi, DEFAULT_CONTAMINANT)
            if not df.empty: val_list.append(get_hazard_data(df))
    return round(np.nanmedian(np.array(val_list)), 2)


def process_NO2_mean():
    for nom_eoi in stations.ESTACIONS["nom_eoi"]:
        eoi_code = stations.get_codi_eoi(nom_eoi)
        print(f"--- {eoi_code} --- {nom_eoi}---")
        valors = []
        for yr in [2019, 2020, 2021, 2022, 2023]:
            if yr in YEAR_OF_DATA:
                valors.append(idaea.get_NO2_mean (eoi_code, yr))
            else:
                valors.append(get_NO2_annual_mean(nom_eoi, yr))
        print(eoi_code, valors, nom_eoi)


# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    #process_NO2_mean()
    streamlit_main()

