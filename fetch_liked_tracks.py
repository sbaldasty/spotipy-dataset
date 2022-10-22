# TODO Why do I need to supply a username before asking the user to authenticate?!
# TODO Page through the liked songs so we can collect all of them
# TODO Looks like we can only get "saved" songs, which are not sctrictly "liked" songs; at least make terminology consistent

import csv
import spotipy
import spotipy.util as util

from shared import append_track

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))

username = '12100797839' # Hardcoded to me, for now
token = util.prompt_for_user_token(username, redirect_uri='http://localhost:8888/spotifycallback', scope='user-library-read')
spotify_client = spotipy.Spotify(auth=token)

output_file = 'saved_tracks_' + username + ".csv"
csv_file = open(output_file, 'a+')
csv_writer = csv.writer(csv_file)

# I guess this is supposed to be a proxy for Liked songs? I don't think it's exactly what we want!
# https://community.spotify.com/t5/Spotify-for-Developers/Expose-liked-songs-playlist-to-3rd-party-API-Sonos/td-p/4959924
saved_tracks = spotify_client.current_user_saved_tracks(limit=30)

track_ids = []
for item in saved_tracks['items']:
    track_ids.append(item['track']['id'])

for track_id in track_ids:
    append_track(spotify_client, csv_writer, track_id)
