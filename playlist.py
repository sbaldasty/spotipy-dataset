# TODO Why do I need to supply a username before asking the user to authenticate?!

import spotipy
import spotipy.util as util

track_ids = ['1VbNiIJyEG0DgojlNREOrQ', '4SO31yImLzc8VZwq110kcZ']

username = '12100797839' # Hardcoded to me, for now
token = util.prompt_for_user_token(username, redirect_uri='http://localhost:8888/spotifycallback', scope='playlist-modify-private')
spotify_client = spotipy.Spotify(auth=token)

my_playlist = spotify_client.user_playlist_create(user=username, name='CS254 Playlist', public=False)
print(my_playlist)
spotify_client.playlist_add_items(my_playlist['id'], track_ids)