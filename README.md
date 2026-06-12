# Project-data-science-3
Este repositorio contiene el desarrollo completo de un sistema de análisis predictivo y visualización interactiva para el estudio de la depresión estudiantil. El proyecto abarca desde la limpieza y codificación de datos hasta el entrenamiento de modelos de Machine Learning y el despliegue de un dashboard interactivo.

## 📁 Estructura del Proyecto
```bash
Project-data-science-3/
│
├── app/                   # Aplicación principal (dashboard y scripts)
│   ├── dashboard.py       # Dashboard interactivo con Dash y Plotly
│   └── generate_profiling_report.py  # Generador de reportes de profiling
│
├── assets/                # Archivos estáticos para el dashboard (CSS)
│   └── styles.css         # Estilos del dashboard
│
├── data/
│   ├── processed/          # Datos limpios, codificados y divididos (train/test)
│   │   ├── Student_Depression_Dataset_Limpio.csv
│   │   ├── Student_Depression_Dataset_codificado.csv
│   │   ├── Student_Depression_Dataset_Train.csv
│   │   ├── Student_Depression_Dataset_Test.csv
│   │   └── Student_Depression_Dataset_Prediction.csv
│   └── raw/                # Datos originales sin procesar
│       └── Student_Depression_Dataset_Original.csv
│
├── notebooks/              # Ciclo de vida del modelado
│   ├── 1.1.Codificación_datos.ipynb       # Limpieza y codificación de variables
│   ├── 1.2.Hiperparams_Random_Forest.ipynb  # Optimización de hiperparámetros
│   ├── 1.3.Supervised_Models_Pipeline.ipynb  # Entrenamiento de modelos supervisados
│   ├── 1.4.Model_Evaluation.ipynb         # Evaluación y comparación de modelos
│   └── 1.5.Predicctions_Ejecution.ipynb   # Generación de predicciones
│
├── outputs/
│   ├── models/             # Modelos entrenados y preprocesador (.pkl)
│   │   ├── random_forest_model.pkl
│   │   └── preprocessor.pkl
│   ├── plots/              # Visualizaciones generadas
│   │   └── metrics/        # Gráficos de evaluación de modelos
│   │       ├── confusion_matrix_rf.png
│   │       ├── feature_importance_rf.png
│   │       └── metrics_comparison.png
│   ├── reports/            # Reportes de análisis
│   │   └── student_depression_profile_report.html
│   └── best_random_forest_hyperparameters.json  # Mejores hiperparámetros
│
├── src/                    # Scripts de soporte
│   ├── __init__.py
│   ├── carga_csv.py        # Carga de datos
│   └── eda_utils.py        # Utilidades para análisis exploratorio
│
├── environment.yml         # Dependencias del proyecto
└── README.md
```

## Tecnologías utilizadas
* Python
* Pandas
* NumPy
* Matplotlib / Seaborn
* Plotly / Dash (para el dashboard)
* Jupyter Notebook
* SciPy
* Scikit-learn
* Conda
* Joblib (para guardar modelos)

## Flujo del proyecto
1. **Carga y limpieza de datos** → `notebooks/1.1.Codificación_datos.ipynb`
2. **Optimización de hiperparámetros** → `notebooks/1.2.Hiperparams_Random_Forest.ipynb`
3. **Entrenamiento de modelos supervisados** → `notebooks/1.3.Supervised_Models_Pipeline.ipynb`
4. **Evaluación de modelos** → `notebooks/1.4.Model_Evaluation.ipynb`
5. **Generación de predicciones** → `notebooks/1.5.Predicctions_Ejecution.ipynb`
6. **Modelos entrenados** → `outputs/models/`
7. **Visualizaciones de evaluación** → `outputs/plots/`
8. **Reportes finales** → `outputs/reports/`
9. **Dashboard interactivo** → `app/dashboard.py`

## Cómo usar el proyecto

### 1. Clonar el repositorio:
```bash
git clone https://github.com/0Trickster/Project-data-science-3
cd Project-data-science-3
```

### 2. Crear entorno virtual:
```bash
conda env create -f environment.yml
conda activate <nombre-del-entorno>
```

### 3. Ejecutar el dashboard:
```bash
python app/dashboard.py
```
El dashboard estará disponible en `http://127.0.0.1:8050/`

### 4. Generar reporte de profiling:
```bash
python app/generate_profiling_report.py
```

### 5. Ejecutar notebooks:
Si quieres explorar o reejecutar los notebooks:
```bash
jupyter notebook
```
