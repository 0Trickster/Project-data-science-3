import dash
from dash import dcc, html, dash_table
from src.dashboard_utils import *
import plotly.express as px
import numpy as np

# Obtener la ruta del directorio del script actual
BASE_DIR = Path(__file__).resolve().parent.parent


app = dash.Dash(__name__, title="Dashboard Depresión Estudiantil - Interactivo", assets_folder=str('assets'))
server = app.server

# Layout del dashboard
app.layout = html.Div(className='dashboard-container', children=[
    html.Div(className='header', children=[
        html.H1("📊 Dashboard de Depresión en Estudiantes - Interactivo")
    ]),

    # Sección de filtros
    html.Div(className='filters-section', children=[
        html.H3("🔍 Filtros"),
        
        # Fila 1: Género, Ciudad, Carrera
        html.Div(className='filter-row', children=[
            html.Div(className='filter-item', children=[
                html.Label("Género:"),
                dcc.Dropdown(
                    id='gender-filter',
                    options=gender_options,
                    value=[],
                    multi=True,
                    placeholder="Selecciona género(s)"
                )
            ]),
            
            html.Div(className='filter-item', children=[
                html.Label("Ciudad:"),
                dcc.Dropdown(
                    id='city-filter',
                    options=city_options,
                    value=[],
                    multi=True,
                    placeholder="Selecciona ciudad(es)"
                )
            ]),
            
            html.Div(className='filter-item', children=[
                html.Label("Carrera:"),
                dcc.Dropdown(
                    id='degree-filter',
                    options=degree_options,
                    value=[],
                    multi=True,
                    placeholder="Selecciona carrera(s)"
                )
            ]),
        ]),
        
        # Fila 2: Sliders de edad, presión académica, CGPA
        html.Div(className='filter-row', children=[
            html.Div(className='filter-item', children=[
                html.Label("Rango de Edad:"),
                dcc.RangeSlider(
                    id='age-slider',
                    min=df['Age'].min(),
                    max=df['Age'].max(),
                    value=[df['Age'].min(), df['Age'].max()],
                    marks={int(age): str(int(age)) for age in np.linspace(df['Age'].min(), df['Age'].max(), 5)},
                    step=1
                )
            ]),
            
            html.Div(className='filter-item', children=[
                html.Label("Presión Académica:"),
                dcc.RangeSlider(
                    id='pressure-slider',
                    min=df['Academic Pressure'].min(),
                    max=df['Academic Pressure'].max(),
                    value=[df['Academic Pressure'].min(), df['Academic Pressure'].max()],
                    marks={int(p): str(int(p)) for p in range(int(df['Academic Pressure'].min()), int(df['Academic Pressure'].max())+1)},
                    step=0.5
                )
            ]),
            
            html.Div(className='filter-item', children=[
                html.Label("CGPA:"),
                dcc.RangeSlider(
                    id='cgpa-slider',
                    min=df['CGPA'].min(),
                    max=df['CGPA'].max(),
                    value=[df['CGPA'].min(), df['CGPA'].max()],
                    marks={round(cgpa, 1): str(round(cgpa, 1)) for cgpa in np.linspace(df['CGPA'].min(), df['CGPA'].max(), 5)},
                    step=0.1
                )
            ]),
        ]),
        
        # Fila 3: Checkboxes de sueño y radio buttons de depresión
        html.Div(className='filter-row', children=[
            html.Div(className='filter-item', children=[
                html.Label("Duración del Sueño:"),
                dcc.Checklist(
                    id='sleep-checklist',
                    options=sleep_options,
                    value=df['Sleep Duration'].unique().tolist(),
                    inline=True
                )
            ]),
            
            html.Div(className='filter-item', children=[
                html.Label("Estado de Depresión:"),
                dcc.RadioItems(
                    id='depression-radio',
                    options=[
                        {'label': 'Todos', 'value': 'all'},
                        {'label': 'Sin Depresión', 'value': 0},
                        {'label': 'Con Depresión', 'value': 1}
                    ],
                    value='all',
                    inline=True
                )
            ]),
        ]),
        
        html.Hr(),
    ]),

    # KPIs
    html.Div(className='kpis-section', children=[
        html.Div(className='kpis-container', children=[
            html.Div(className='kpi-card kpi-total', children=[
                html.H4("👥 Total Estudiantes"),
                html.H2(id='kpi-total')
            ]),
            
            html.Div(className='kpi-card kpi-depression', children=[
                html.H4("😔 Tasa de Depresión"),
                html.H2(id='kpi-depression')
            ]),
            
            html.Div(className='kpi-card kpi-age', children=[
                html.H4("🎂 Edad Promedio"),
                html.H2(id='kpi-age')
            ]),
            
            html.Div(className='kpi-card kpi-cgpa', children=[
                html.H4("📚 CGPA Promedio"),
                html.H2(id='kpi-cgpa')
            ]),
        ]),
    ]),

    # Gráficos
    html.Div(className='charts-section', children=[
        # Fila 1
        html.Div(className='chart-row', children=[
            html.Div(className='chart-card', children=[
                dcc.Graph(id='depression-pie')
            ]),
            
            html.Div(className='chart-card', children=[
                dcc.Graph(id='gender-bar')
            ]),
        ]),
        
        # Fila 2
        html.Div(className='chart-row', children=[
            html.Div(className='chart-card', children=[
                dcc.Graph(id='sleep-bar')
            ]),
            
            html.Div(className='chart-card', children=[
                dcc.Graph(id='degree-bar')
            ]),
        ]),
        
        # Fila 3: Datos filtrados
        html.Div(className='chart-row', children=[
            html.Div(className='table-card', children=[
                html.H3("📋 Datos Filtrados"),
                dash_table.DataTable(
                    id='filtered-table',
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_header={'backgroundColor': COLORS['table_header'], 'color': 'white', 'fontWeight': 'bold'},
                    style_cell={'textAlign': 'left', 'padding': '8px'}
                )
            ]),
        ]),
    ])
])

if __name__ == '__main__':
    app.run(debug=False)
