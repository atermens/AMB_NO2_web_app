# -*- coding: utf-8 -*-

import pandas as pd

#
# definim dades estacions a tractar de l'AMB.
# L'estructura del diccionari es la idoneia per generar després el DataFrame.
#
ESTACIONS = {
    "nom_eoi": [
        "Badalona",
        "Barberà del Vallès",
        "Barcelona (Ciutadella)",
        "Barcelona (Eixample)",
        "Barcelona (Gràcia - Sant Gervasi)",
        "Barcelona (Observatori Fabra)",
        "Barcelona (Palau Reial)",
        "Barcelona (Parc Vall Hebron)",
        "Barcelona (Poblenou)",
        "Barcelona (Sants)",
        "Gavà",
        "L'Hospitalet de Llobregat",
        "Montcada i Reixac",
        "Pallejà (Roca de Vilana)",
        "El Prat de Llobregat (Jardins de la Pau)",
        "El Prat de Llobregat (Sagnier)",
        "Sant Adrià del Besòs",
        "Sant Andreu de la Barca",
        "Sant Cugat del Vallès",
        "Sant Vicenç dels Horts (Ribot)",
        "Sant Vicenç dels Horts",
        "Santa Coloma de Gramanet",
        "Viladecans - Atrium",
    ],
    "codi_eoi": [
        '08015021',
        '08252006',
        '08019050',
        '08019043',
        '08019044',
        '08019058',
        '08019057',
        '08019054',
        '08019004',
        '08019042',
        '08089005',
        '08101001',
        '08125002',
        '08157003',
        '08169008',
        '08169009',
        '08194008',
        '08196001',
        '08205002',
        '08263001',
        '08263007',
        '08245012',
        '08301004',
    ],
    "lon": [
        2.2378986,
        2.1253984,
        2.1873982,
        2.1537998,
        2.1533988,
        2.1238973,
        2.1151996,
        2.1480017,
        2.2045010,
        2.1330990,
        1.9914981,
        2.1149993,
        2.1882975,
        1.9905012,
        2.0977015,
        2.0821000,
        2.2221997,
        1.9748996,
        2.0889983,
        2.0097985,
        1.9997202,
        2.2094970,
        2.0136087,
    ],
    "lat": [
        41.443985,
        41.512684,
        41.386406,
        41.385315,
        41.398724,
        41.418430,
        41.387490,
        41.426110,
        41.403880,
        41.378780,
        41.303097,
        41.370476,
        41.481970,
        41.415280,
        41.321487,
        41.321774,
        41.425594,
        41.450800,
        41.476814,
        41.392190,
        41.400845,
        41.447422,
        41.313350,
    ],
    "etiqueta": [
        'Badalona',
        'Barbera_Valles',
        'BCN_Ciutadella',
        'BCN_Eixample',
        'BCN_Gracia',
        'BCN_ObsFabra',
        'BCN_Palau_Reial',
        'BCN_Vall_Hebron',
        'BCN_Poblenou',
        'BCN_Sants',
        'Gava',
        'Hospitalet',
        'Montcada_i_Reixac',
        'Palleja_RocaVilana',
        'ElPrat_Jardins_Pau',
        'ElPrat_Sagnier',
        'SAdria_Besos',
        'SAndreu_Barca',
        'SCugat_Valles',
        'SVHorts_Ribot',
        'SVHorts',
        'StaColoma_Gramanet',
        'Viladecans',
    ],
}

EOI_DF = pd.DataFrame(ESTACIONS)


def get_nom_eoi(codi: str) -> str:
    df = EOI_DF[EOI_DF.codi_eoi == codi]
    if df.shape[0] == 1:
        return df['nom_eoi'].iloc[0]
    else:
        return f"None"


def get_codi_eoi(nom:str) -> str:
    df = EOI_DF[EOI_DF.nom_eoi == nom]
    if df.shape[0] == 1:
        return df['codi_eoi'].iloc[0]
    else:
        return f"None"

