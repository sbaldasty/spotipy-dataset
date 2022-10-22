# TODO Why do I need to supply a username before asking the user to authenticate?!
# TODO Looks like we can only get "saved" songs, which are not sctrictly "liked" songs; at least make terminology consistent

import csv
import spotipy
import spotipy.util as util

from shared import append_track

username = '12100797839' # Hardcoded to me, for now
token = util.prompt_for_user_token(username, redirect_uri='http://localhost:8888/spotifycallback', scope='user-library-read')
spotify_client = spotipy.Spotify(auth=token)

output_file = 'saved_tracks_' + username + ".csv"
csv_file = open(output_file, 'a+')
csv_writer = csv.writer(csv_file)

offset = 0
while True:

    # I guess this is supposed to be a proxy for Liked songs? I don't think it's exactly what we want!
    # https://community.spotify.com/t5/Spotify-for-Developers/Expose-liked-songs-playlist-to-3rd-party-API-Sonos/td-p/4959924
    saved_tracks = spotify_client.current_user_saved_tracks(limit=2, offset=offset)

    if len(saved_tracks['items']) == 0:
        break

    for item in saved_tracks['items']:
        append_track(spotify_client, csv_writer, item['track']['id'])
        offset += 1
