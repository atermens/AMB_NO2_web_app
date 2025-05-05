# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Indicador: Indice de envejecimiento
# ----------------------------------------------------------------------------------------------------------------------
# Definicion: Expresa la relacion entre la cantidad de personas adultas mayores y la cantidad de menores.
# Calculo: Cociente entre personas de 65 y mas con respecto a las personas menores de 15, multiplicado por 100.
#
#          100 * (P_65_I_MES / P_0_14)
#
# Interpretacion estadistica:
# Un valor de 10 significa que hay 10 adultos mayores (de 65 y más) por cada 100 menores de 15.
#
# Interpretacion contextual y pertinencia:
# En la sociedad occidental, si bien se reconoce que la vejez es un fenomeno multidimensional, suele estar definida por
# límites de edad. En los pueblos indígenas, lo que distingue la vejez es el cambio de etapa en el ciclo vital y el
# limite cronologico pierde sentido; a lo sumo puede establecerse una frontera asociada a la perdida de capacidades
# fisiologicas o cuando no pueden realizar tareas para la reproduccion material de la familia y comunidad.
# Asimismo, el estatus y el rol social puede aumentar en la medida en que se "envejece", ya que se trata de las personas
# que atesoran la sabiduria y la memoria colectiva que debe ser transmitida a los jovenes para asegurar la reproduccion
# cultural del grupo o pueblo. Por lo tanto, no cabe una interpretacion "negativa", sino de continuidad cultural.
#
# Observaciones:
# Segun su interpretacion convencional, se trata de un indicador asociado a las transferencias intergeneracionales
# y su aumento sistematico implica para los estados una mayor inversion en salud y seguridad social orientada a las
# personas de edad, beneficios de los cuales no deberian estar exentos los pueblos indígenas.
#
# En Espanya el indice de envejecimiento con las cifras de 2021 se situaba en el 129.1% segun apunta el INE.
# Siendo bastante superior (casi por un 30%) el numero de personas mayores de 65 años que el de adolescentes, podemos
# ver como el envejecimiento de la poblacion es un hecho. Con el avance de la esperanza de vida y la disminucion de la
# natalidad, la piramide demografica se va invirtiendo, teniendo cada vez una base mas estrecha.
#
# Ademas, analizando los datos que nos ofrece el INE podemos definir este aumento como progresivo y sostenido en el
# tiempo. El indice de envejecimiento lleva subiendo sin parar en los ultimos años. En 2020 el indice de envejecimiento
# era del 125.75%. En 2018, el indice de envejecimiento se situaba en el 120.46%. En 2017 este indice no superaba
# el 120%.
#
# Como vemos, el indicador de envejecimiento crece anyo tras anyo debido a un envejecimiento de la poblacion y a un
# descenso en la natalidad. En enero de 2021, se calculaba que las personas mayores de 65 anyos eran mas de 9 millones.
# Esto se traduce en que alrededor del 19% de la población española son personas mayores.  Conviene recordar que las
# personas mayores de 65 suponen mas o menos una quinta parte de los españoles para poder darles la importancia
# demografica que se merecen.
#
# Para hacernos una mayor idea del volumen de personas mayores podemos compararlos con otros grupos en Espanya para
# relativizar su importancia. En 2021, mismo anyo en el que se calculaban 9 millones de personas mayores de 65 años,
# se registraban 2.7 millones de empleados publicos. Siendo los funcionarios un volumen de la poblacion activa
# importante, conviene recordar que las personas mayores son un grupo de poblacion tres veces más numeroso.
#
# Si incluimos en estos calculos tanto al sector publico como al privado, se contabiliza que en 2022 hay 19 millones de
# personas trabajando en nuestro pais. Este volumen de trabajadores es poco mas del doble que el de personas mayores
# de 65 anyos. Hay que tener en cuenta que en estas cifras se contabiliza a todas las personas que estan cotizando,
# sin importar el tipo de contrato. Trabajadores con media jornada, contratos de practicas o sueldos precarios tambien
# entran en esos 19 millones. Estas cifras muestran un equilibrio delicado, ya que la cotizacion de estos trabajadores
# es un pilar fundamental del que dependen las pensiones.
#
# El indice de envejecimiento creciente es una realidad que se debe tener en cuenta desde la administracion publica
# para crear una sociedad inclusiva e igualitaria. El cambio demografico que estamos viviendo ofrece una oportunidad
# para adaptarnos como sociedad si sabemos como.
# ----------------------------------------------------------------------------------------------------------------------
def get_pob_data(eoi_code: str, yr: int) -> tuple:
    from air_pollution_data.datos import EOI_POB

    # output: n, [p_0_14, p_15_64, p_65]
    dicc = EOI_POB.get(eoi_code, {})  # { yr: [0, ...], yr: [1, ...]}

    llista = dicc.get(yr, [])
    if not llista:
        return 0, []
    else:
        # tenemos que ver cual es la version: si es de tipo 0 o tipo 1...
        match llista[0]:
            case 0:
                #  0  1      2      3      4      5      6     7      8       9           10          11
                # [0, TOTAL, HOMES, DONES, P0014, P1564, P65_, P_ESP, P_ESTR, P_NASC_CAT, P_NASC_RES, P_NASC_EST,],
                return 3, llista[4:7]
            case 1:
                #  0   1          2             3         4          5          6
                # [1, P_H_0_14, P_H_15_64, P_H_65_I_MES, P_D_0_14, P_D_15_64, P_D_65_I_MES,],
                return 3, [llista[i+1] + llista[i+4] for i in range(3)]
            case _:
                return 0, []


def get_cvp(eoi_code: str, yr: int, ip: int) -> float:
    import numpy as np

    # iP: num. indice o tasa
    #
    # 0. El indice o mal llamada «tasa» de envejecimiento (por que no es una tasa), en realidad es simplemente la
    #    proporcion de mayores de 64 anyos
    #    = ((Poblacion >64 anyos / Poblacion total) x100) (proporcion de individuos
    #    mayores de 64 anyos sobre el total de la poblacion. Se suele expresar como porcentaje).
    #
    # 1. 100* (P_0_14 + P_65_I_MES) / TOTAL  que es la poblacio vulnerable (= docs Joan)
    #
    # 2. Index d'envelliment (IDESCAT). Poblacio de 65 anys i mes per cada 100 habitants de menys de 15 anys.
    #    https://www.idescat.cat/pub/?id=inddt&m=m
    #    A REVISAR !!!!
    
    n, datos = get_pob_data(eoi_code, yr)   # datos = [p_0_14, p_15_64, p_65]

    # check if datos is empty
    if n == 0:
        return np.nan
    else:
        match ip:
            case 0:
                return round(100.0 * float(datos[2]) / float(sum(datos)), 2)
            case 1:
                return round(100.0 * float(datos[0] + datos[2]) / float(sum(datos)), 2)
            case 2:
                return round(100.0 * float(datos[2]) / float(datos[0]), 2)
            case _:
                return np.nan
