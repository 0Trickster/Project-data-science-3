
from dash import Input, Output, callback
import plotly.graph_objects as go
from .dashboard_config import COLORS
from .dashboard_data import filter_data

def register_callbacks(app, df):
    
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
        filtered_df = filter_data(df, genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
        
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
        filtered_df = filter_data(df, genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
        
        depression_counts = filtered_df['Depression'].value_counts().sort_index()
        depression_labels = {0: 'Sin Depresión', 1: 'Con Depresión'}
        
        fig = go.Figure(data=[go.Pie(
            labels=[depression_labels.get(x, str(x)) for x in depression_counts.index],
            values=depression_counts.values,
            hole=0.4,
            marker_colors=[COLORS['no_depression'], COLORS['yes_depression']],
            textinfo='percent+label',
            textfont_size=14
        )])
        
        fig.update_layout(
            title="Distribución de Depresión",
            showlegend=False
        )
        
        return fig

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
        filtered_df = filter_data(df, genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
        
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
                marker_color=COLORS['no_depression']
            ))
        if 1 in gender_depression_pct.columns:
            fig.add_trace(go.Bar(
                name='Con Depresión',
                x=gender_depression_pct.index,
                y=gender_depression_pct[1],
                marker_color=COLORS['yes_depression']
            ))
        
        fig.update_layout(
            title="Depresión por Género (%)",
            barmode='stack',
            xaxis_title="Género",
            yaxis_title="Porcentaje"
        )
        
        return fig

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
        filtered_df = filter_data(df, genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
        
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
                marker_color=COLORS['no_depression']
            ))
        if 1 in sleep_depression_pct.columns:
            fig.add_trace(go.Bar(
                name='Con Depresión',
                x=sleep_depression_pct.index,
                y=sleep_depression_pct[1],
                marker_color=COLORS['yes_depression']
            ))
        
        fig.update_layout(
            title="Depresión por Duración del Sueño (%)",
            barmode='stack',
            xaxis_title="Duración del Sueño",
            yaxis_title="Porcentaje"
        )
        
        return fig

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
        filtered_df = filter_data(df, genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
        
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
                marker_color=COLORS['no_depression']
            ))
        if 1 in degree_depression_pct.columns:
            fig.add_trace(go.Bar(
                name='Con Depresión',
                y=degree_depression_pct.index,
                x=degree_depression_pct[1],
                orientation='h',
                marker_color=COLORS['yes_depression']
            ))
        
        fig.update_layout(
            title="Depresión por Carrera (%)",
            barmode='stack',
            yaxis_title="Carrera",
            xaxis_title="Porcentaje",
            height=600
        )
        
        return fig

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
        filtered_df = filter_data(df, genders, cities, degrees, age_range, pressure_range, cgpa_range, sleep_values, depression_status)
        
        columns = [{'name': col, 'id': col} for col in filtered_df.columns]
        data = filtered_df.to_dict('records')
        
        return columns, data

