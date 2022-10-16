import csv
import os
import spotipy
import traceback

from pathlib import Path
from spotipy.oauth2 import SpotifyClientCredentials

def ensure_file_exists(filename):
    Path(filename).touch(exist_ok=True)

def load_list(filename):
    ensure_file_exists(filename)
    with open(filename, mode='r', encoding='utf-8') as file:
        return file.read().splitlines()

def save_list(filename, list):
    with open(filename, mode='wt', encoding='utf-8') as file:
        for element in list:
            file.write(element + '\n')

def append_audio_analysis(row):
    # TODO Actually append audio analysis...
    audio_analysis = spotify_client.audio_analysis(row[0])
    row.append(audio_analysis[''])

class SearchQueue:

    def __init__(self, name):
        self.frontier_filename = name + '_frontier'
        self.searched_elements_filename = name + '_searched'
        self.frontier = []
        self.searched_elements = set()

    def add(self, e):
        if e not in self.searched_elements:
            self.frontier.append(e)
            self.searched_elements.add(e)

    def remove(self):
        return self.frontier.pop()

    def is_empty(self):
        return len(self.frontier) == 0

    def load(self):
        self.frontier = load_list(self.frontier_filename)
        self.searched_elements = set(load_list(self.searched_elements_filename))

    def save(self):
        save_list(self.frontier_filename, self.frontier)
        save_list(self.searched_elements_filename, self.searched_elements)
    
class SpotifySearch:

    def __init__(self, client):
        self.client = client
        self.artist_ids = SearchQueue('artists')
        self.album_ids = SearchQueue('albums')
        self.track_ids = SearchQueue('tracks')

    def get_next_artist(self):
        artist_id = self.artist_ids.remove()
        related_artists = self.client.artist_related_artists(artist_id)['artists']

        for related_artist in related_artists:
            self.artist_ids.add(related_artist['id'])

        return artist_id

    def get_next_album(self):
        while self.album_ids.is_empty():
            artist_id = self.get_next_artist()
            response = self.client.artist_albums(artist_id, limit=50)
            for item in response['items']:
                self.album_ids.add(item['id'])

        return self.album_ids.remove()

    def get_next_track(self):
        while self.track_ids.is_empty():
            album_id = self.get_next_album()
            response = self.client.album_tracks(album_id, limit=50, market='US')
            for item in response['items']:
                self.track_ids.add(item['id'])

        return self.track_ids.remove()

    def load(self):
        self.artist_ids.load()
        self.album_ids.load()
        self.track_ids.load()

    def save(self):
        self.artist_ids.save()
        self.album_ids.save()
        self.track_ids.save()

spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_credentials = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
spotify_client = spotipy.Spotify(auth_manager=spotify_credentials)

output_file = 'output.csv'
csv_file = open(output_file, 'a+')
csv_writer = csv.writer(csv_file)
search = SpotifySearch(spotify_client)

if os.path.getsize(output_file) > 0:
    # Pick up where we left off
    search.load()
else:
    # Or start fresh seeding with any old artist
    search.artist_ids.add('0TnOYISbd1XYRBk9myaseg')

try:
    for i in range(30):
        track_id = search.get_next_track()
        track = spotify_client.track(track_id)
        audio_feature = spotify_client.audio_features([track_id])[0]
        row = []

        # Just a sanity check
        print('[ARTIST] ', track['artists'][0]['name'], ' [ALBUM] ', track['album']['name'], ' [TRACK] ', track['name'])

        row.append(track_id)
        row.append(track['explicit'])
        row.append(audio_feature['acousticness'])
        row.append(audio_feature['danceability'])
        row.append(audio_feature['duration_ms'])
        row.append(audio_feature['energy'])
        row.append(audio_feature['instrumentalness'])
        row.append(audio_feature['key'])
        row.append(audio_feature['liveness'])
        row.append(audio_feature['loudness'])
        row.append(audio_feature['mode'])
        row.append(audio_feature['speechiness'])
        row.append(audio_feature['tempo'])
        row.append(audio_feature['time_signature'])
        row.append(audio_feature['valence'])
        #append_audio_analysis(row)
        csv_writer.writerow(row)

except:
    # Guess this doesn't happen automatically if there's a finally block?!
    traceback.print_exc()

finally:
    csv_file.close()
    search.save()
