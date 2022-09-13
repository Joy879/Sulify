from logging import PlaceHolder
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import dash
from dash import html, dcc, dash_table,  callback
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
#                                  SETUP PAGE DETAILS
# ----------------------------------------------------------------------------------##
dash.register_page(__name__, path='/',title='Sulify',name='Sulify')
# ----------------------------------------------------------------------------------##
#                                  TOOLTIPS
# ----------------------------------------------------------------------------------##
tooltip1 = dbc.Tooltip(
            "Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).",
            target="valence",
        )
tooltip2 = dbc.Tooltip(
            "Whether the track is acoustic. 100% represents high confidence the track is acoustic.",
            target="acousticness",
        )

tooltip3 = dbc.Tooltip(
            "How suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.",
            target="danceability",
        )
tooltip4 = dbc.Tooltip(
            "a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. ",
            target="energy",
        )
# ----------------------------------------------------------------------------------##
#                                  LAYOUT
# ----------------------------------------------------------------------------------##

layout = html.Div(
                    [
                        html.Div( className="decor", children=[
                            # html.H6('Sulify', style={'align-items':'right'}),
                        dbc.Container([
                            dbc.Row(className='row row-cols-auto', children=[
                                html.Div(children=[
                                    dcc.Input(
                                        className="search",
                                        id="search-input",
                                        placeholder="Search for any favorite song",
                                        style={
                                            'width': '250px',
                                            'display': 'flex',
                                            'justifyContent': 'center',
                                            'font-size': '16px'})]),
                        ]),
                        ]),]),
                        dbc.Container([
                            dbc.Row([
                                html.Div(
                                    className="dash-bootstrap",
                                    children=[
                                        dcc.Dropdown(
                                            id="music-list",
                                            placeholder="Select your song/track:",
                                            style={'border-radius':'10px', 'font-size':'16px'})]),
                            ]),
                            html.Hr(),
                            dbc.Row(className='row row-cols-auto', children=[
                                html.Div(
                                    className='preview', id='music-preview'),
                                html.Br(),
                                dbc.Row(
                                    className='row row-cols-auto',
                                    children=[dbc.Card([
                                        dbc.CardBody(
                                            [html.H6("Valence", className="card-title2"),
                                            html.H5(id="valence", className="card_info2"),],),
                                        tooltip1],
                                            style={'width':'40%',
                                            'height':'10rem', 'border-radius':'8px'},
                                            ),
                                            
                                    html.Br(),
                                    dbc.Card([
                                        dbc.CardBody(
                                            [html.H6("Acousticness", className="card-title2"),
                                            html.H5(id="acousticness", className="card_info2"),],),
                                        tooltip2],
                                            style={'width':'40%', 'height':'10rem', 'border-radius':'8px'}),
                                    html.Br(),
                                    dbc.Card([
                                        dbc.CardBody(
                                            [html.H6("Danceability", className="card-title2"),
                                            html.H5(id="danceability", className="card_info2"),],),
                                         tooltip3],
                                            style={'width':'40%', 'height':'10rem', 'border-radius':'8px'}),
                                    html.Br(),
                                    dbc.Card([
                                        dbc.CardBody(
                                            [html.H6("Energy", className="card-title2"),
                                            html.H5(id="energy", className="card_info2"),],),
                                         tooltip4],
                                        style={'width':'40%', 'height':'10rem', 'border-radius':'8px'} ),
                                    html.Br(),
        
                                ]),]),
                        ]),                       
                        dbc.Container([
                            dcc.Store(id="main_store"),
                            html.H3("Audio Features"),
                            html.Hr(),
                            dbc.Tabs(
                                [
                                    dbc.Tab(
                                        label= "Polar",
                                        tab_id= "polar",
                                        label_style={'font-size':'15px'}),
                                    dbc.Tab(
                                        label= "Bar Graphs",
                                        tab_id= "bar-graphs",
                                        label_style={'font-size':'15px'}),
                                ], id="tabs", active_tab="polar"),
                            html.Div(id="tab-content", className="p-4"),
                            ])
                            ]
                        )

# ----------------------------------------------------------------------------------##
#                                  CALLBACKS 
# ----------------------------------------------------------------------------------##
@callback(
    Output('music-list', 'options'),
    Input('search-input', 'value'),
)
def search(value):
    search_results=[]
    if value is not None and len(str(value)) > 0:
        tracks = sp.search(q='track:'+ value,type='track', limit=20)
        tracks_list = tracks['tracks']['items']
        if len(tracks_list) > 0:
            for track in tracks_list:
                #st.write(track['name'] + " - By - " + track['artists'][0]['name'])
                search_results.append(track['name'] + " - By - " + track['artists'][0]['name'])
    return [item for item  in search_results]

@callback(
    Output('music-preview', 'children'),
    Output('main_store', 'data'),
    Input('music-list', 'value'),
)
def song_image(value):
    song_name = str(value).split('-')[0]
    artist_name = str(value).split('-')[-1]
    track_res = sp.search(q='artist:' + artist_name + ' track:' + song_name,
                          limit=1,
                          offset=0,
                          type='track', market=None)
    track_id = track_res['tracks']['items'][0]['id']
    iframe = html.Iframe(src=f'https://open.spotify.com/embed/track/{track_id}',
                         width='350',
                         height='425',
                         style={'border-style': 'none', 'background-color':'rgba(0,0,0,0)', 'font-size':'15px'})
    features = sp.audio_features(track_id)
    return iframe, features

@callback(
    Output('energy', 'children'),
    Output('danceability', 'children'),
    Output('valence', 'children'),
    Output('acousticness', 'children'),
    Input('main_store', 'data'),
)
def features(data):
    dance = data[0]['danceability']
    valence = data[0]['valence']
    acoustic = data[0]['acousticness']
    energy = data[0]['energy']
    dance, valence, acoustic, energy = f'{round(dance*100, 1)}%',
                                       f'{round(valence*100,1)}%',
                                       f'{round(acoustic*100, 1)}%',
                                       f'{round(energy*100, 1)}%'
    return  energy, dance, valence, acoustic


@callback(
    Output("tab-content", "children"),
    [
    Input("tabs", "active_tab"), 
    Input("main_store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        df = pd.DataFrame(data)
        if active_tab == "polar":
            df1 = df[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
            fig = px.line_polar(df1,
                                r=df1.values.flatten(),
                                theta=df1.columns,
                                line_close=True,
                                template='plotly_dark')
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor = "rgba(0,0,0,0)",
                font_color="#e7d7f1",
                title={'y':0.85,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_family="Century Gothic",
                title_font_color="#e7d7f1",
                title_font_size=20,
                )
            polar = dcc.Graph(figure=fig)
            return polar
        elif active_tab == "bar-graphs":
            df1 = df[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
            df2 = df1[df1.values>0]
            fig = px.bar(
                x=df1.columns,
                y=df1.values.flatten(),
                color=df1.columns,
                labels={
                     "x": "Audio Features",
                     "y": "Values",
                     "color": "Audio Features"
                 } 
                )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor = "rgba(0,0,0,0)",
                font_color="#e7d7f1",
                title={'y':0.85,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                title_font_family="Century Gothic",
                title_font_color="#e7d7f1",
                title_font_size=20,
                xaxis = dict(showgrid=False),
                yaxis = dict(title =None, showgrid = False)
                )
            bar = dcc.Graph(figure=fig)
            return bar
              
    return "No tab selected"
