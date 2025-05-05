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
import pandas as pd
import datetime

import streamlit as st
import pydeck as pdk

import air_pollution_data as apd
from air_pollution_data.datos import EOI_DF, DEFAULT_CONTAMINANT, DEFAULT_VERSION


def streamlit_main():
    # SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON (1rst sentence Streamlit!!!)
    st.set_page_config(layout="wide", page_title="Air Quality Index", page_icon=":earth:")

    st.title("Air Pollution Data and Local Climate Zones in the AMB")

    with st.expander("About"):
        st.markdown("""
            Cities are growing fast and LCZs are a new way of classifying urban areas. 
            We know that air pollution is a factor that internally affects humans and their health. 
            It has direct repercussions on the human being and its analysis helps to know and understand what we must 
            do to mitigate the damage.

            This viewer contains cross information between the classifications of the LCZs and air quality data, 
            with NO2 concentrations as target pollutant, at the Barcelona Metropolitan Area (AMB).

            We use NO2 values from the dataset <tasf-thgu> of dadesobertes.gencat.cat.
            """)

    # ======================================================
    row1_1, row1_2, row1_3 = st.columns((1, 1, 3))

    row1_1.subheader(f"Select...")
    eoi_name = row1_1.selectbox("station", EOI_DF)  # escogemos el nombre de la estacion
    
    # escogemos la fecha que nos interesa, por defecto el dia anterior al de la consulta, ya que el dataset
    # de dadesobertes se actualiza a las 4 am de cada dia...
    # st.date_input(label,
    #               value="today", min_value=None, max_value=None, key=None, help=None, on_change=None, args=None,
    #               kwargs=None, *, format="YYYY/MM/DD", disabled=False, label_visibility="visible")

    today = datetime.datetime.now().date()
    yesterday = datetime.date(today.year, today.month, today.day-1)

    row1_2.subheader(f" ")
    ymd = row1_2.date_input("one day", value=yesterday, format="YYYY-MM-DD")  # ymd is datetime.date

    # Restringimos a los dos contaminantes descritos en el TFM, aunque por defecto trataremos siempre el NO2.
    # contaminante = row1_1.radio("pollutant:", ('NO2', 'PM2.5'))
    # contaminante = row1_1.selectbox("contaminant:", pd.DataFrame(CONTAMINANTS))
    contaminante = DEFAULT_CONTAMINANT

    # A partir de estos datos, obtenemos los datos (JSON) del dataset de dades obertes.
    # En principio nos tiene que devolver un DataFrame con solo una fila. En caso contrario el DataFrame estara vacio.
    df = apd.get_eoi_data_contaminant(ymd, eoi_name, contaminante)
    if df.shape[0] == 1:
        contaminant_metadata = (df['magnitud'].iloc[0], df['contaminant'].iloc[0], df['unitats'].iloc[0])
    else:
        df = pd.DataFrame()
        contaminant_metadata = (8, DEFAULT_CONTAMINANT, 'mu-g/m3')

    # Primero, vamos a pintar el mapa de situacion de las estaciones:
    mapstyle, initviewstate, selectedlayers = apd.get_station_map_data(df)
    # row1_2.map(data=df, zoom=13, use_container_width=True)
    row1_3.pydeck_chart(pdk.Deck(map_style=mapstyle, initial_view_state=initviewstate, layers=selectedlayers))

    # buscamos el codigo de estacion asociado a eoi_name:
    eoi_code = apd.get_codi_eoi(eoi_name)

    # calculamos todos los datos del riesgo associado al contaminante:
    rdi = apd.AirPollutionIndex(eoi_code)
    rd = apd.AirPollutionRisk(eoi_code, df)

    row1_1.write(" ")
    row1_1.subheader(f" {contaminante} Daily Mean Concentration:")
    # row1_1.subheader(f" {contaminante} Air Quality Index ({DEFAULT_YEAR}):")
    # aqui pondremos el semaforo con el risk_data.risk
    semafor = rd.risk_image
    if os.path.isfile(semafor):
        row1_1.image(semafor, caption=rd.risk_caption, width=150)

    row1_2.write(" ")
    row1_2.subheader(f" Complex Vulnerability Index:")
    # aqui pondremos el semaforo con el risk_data.risk
    semafor = rd.vi_image
    if os.path.isfile(semafor):
        row1_2.image(semafor, caption=rd.vi_caption, width=150)

    # ======================================================
    # Vamos a comprovar si tenemos datos o no y calculamos todos los datos del riesgo asociado al contaminante:
    st.write(f" ")
    st.subheader(apd.get_information_about_data(df, eoi_name, ymd, contaminante))
    # st.write(f"--- Year: DEFAULT_YEAR ---")
    # st.write(f"LCZ max: {rd.lcz_max.get(yr, '-')} | VUCI: {rd.vuci.get(yr, '-')} | CVP: {rd.cvpi.get(yr, '-')}")
    # st.write(f"Hazard({contaminante}): {rd.hazard_value.get(yr, '-')} | NO2 mean: {rd.no2_mean.get(yr, '-')}")
    # st.write(f" Scenario: {rd.scenario_code.get(yr, '-')} | Risk: {rd.risk.get(yr, '-')}")

    # ======================================================
    row2_1, row2_2 = st.columns((2, 3))
    # imagen del buffer de LCZ de la estacion escogida (eoi_code)
    row2_1.write(f"Local Climate Zones (LCZ) data in {eoi_name} area")
    img = apd.get_lcz_station_image(eoi_code, DEFAULT_VERSION)
    if os.path.isfile(img):
        row2_1.image(img)

    # pintamos ahora el histograma de valores del contaminante...
    if not df.empty:
        contamina = contaminant_metadata[1]
        row2_2.write(f"{contamina} [{contaminant_metadata[2]}] data in {eoi_name} ({ymd})")
        cdf = apd.get_df_histograma_hores(df, contamina)
        row2_2.line_chart(cdf,
                          x="hora",
                          y=[f"{contamina}", "mean", "good", "moderate", "bad"],
                          color=["#0033cc", "#ff0000", "#33cc33", "#66ccff", "#ff9900"])

        # plot modo histograma. En aquest cas, es fa un histograma acumulat...
        # row2_2.write(f"{contaminante} data in {eoi_name} ({ymd}) - cumulative histogram")
        # row2_2.bar_chart(get_df_histograma_hores(contaminante, df))

    # ======================================================
    st.subheader(f"LCZ distribution:")
    # vamos a pintar la informacion asociada a cada LCZ, con la imagen associada
    # el procedimiento va a ser muy rudimentario y seguro que se puede optimizar mas...
    # partimos la columna en 10 subcolumnas (una para cada LCZ)
    # ck = [ ['1', 'A'], ['2', 'B'], ['3', 'C'], ['4', 'D'], ['5', 'E'], ['6', 'F'], ['7', 'G'], ['8'], ['9'], ['10'] ]
    ck = [['1', '6', 'A', 'F'], ['2', '7', 'B', 'G'], ['3', '8', 'C'], ['4', '9', 'D'], ['5', '10', 'E']]

    # for i, col in enumerate(st.columns(10)):
    for i, col in enumerate(st.columns(5)):
        for c in ck[i]:
            # col.metric(f"% LCZ {c}", rdi.lcz_dict.get(c, -99.99))
            col.metric(f">", f"{rdi.lcz_dict.get(c, -99.99)} %")
            col.image(apd.get_lcz_image(c))
            # col.metric(LCZ_NAME.get(c, ''), '')


# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # process_NO2_mean()
    streamlit_main()
