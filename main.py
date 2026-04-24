import pandas as pd
import numpy as np
import os
import glob

# Limpieza de datos brutos
# datos faltantes
# Se corrige las unidades y su formato

def normalizar_unidades(valor, unidad):
    if pd.isna(valor):
        return valor
    u = str(unidad).strip().lower()
    if u in ['mv', 'ma', 'mohm']:
         return valor / 1000
    elif u == 'uv':
            valor / 1000000
    else:
        return valor

# Se busca crear una base solida del prompt, que pueda tratar con muchos archivos csv con datos de campo 
# simulando una campaña de sondajes geofísicos
# Creamos una estructura de directorios 

carpeta_entrada = 'Datos'
carpeta_salida = 'Resultados'


# Se crea la carpeta que almacenara los Resultados

if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)
    print(f"Directorio creado: {carpeta_salida}/")

# Buscador de archivos con formato csv que existan en la carpeta de entrada

patron_busqueda = os.path.join(carpeta_entrada, '*.csv')
archivos_csv = glob.glob(patron_busqueda)

# Informe de archivos, cantidad y nos alerta si no existe alguno

if len(archivos_csv) ==0:
    print(f"Error: No se encontraros archivos .csv en la carpeta '{carpeta_entrada}'.")
else:
    print(f"Se detecttaron {len(archivos_csv)} sondajes. Iniciando procesamiento de lotes...\n")
       
    for ruta_archivo in archivos_csv:
        nombre_base = os.path.basename(ruta_archivo).replace('.csv', '')
        print(f"Procesando sondaje: {nombre_base}")        
        df =pd.read_csv(ruta_archivo, sep=';')
            
# Calcularemos el factor 'K' para poder calcular la resistividad aparente
# Haciendo antes una modificacion matemÁtica para simplicar la formula general = pi*(AM*AN/MN)

        df['V_normal'] = df.apply(lambda fila: normalizar_unidades(fila['V'], fila['Unidad_V']), axis=1)
        df['I_normal'] = df.apply(lambda fila: normalizar_unidades(fila['I'], fila['Unidad_I']), axis=1)
        df['R_normal'] = df.apply(lambda fila: normalizar_unidades(fila['R'], fila['Unidad_R']), axis=1)
        df['PS_normal'] = df.apply(lambda fila: normalizar_unidades(fila ['PS'], fila['Unidad_PS']), axis=1)
        
        AB2 = df['AB_2']
        MN2 = df['MN_2']
        
        df['k'] = np.pi * ((AB2**2 - MN2**2) / (2*MN2))

# Calculamos la resistividad aparente = K * R

        df['R_aparente'] = df['k'] * df['R_normal']

# Debemos corregir una pequeña alteracion en la resistividad al haber ampliado la distancia MN por la configuracion de Schlumberger
# Esto se considera un ruido superficial que interrumpe una lectura profunda

        df['R_corregida'] = df['R_aparente'].copy()

        for i in range(1, len(df)):
             if (df.loc[i, 'AB_2'] == df.loc[i-1, 'AB_2']) and (df.loc[i, 'MN_2'] > df.loc[i-1, 'MN_2']):
                factor = df.loc[i, 'R_corregida'] / df.loc[i-1, 'R_corregida']
                df.loc[:i-1, 'R_corregida'] = df.loc[:i-1, 'R_corregida'] * factor  

# hacemos un motor de exportacion, util para subir los datos ya corregidos a IPI2WIN, sin necesidad de excel
# Exportamos y generamos un nombre unico para cada sondeo ya corregido

                ruta_exportacion = os.path.join(carpeta_salida, f"{nombre_base}_CORREGIDO.txt")
                df_export = df[['AB_2', 'MN_2', 'R_corregida']]
                df_export.to_csv(ruta_exportacion, sep='\t', index=False)
                print(f"[OK] Guardado en: {ruta_exportacion}\n")

print("Proceso finalizado con éxito.")





