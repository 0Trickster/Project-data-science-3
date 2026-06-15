import pandas as pd
from ydata_profiling import ProfileReport
from pathlib import Path

# Obtener la ruta del directorio del script actual
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar datos
df = pd.read_csv(BASE_DIR / 'data' / 'processed' / 'Student_Depression_Dataset_Limpio.csv')

# Generar reporte
profile = ProfileReport(df, title="Student Depression Dataset - Profiling Report")

# Guardar como HTML
profile.to_file(BASE_DIR / 'outputs' / 'reports' / 'student_depression_profile_report.html')

print("Reporte generado exitosamente: student_depression_profile_report.html")
