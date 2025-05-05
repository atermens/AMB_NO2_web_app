# -*- coding: utf-8 -*-
def get_nom_eoi(codi: str) -> str:
    from air_pollution_data.datos import EOI_DF

    df = EOI_DF[EOI_DF.codi_eoi == codi]
    nom = df['nom_eoi'].iloc[0] if df.shape[0] == 1 else "None"

    return nom


def get_codi_eoi(nom: str) -> str:
    from air_pollution_data.datos import EOI_DF

    df = EOI_DF[EOI_DF.nom_eoi == nom]
    codi = df['codi_eoi'].iloc[0] if df.shape[0] == 1 else "None"

    return codi
