# --------------------------------------------------------------------------------------------------------------------------------------##
#                                                                   IMPORTS 
# --------------------------------------------------------------------------------------------------------------------------------------##
from logging import PlaceHolder
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import random
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import time
import requests
import os
load_dotenv()
import warnings
warnings.filterwarnings('ignore')
import random

# --------------------------------------------------------------------------------------------------------------------------------------##
#                                                       LOADING SECRETS
# --------------------------------------------------------------------------------------------------------------------------------------##

SPOTIPY_CLIENT_ID=os.environ.get('CLIENT_ID')
SPOTIPY_CLIENT_SECRET=os.environ.get('CLIENT_SECRET')
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# --------------------------------------------------------------------------------------------------------------------------------------##
#                                                       INITIALIZING APP 
# --------------------------------------------------------------------------------------------------------------------------------------##


external_stylesheets = [dbc.themes.CYBORG, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.title = "Sulify"
server = app.server

# -------------------------------------------------------------------------------------------------------------------------------------##
#                                                   SETUP SULIAPI AND TOOLTIPS
# -------------------------------------------------------------------------------------------------------------------------------------##

def get_predictions(genre, test_feat):
    url = 'https://suliapi.herokuapp.com/predict?genre={genre}&test_feat={test_feat}'.format(genre = genre, test_feat = test_feat)
    response = requests.get(url)
    json_response = response.json()
    uris =json_response['uris']
    return uris

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
ssalert1 = dbc.Alert("Well what's a similarity score if there is nothing to compare.", color='info')
ssalert2 = dbc.Alert("Simply put, we need several songs for this graph to show", color='secondary')
alert3 = dbc.Alert("None for now, enjoy the colorful spinning circles", color='secondary')
alert4 = dbc.Alert("I'm afraid its time to choose another song", color='info')
alert5 = dbc.Alert("Sorry it seems you have better music taste than us", color="info")

alerts = [ alert3, alert4, alert5]
ssalerts = [ssalert1, ssalert2]
#------------------------------------------------------------------------------------------------------------------------------#
#                                                   LAYOUT
#------------------------------------------------------------------------------------------------------------------------------#

app.layout = html.Div(
    children=[
        dbc.NavbarSimple(
            brand="Sulify",
            color="rgba(1,1,1,1)",
            dark=True,
            fluid=True,
            brand_style={'width':'100%', 'font-size':'20px','font-family':'sans-serif'}),               
        html.Div( className="decor",
         children=[
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
                                dcc.Loading(
                                    id="loading-1",
                                    type="circle",
                                    children=[
                                dcc.Dropdown(
                                    id="music-list",
                                    placeholder="Select your song/track:",
                                    style={'border-radius':'10px', 'font-size':'16px'})]),
                    ]),],),
                    html.Br(),
                    html.Div(className='preview', id='music-preview'),
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                label= "Audio Features",
                                tab_id= "audio",
                                label_style={'font-size':'15px'}, 
                                children=[
                                    html.Br(),
                                    dbc.Row( children=[
                                    
                                    dbc.Row(
                                        children=[
                                            dbc.Col(dbc.Card([
                                            dbc.CardBody(
                                                [html.H6("Valence", className="card-title2"),
                                                html.H5(id="valence", className="card_info2"),],),
                                            tooltip1],
                                                style={'border-radius':'8px'},
                                                ),width=6, lg=3),
                                        html.Br(),
                                        dbc.Col(dbc.Card([
                                            dbc.CardBody(
                                                [html.H6("Acousticness", className="card-title2"),
                                                html.H5(id="acousticness", className="card_info2"),],),
                                            tooltip2],
                                                style={'border-radius':'8px'},
                                                ),width=6, lg=3),
                                        html.Br(),
                                        dbc.Col(dbc.Card([
                                            dbc.CardBody(
                                                [html.H6("Danceability", className="card-title2"),
                                                html.H5(id="danceability", className="card_info2"),],),
                                            tooltip3],
                                            style={'border-radius':'8px'},
                                                ),width=6, lg=3),
                                        html.Br(),
                                        dbc.Col(dbc.Card([
                                            dbc.CardBody(
                                                [html.H6("Energy", className="card-title2"),
                                                html.H5(id="energy", className="card_info2"),],),
                                            tooltip4],
                                            style={'border-radius':'8px'},
                                             ),width=6, lg=3),
                                        html.Br(),
                                    ]),])
                            ,
                            html.Br(),
                            dbc.Row([
                                dcc.Store(id="main_store"),
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
                                html.Div(id="tab-content2", className="p-4"),
                                ]),]),
                            dbc.Tab(
                                label= "Recommendations",
                                tab_id= "recommender",
                                label_style={'font-size':'15px'},
                                children=[
                                    html.Br(),
                                    dbc.Button("Get Recommendations", id='recommender'),
                                    
                                    dcc.Loading(
                                    id="loading-2",
                                    type="circle",
                                    children=[
                                        html.H4("Similar Songs"),
                                        dbc.Row( className='row row-cols-auto', id='song-results'),]),
                                    dcc.Store(id='rec-store'),
                                    dcc.Store(id='song-store'),
                                    dbc.Button("View similarity Scores", id='similarity'),
                                    dcc.Loading(
                                    id="loading-3",
                                    type="circle",
                                    children=[dbc.Row(id='tsne-graph')]),
                                ])
                        ], id="tabs1", active_tab="audio")])])
#------------------------------------------------------------------------------------------------------------------------------#
#                                                   CALLBACKS
#------------------------------------------------------------------------------------------------------------------------------#

@app.callback(
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
                search_results.append(track['name'] + " - By - " + track['artists'][0]['name'])
    return [item for item  in search_results]
def input_triggers_nested(value):
    time.sleep(1)
    return value



@app.callback(
    Output('music-preview', 'children'),
    Output('main_store', 'data'),
    Input('music-list', 'value'),
)
def song_image(value):
    song_name = str(value).split('-')[0]
    artist_name = str(value).split('-')[-1]
    track_res = sp.search(q='artist:' + artist_name + ' track:' + song_name, limit=1, offset=0, type='track', market=None)
    track_id = track_res['tracks']['items'][0]['id']
    iframe = html.Iframe(src=f'https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0', width='80%',
     height='80',
      style={'border-radius':'12px', 'background-color':'rgba(0,0,0,0)', 'font-size':'15px'},
       allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture")
    features = sp.audio_features(track_id)
    return iframe, features


@app.callback(
    Output('song-store','data'),
    Output('rec-store','data'),
    Output('song-results', 'children'),
    Input('recommender', 'n_clicks'),
    Input('music-list', 'value')
)
def recommender(n_clicks, value):
    if n_clicks and value is not None:
        song_name = str(value).split('-')[0]
        artist_name = str(value).split('-')[-1]
        track_res = sp.search(q='artist:' + artist_name + ' track:' + song_name, limit=1, offset=0, type='track', market=None)
        track_id = track_res['tracks']['items'][0]['id']
        artist = sp.artist(track_res['tracks']['items'][0]["artists"][0]["external_urls"]["spotify"])
        genre = artist["genres"][0]
        features = sp.audio_features(track_id)
        vals = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'valence', 'tempo']
        test_feat = []
        for val in vals:
            test_feat.append(features[0][val])
        try:
            uris = get_predictions(genre, test_feat)
            songs = []
            for uri in uris[:10]:
                songs.append(html.Iframe(src=f'https://open.spotify.com/embed/track/{uri}', width='350', height='80', style={'border-style': 'none', 'background-color':'rgba(0,0,0,0)', 'font-size':'15px'}))
            return features, uris[:10], songs
        except requests.JSONDecodeError:
            return None, None, random.choice(alerts)
    elif value is None:
        return None, None, dbc.Alert("Please search and select one song .", color="info")
def input_triggers_nested(value):
    time.sleep(2)
    return value


@app.callback(
    Output('tsne-graph', 'children'),
    Input('rec-store', 'data'),
    Input('similarity', 'n_clicks'),
    Input('song-store', 'data'),
    Input('music-list', 'value')
)
def tsnegraph(rdata, n_clicks, sdata, value):
    if n_clicks and rdata is not None:
        all_data = pd.DataFrame()
        song = pd.Series()
        song_name = str(value).split('-')[0]
        for track in rdata:
            f = sp.audio_features(track)
            df = pd.DataFrame(f)
            all_data = pd.concat([all_data, df])
            s = sp.track(track)
            name = pd.Series(s['name'])
            song = pd.concat([song, name])
        all_data = all_data.reset_index()
        all_data['song_name'] = song.reset_index()[0]
        s_data= pd.DataFrame(sdata)
        s_data['song_name'] = song_name
        all_data = pd.concat([all_data, s_data])
        all_data = all_data.reset_index()
        X = (all_data.filter(['acousticness', 'danceability', 'duration_ms', 'energy',
        'instrumentalness', 'liveness', 'loudness', 'tempo', 'valence']))

        # algo will do better if data is standardized (zero mean, unit variance)
        Xs = StandardScaler().fit_transform(X)
        tsne = TSNE(n_components=2, perplexity=5,early_exaggeration=2, random_state=3).fit_transform(Xs)

        # convert to dataframe for plotting purposes
        tsne = pd.DataFrame(tsne)
        tsne['duration_ms'] = all_data['duration_ms']
        tsne['Song name'] = all_data['song_name']
        fig = px.scatter(tsne, x=0, y=1, size='duration_ms', size_max=60, hover_name='Song name',template='plotly_dark',color='Song name', title="Similarity Scores")
        fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor = "rgba(0,0,0,0)")
        return dcc.Graph(figure=fig)
        

    elif rdata and sdata is None:
        return random.choice(ssalerts)
    else:
        return dbc.Alert("Please get song recommendations", color='secondary')


@app.callback(
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
    dance, valence, acoustic, energy = f'{round(dance*100, 1)}%',f'{round(valence*100,1)}%',f'{round(acoustic*100, 1)}%',f'{round(energy*100, 1)}%'
    return  energy, dance, valence, acoustic
def input_triggers_nested(value):
    time.sleep(3)
    return value



@app.callback(
    Output("tab-content2", "children"),
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
            fig = px.line_polar(df1, r=df1.values.flatten(), theta=df1.columns,line_close=True,template='plotly_dark')
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

# ----------------------------------------------------------------------------------##
#                                   LAUNCH
# ----------------------------------------------------------------------------------##
    
if __name__ == "__main__":
    app.run_server(debug=True)
