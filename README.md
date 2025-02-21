# Proyecto: Clasificación de Fallas en Placas de Acero

Este proyecto de Machine Learning tiene como objetivo **detectar fallas en placas de acero** (Steel Plates Faults) utilizando algoritmos de clasificación. Está orientado al ámbito de **automatización de procesos industriales**, para ilustrar cómo se pueden analizar datos de sensores o características físicas con el fin de identificar o predecir defectos en la producción.

## Estructura del Proyecto

- **data/**  
  Contiene el dataset `SteelPlateFaults.csv` (descargado de UCI o fuente correspondiente).

- **notebooks/**  
  Contiene los cuadernos de Jupyter con el análisis exploratorio de datos (EDA), el preprocesamiento y los modelos de Machine Learning.

- **README.md**  
  Descripción general del proyecto, instrucciones de uso y guía de instalación.

- **.gitignore**  
  Archivo que indica los ficheros y carpetas que no se deben incluir en el repositorio.

- **environment.yml** *(opcional)*  
  Archivo para reproducir el entorno de conda.

## Configuración del Entorno

1. Instala [Anaconda/Miniconda](https://docs.conda.io/en/latest/).
2. Crea el entorno `SteelPlatesEnv` usando `conda create --prefix "ruta\SteelPlatesEnv" python=3.9 -y`.
3. Activa el entorno con `conda activate "ruta\SteelPlatesEnv"`.
4. Instala los paquetes necesarios: `conda install jupyter pandas numpy scikit-learn matplotlib seaborn -y`.
5. Lanza Jupyter Notebook con `jupyter notebook`.

## Uso

1. Clona este repositorio en tu máquina local.
2. Navega hasta `notebooks/`.
3. Abre el archivo `01_classification_steel_plates_faults.ipynb` con Jupyter Notebook.
4. Ejecuta las celdas paso a paso para:
   - Realizar el análisis exploratorio de datos (EDA).
   - Preprocesar el dataset.
   - Entrenar y evaluar modelos de clasificación (Logistic Regression, Random Forest, etc.).
   - Ajustar hiperparámetros y ver la evolución de los resultados.

## Registro Diario

- Se encuentra en la última sección del Notebook, donde se registran los algoritmos probados, el mejor rendimiento obtenido y una breve explicación de por qué.

## Contribuciones

¡Siéntete libre de contribuir con mejoras, nuevas funcionalidades o correcciones!

---
