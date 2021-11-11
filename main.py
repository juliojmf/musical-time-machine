from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Client_ID = "" # your client_id on spotify

Client_Secret = "" # your client_secret on spotify

scope = "playlist-modify-private"

sp = SpotifyOAuth(client_id=Client_ID, client_secret=Client_Secret, redirect_uri="http://example.com", scope=scope)
token = sp.get_access_token(as_dict=False)
client = spotipy.client.Spotify(auth=token)
user_id = client.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

song_list = soup.find_all("span", class_="chart-element__information__song")
song_titles = [song.getText() for song in song_list]

playlist = []

for song_title in song_titles:
    try:
        track_link = client.search(f"track: {song_title} year: {date[0:4]}", limit=1)["tracks"]["items"][0]["external_urls"]["spotify"]
        playlist.append(track_link)
    except:
        pass

playlist_id = client.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)["id"]
client.playlist_add_items(playlist_id=playlist_id, items=playlist)
