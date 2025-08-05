import os
import re
import pandas as pd
from youtubesearchpython import VideosSearch
import yt_dlp

# loads all CSV exports
export_folder = 'exports'
exports = [f for f in os.listdir(export_folder) if f.endswith('.csv')]

if not exports:
    print("No CSV exports found in the 'exports' folder.")
    exit(1)

# displays available playlists
print("🎵 Available playlists:")
for i, file in enumerate(exports, 1):
    playlist_name = os.path.splitext(file)[0]
    print(f"{i}. {playlist_name}")

# prompts user to select a playlist to download
while True:
    try:
        choice = int(input("\nEnter the number of the playlist you want to download:\n"))

        if 1 <= choice <= len(exports):
            selected_file = exports[choice - 1]
            csv_file = os.path.join(export_folder, exports[choice - 1])
            playlist_name = os.path.splitext(selected_file)[0]
            break
        else:
            print("⚠️  Invalid number. Try again.")
    except ValueError:
        print("⚠️  You must enter a number.")

print(f"\n⏳ Downloading songs from {playlist_name}...\n")

# creates "dowloads" directory if it doesn't exist
output_folder = os.path.join('downloads', playlist_name)
os.makedirs(output_folder, exist_ok=True)

# normalizes song names
def normalize(name):
    return name.strip().lower().replace('  ', ' ').replace(':', '').replace('"', '').replace('?', '')

# loads already downloaded songs from the "downloads" folder
already_downloaded = set()

for filename in os.listdir(output_folder):
    if filename.endswith('.mp3'):
        base_name = os.path.splitext(filename)[0]
        normalized_title = normalize(base_name)
        already_downloaded.add(normalized_title)

# loads CSV with song names and artists
df = pd.read_csv(csv_file)

# logging variables
skipped = []
failed = []
successful = 0

# downloads MP3s
for index, row in enumerate(df.itertuples(), start=1):
    song = row.name.strip()
    artist = row.artist.strip()
    query = f"{song} {artist}"
    filename_base = f"{artist} - {song}"
    normalized_filename = normalize(filename_base)

    if normalized_filename in already_downloaded:
        print(f"⏭️  {filename_base} is already downloaded. Skipping...")
        skipped.append(filename_base)
        continue

    try:
        search = VideosSearch(query, limit=1)
        result = search.result()

        if not result['result']:
            print(f"{index}. ❌ No results found for: {query}")
            failed.append(filename_base)
            continue
        
        video = result['result'][0]
        video_url = video['link']

        print(f"{index}. Downloading: {filename_base} from {video_url}")

        # sets output template for current song
        output_template = os.path.join(output_folder, f'{filename_base}.%(ext)s')
        
        #yt-dlp configuration
        ydl_config = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'ffmpeg_location': os.path.join(os.getcwd(), 'ffmpeg', 'bin'),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
            'quiet': False,
            'nonplaylist': True,
            'nocheckcertificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_config) as ydl:
            ydl.download([video_url])
            print(f"✔️  Downloaded: {filename_base}")

        already_downloaded.add(normalized_filename)
        successful += 1
    except Exception as e:
        print(f"❌ Error downloading {filename_base}: {e}")
        failed.append(filename_base)

# deletes any leftover .webm files
for file in os.listdir(output_folder):
    if file.endswith('.webm'):
        try:
            os.remove(os.path.join(output_folder, file))
        except Exception as e:
            print(f"❌ Could not delete {file}: {e}")

# download summary
print("\n--- Download Summary ---")
print(f"Total downloads successful: {successful}")
print(f"Total downloads skipped: {len(skipped)}")
print(f"Total downloads failed: {len(failed)}")

if len(skipped) == len(df):
    print("\n✔️  All songs already downloaded")

if failed:
    print("\n❌ Failed downloads:")
    for song in failed:
        print(f"- {song}")