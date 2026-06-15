
import pandas as pd
import numpy as np
from .dashboard_config import BASE_DIR

def cargar_datos():
    df = pd.read_csv(BASE_DIR / 'data' / 'processed' / 'Student_Depression_Dataset_Limpio.csv')
    return df

def obtener_opciones_filtros(df):
    gender_options = [{'label': g, 'value': g} for g in df['Gender'].unique()]
    city_options = [{'label': c, 'value': c} for c in df['City'].unique()]
    degree_options = [{'label': d, 'value': d} for d in df['Degree'].unique()]
    sleep_options = [{'label': s, 'value': s} for s in df['Sleep Duration'].unique()]
    return gender_options, city_options, degree_options, sleep_options

def filter_data(df, genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status):
    filtered_df = df.copy()
    
    if genders and len(genders) > 0:
        filtered_df = filtered_df[filtered_df['Gender'].isin(genders)]
    
    if cities and len(cities) > 0:
        filtered_df = filtered_df[filtered_df['City'].isin(cities)]
    
    if degrees and len(degrees) > 0:
        filtered_df = filtered_df[filtered_df['Degree'].isin(degrees)]
    
    if sleep_values and len(sleep_values) > 0:
        filtered_df = filtered_df[filtered_df['Sleep Duration'].isin(sleep_values)]
    
    filtered_df = filtered_df[
        (filtered_df['Age'] >= age_range[0]) &
        (filtered_df['Age'] <= age_range[1]) &
        (filtered_df['Academic Pressure'] >= pressure_range[0]) &
        (filtered_df['Academic Pressure'] <= pressure_range[1]) &
        (filtered_df['CGPA'] >= cgpa_range[0]) &
        (filtered_df['CGPA'] <= cgpa_range[1])
    ]
    
    if depression_status != 'all':
        filtered_df = filtered_df[filtered_df['Depression'] == depression_status]
    
    return filtered_df

