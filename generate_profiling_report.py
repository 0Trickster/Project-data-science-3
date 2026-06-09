import pandas as pd
from data_profiling import ProfileReport

# Cargar datos
df = pd.read_csv('data/processed/Student_Depression_Dataset_Limpio.csv')

# Generar reporte
profile = ProfileReport(df, title="Student Depression Dataset - Profiling Report")

# Guardar como HTML
profile.to_file("outputs/reports/student_depression_profile_report.html")

print("Reporte generado exitosamente: student_depression_profile_report.html")
