from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
print('''
                    ███╗   ███╗██╗   ██╗███████╗██╗ ██████╗ █████╗ ██╗                     
                    ████╗ ████║██║   ██║██╔════╝██║██╔════╝██╔══██╗██║                     
                    ██╔████╔██║██║   ██║███████╗██║██║     ███████║██║                     
                    ██║╚██╔╝██║██║   ██║╚════██║██║██║     ██╔══██║██║                     
                    ██║ ╚═╝ ██║╚██████╔╝███████║██║╚██████╗██║  ██║███████╗                
                    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝                
                                                                                           
████████╗██╗███╗   ███╗███████╗    ███╗   ███╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗███████╗
╚══██╔══╝██║████╗ ████║██╔════╝    ████╗ ████║██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝
   ██║   ██║██╔████╔██║█████╗      ██╔████╔██║███████║██║     ███████║██║██╔██╗ ██║█████╗  
   ██║   ██║██║╚██╔╝██║██╔══╝      ██║╚██╔╝██║██╔══██║██║     ██╔══██║██║██║╚██╗██║██╔══╝  
   ██║   ██║██║ ╚═╝ ██║███████╗    ██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║██║██║ ╚████║███████╗
   ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝
                                                                                           
''')

url="https://www.billboard.com/charts/hot-100/"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/callback/",
        client_id="Enter here your spotify client id"
        client_secret="Enter here your client_secret",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

date=input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
new_url=f"{url}/{date}/"

reposense=requests.get(new_url)
billboard_web=reposense.text

soup=BeautifulSoup(billboard_web,"html.parser")

track_titles = soup.select("li ul li h3")
song_names = [track.getText().replace("\n", "").replace("\t", "") for track in track_titles]

song_uris = []
year = date.split("-")[0]


for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# print(f"this is found\n{song_uris}")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)