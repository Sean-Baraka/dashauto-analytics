"""
Shared Controls and Reusable Components
=======================================
This module contains common UI controls used across multiple tabs
in the DashAuto Analytics application.
"""

from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from config import DEFAULT_THEME, SUPPORTED_THEMES


def create_theme_switcher():
    """Theme Switcher Control"""
    return dbc.ButtonGroup([
        dbc.Button(
            "🌙 Dark", 
            id="theme-dark", 
            color="dark", 
            outline=True,
            active=DEFAULT_THEME in ["CYBORG", "DARKLY"]
        ),
        dbc.Button(
            "☀️ Light", 
            id="theme-light", 
            color="light", 
            outline=True
        ),
    ], className="mb-3")


def create_global_controls():
    """Global Controls (appears on top of most tabs)"""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                # Refresh All
                dbc.Col([
                    dbc.Button(
                        [html.I(className="fas fa-sync-alt me-2"), "Refresh All"],
                        id="global-refresh",
                        color="primary",
                        size="sm"
                    )
                ], width="auto"),

                # Dataset Info
                dbc.Col([
                    html.Div(id="global-dataset-info", className="small text-muted")
                ], width=True),

                # Export All Button
                dbc.Col([
                    dbc.Button(
                        [html.I(className="fas fa-download me-2"), "Export Dashboard"],
                        id="export-dashboard",
                        color="success",
                        size="sm",
                        className="float-end"
                    )
                ], width="auto"),

                # Theme Switcher
                dbc.Col([
                    create_theme_switcher()
                ], width="auto"),
            ], align="center")
        ])
    ], className="mb-4 shadow-sm")


def create_filter_controls():
    """Advanced Global Filters"""
    return html.Div([
        dbc.Accordion([
            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col([
                        html.Label("Filter by Column"),
                        dcc.Dropdown(id="global-filter-column", placeholder="Select column...")
                    ], md=4),
                    dbc.Col([
                        html.Label("Filter Condition"),
                        dcc.Dropdown(
                            id="global-filter-operator",
                            options=[
                                {"label": "Equals", "value": "eq"},
                                {"label": "Greater Than", "value": "gt"},
                                {"label": "Less Than", "value": "lt"},
                                {"label": "Contains", "value": "contains"},
                            ],
                            value="eq"
                        )
                    ], md=4),
                    dbc.Col([
                        html.Label("Value"),
                        dcc.Input(id="global-filter-value", type="text", placeholder="Enter value...", className="form-control")
                    ], md=4),
                ]),
                html.Br(),
                dbc.Button("Apply Global Filter", id="apply-global-filter", color="warning", size="sm")
            ], title="🔍 Advanced Global Filters")
        ], start_collapsed=True)
    ])


# ==================== CALLBACKS ====================

def register_controls_callbacks(app):
    """Register callbacks for shared controls"""

    @callback(
        Output("global-dataset-info", "children"),
        Input("stored-data", "data")
    )
    def update_global_info(json_data):
        if not json_data:
            return "No dataset loaded"
        
        try:
            import pandas as pd
            import io
            df = pd.read_json(io.StringIO(json_data), orient='split')
            return f"📊 Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns"
        except:
            return "Error reading dataset"

    # Theme Switcher Callback (Basic)
    @callback(
        Output("main-tabs", "children"),  # You can expand this to dynamically change themes
        Input("theme-dark", "n_clicks"),
        Input("theme-light", "n_clicks"),
        prevent_initial_call=True
    )
    def switch_theme(dark_clicks, light_clicks):
        # In a full implementation, you would use clientside callbacks 
        # or store the theme and reload components
        ctx = callback_context.triggered_id
        print(f"Theme switched to: {'Dark' if ctx == 'theme-dark' else 'Light'}")
        return dash.no_update   # Placeholder - can be expanded


# Make functions available for import
__all__ = [
    'create_theme_switcher',
    'create_global_controls',
    'create_filter_controls',
    'register_controls_callbacks'
]
