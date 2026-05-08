def create_eda_layout():
    return html.Div([
        dbc.Row([
            dbc.Col(html.H3("Automated Exploratory Data Analysis"), md=9),
            dbc.Col(dbc.Button("Run Full Analysis", id="run-eda-btn", color="success", size="lg"), md=3)
        ]),
        html.Div(id="eda-results-container", className="mt-4")
    ])

@callback(
    Output("eda-results-container", "children"),
    Input("run-eda-btn", "n_clicks"),
    Input("stored-data", "data"),
    prevent_initial_call=True
)
def render_eda_results(n, json_data):
    if not json_data:
        return dbc.Alert("Please upload a dataset first", color="warning")
    
    df = pd.read_json(io.StringIO(json_data), orient='split')
    profile = generate_full_profile(df)  # Recompute or use stored
    
   
 # Generate multiple figures
    missing_fig = px.bar(x=list(profile['missing'].keys()), 
                        y=list(profile['missing'].values()),
                        title="Missing Values per Column")
    
    return dbc.Row([
        dbc.Col(dbc.Card([dbc.CardHeader("Dataset Summary"), dbc.CardBody([...])]), md=4),
        dbc.Col(dcc.Graph(figure=missing_fig), md=8),
        # Add 8+ more cards: distributions, correlations, outliers, etc.
    ])
