import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargamos los datos
# Indicamos que el delimitador de columnas es el punto y coma.

ruta = 'Datos/SEV_02_141225_CAMPO.csv'
df = pd.read_csv(ruta, sep=";")

# Limpieza de datos brutos
# Se busca trabajar con datos faltantes que pueda contener la data

def normalizar_unidades(valor, unidad):
    if pd.isna(valor):
        return valor

# Se corrige el formato de las unidades,a uno mas uniforme

    u = str(unidad).strip().lower()

# Hay data con distintas unidades en el voltaje, corriente y resistencia electrica, la cual se debe corregir.
    
    if u in ['mv', 'ma', 'mohm']:
        return valor / 1000
    elif u == 'uv':
        return valor / 1000000
    else:
        return valor

df['V_normal'] = df.apply(lambda fila: normalizar_unidades(fila['V'], fila['Unidad_V']), axis=1)
df['I_normal'] = df.apply(lambda fila: normalizar_unidades(fila['I'], fila['Unidad_I']), axis=1)
df['R_normal'] = df.apply(lambda fila: normalizar_unidades(fila['R'], fila['Unidad_R']), axis=1)
df['PS_normal'] = df.apply(lambda fila: normalizar_unidades(fila ['PS'], fila['Unidad_PS']), axis=1)



# Calcularemos el factor 'K' para poder calcular la resistividad aparente
# Haciendo antes una modificacion matemÁtica para simplicar la formula general = pi*(AM*AN/MN)

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

# Representación grafica AB/2 V Resistividad aparente Cruda o con saltos, y curva con Resisitividad corregida

plt.figure(figsize=(10, 6))

# Usamos una escala logaritmica 
plt.loglog(df['AB_2'], df['R_aparente'], 'ro-', alpha=0.5, label= 'Curva de Cruda (Con saltos)')
plt.loglog(df['AB_2'], df['R_corregida'], 'bo-', label='Curva Corregida (Continua)')

# hacemos un motor de exportacion, util para subir los datos ya corregidos a IPI2WIN, sin necesidad de excel

df_export = df[['AB_2', 'MN_2', 'R_corregida']]
ruta_salida = 'Datos/SEV_O2_listos.txt'
df_export.to_csv(ruta_salida, sep='\t', index=False)

print(f"\n[PROCESO TERMINADO] Datos exportados con exito a: {ruta_salida}")

# Configuramos los ejes y el resto del grafico

plt.title('Sondaje Eléctrico Vertical - Correccion de Empalmes')
plt.xlabel('AB/2 (metros)')
plt.ylabel('Resistividad (Ohm-m)')
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.legend()

plt.show()