import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = dash.Dash(__name__, title="Dashboard Depresión Estudiantil - Interactivo")
server = app.server

# Cargar datos
df = pd.read_csv('data/processed/Student_Depression_Dataset_Limpio.csv')

# Preparar opciones para filtros
gender_options = [{'label': g, 'value': g} for g in df['Gender'].unique()]
city_options = [{'label': c, 'value': c} for c in df['City'].unique()]
degree_options = [{'label': d, 'value': d} for d in df['Degree'].unique()]
sleep_options = [{'label': s, 'value': s} for s in df['Sleep Duration'].unique()]

# Layout del dashboard
app.layout = html.Div([
    html.Div([
        html.H1("📊 Dashboard de Depresión en Estudiantes - Interactivo", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30, 'paddingTop': 20})
    ], style={'backgroundColor': '#f8f9fa', 'paddingBottom': 20}),

    # Sección de filtros
    html.Div([
        html.Div([
            html.H3("🔍 Filtros", style={'color': '#2c3e50', 'marginBottom': 15}),
            
            # Fila 1: Género, Ciudad, Carrera
            html.Div([
                html.Div([
                    html.Label("Género:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='gender-filter',
                        options=gender_options,
                        value=[],
                        multi=True,
                        placeholder="Selecciona género(s)"
                    )
                ], style={'flex': 1, 'padding': 10}),
                
                html.Div([
                    html.Label("Ciudad:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='city-filter',
                        options=city_options,
                        value=[],
                        multi=True,
                        placeholder="Selecciona ciudad(es)"
                    )
                ], style={'flex': 1, 'padding': 10}),
                
                html.Div([
                    html.Label("Carrera:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='degree-filter',
                        options=degree_options,
                        value=[],
                        multi=True,
                        placeholder="Selecciona carrera(s)"
                    )
                ], style={'flex': 1, 'padding': 10}),
            ], style={'display': 'flex', 'marginBottom': 20}),
            
            # Fila 2: Sliders de edad, presión académica, CGPA
            html.Div([
                html.Div([
                    html.Label("Rango de Edad:", style={'fontWeight': 'bold'}),
                    dcc.RangeSlider(
                        id='age-slider',
                        min=df['Age'].min(),
                        max=df['Age'].max(),
                        value=[df['Age'].min(), df['Age'].max()],
                        marks={int(age): str(int(age)) for age in np.linspace(df['Age'].min(), df['Age'].max(), 5)},
                        step=1
                    )
                ], style={'flex': 1, 'padding': 10}),
                
                html.Div([
                    html.Label("Presión Académica:", style={'fontWeight': 'bold'}),
                    dcc.RangeSlider(
                        id='pressure-slider',
                        min=df['Academic Pressure'].min(),
                        max=df['Academic Pressure'].max(),
                        value=[df['Academic Pressure'].min(), df['Academic Pressure'].max()],
                        marks={int(p): str(int(p)) for p in range(int(df['Academic Pressure'].min()), int(df['Academic Pressure'].max())+1)},
                        step=0.5
                    )
                ], style={'flex': 1, 'padding': 10}),
                
                html.Div([
                    html.Label("CGPA:", style={'fontWeight': 'bold'}),
                    dcc.RangeSlider(
                        id='cgpa-slider',
                        min=df['CGPA'].min(),
                        max=df['CGPA'].max(),
                        value=[df['CGPA'].min(), df['CGPA'].max()],
                        marks={round(cgpa, 1): str(round(cgpa, 1)) for cgpa in np.linspace(df['CGPA'].min(), df['CGPA'].max(), 5)},
                        step=0.1
                    )
                ], style={'flex': 1, 'padding': 10}),
            ], style={'display': 'flex', 'marginBottom': 20}),
            
            # Fila 3: Checkboxes de sueño y radio buttons de depresión
            html.Div([
                html.Div([
                    html.Label("Duración del Sueño:", style={'fontWeight': 'bold'}),
                    dcc.Checklist(
                        id='sleep-checklist',
                        options=sleep_options,
                        value=df['Sleep Duration'].unique().tolist(),
                        inline=True
                    )
                ], style={'flex': 1, 'padding': 10}),
                
                html.Div([
                    html.Label("Estado de Depresión:", style={'fontWeight': 'bold'}),
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
                ], style={'flex': 1, 'padding': 10}),
            ], style={'display': 'flex', 'marginBottom': 20}),
            
            html.Hr(),
        ], style={'backgroundColor': 'white', 'padding': 20, 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'margin': '0 20px 20px 20px'}),
    ]),

    # KPIs
    html.Div([
        html.Div([
            html.Div([
                html.H4("👥 Total Estudiantes"),
                html.H2(id='kpi-total', style={'color': '#3498db'})
            ], className='kpi-card', style={'flex': 1, 'padding': 20, 'background': '#f8f9fa', 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
            
            html.Div([
                html.H4("😔 Tasa de Depresión"),
                html.H2(id='kpi-depression', style={'color': '#e74c3c'})
            ], className='kpi-card', style={'flex': 1, 'padding': 20, 'background': '#f8f9fa', 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
            
            html.Div([
                html.H4("🎂 Edad Promedio"),
                html.H2(id='kpi-age', style={'color': '#2ecc71'})
            ], className='kpi-card', style={'flex': 1, 'padding': 20, 'background': '#f8f9fa', 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
            
            html.Div([
                html.H4("📚 CGPA Promedio"),
                html.H2(id='kpi-cgpa', style={'color': '#f39c12'})
            ], className='kpi-card', style={'flex': 1, 'padding': 20, 'background': '#f8f9fa', 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        ], style={'display': 'flex', 'gap': 20, 'marginBottom': 20, 'padding': '0 20px'}),
    ]),

    # Gráficos
    html.Div([
        # Fila 1
        html.Div([
            html.Div([
                dcc.Graph(id='depression-pie')
            ], style={'flex': 1, 'padding': 20, 'background': 'white', 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
            
            html.Div([
                dcc.Graph(id='gender-bar')
            ], style={'flex': 1, 'padding': 20, 'background': 'white', 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        ], style={'display': 'flex', 'gap': 20, 'marginBottom': 20, 'padding': '0 20px'}),
        
        # Fila 2
        html.Div([
            html.Div([
                dcc.Graph(id='sleep-bar')
            ], style={'flex': 1, 'padding': 20, 'background': 'white', 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
            
            html.Div([
                dcc.Graph(id='pressure-cgpa-scatter')
            ], style={'flex': 1, 'padding': 20, 'background': 'white', 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        ], style={'display': 'flex', 'gap': 20, 'marginBottom': 20, 'padding': '0 20px'}),
        
        # Fila 3
        html.Div([
            html.Div([
                dcc.Graph(id='degree-bar')
            ], style={'flex': 1, 'padding': 20, 'background': 'white', 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        ], style={'display': 'flex', 'gap': 20, 'marginBottom': 20, 'padding': '0 20px'}),
        
        # Fila 4: Datos filtrados
        html.Div([
            html.Div([
                html.H3("📋 Datos Filtrados", style={'color': '#2c3e50'}),
                dash_table.DataTable(
                    id='filtered-table',
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
                    style_cell={'textAlign': 'left', 'padding': '8px'}
                )
            ], style={'flex': 1, 'padding': 20, 'background': 'white', 'borderRadius': 10, 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        ], style={'display': 'flex', 'gap': 20, 'marginBottom': 20, 'padding': '0 20px'}),
    ])
])

# Función para filtrar datos
def filter_data(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status):
    filtered_df = df.copy()
    
    # Aplicar filtros
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

# Callback para actualizar KPIs
@callback(
    [Output('kpi-total', 'children'),
     Output('kpi-depression', 'children'),
     Output('kpi-age', 'children'),
     Output('kpi-cgpa', 'children')],
    [Input('gender-filter', 'value'),
     Input('city-filter', 'value'),
     Input('degree-filter', 'value'),
     Input('age-slider', 'value'),
     Input('pressure-slider', 'value'),
     Input('cgpa-slider', 'value'),
     Input('sleep-checklist', 'value'),
     Input('depression-radio', 'value')]
)
def update_kpis(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status):
    filtered_df = filter_data(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
    
    total = len(filtered_df)
    depression_rate = (filtered_df['Depression'].mean() * 100).round(1) if total > 0 else 0
    avg_age = filtered_df['Age'].mean().round(1) if total > 0 else 0
    avg_cgpa = filtered_df['CGPA'].mean().round(2) if total > 0 else 0
    
    return (
        f"{total}",
        f"{depression_rate}%",
        f"{avg_age}",
        f"{avg_cgpa}"
    )

# Callback para gráfico de pastel
@callback(
    Output('depression-pie', 'figure'),
    [Input('gender-filter', 'value'),
     Input('city-filter', 'value'),
     Input('degree-filter', 'value'),
     Input('age-slider', 'value'),
     Input('pressure-slider', 'value'),
     Input('cgpa-slider', 'value'),
     Input('sleep-checklist', 'value'),
     Input('depression-radio', 'value')]
)
def update_depression_pie(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status):
    filtered_df = filter_data(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
    
    depression_counts = filtered_df['Depression'].value_counts().sort_index()
    depression_labels = {0: 'Sin Depresión', 1: 'Con Depresión'}
    
    fig = go.Figure(data=[go.Pie(
        labels=[depression_labels.get(x, str(x)) for x in depression_counts.index],
        values=depression_counts.values,
        hole=0.4,
        marker_colors=['#2ecc71', '#e74c3c'],
        textinfo='percent+label',
        textfont_size=14
    )])
    
    fig.update_layout(
        title="Distribución de Depresión",
        showlegend=False
    )
    
    return fig

# Callback para gráfico de género
@callback(
    Output('gender-bar', 'figure'),
    [Input('gender-filter', 'value'),
     Input('city-filter', 'value'),
     Input('degree-filter', 'value'),
     Input('age-slider', 'value'),
     Input('pressure-slider', 'value'),
     Input('cgpa-slider', 'value'),
     Input('sleep-checklist', 'value'),
     Input('depression-radio', 'value')]
)
def update_gender_bar(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status):
    filtered_df = filter_data(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
    
    gender_depression = filtered_df.groupby(['Gender', 'Depression']).size().unstack(fill_value=0)
    if gender_depression.empty:
        return go.Figure().update_layout(title="Depresión por Género")
    
    gender_depression_pct = gender_depression.div(gender_depression.sum(axis=1), axis=0) * 100
    
    fig = go.Figure()
    if 0 in gender_depression_pct.columns:
        fig.add_trace(go.Bar(
            name='Sin Depresión',
            x=gender_depression_pct.index,
            y=gender_depression_pct[0],
            marker_color='#2ecc71'
        ))
    if 1 in gender_depression_pct.columns:
        fig.add_trace(go.Bar(
            name='Con Depresión',
            x=gender_depression_pct.index,
            y=gender_depression_pct[1],
            marker_color='#e74c3c'
        ))
    
    fig.update_layout(
        title="Depresión por Género (%)",
        barmode='stack',
        xaxis_title="Género",
        yaxis_title="Porcentaje"
    )
    
    return fig

# Callback para gráfico de sueño
@callback(
    Output('sleep-bar', 'figure'),
    [Input('gender-filter', 'value'),
     Input('city-filter', 'value'),
     Input('degree-filter', 'value'),
     Input('age-slider', 'value'),
     Input('pressure-slider', 'value'),
     Input('cgpa-slider', 'value'),
     Input('sleep-checklist', 'value'),
     Input('depression-radio', 'value')]
)
def update_sleep_bar(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status):
    filtered_df = filter_data(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
    
    sleep_order = ['Less than 5 hours', '5-6 hours', '7-8 hours', 'More than 8 hours']
    sleep_depression = filtered_df.groupby(['Sleep Duration', 'Depression']).size().unstack(fill_value=0)
    if sleep_depression.empty:
        return go.Figure().update_layout(title="Depresión por Duración del Sueño")
    
    sleep_depression = sleep_depression.reindex(sleep_order).dropna(how='all')
    sleep_depression_pct = sleep_depression.div(sleep_depression.sum(axis=1), axis=0) * 100
    
    fig = go.Figure()
    if 0 in sleep_depression_pct.columns:
        fig.add_trace(go.Bar(
            name='Sin Depresión',
            x=sleep_depression_pct.index,
            y=sleep_depression_pct[0],
            marker_color='#2ecc71'
        ))
    if 1 in sleep_depression_pct.columns:
        fig.add_trace(go.Bar(
            name='Con Depresión',
            x=sleep_depression_pct.index,
            y=sleep_depression_pct[1],
            marker_color='#e74c3c'
        ))
    
    fig.update_layout(
        title="Depresión por Duración del Sueño (%)",
        barmode='stack',
        xaxis_title="Duración del Sueño",
        yaxis_title="Porcentaje"
    )
    
    return fig

# Callback para gráfico de presión académica vs CGPA
@callback(
    Output('pressure-cgpa-scatter', 'figure'),
    [Input('gender-filter', 'value'),
     Input('city-filter', 'value'),
     Input('degree-filter', 'value'),
     Input('age-slider', 'value'),
     Input('pressure-slider', 'value'),
     Input('cgpa-slider', 'value'),
     Input('sleep-checklist', 'value'),
     Input('depression-radio', 'value')]
)
def update_pressure_cgpa_scatter(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status):
    filtered_df = filter_data(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
    
    fig = px.scatter(
        filtered_df,
        x='Academic Pressure',
        y='CGPA',
        color='Depression',
        color_continuous_scale=['#2ecc71', '#e74c3c'],
        title="Presión Académica vs CGPA",
        labels={'Depression': 'Depresión (0=No, 1=Sí)'},
        hover_data=['Age', 'Gender', 'City', 'Degree']
    )
    
    fig.update_layout(
        xaxis_title="Presión Académica",
        yaxis_title="CGPA"
    )
    
    return fig

# Callback para gráfico de carrera
@callback(
    Output('degree-bar', 'figure'),
    [Input('gender-filter', 'value'),
     Input('city-filter', 'value'),
     Input('degree-filter', 'value'),
     Input('age-slider', 'value'),
     Input('pressure-slider', 'value'),
     Input('cgpa-slider', 'value'),
     Input('sleep-checklist', 'value'),
     Input('depression-radio', 'value')]
)
def update_degree_bar(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status):
    filtered_df = filter_data(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
    
    degree_depression = filtered_df.groupby(['Degree', 'Depression']).size().unstack(fill_value=0)
    if degree_depression.empty:
        return go.Figure().update_layout(title="Depresión por Carrera", height=600)
    
    degree_depression_pct = degree_depression.div(degree_depression.sum(axis=1), axis=0) * 100
    degree_depression_pct = degree_depression_pct.sort_values(by=1 if 1 in degree_depression_pct.columns else degree_depression_pct.columns[0], ascending=False)
    
    fig = go.Figure()
    if 0 in degree_depression_pct.columns:
        fig.add_trace(go.Bar(
            name='Sin Depresión',
            y=degree_depression_pct.index,
            x=degree_depression_pct[0],
            orientation='h',
            marker_color='#2ecc71'
        ))
    if 1 in degree_depression_pct.columns:
        fig.add_trace(go.Bar(
            name='Con Depresión',
            y=degree_depression_pct.index,
            x=degree_depression_pct[1],
            orientation='h',
            marker_color='#e74c3c'
        ))
    
    fig.update_layout(
        title="Depresión por Carrera (%)",
        barmode='stack',
        yaxis_title="Carrera",
        xaxis_title="Porcentaje",
        height=600
    )
    
    return fig

# Callback para la tabla de datos
@callback(
    [Output('filtered-table', 'columns'),
     Output('filtered-table', 'data')],
    [Input('gender-filter', 'value'),
     Input('city-filter', 'value'),
     Input('degree-filter', 'value'),
     Input('age-slider', 'value'),
     Input('pressure-slider', 'value'),
     Input('cgpa-slider', 'value'),
     Input('sleep-checklist', 'value'),
     Input('depression-radio', 'value')]
)
def update_table(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status):
    filtered_df = filter_data(genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
    
    columns = [{'name': col, 'id': col} for col in filtered_df.columns]
    data = filtered_df.to_dict('records')
    
    return columns, data

if __name__ == '__main__':
    app.run(debug=False)
