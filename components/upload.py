from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import base64
import io
import pandas as pd
from utils.data_processor import clean_dataset, generate_profile

def upload_layout():
    return html.Div([
        dbc.Card([
            dbc.CardBody([
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select CSV/Excel File')
                    ], className="text-center"),
                    style={
                        'width': '100%', 'height': '120px', 'lineHeight': '120px',
                        'borderWidth': '2px', 'borderStyle': 'dashed',
                        'borderRadius': '10px', 'textAlign': 'center'
                    },
                    multiple=False
                ),
                html.Div(id='upload-feedback', className="mt-3")
            ])
        ], className="shadow")
    ])

def register_upload_callbacks(app):
    @callback(
        [Output('stored-data', 'data'),
         Output('upload-feedback', 'children'),
         Output('data-profile', 'data')],
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )
    def process_upload(contents, filename):
        if contents is None:
            return None, "", None
        
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            else:
                df = pd.read_excel(io.BytesIO(decoded))
            
            df_clean = clean_dataset(df)
            profile = generate_profile(df_clean)
            
            return (df_clean.to_json(date_format='iso', orient='split'),
                    dbc.Alert(f"✅ Successfully loaded {filename} ({df_clean.shape[0]:,} rows, {df_clean.shape[1]} columns)", 
                             color="success"),
                    profile)
        except Exception as e:
            return None, dbc.Alert(f"❌ Error: {str(e)}", color="danger"), None
