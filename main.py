import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Spotify
SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIFY_USERNAME = os.getenv("USERNAME")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=SPOTIFY_USERNAME,
    )
)
user_id = sp.current_user()["id"]

while True:
    try:
        # Prompt user for travel date
        travel_date = input(
            "Which year would you like to travel to in YYYY-MM-DD format?"
        ).strip()  # Strip leading/trailing spaces

        # Debug the input
        print(f"Debugging Input: '{travel_date}' (Length: {len(travel_date)})")

        # Validate and parse the input
        valid_date = dt.strptime(travel_date, "%Y-%m-%d").date()

        # If valid, break the loop
        print(f"Valid date: {valid_date}")
        break

    except ValueError as e:
        # Debug exception
        print(f"Error: {e}")
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
}

# "https://www.billboard.com/charts/hot-100/2000-08-12"
URL = f"https://www.billboard.com/charts/hot-100/{valid_date}/"

print(URL)

response = requests.get(url=URL, headers=header)
# print(response)
billboard = response.text
# print(billboard)
soup = BeautifulSoup(billboard, "html.parser")

with open(
    "python_practice_music_playlist/01_billboard.html",
    "w",
    encoding="utf-8",
) as file:
    file.write(soup.prettify())  # Prettify formats the HTML nicely

# name of h3 and class of c-title
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

with open(
    "python_practice_music_playlist/02_song_names.txt",
    "w",
) as file:
    for name in song_names:
        file.write(name + "\n")

song_uris = []
print(f"check year of valid_date: {valid_date}")
year = valid_date.year
print(year)

userID = sp.current_user()["id"]
print(userID)

spotify_uri_list = []
for song in song_names:
    spotify_result = sp.search(q=f"track:{song} year:{year}", type="track")
    for result_num in range(0, len(spotify_result)):
        try:
            if spotify_result["tracks"]["items"][result_num]["name"] == song:
                spotify_uri_list.append(
                    spotify_result["tracks"]["items"][result_num]["uri"]
                )
                with open(
                    "python_practice_music_playlist/03_spotify_result.txt",
                    "w",
                ) as file:
                    file.write(f"{spotify_result} \n")
                with open(
                    "python_practice_music_playlist/04_spotify_uri_list.txt",
                    "w",
                ) as file:
                    file.write(f"{spotify_uri_list} \n")
        except IndexError:
            print("{song} not found")
print(spotify_uri_list)

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(
    user=user_id, name=f"{valid_date} Billboard 100", public=False
)
print(playlist)
with open(
    "python_practice_music_playlist/05_playlist.txt",
    "w",
) as file:
    file.write(f"{playlist} \n")

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=spotify_uri_list)
