import spotipy
import spotipy.util as util

token = util.prompt_for_user_token('MugBergerFries', 'user-library-read', client_id='0ffe4f5e083f464f8ad6061cd80785ca',
                                   client_secret='e1c15024a0c744a792d729510575a0ca', redirect_uri='http://localhost'
                                                                                                  ':8888/callback')
spotify = spotipy.Spotify()
results = spotify.search(q='artist:' + 'Johari', type='artist')
print(results)
