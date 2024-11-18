from functions import *
import tkinter as tk
import subprocess
import time

# create a folder to scrape from -> https://open.spotify.com/playlist/######################?si=REDACTED
# the hashed stuff is the playlist ID

# get clientID and clientSECRET from here -> https://developer.spotify.com/dashboard

load_dotenv()
CLIENT_ID: Final[str] = os.getenv('CLIENT_ID')
SECRET: Final[str] = os.getenv('CLIENT_SECRET')
USER: Final[str] = os.getenv('USERNAME')
PLAYLIST: Final[str] = os.getenv('PLAYLIST_ID')

# creates a Spotify object 
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def start_flask_app():
    print("Starting Flask app...")
    # Start `app.py` as a subprocess
    subprocess.Popen(
        ["python", "app.py"],  # Command to run app.py
        cwd=os.path.dirname(os.path.abspath(__file__)),  # Ensure the correct working directory
    )
    time.sleep(2)

TRACKS = scrape_playlist(sp, USER, PLAYLIST)
print("Going through your playlist...")

downloaded = 0
for i in TRACKS:
    track = parse_track(sp, i)
    track_name = track[1]
    track_length = track[2]
    track_artist = track[6]
    
    search = scrapetube.get_search(f"{track_name} by {track_artist} song")
    for vid in search:
        vidid = vid['videoId']
        spotify_time = convert_ms(track_length)
        youtube_time = vid['lengthText']['simpleText']
        difference = time_difference(spotify_time, youtube_time)

        if(difference <= 10):
            output_template = os.path.join(folder_path, f"/{track_name}.mp3")
            download_song(output_template, vidid)
            downloaded+= 1
        else:
            print(f"{track_name} SONG NOT DOWNLOADED.\nFOUND LINK : https://www.youtube.com/watch?v={vidid}\nTIME DIFFERENCE : {difference}\n{spotify_time} {youtube_time}")
        break

print(f"\n{downloaded}/{len(TRACKS)} songs succesfully saved")
songs = get_songs()
print("SAVED SONGS : ", songs)

start_flask_app()