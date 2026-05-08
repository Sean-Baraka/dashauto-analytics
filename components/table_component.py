from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import io
import json

def table_layout():
    """Returns the layout for the Interactive Data Table tab"""
    return html.Div([
        dbc.Row([
            dbc.Col(html.H4("📋 Interactive Data Table & Filtering"), width=8),
            dbc.Col([
                dbc.Button("Refresh Table", id="refresh-table", color="primary", size="sm", className="float-end"),
                dbc.Button("Export to CSV", id="export-csv", color="success", size="sm", className="float-end me-2")
            ], width=4)
        ], className="mb-3"),
        
        dbc.Card([
            dbc.CardBody([
                # Data Table using Dash AG Grid (High Performance)
                dag.AgGrid(
                    id="data-ag-grid",
                    columnDefs=[],           # Will be populated dynamically
                    rowData=[],              # Will be populated dynamically
                    defaultColDef={
                        "filter": True,
                        "sortable": True,
                        "resizable": True,
                        "minWidth": 120,
                    },
                    dashGridOptions={
                        "pagination": True,
                        "paginationPageSize": 20,
                        "enableCellTextSelection": True,
                    },
                    style={"height": "650px", "width": "100%"},
                    className="ag-theme-alpine-dark"
                ),
            ])
        ], className="shadow-sm"),
        
        html.Br(),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Quick Stats"),
                    dbc.CardBody(id="table-stats", children="Upload a dataset to view statistics")
                ])
            ], width=12)
        ])
    ], className="mt-3")


def register_table_callbacks(app):
    """Register all callbacks related to the data table"""

    @callback(
        [Output("data-ag-grid", "columnDefs"),
         Output("data-ag-grid", "rowData"),
         Output("table-stats", "children")],
        Input("stored-data", "data"),
        Input("refresh-table", "n_clicks"),
        prevent_initial_call=True
    )
    def update_data_table(json_data, n_clicks):
        if not json_data:
            return [], [], dbc.Alert("No data available. Please upload a dataset first.", color="warning")
        
        try:
            df = pd.read_json(io.StringIO(json_data), orient='split')
            
            # Create column definitions for AG Grid
            column_defs = [
                {
                    "field": col,
                    "headerName": col,
                    "filter": True,
                    "sortable": True,
                    "editable": True if df[col].dtype.kind in 'biufc' else False
                } for col in df.columns
            ]
            
            # Convert DataFrame to records for AG Grid
            row_data = df.to_dict('records')
            
            # Quick statistics
            stats = html.Div([
                dbc.Row([
                    dbc.Col(html.P(f"**Rows:** {len(df):,}", className="mb-1"), width=3),
                    dbc.Col(html.P(f"**Columns:** {len(df.columns)}", className="mb-1"), width=3),
                    dbc.Col(html.P(f"**Missing Values:** {df.isnull().sum().sum():,}", className="mb-1"), width=3),
                    dbc.Col(html.P(f"**Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB", 
                                 className="mb-1"), width=3),
                ])
            ])
            
            return column_defs, row_data, stats
            
        except Exception as e:
            return [], [], dbc.Alert(f"Error updating table: {str(e)}", color="danger")


    # Export to CSV Callback
    @callback(
        Output("export-csv", "n_clicks"),  # Dummy output to trigger download
        Input("export-csv", "n_clicks"),
        State("stored-data", "data"),
        prevent_initial_call=True
    )
    def export_table_to_csv(n_clicks, json_data):
        if not json_data or n_clicks is None:
            return None
        
        # In a real app, you would use dcc.Download component for actual file download
        # This is a placeholder - you can expand it with dcc.Download
        print("✅ CSV Export requested (implement dcc.Download for full functionality)")
        return None
