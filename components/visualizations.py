from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import io

def viz_layout():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("X Variable"), 
                dcc.Dropdown(id="x-var", placeholder="Select X")
            ], md=3),
            dbc.Col([
                html.Label("Y Variable"), 
                dcc.Dropdown(id="y-var", placeholder="Select Y")
            ], md=3),
            dbc.Col([
                html.Label("Chart Type"),
                dcc.Dropdown(id="chart-type", options=[
                    {"label": "Scatter", "value": "scatter"},
                    {"label": "Bar", "value": "bar"},
                    {"label": "Histogram", "value": "histogram"},
                    {"label": "Box Plot", "value": "box"},
                    {"label": "Violin", "value": "violin"}
                ], value="scatter")
            ], md=3),
            dbc.Col(dbc.Button("Generate Plot", id="gen-plot", color="primary", className="mt-4"), md=3)
        ]),
        dcc.Graph(id="main-graph", style={"height": "650px"})
    ])

def register_viz_callbacks(app):
    @callback(
        [Output("x-var", "options"), Output("y-var", "options")],
        Input("stored-data", "data")
    )
    def update_dropdowns(json_data):
        if not json_data:
            return [], []
        df = pd.read_json(io.StringIO(json_data), orient='split')
        cols = [{"label": col, "value": col} for col in df.columns]
        return cols, cols

    @callback(
        Output("main-graph", "figure"),
        Input("gen-plot", "n_clicks"),
        State("x-var", "value"),
        State("y-var", "value"),
        State("chart-type", "value"),
        State("stored-data", "data"),
        prevent_initial_call=True
    )
    def generate_plot(n, x, y, chart_type, json_data):
        if not json_data or not x:
            return px.scatter(title="Upload data and select variables")
        
        df = pd.read_json(io.StringIO(json_data), orient='split')
        
        if chart_type == "scatter":
            return px.scatter(df, x=x, y=y, title=f"{y} vs {x}")
        elif chart_type == "bar":
            return px.bar(df, x=x, y=y if y else None)
        elif chart_type == "histogram":
            return px.histogram(df, x=x)
        elif chart_type == "box":
            return px.box(df, x=x, y=y)
        return px.scatter(df, x=x, y=y)
