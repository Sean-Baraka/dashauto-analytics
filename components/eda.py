from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import io
from utils.data_processor import generate_profile

def eda_layout():
    return html.Div([
        dbc.Button("Run Full Automated EDA", id="run-eda", color="success", size="lg", className="mb-3"),
        html.Div(id="eda-results", className="mt-3")
    ])

def register_eda_callbacks(app):
    @callback(
        Output("eda-results", "children"),
        Input("run-eda", "n_clicks"),
        Input("stored-data", "data"),
        prevent_initial_call=True
    )
    def show_eda(n, json_data):
        if not json_data:
            return dbc.Alert("Please upload data first!", color="warning")
        
        df = pd.read_json(io.StringIO(json_data), orient='split')
        profile = generate_profile(df)
        
        missing_fig = px.bar(x=list(profile['missing'].keys()), 
                           y=list(profile['missing'].values()), 
                           title="Missing Values by Column")
        
        corr_fig = px.imshow(pd.DataFrame(profile['correlation']), 
                           text_auto=True, title="Correlation Heatmap")
        
        return dbc.Row([
            dbc.Col(dbc.Card([dbc.CardHeader("Dataset Summary"), 
                            dbc.CardBody([html.P(f"Rows: {profile['shape'][0]:,}, Columns: {profile['shape'][1]}")])]), md=4),
            dbc.Col(dcc.Graph(figure=missing_fig), md=8),
            dbc.Col(dcc.Graph(figure=corr_fig), md=12, className="mt-4"),
        ])
