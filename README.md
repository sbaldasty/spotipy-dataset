**<span style="color:red">Advisory: These scripts are not ready or recommended for public use at the moment!</span>**

# Setup
Install Spotipy package
```
pip install spotipy
```
Needs a Spotify App to authenticate to API, here's a [tutorial on how to create one](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/). The redirect URL in the script is currently hard-coded to http://localhost:8888/spotifycallback, and the redirect URL of your app needs to match.

# crawl_catalog.py
Gathers a dataset of spotify tracks from the collection at large into a file *output.csv*.

The columns are
1. track id
2. explicit
3. acousticness
4. danceability
5. duration_ms
6. energy
7. instrumentalness
8. key
9. liveness
10. loudness
11. mode
12. speechiness
13. tempo
14. time_signature
15. valence
16. bar count
17. mean bar duration
18. std dev bar duration
19. mean bar confidence
20. std dev bar confidence
21. beat count
22. mean beat duration
23. std dev beat duration
24. mean bar confidence
25. std dev bar confidence
26. section count
27. mean section duration
28. std dev section duration
29. mean section confidence
30. std dev section confidence
31. mean section loudness
32. std dev section loudness
33. mean section tempo
34. std dev section tempo
35. section key count
36. mean section key confidence
37. std dev section key confidence
38. section mode count
39. mean section mode confidence
40. std dev section mode confidence
41. section time signature count
42. mean section time signature confidence
43. std dev time signature confidence
44. tatum count
45. mean tatum duration
46. std dev tatum duration
47. mean tatum confidence
48. std dev tatum confidence

# fetch_saved_tracks.py
Gathers a dataset of spotify tracks from a user's saved songs into a file *saved_tracks_**[userid]**.csv*.
