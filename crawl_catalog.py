import csv
import os
import spotipy
import traceback

from math import sqrt
from pathlib import Path
from spotipy.oauth2 import SpotifyClientCredentials

spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
spotify_credentials = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
spotify_client = spotipy.Spotify(auth_manager=spotify_credentials)

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

def count_distinct_values(list, property):
    values = set()
    for element in list:
        values.add(element[property])
    return len(values)

def mean(list, property):
    sum = 0
    count = len(list)
    for element in list:
        sum += element[property]
    return 0 if count == 0 else sum / count

def standard_deviation(list, property):
    sum = 0
    count = len(list)
    avg = mean(list, property)
    for element in list:
        sum += (element[property] - avg) ** 2
    return 0 if count == 0 else sqrt(sum / count)

def append_audio_features(row):
    audio_feature = spotify_client.audio_features([row[0]])[0]
    row.append(audio_feature['acousticness']) # Column 3
    row.append(audio_feature['danceability']) # Column 4
    row.append(audio_feature['duration_ms']) # Column 5
    row.append(audio_feature['energy']) # Column 6
    row.append(audio_feature['instrumentalness']) # Column 7
    row.append(audio_feature['key']) # Column 8
    row.append(audio_feature['liveness']) # Column 9
    row.append(audio_feature['loudness']) # Column 10
    row.append(audio_feature['mode']) # Column 11
    row.append(audio_feature['speechiness']) # Column 12
    row.append(audio_feature['tempo']) # Column 13
    row.append(audio_feature['time_signature']) # Column 14
    row.append(audio_feature['valence']) # Column 15

def append_audio_analysis(row):
    audio_analysis = spotify_client.audio_analysis(row[0])

    # Bars
    row.append(len(audio_analysis['bars'])) # Column 16
    row.append(mean(audio_analysis['bars'], 'duration')) # Column 17
    row.append(standard_deviation(audio_analysis['bars'], 'duration')) # Column 18
    row.append(mean(audio_analysis['bars'], 'confidence')) # Column 19
    row.append(standard_deviation(audio_analysis['bars'], 'confidence')) # Column 20

    # Beats
    row.append(len(audio_analysis['beats'])) # Column 21
    row.append(mean(audio_analysis['beats'], 'duration')) # Column 22
    row.append(standard_deviation(audio_analysis['beats'], 'duration')) # Column 23
    row.append(mean(audio_analysis['beats'], 'confidence')) # Column 24
    row.append(standard_deviation(audio_analysis['beats'], 'confidence')) # Column 25

    # Sections
    row.append(len(audio_analysis['sections'])) # Column 26
    row.append(mean(audio_analysis['sections'], 'duration')) # Column 27
    row.append(standard_deviation(audio_analysis['sections'], 'duration')) # Column 28
    row.append(mean(audio_analysis['sections'], 'confidence')) # Column 29
    row.append(standard_deviation(audio_analysis['sections'], 'confidence')) # Column 30
    row.append(mean(audio_analysis['sections'], 'loudness')) # Column 31
    row.append(standard_deviation(audio_analysis['sections'], 'loudness')) # Column 32
    row.append(mean(audio_analysis['sections'], 'tempo')) # Column 33
    row.append(standard_deviation(audio_analysis['sections'], 'tempo')) # Column 34
    row.append(count_distinct_values(audio_analysis['sections'], 'key')) # Column 35
    row.append(mean(audio_analysis['sections'], 'key_confidence')) # Column 36
    row.append(standard_deviation(audio_analysis['sections'], 'key_confidence')) # Column 37
    row.append(count_distinct_values(audio_analysis['sections'], 'mode')) # Column 38
    row.append(mean(audio_analysis['sections'], 'mode_confidence')) # Column 39
    row.append(standard_deviation(audio_analysis['sections'], 'mode_confidence')) # Column 40
    row.append(count_distinct_values(audio_analysis['sections'], 'time_signature')) # Column 41
    row.append(mean(audio_analysis['sections'], 'time_signature_confidence')) # Column 42
    row.append(standard_deviation(audio_analysis['sections'], 'time_signature_confidence')) # Column 43

    # Tatums
    row.append(len(audio_analysis['tatums'])) # Column 44
    row.append(mean(audio_analysis['tatums'], 'duration')) # Column 45
    row.append(standard_deviation(audio_analysis['tatums'], 'duration')) # Column 46
    row.append(mean(audio_analysis['tatums'], 'confidence')) # Column 47
    row.append(standard_deviation(audio_analysis['tatums'], 'confidence')) # Column 48

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

output_file = 'output.csv'
csv_file = open(output_file, 'a+')
csv_writer = csv.writer(csv_file)
search = SpotifySearch(spotify_client)

if os.path.getsize(output_file) > 0:
    print('File ' + output_file + ' exists, attempting to continue data gathering')
    search.load()
else:
    print('No saved progress, starting fresh with any old artist')
    search.artist_ids.add('0TnOYISbd1XYRBk9myaseg')

try:
    for i in range(9000):
        track_id = search.get_next_track()
        track = spotify_client.track(track_id)
        print('[ARTIST] ', track['artists'][0]['name'], ' [ALBUM] ', track['album']['name'], ' [TRACK] ', track['name'])

        row = []
        row.append(track_id) # Column 1
        row.append(track['explicit']) # Column 2
        append_audio_features(row)
        append_audio_analysis(row)
        csv_writer.writerow(row)

except:
    # Guess this doesn't happen automatically if there's a finally block?!
    traceback.print_exc()

finally:
    csv_file.close()
    search.save()
