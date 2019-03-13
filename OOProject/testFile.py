import spotipy
spotify = spotipy.Spotify()
results = spotify.search(q='artist:' + 'Johari', type='artist')
print(results)