"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import numpy as np
import os
import re  

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    data = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", encoding='utf-8')

    solicitudes= data.drop('Unnamed: 0', axis=1)
    
    # Normalizar fecha
    def normalizar_fecha(texto):
        try:
            if re.match(r'^\d{4}/\d{1,2}/\d{1,2}$', str(texto)):
                partes = texto.split('/')
                año = partes[0]
                mes = partes[1].zfill(2)
                dia = partes[2].zfill(2)
                return f"{dia}/{mes}/{año}"
            else:
                return texto
        except:
            return texto

    solicitudes['fecha_de_beneficio'] = solicitudes['fecha_de_beneficio'].apply(normalizar_fecha)
    solicitudes['fecha_de_beneficio'] = pd.to_datetime(solicitudes['fecha_de_beneficio'], errors='coerce', dayfirst=True)

    #Convertir a minúscula
    cols = ["sexo", "tipo_de_emprendimiento", "idea_negocio","barrio","línea_credito"]
    solicitudes[cols] = solicitudes[cols].apply(lambda x: x.str.lower())

    cols=['idea_negocio','línea_credito']
    solicitudes[cols]=solicitudes[cols].apply(lambda x: x.replace({'_': ' ','-': ' '}, regex=True).str.strip())

    solicitudes['barrio'] = solicitudes['barrio'].replace({'_': ' ','-': ' '}, regex=True)

    # Limpiar la data como función
    #def limpiar_texto_columnas(df, columnas, strip=True, lower=True, replace_chars=True):
            #for col in columnas:
                #df[col] = df[col].astype(str).str.lower()
                #df[col] = df[col].replace({'_': ' ','-': ' '}, regex=True)
                #df[col] = df[col].str.strip()

            #return df
    
    #limpiar_texto_columnas(solicitudes, columnas=['idea_negocio','línea_credito'])

    # Normalizar monto
    solicitudes['monto_del_credito'] = solicitudes['monto_del_credito'].str.replace('$', '').str.replace('_', ' ').str.replace('-', ' ')
    solicitudes['monto_del_credito'] = solicitudes['monto_del_credito'].str.replace(' ', '') 
    solicitudes['monto_del_credito'] = solicitudes['monto_del_credito'].str.replace(',', '') 
    solicitudes['monto_del_credito'] = solicitudes['monto_del_credito'].astype(float)
        
    # Eliminar filas con nulos y duplicados en columnas
    solicitudes = solicitudes.dropna()
    solicitudes = solicitudes.drop_duplicates()

    # Crear carpeta de salida si no existe
    if not os.path.exists("files/output"):
        os.makedirs("files/output")
    # Guardar el DataFrame limpio en un archivo CSV
    solicitudes.to_csv("files/output/solicitudes_de_credito.csv",sep=";", index=False)

    return solicitudes

if __name__ == "__main__":
    solicitudes=pregunta_01()
