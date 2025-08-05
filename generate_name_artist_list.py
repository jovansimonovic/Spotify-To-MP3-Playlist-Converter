import os
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from dotenv import load_dotenv

# loads environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# scope for accessing user playlists
SCOPE = 'playlist-read-private'

# prompts user to enter the playlist URL
playlist_url = input("Enter the URL of the playlist you want to export:\n").strip()
playlist_id = playlist_url.split("/")[-1].split("?")[0]

# auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE))

# fetches playlist name
playlist_info = sp.playlist(playlist_id)
playlist_name = playlist_info['name']

# sanitizes the playlist name for file naming
safe_name = re.sub(r'[\\/*?:"<>|]', "", playlist_name)

# creates "exports" directory if it doesn't exist
export_dir = 'exports'
os.makedirs(export_dir, exist_ok=True)

# fetches songs
songs = []
results = sp.playlist_items(playlist_id, additional_types=['track'])

while results:
    for item in results['items']:
        song = item['track']
        if song:
            songs.append({
               'name': song['name'],
               'artist': ', '.join(artist['name'] for artist in song['artists']),
            })

    results = sp.next(results) if results['next'] else None

# save to CSV
csv_filename = os.path.join(export_dir, f"{safe_name}.csv")
df = pd.DataFrame(songs)
df.to_csv(csv_filename, index=False)

print(f"\n✔️  Exported {len(songs)} songs to {csv_filename}\n")