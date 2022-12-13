import numpy as np
import pandas as pd

from numpy import unique
from numpy import where
from shared import create_spotify_user_client
from shared import csv_header_row
from shared import get_username
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def create_track_list(clusters, min_cluster_size, max_cluster_size):
    output = []
    for cluster in clusters:
        if len(cluster) <= min_cluster_size and len(cluster) <= max_cluster_size:
            output += cluster

    return output

def dataframe_to_id_set(df):
    result = set()
    for index, row in df.iterrows():
        result.add(row[0])

    return result

def create_recommendation_playlist(playlist_name, library_path, saved_songs_path, dbscan_eps, min_cluster_size, max_cluster_size, num_clusters):
    library_df = pd.read_csv(library_path, header=0)
    library_df = library_df.drop_duplicates(subset=csv_header_row[4:12])

    saved_songs_df = pd.read_csv(saved_songs_path, header=0)
    cols = library_df.shape[1]

    combined_df = pd.concat([library_df, saved_songs_df], axis=0)
    X = combined_df.iloc[:,2:cols]
    X = np.array(X.values)
    X = StandardScaler().fit_transform(X)
    X = PCA(n_components=6).fit_transform(X)
    prediction = DBSCAN(eps=dbscan_eps, min_samples=5).fit_predict(X)

    saved_track_ids = dataframe_to_id_set(saved_songs_df)

    clusters = []
    for cluster in unique(prediction):
        ids = set()
        for index in where(prediction == cluster)[0]:
            ids.add(combined_df.iloc[index][0])

        diff = ids - saved_track_ids
        if len(diff) < len(ids) and len(diff) > 0:
            clusters.append(diff)

    track_ids = create_track_list(clusters, min_cluster_size, max_cluster_size)
    client = create_spotify_user_client('playlist-modify-private')
    playlist = client.user_playlist_create(user=get_username(), name=playlist_name, public=False)

    if len(track_ids) > 0:
        client.playlist_add_items(playlist['id'], track_ids[:100])

create_recommendation_playlist(
    playlist_name='Playlisteners - Emmett',
    library_path='output.csv',
    saved_songs_path='saved_tracks_doublelock.csv',
    dbscan_eps=0.55,
    min_cluster_size=3,
    max_cluster_size=50,
    num_clusters=20)

create_recommendation_playlist(
    playlist_name='Playlisteners - Luke',
    library_path='output.csv',
    saved_songs_path='saved_tracks_lbzeppelin.csv',
    dbscan_eps=0.95,
    min_cluster_size=3,
    max_cluster_size=50,
    num_clusters=20)

create_recommendation_playlist(
    playlist_name='Playlisteners - Steven',
    library_path='output.csv',
    saved_songs_path='saved_tracks_12100797839.csv',
    dbscan_eps=0.95,
    min_cluster_size=3,
    max_cluster_size=50,
    num_clusters=20)
