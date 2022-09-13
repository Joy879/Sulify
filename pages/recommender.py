import dash
from dash import html, dcc, callback, Input, Output
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
import os
load_dotenv()

# ----------------------------------------------------------------------------------##
#                                  LOADING SECRETS
# ----------------------------------------------------------------------------------##

SPOTIPY_CLIENT_ID=os.environ.get('CLIENT_ID')
SPOTIPY_CLIENT_SECRET=os.environ.get('CLIENT_SECRET')
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_predictions(genre, test_feat):
    url = 'https://suliapi.herokuapp.com/predict?genre={genre}&test_feat={test_feat}'.format(genre = genre, test_feat = test_feat)
    response = requests.get(url)
    json_response = response.json()
    uris =json_response['uris']
    return uris

dash.register_page(__name__, path='/Recommendations',title='Sulify Recommender',name='Sulify Recommender')

layout = html.Div(
                    [
                        html.Div( children=[
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
                        ]),
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
                            dbc.Button("Get Recommendations", id='recommender'),
                            html.H3("Similar Songs"),
                            dbc.Row( className='row row-cols-auto', id='song-results'),
                            dcc.Store(id='rec-store'),
                            dcc.Store(id='song-store'),
                            dbc.Button("View similarity Scores", id='similarity'),
                            dbc.Row(id='tsne-graph')
                        ])]),])


@callback(
    Output('song-store','data'),
    Output('rec-store','data'),
    Output('song-results', 'children'),
    Input('recommender', 'n_clicks'),
    Input('music-list', 'value')
)
def recommender(value, n_clicks):
    if value is not None:
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
        uris = get_predictions(genre, test_feat)
        songs = []
        for uri in uris[:10]:
            songs.append(html.Iframe(src=f'https://open.spotify.com/embed/track/{uri}', width='350', height='100', style={'border-style': 'none', 'background-color':'rgba(0,0,0,0)', 'font-size':'15px'}))
        return features, uris[:10], songs
    elif value is None:
        return None, None, dbc.Alert("Please search and select one song .", color="warning")

@callback(
    Output('tsne-graph', 'children'),
    Input('rec-store', 'data'),
    Input('similarity', 'n_clicks'),
    Input('song-store', 'data'),
    Input('music-list', 'value')
)
def tsnegraph(rdata, n_clicks, sdata, value):
    if rdata is not None:
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
        return dcc.Graph(figure=fig)
    elif rdata is None:
        return dbc.Alert("Please get song recommendations.", color='warning')

        
  