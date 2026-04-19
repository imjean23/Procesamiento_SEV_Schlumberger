# Procesamiento y Corrección de Datos SEV (Arreglo Schlumberger)

## ¿De qué trata este proyecto?
Este es un script en Python diseñado para automatizar el procesamiento de datos crudos de Sondeos Eléctricos Verticales (SEV). 

Durante el trabajo de campo con el método Schlumberger, es obligatorio abrir los electrodos de potencial (MN) a medida que la señal pierde fuerza. Esto genera "saltos" en la curva de resistividad aparente debido a las variaciones laterales superficiales del terreno. Si estos datos con ruido se introducen directamente a un software de inversión, el programa calculará estratos falsos.

Este código toma el archivo crudo del equipo, normaliza las unidades, hace los cálculos geofísicos base y aplica un algoritmo de *shifting* para empalmar la curva. El resultado es un modelo 1D continuo, listo para la inversión geofísica.

## Stack Tecnológico
* **Python 3**
* **Pandas:** Para la ingesta del archivo `.csv` y la manipulación de la base de datos (reemplazando el trabajo manual en Excel).
* **NumPy:** Para el cálculo de constantes matemáticas (Pi) y operaciones del factor geométrico (K).
* **Matplotlib:** Para renderizar la gráfica de control en escala bilogarítmica.

## Pipeline del Script
1. **Ingesta y Limpieza:** Lee un `.csv` con las lecturas de campo (`AB_2`, `MN_2`, `V`, `I`, `R`). Una función estandariza automáticamente las unidades eléctricas a un solo formato (mV, uV, mA, etc.).
2. **Cálculo Base:** Determina el Factor Geométrico (K) y calcula la Resistividad Aparente ($\rho_a$) inicial.
3. **Empalme Matemático:** El algoritmo detecta los puntos de solapamiento (donde se repite $AB/2$ al cambiar $MN$) y calcula un factor de corrección. Este factor se aplica de forma acumulativa al tramo anterior de la curva, eliminando el error geométrico sin alterar la pendiente de las capas.
4. **Exportación a IPI2Win:** Extrae únicamente las columnas de distancia y resistividad corregida, y genera un archivo `.txt` delimitado por tabulaciones (sin índices de fila). Este es el formato estricto que exigen los softwares de inversión como IPI2Win o RES1D.

## Ejecución
Asegúrate de que tu archivo crudo esté en la carpeta `Datos/` y corre el script principal:
```bash
python main.py
```

## Autor
**Jean Ruiz Renteria** Estudiante de Ingeniería Geológica (Universidad Nacional de Piura).  
Enfocado en la integración de Data Science y programación en Python aplicados a la geomecánica, geotecnia y geofísica.