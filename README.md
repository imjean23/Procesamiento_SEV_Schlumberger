# Corrección y Empalme de Sondeos SEV (Schlumberger)

## El Problema Físico
Cuando hacemos sondeos eléctricos verticales en campo y nos toca abrir los electrodos de potencial (MN), la curva de resistividad aparente suele dar un "salto" debido al ruido o las variaciones superficiales del terreno. 

Si agarramos estos datos crudos del resistivímetro y los metemos directamente a un software de inversión como IPI2Win, el programa va a intentar ajustar la curva inventando capas geológicas falsas que no existen en la realidad.

## ¿Qué hace este código?
Escribí este programa para dejar de corregir empalmes a mano en Excel. 

El script no procesa los archivos uno por uno. Lee una carpeta entera llena de sondeos crudos en `.csv`, estandariza las unidades eléctricas que escupe el equipo (mV, mA, etc.) y aplica un factor de corrección matemático (*shifting*). El algoritmo ancla la parte profunda de la curva (que es más confiable) y arrastra los datos superficiales para cerrar el escalón, preservando la pendiente logarítmica real.

Al terminar, genera archivos `.txt` limpios y formateados estrictamente para leerlos directo en software de inversión.

## Herramientas Utilizadas
* **Python 3**
* **Pandas & NumPy:** Para calcular el Factor Geométrico (K) vectorizando columnas enteras en lugar de usar celdas.
* **os & glob:** Para el procesamiento masivo. El programa entra al directorio, detecta todos los archivos `.csv` y los procesa en bucle sin que yo tenga que escribir los nombres manualmente.

## Cómo usarlo
1. Mete todos tus archivos `.csv` crudos en la carpeta `Datos/`.
2. Ejecuta el script desde la terminal:

```bash
python main.py
```

3. El programa escupirá los archivos corregidos automáticamente en la carpeta `Resultados/`.

## Autor
**Jean Ruiz Renteria**
Estudiante de Ingeniería Geológica (Universidad Nacional de Piura).
Enfocado en aplicar Python para solucionar problemas operativos de geomecánica, geotecnia y geofísica.