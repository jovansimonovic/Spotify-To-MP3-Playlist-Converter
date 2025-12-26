# 🎵 Spotify to MP3 Playlist Converter

Convert any **Spotify playlist** into locally downloaded **MP3 files** using **YouTube** as the audio source.

This tool extracts all song and artist names from a given Spotify playlist, then searches and downloads the corresponding audio using `yt-dlp`. It's lightweight, easy to use, and perfect for backing up playlists for offline listening.

---

## 🚀 Features
- Exports a `.csv` file with song & artist names from any Spotify playlist.
- Searches for matching songs on YouTube.
- Downloads audio using `yt-dlp` in MP3 format.
- Automatically organizes downloads into folders by playlist name.

---

## 📦 Requirements

The following Python libraries are used:

```
pandas==2.3.1
yt-dlp==2025.7.21
spotipy==2.25.1
python-dotenv==1.1.1
youtube-search-python==1.6.6
```

Ensure you are using **Python 3.10+** for full compatibility.

---

## 🛠️ Setup

1. **Clone the repository**

```bash
git clone https://github.com/jovansimonovic/spotify-to-mp3-playlist-converter.git
cd spotify-to-mp3-playlist-converter
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up your Spotify API credentials**

Create a `.env` file in the root directory based on the included `.env.example`:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback/
```

5. **Ensure ffmpeg is available**

This project includes a prepackaged `ffmpeg` folder. If needed, add it to your system PATH or ensure your script uses it directly.

---

## ▶️ Usage

To run the application:

```bash
python main.py
```

### Flow:
1. Enter a Spotify playlist URL.
2. Choose one of the generated `.csv` files to select which songs to download.
3. Songs will be downloaded using YouTube as the source and stored locally.

---

## 📂 Output

- **Exports**: The app generates a `.csv` file listing song titles and artists.
- **Downloads**: MP3 files are saved into the `downloads/` folder, automatically categorized by playlist name.

---

## 👤 Author

GitHub: [jovansimonovic](https://github.com/jovansimonovic)
