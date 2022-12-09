from shared import get_client_id
from shared import get_client_secret

import spotipy
import spotipy.util as util

from numpy import unique
from numpy import where

from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import numpy as np
import pandas as pd

liked_df = pd.read_csv('saved_tracks_12100797839.csv', header=0)
library_df = pd.read_csv('48k_pitbull_and_23k_gratefuldead_8k_avicii_joint.csv', header=0)

colsU = liked_df.shape[1]
uX = liked_df.iloc[:,2:colsU]

cols = library_df.shape[1]
library_df = library_df.drop_duplicates(subset=['duration_ms', 'Acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness'])

combined_df = pd.concat([library_df, liked_df], axis=0)
X = combined_df.iloc[:,2:cols]
X = np.array(X.values)

def dataframe_to_id_set(df):
  result = set()
  for index, row in df.iterrows():
    result.add(row[0])
  return result

userTrackIDs = dataframe_to_id_set(liked_df)

scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

pca = PCA(n_components=6)
X_transformed = pca.fit_transform(X_scaled)
x = X_transformed[:,0]
y = X_transformed[:,1]

model = DBSCAN(eps=0.95, min_samples=5)
prediction = model.fit_predict(X_transformed)#xDB)
clusters = unique(prediction)

def clustersToSet(clusters):
  cluster_list = []
  for cluster in clusters:
    ids = set()
    for index in where(prediction == cluster)[0]:
      ids.add(combined_df.iloc[index][0])
    cluster_list.append(ids)
  return cluster_list

clusterIDSet = clustersToSet(clusters)

def remove_user_songs(cluster_list, liked_track_ids):
  output = []
  for cluster in cluster_list:
    diff = cluster.difference(liked_track_ids)
    if len(diff) < len(cluster) and len(diff) > 0:
      output.append(diff)
  return output

cluster_list = remove_user_songs(clusterIDSet, userTrackIDs)


username = '12100797839' # Hardcoded to me, for now

token = util.prompt_for_user_token(username,
  client_id=get_client_id(),
  client_secret=get_client_secret(),
  redirect_uri='http://localhost:8888/spotifycallback',
  scope='playlist-modify-private')

spotify_client = spotipy.Spotify(auth=token)

my_playlist = spotify_client.user_playlist_create(user=username, name='Playlisteners - Steven', public=False)
spotify_client.playlist_add_items(my_playlist['id'], cluster_list[2])
