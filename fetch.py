import os
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

def create_client():
    id = os.environ['SPOTIFY_CLIENT_ID']
    secret = os.environ['SPOTIFY_CLIENT_SECRET']
    credentials = SpotifyClientCredentials(client_id=id, client_secret=secret)

    return spotipy.Spotify(auth_manager=credentials)

client = create_client()

results = client.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])
