# ----------------------------------------------------------------------------------##
#                                  IMPORTS 
# ----------------------------------------------------------------------------------##
from logging import PlaceHolder
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
load_dotenv()

# ----------------------------------------------------------------------------------##
#                                  LOADING SECRETS
# ----------------------------------------------------------------------------------##

SPOTIPY_CLIENT_ID=os.environ.get('CLIENT_ID')
SPOTIPY_CLIENT_SECRET=os.environ.get('CLIENT_SECRET')
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ----------------------------------------------------------------------------------##
#                                  INITIALIZING APP 
# ----------------------------------------------------------------------------------##


external_stylesheets = [dbc.themes.CYBORG, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
app = dash.Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)
app.title = "Sulify"
server = app.server

# ----------------------------------------------------------------------------------##
#                                  LAYOUT 
# ----------------------------------------------------------------------------------##

app.layout = html.Div(
    children=[
        dbc.NavbarSimple(
            children=[
                dbc.NavItem([
                dbc.NavLink('Home', href=dash.page_registry['pages.main']['path'], style={'font-size':'15px'}),
                ]),
                dbc.NavItem([
                dbc.NavLink('Recommender', href=dash.page_registry['pages.recommender']['path'], style={'font-size':'15px'}
                )
                ]),
            ],
            brand="Sulify",
            color="rgba(1,1,1,1)",
            dark=True,
            fluid=True,
            brand_style={'width':'100%', 'font-size':'20px','font-family':'sans-serif'}),
        dash.page_container,                
            ])

# ----------------------------------------------------------------------------------##
#                                   LAUNCH
# ----------------------------------------------------------------------------------##
    
if __name__ == "__main__":
    app.run_server(debug=True)
