# Análisis de Parpadeo 👀

## Descripción
Este proyecto tiene como objetivo realizar un análisis de la frecuencia de parpadeos durante el trabajo frente a una pantalla. Se compararán los datos recopilados sobre la frecuencia de parpadeos en condiciones laborales con datos obtenidos en condiciones normales. La investigación se enfocará en entender cómo el tiempo de exposición a pantallas afecta los patrones de parpadeo, lo que puede tener implicaciones en la salud ocular y el bienestar general.

## Objetivos
1. Evaluar la frecuencia de parpadeos en entornos laborales frente a pantallas.
2. Comparar los datos de parpadeos en condiciones de trabajo con condiciones normales.
3. Proporcionar recomendaciones para mejorar la salud ocular y reducir la fatiga visual en entornos laborales.

## Herramientas y Tecnologías

### Recolección de Datos
- **OpenCV**: Para el análisis de videos o imágenes y la detección de parpadeos. 
  - **Python**: Lenguaje de programación principal utilizado en el proyecto.

### Análisis de Datos
- **Pandas**: Para la manipulación y análisis de datos. Se utilizará para organizar los datos de parpadeos en un DataFrame, facilitando el análisis estadístico.
- **NumPy**: Para realizar cálculos numéricos y operaciones matemáticas sobre los datos.
- **SciPy**: Para realizar análisis estadísticos avanzados, como pruebas de hipótesis y análisis de varianza (ANOVA).

### Visualización de Datos
- **Matplotlib**: Para crear gráficos y visualizaciones que muestren las diferencias en la frecuencia de parpadeos.
- **Seaborn**: Para mejorar las visualizaciones con estilos más atractivos y gráficos más complejos.

## Estructura del Proyecto
El proyecto se estructurará de la siguiente manera:

Analisis-de-Parpadeo/ │ ├── data/ │ ├── parpadeos_laborales.csv │ └── parpadeos_normales.csv │ ├── notebooks/ │ ├── 01_recoleccion_datos.ipynb │ ├── 02_analisis_datos.ipynb │ └── 03_visualizacion.ipynb │ ├── src/ │ ├── data_collection.py │ ├── data_analysis.py │ └── visualization.py │ ├── requirements.txt └── README.md

### Detalles de las Carpetas
- **data/**: Contendrá los datasets de parpadeos en formato CSV.
- **notebooks/**: Incluirá Jupyter Notebooks con la recolección de datos, análisis y visualización.
- **src/**: Contendrá scripts de Python para la recolección de datos, análisis y visualización.
- **requirements.txt**: Listará las bibliotecas necesarias para ejecutar el proyecto.

## Creación del Dataset
Para crear el dataset, se registrarán videos durante el trabajo frente a una pantalla y en condiciones normales. A continuación, se realizará el análisis de los videos utilizando OpenCV para detectar y contar la frecuencia de parpadeos. Los datos se almacenarán en archivos CSV que incluirán columnas como:
- `timestamp`: Momento en el que se detectó el parpadeo.
- `condition`: Condición bajo la cual se realizó el análisis (laboral o normal).
- `blink_count`: Conteo total de parpadeos en el intervalo de tiempo.

## Análisis de Datos
Utilizando Pandas, se cargarán los datos de los archivos CSV y se realizarán análisis estadísticos para evaluar patrones y correlaciones. Se calcularán métricas como la media, mediana y desviación estándar de la frecuencia de parpadeos.

## Visualización de Datos
Se crearán gráficos utilizando Matplotlib y Seaborn para mostrar las diferencias en la frecuencia de parpadeos entre las condiciones laborales y normales. Ejemplos de visualizaciones incluirán:
- Gráficos de barras para comparar el conteo de parpadeos entre ambas condiciones.
- Histogramas para mostrar la distribución de la frecuencia de parpadeos.
- Gráficos de caja (box plots) para visualizar la variabilidad y posibles outliers.

## Asistencia
- **YouTube**: Se consultaron tutoriales específicos sobre OpenCV, Pandas y visualización de datos.
- **Documentación Oficial**: Documentación de [OpenCV](https://opencv.org/documentation/) y [Pandas](https://pandas.pydata.org/docs/).
- **Asistencia de ChatGPT**: Se utilizó ChatGPT para obtener aclaraciones sobre conceptos técnicos y recomendaciones para el análisis de resultados.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas colaborar en este proyecto, por favor abre un "issue" o envía un "pull request".
