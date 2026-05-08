from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import io
import json

def viz_layout():
    """Layout for the Interactive Visualizations Tab"""
    return html.Div([
        dbc.Row([
            dbc.Col(html.H4("📈 Custom Interactive Visualizations"), width=8),
            dbc.Col(
                dbc.Button("🔄 Clear Plot", id="clear-plot", color="secondary", size="sm", className="float-end"),
                width=4
            )
        ], className="mb-3"),

        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    # X Variable
                    dbc.Col([
                        html.Label("X Axis Variable"),
                        dcc.Dropdown(id="x-var", placeholder="Select X variable...", clearable=True)
                    ], md=3),

                    # Y Variable
                    dbc.Col([
                        html.Label("Y Axis Variable (Optional)"),
                        dcc.Dropdown(id="y-var", placeholder="Select Y variable...", clearable=True)
                    ], md=3),

                    # Chart Type
                    dbc.Col([
                        html.Label("Chart Type"),
                        dcc.Dropdown(
                            id="chart-type",
                            options=[
                                {"label": "Scatter Plot", "value": "scatter"},
                                {"label": "Line Plot", "value": "line"},
                                {"label": "Bar Chart", "value": "bar"},
                                {"label": "Histogram", "value": "histogram"},
                                {"label": "Box Plot", "value": "box"},
                                {"label": "Violin Plot", "value": "violin"},
                                {"label": "Heatmap (Correlation)", "value": "heatmap"},
                                {"label": "3D Scatter", "value": "scatter_3d"},
                            ],
                            value="scatter",
                            clearable=False
                        )
                    ], md=3),

                    # Color Variable
                    dbc.Col([
                        html.Label("Color By (Optional)"),
                        dcc.Dropdown(id="color-var", placeholder="Color by variable...", clearable=True)
                    ], md=3),
                ], className="mb-4"),

                dbc.Button("Generate Visualization", id="generate-plot-btn", 
                          color="primary", size="lg", className="w-100 mb-4")
            ])
        ], className="shadow-sm mb-4"),

        # Main Graph Area
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(
                    id="main-visualization",
                    style={"height": "680px"},
                    config={"displayModeBar": True, "scrollZoom": True}
                )
            ])
        ], className="shadow-sm"),

        html.Br(),

        # Additional Info
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Plot Information"),
                    dbc.CardBody(id="plot-info", children="Select variables and chart type then click Generate")
                ])
            ], width=12)
        ])
    ])


def register_viz_callbacks(app):
    """Register all visualization-related callbacks"""

    @callback(
        [Output("x-var", "options"),
         Output("y-var", "options"),
         Output("color-var", "options")],
        Input("stored-data", "data")
    )
    def populate_dropdowns(json_data):
        if not json_data:
            return [], [], []
        
        df = pd.read_json(io.StringIO(json_data), orient='split')
        options = [{"label": col, "value": col} for col in df.columns]
        return options, options, options

    @callback(
        [Output("main-visualization", "figure"),
         Output("plot-info", "children")],
        Input("generate-plot-btn", "n_clicks"),
        State("x-var", "value"),
        State("y-var", "value"),
        State("color-var", "value"),
        State("chart-type", "value"),
        State("stored-data", "data"),
        prevent_initial_call=True
    )
    def generate_visualization(n_clicks, x, y, color, chart_type, json_data):
        if not json_data or not x:
            return px.scatter(title="Please upload data and select at least X variable"), \
                   dbc.Alert("Please select at least X variable", color="warning")

        df = pd.read_json(io.StringIO(json_data), orient='split')
        
        # Intelligent sampling for large datasets
        if len(df) > 10000:
            df = df.sample(n=10000, random_state=42)
            sample_note = " (Sampled to 10,000 rows for performance)"
        else:
            sample_note = ""

        try:
            fig = None
            info = f"Chart Type: {chart_type.upper()} | X: {x} | Y: {y or 'None'}"

            if chart_type == "scatter":
                fig = px.scatter(df, x=x, y=y, color=color, title=f"{y} vs {x}{sample_note}")
            
            elif chart_type == "line":
                fig = px.line(df, x=x, y=y, color=color, title=f"Line Plot: {y} over {x}{sample_note}")
            
            elif chart_type == "bar":
                fig = px.bar(df, x=x, y=y, color=color, title=f"Bar Chart: {y} by {x}{sample_note}")
            
            elif chart_type == "histogram":
                fig = px.histogram(df, x=x, color=color, title=f"Distribution of {x}{sample_note}")
            
            elif chart_type == "box":
                fig = px.box(df, x=x, y=y, color=color, title=f"Box Plot: {y} by {x}{sample_note}")
            
            elif chart_type == "violin":
                fig = px.violin(df, x=x, y=y, color=color, title=f"Violin Plot: {y} by {x}{sample_note}")
            
            elif chart_type == "heatmap":
                corr = df.select_dtypes(include=['number']).corr()
                fig = px.imshow(corr, text_auto=True, aspect="auto", 
                              color_continuous_scale='RdBu_r',
                              title="Correlation Heatmap")
            
            elif chart_type == "scatter_3d":
                if y and color:
                    fig = px.scatter_3d(df, x=x, y=y, z=color, 
                                      title=f"3D Scatter: {x}, {y}, {color}{sample_note}")
                else:
                    fig = px.scatter_3d(df, x=x, y=df.columns[1] if len(df.columns)>1 else x, 
                                      z=df.columns[2] if len(df.columns)>2 else x,
                                      title="3D Scatter (First 3 Numeric Columns)")

            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=40, r=40, t=60, b=40),
                height=680
            )

            return fig, html.Div([
                html.P(info, className="mb-1"),
                html.Small(f"Dataset: {len(df):,} rows displayed{sample_note}", className="text-muted")
            ])

        except Exception as e:
            error_fig = px.scatter(title="Error generating plot")
            return error_fig, dbc.Alert(f"Error: {str(e)}", color="danger")

    # Clear Plot Callback
    @callback(
        Output("main-visualization", "figure"),
        Input("clear-plot", "n_clicks"),
        prevent_initial_call=True
    )
    def clear_visualization(n_clicks):
        return px.scatter(title="Plot cleared. Select new variables and generate again.")
