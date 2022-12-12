import math
import os
import spotipy

csv_header_row = [
    'Track ID',
    'Explicit',
    'Acousticness',
    'danceability',
    'duration_ms',
    'energy',
    'instrumentalness',
    'key',
    'liveness',
    'loudness',
    'mode',
    'speechiness',
    'tempo',
    'time_signature',
    'valence',
    'bar count',
    'mean bar duration',
    'std dev bar duration',
    'mean bar confidence',
    'std dev bar confidence',
    'beat count',
    'mean beat duration',
    'std dev beat duration',
    'mean bar confidence',
    'std dev bar confidence',
    'section count',
    'mean section duration',
    'std dev section duration',
    'mean section confidence',
    'std dev section confidence',
    'mean section loudness',
    'std dev section loudness',
    'mean section tempo',
    'std dev section tempo',
    'section key count',
    'mean section key confidence',
    'std dev section key confidence',
    'section mode count',
    'mean section mode confidence',
    'std dev section mode confidence',
    'section time signature count',
    'mean section time signature confidence',
    'std dev time signature confidence',
    'tatum count',
    'mean tatum duration',
    'std dev tatum duration',
    'mean tatum confidence',
    'std dev tatum confidence']

def get_client_id():
    return os.environ['SPOTIPY_CLIENT_ID']

def get_client_secret():
    return os.environ['SPOTIPY_CLIENT_SECRET']

def get_username():
    return os.environ['SPOTIFY_USERNAME']

def create_spotify_user_client(scope):
    token = spotipy.util.prompt_for_user_token(
        username=get_username(),
        client_id=get_client_id(),
        client_secret=get_client_secret(),
        redirect_uri='http://localhost:8888/spotifycallback',
        scope=scope)

    return spotipy.Spotify(auth=token)

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
    return 0 if count == 0 else math.sqrt(sum / count)

def append_audio_features(spotify_client, row):
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

def append_audio_analysis(spotify_client, row):
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

def append_track(spotify_client, csv_writer, track_id):
    track = spotify_client.track(track_id)

    row = []
    row.append(track_id) # Column 1
    row.append(track['explicit']) # Column 2
    append_audio_features(spotify_client, row)
    append_audio_analysis(spotify_client, row)
    csv_writer.writerow(row)
