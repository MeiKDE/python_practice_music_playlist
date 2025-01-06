# Spotify Playlist Generator

This project generates a Spotify playlist based on the Billboard Hot 100 chart for a user-specified date. It scrapes the Billboard website for song names, matches them with Spotify tracks, and creates a private playlist.

## Features
- Fetches the Billboard Hot 100 chart for a specific date.
- Extracts song names using web scraping with BeautifulSoup.
- Searches for corresponding Spotify tracks using the Spotify API.
- Creates a private playlist in the user's Spotify account and adds the matched songs.

## Prerequisites

### 1. Environment Variables
Ensure the following environment variables are set:
- **CLIENT_ID**: Your Spotify API client ID.
- **CLIENT_SECRET**: Your Spotify API client secret.
- **USERNAME**: Your Spotify username.

Set these variables in your shell configuration file (e.g., `~/.zshrc`, `~/.bashrc`) or a `.env` file if you are using `python-dotenv`.

### 2. Install Required Libraries
Install the necessary Python libraries:

```bash
pip install requests beautifulsoup4 spotipy
```

## How It Works

### Step 1: Prompt User for Date
The script prompts the user to input a date in `YYYY-MM-DD` format and validates the input:
```python
travel_date = input("Which year would you like to travel to in YYYY-MM-DD format?")
```

### Step 2: Scrape Billboard Hot 100
Using `requests` and `BeautifulSoup`, the script fetches the Billboard Hot 100 chart for the specified date:
```python
URL = f"https://www.billboard.com/charts/hot-100/{valid_date}/"
soup = BeautifulSoup(billboard, "html.parser")
song_names = [song.getText().strip() for song in soup.select("li ul li h3")]
```

### Step 3: Match Songs on Spotify
The script uses the Spotify API to search for songs by name and year:
```python
spotify_result = sp.search(q=f"track:{song} year:{year}", type="track")
spotify_uri_list.append(spotify_result["tracks"]["items"][0]["uri"])
```

### Step 4: Create Spotify Playlist
Creates a private playlist and adds the matched songs:
```python
playlist = sp.user_playlist_create(
    user=user_id, name=f"{valid_date} Billboard 100", public=False
)
sp.playlist_add_items(playlist_id=playlist["id"], items=spotify_uri_list)
```

### Step 5: Save Results
The script saves intermediate results and outputs to text files for debugging and logging purposes:
- `01_billboard.html`: Raw HTML of the Billboard page.
- `02_song_names.txt`: Extracted song names.
- `03_spotify_result.txt`: Spotify search results.
- `04_spotify_uri_list.txt`: List of Spotify track URIs.
- `05_playlist.txt`: Details of the created playlist.