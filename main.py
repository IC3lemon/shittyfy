import spotipy
import os
import yt_dlp
import scrapetube
import random
import pygame
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from dotenv import load_dotenv
from typing import Final
from playsound import playsound
from tqdm import *

# create a folder to scrape from -> https://open.spotify.com/playlist/######################?si=REDACTED
# the hashed stuff is the playlist ID

# get clientID and clientSECRET from here -> https://developer.spotify.com/dashboard

load_dotenv()
CLIENT_ID: Final[str] = os.getenv('CLIENT_ID')
SECRET: Final[str] = os.getenv('CLIENT_SECRET')
USER: Final[str] = os.getenv('USERNAME')
PLAYLIST: Final[str] = os.getenv('PLAYLIST_ID')
folder_path = './songs'

class FileAlreadyDownloaded(Exception):
    "This song has already been downloaded"
    pass

# function extracted from : https://gist.github.com/JGarrechtMetzger/21b04767a2b5624dca2629ae8d894355
# parses and returns track metadata from spotify track ID
def parse_track(track_id):
    track_info = sp.track(track_id)
    track_id = track_info['id'] 
    track_name = track_info['name']
    track_length = track_info['duration_ms']
    track_preview_url = track_info['preview_url']
    track_number = track_info['track_number']
    track_href = track_info['href']
    track_external_urls = track_info['external_urls']['spotify']
    track_external_id_isrc = track_info['external_ids']['isrc']
    album_id = track_info['album']['id']
    album_name = track_info['album']['name']
    album_href = track_info['album']['href']
    album_ext_url = track_info['album']['external_urls']['spotify']
    album_release_date = track_info['album']['release_date']
    album_release_date_precision = track_info['album']['release_date_precision']
    album_total_tracks = track_info['album']['total_tracks']
    album_type = track_info['album']['type']
    album_image_large = track_info['album']['images'][0]['url']
    album_image_medium = track_info['album']['images'][1]['url']
    album_image_small = track_info['album']['images'][2]['url']
    artist_id = track_info['album']['artists'][0]['id']
    artist_name = track_info['album']['artists'][0]['name']
    artist_href = track_info['album']['artists'][0]['href']
    artists_ext_url = track_info['album']['artists'][0]['external_urls']['spotify']
    track_data = [track_id, track_name, track_length, album_id, album_name,
                  artist_id, artist_name, track_preview_url,
                  track_number, track_href, track_external_urls,
                  track_external_id_isrc, album_href, album_ext_url,
                  album_release_date, album_release_date_precision,
                  album_total_tracks, album_type, album_image_large,
                  album_image_medium, album_image_small, artist_href,
                  artists_ext_url]
    
    return track_data

# creates a Spotify object 
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def scrape_playlist():
    all_tracks = get_playlist_tracks(USER,PLAYLIST)
    track_ids = []
    track_count=0
    for i in tqdm(all_tracks, desc="scraping tracks", unit="tracks"):
        track_ids.append(i['track']['id'])
        track_count += 1
    print("\n----------------------------- SONGS -----------------------------")
    for i in range(len(track_ids)):
        print(i+1,'.', parse_track(track_ids[i])[1])
    print("\n-----------------------------------------------------------------")
    return track_ids

def ytsearch(name):
    videos = scrapetube.get_search(name)
    for video in videos:
        videoId = video['videoId']
        yt = YouTube('http://youtube.com/watch?v='+videoId)
        vidinfo = yt.vid_info
        length = vidinfo['videoDetails']['lengthSeconds']
        title = vidinfo['videoDetails']['title']
        artist = vidinfo['videoDetails']['author']

        return videoId, [vidinfo, title, length, artist]

def download(videoId,video_name):
    print(f"[ # ] Downloading {video_name} ...")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    output_template = os.path.join(folder_path, f"{video_name}.mp3")
    try:
        if os.path.exists(output_template):
            raise FileAlreadyDownloaded
    except FileAlreadyDownloaded:
        print("[ # ] song already downloaded...")
        return 

    ydl_opts = {
        'format': 'bestaudio/best',  # Choose best available audio
        'outtmpl': output_template,  # Save as the specified name in the folder
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Set audio quality
        }],
        'quiet': True,  # Suppress detailed output
        'noplaylist': True,  # Only download single video if the URL is a playlist
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['http://youtube.com/watch?v='+videoId])
        print(f"[ # ] Audio downloaded and saved to {output_template}")
    except Exception as e:
        print(f"[ # ] Error downloading video: {e}")

TRACKS = scrape_playlist()
print("Going through your playlist...")

for i in TRACKS:
    track = parse_track(i)
    track_name = track[1]
    track_length = track[2]
    track_artist = track[6]
    
    output_template = os.path.join(folder_path, f"{track_name}.mp3")
    if os.path.exists(output_template):
        continue
    
    print(f"ooh new song {track_name}, installing...")
    videoId, vid = ytsearch(track_name)
    vid_name = vid[1]
    vid_length = vid[2]
    vid_artist = vid[3]
    
    if((track_name in vid_name) and (track_artist in vid_artist)):
        print(f"{track_name} FOUND ON YOUTUBE")
        download(videoId, track_name)
    else:
        print(f"{track_name} not found on yt...")

print("\nPLAYLIST UP TO DATE!")
print("shuffling & playing ... ")

songs = []
for file in os.listdir(folder_path):
    songs.append(file)

def play_mp3_files(mp3_files, folder_path, looping):
    # Initialize pygame mixer
    pygame.mixer.init()
    
    if looping:
        while looping:
        # Play each mp3 file in the list
            for file_name in mp3_files:
                file_path = os.path.join(folder_path, file_name)
                print(f"Now playing: {file_name}")
                
                # Load and play the mp3 file
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                
                # Wait for the song to finish
                while pygame.mixer.music.get_busy():
                    continue  # Loop while the song is playing
    else:
          for file_name in mp3_files:
                file_path = os.path.join(folder_path, file_name)
                print(f"Now playing: {file_name}")
                
                # Load and play the mp3 file
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                
                # Wait for the song to finish
                while pygame.mixer.music.get_busy():
                    continue  # Loop while the song is playing
    # Quit pygame mixer after all songs are played
    pygame.mixer.quit()

play_mp3_files(songs, folder_path, looping=True)
