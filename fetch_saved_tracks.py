import csv

from shared import append_track
from shared import create_spotify_user_client
from shared import csv_header_row
from shared import get_username

spotify_client = create_spotify_user_client('user-library-read')
output_file = 'saved_tracks_' + get_username() + ".csv"
csv_file = open(output_file, 'a+', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(csv_header_row)

offset = 0
trackCounter = 0

while True:

    # I guess this is supposed to be a proxy for Liked songs? I don't think it's exactly what we want!
    # https://community.spotify.com/t5/Spotify-for-Developers/Expose-liked-songs-playlist-to-3rd-party-API-Sonos/td-p/4959924
    saved_tracks = spotify_client.current_user_saved_tracks(limit=30, offset=offset)

    if len(saved_tracks['items']) == 0:
        break

    for item in saved_tracks['items']:
        try:
            append_track(spotify_client, csv_writer, item['track']['id'])
            offset += 1
            trackCounter += 1
            if trackCounter % 10 == 0:
                print('Track Count: ' + str(trackCounter))

        except KeyboardInterrupt:
            break

        except:
            print('ERROR: No audio features')
            offset += 1
