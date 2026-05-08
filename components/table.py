from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

def table_layout():
    return html.Div([
        html.H4("Interactive Data Table"),
        dag.AgGrid(id="data-table", columnDefs=[], rowData=[], defaultColDef={"filter": True, "sortable": True})
    ])

def register_table_callbacks(app):
    # Can be expanded further
    pass
