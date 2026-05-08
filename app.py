import dash
from dash import dcc, html, Input, Output, State, callback, ALL, MATCH
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import io
import json
from datetime import datetime
from components.upload_component import create_upload_layout
from components.eda_component import create_eda_layout
from components.viz_component import create_viz_layout
from components.table_component import create_table_layout
from utils.data_utils import clean_dataset, generate_full_profile
from utils.plot_utils import create_correlation_heatmap

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="DashAuto Analytics",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

server = app.server

# Global layout
app.layout = dbc.Container([
    dbc.Navbar(
        dbc.Container([
            html.A("📊 DashAuto Analytics", className="navbar-brand fw-bold fs-3"),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Upload", id="nav-upload", href="#")),
                dbc.NavItem(dbc.NavLink("EDA", id="nav-eda", href="#")),
                dbc.NavItem(dbc.NavLink("Visualize", id="nav-viz", href="#")),
                dbc.NavItem(dbc.NavLink("Table", id="nav-table", href="#")),
            ], className="ms-auto")
        ]),
        color="dark",
        dark=True,
    ),
    
    dcc.Store(id='stored-data', storage_type='memory'),
    dcc.Store(id='dataset-profile', storage_type='memory'),
    
    dbc.Row([
        dbc.Col([
            html.Div(id="main-content")
        ], width=12)
    ], className="mt-3"),
    
    dbc.Footer([
        html.P("Postgraduate Diploma Project • Built with ❤️ using Plotly Dash", className="text-center text-muted small")
    ], className="mt-5")
], fluid=True, className="p-0")

# Callbacks for navigation and core functionality
@callback(
    Output('main-content', 'children'),
    Input('nav-upload', 'n_clicks'),
    Input('nav-eda', 'n_clicks'),
    Input('nav-viz', 'n_clicks'),
    Input('nav-table', 'n_clicks'),
    prevent_initial_call=True
)
def update_main_content(n1, n2, n3, n4):
    ctx = dash.callback_context.triggered_id
    if ctx == 'nav-upload' or not ctx:
        return create_upload_layout()
    elif ctx == 'nav-eda':
        return create_eda_layout()
    elif ctx == 'nav-viz':
        return create_viz_layout()
    elif ctx == 'nav-table':
        return create_table_layout()
    return create_upload_layout()

# File Upload Callback
@callback(
    [Output('stored-data', 'data'),
     Output('upload-feedback', 'children'),
     Output('dataset-profile', 'data')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def process_upload(contents, filename):
    if contents is None:
        return None, "", None
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None, dbc.Alert("Unsupported format", color="danger"), None
        
        # Process data
        df_clean = clean_dataset(df)
        profile = generate_full_profile(df_clean)
        
        return df_clean.to_json(date_format='iso', orient='split'), \
               dbc.Alert(f"✅ Loaded {filename} successfully ({df_clean.shape[0]:,} rows, {df_clean.shape[1]} columns)", color="success"), \
               profile
               
    except Exception as e:
        return None, dbc.Alert(f"Error processing file: {str(e)}", color="danger"), None
