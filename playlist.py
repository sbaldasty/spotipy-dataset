from shared import get_client_id
from shared import get_client_secret

import spotipy
import spotipy.util as util

from numpy import unique
from numpy import where

from sklearn.datasets import make_classification
from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import MeanShift
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot

import numpy as np
import pandas as pd
import csv
import os

path = '48k_pitbull_and_23k_gratefuldead_8k_avicii_joint.csv'
data = pd.read_csv(path, header=None)

cols = data.shape[1]
X = data.iloc[:,2:cols]
X = np.array(X.values)

scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

pca = PCA(n_components=5)
X_transformed = pca.fit_transform(X_scaled)
x = X_transformed[:,0]
y = X_transformed[:,1]

model = DBSCAN(eps=.25, min_samples=6)
prediction = model.fit_predict(X_transformed)#xDB)
clusters = unique(prediction)

cluster_list = []
for cluster in clusters:
  ids = []
  for index in where(prediction == cluster)[0]:
    ids.append(data.iloc[index][0])
  cluster_list.append(ids)

#track_ids = cluster_list[2]

username = '12100797839' # Hardcoded to me, for now
token = util.prompt_for_user_token(username,
  client_id=get_client_id(),
  client_secret=get_client_secret(),
  redirect_uri='http://localhost:8888/spotifycallback', scope='playlist-modify-private')

spotify_client = spotipy.Spotify(auth=token)

my_playlist = spotify_client.user_playlist_create(user=username, name='CS254 Playlist 2', public=False)
spotify_client.playlist_add_items(my_playlist['id'], cluster_list[1])

my_playlist = spotify_client.user_playlist_create(user=username, name='CS254 Playlist 2', public=False)
spotify_client.playlist_add_items(my_playlist['id'], cluster_list[2])