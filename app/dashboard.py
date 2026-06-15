
import dash
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dashboard_config import BASE_DIR
from src.dashboard_data import cargar_datos, obtener_opciones_filtros
from src.dashboard_layout import create_layout
from src.dashboard_callbacks import register_callbacks

app = dash.Dash(__name__, title="Dashboard Depresión Estudiantil - Interactivo", assets_folder=str(BASE_DIR / 'assets'))
server = app.server

df = cargar_datos()
gender_options, city_options, degree_options, sleep_options = obtener_opciones_filtros(df)

app.layout = create_layout(df, gender_options, city_options, degree_options, sleep_options)

register_callbacks(app, df)

if __name__ == '__main__':
    app.run(debug=False)
