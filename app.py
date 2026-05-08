import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from components.upload import upload_layout, register_upload_callbacks
from components.eda import eda_layout, register_eda_callbacks
from components.visualizations import viz_layout, register_viz_callbacks
from components.table import table_layout, register_table_callbacks

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    title="DashAuto Analytics"
)

server = app.server

app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand=html.H2("📊 DashAuto Analytics", className="text-white"),
        color="dark",
        dark=True,
        className="mb-4"
    ),
    
    dcc.Store(id='stored-data', storage_type='memory'),
    dcc.Store(id='data-profile', storage_type='memory'),
    
    dbc.Tabs(id="main-tabs", active_tab="upload", children=[
        dbc.Tab(label="📤 Upload", tab_id="upload", children=upload_layout()),
        dbc.Tab(label="📊 Auto EDA", tab_id="eda", children=eda_layout()),
        dbc.Tab(label="📈 Visualizations", tab_id="viz", children=viz_layout()),
        dbc.Tab(label="📋 Data Table", tab_id="table", children=table_layout()),
    ]),
    
    html.Br(),
    dbc.Footer("Postgraduate Diploma Project © 2026 | Built with Plotly Dash", 
               className="text-center text-muted")
], fluid=True)

# Register Callbacks
register_upload_callbacks(app)
register_eda_callbacks(app)
register_viz_callbacks(app)
register_table_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
