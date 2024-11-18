import spotipy
import os
import random
import pygame
import scrapetube
import yt_dlp
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from typing import Final
from tqdm import *

folder_path = './songs'
class FileAlreadyDownloaded(Exception):
    "This song has already been downloaded"
    pass

# function extracted from : https://gist.github.com/JGarrechtMetzger/21b04767a2b5624dca2629ae8d894355
# parses and returns track metadata from spotify track ID
def parse_track(sp, track_id):
    track_info = sp.track(track_id)
    track_id = track_info['id'] 
    track_name = track_info['name']
    track_length = track_info['duration_ms']
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
                  artist_id, artist_name, 
                  track_number, track_href, track_external_urls,
                  track_external_id_isrc, album_href, album_ext_url,
                  album_release_date, album_release_date_precision,
                  album_total_tracks, album_type, album_image_large,
                  album_image_medium, album_image_small, artist_href,
                  artists_ext_url]
    
    return track_data

def get_playlist_tracks(sp, username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def scrape_playlist(sp, USER, PLAYLIST):
    all_tracks = get_playlist_tracks(sp, USER,PLAYLIST)
    track_ids = []
    track_count=0
    for i in tqdm(all_tracks, desc="scraping tracks", unit="tracks"):
        track_ids.append(i['track']['id'])
        track_count += 1
    print("\n----------------------------- SONGS -----------------------------")
    for i in range(len(track_ids)):
        print(i+1,'.', parse_track(sp, track_ids[i])[1])
    print("\n-----------------------------------------------------------------")
    return track_ids

def download_song(output_template, videoId):
    output_template = folder_path + output_template[:-4]
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    try:
        if os.path.exists(output_template + ".mp3") or os.path.exists(output_template + "#.mp3"):
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

def convert_ms(milliseconds):
    seconds = int(milliseconds) / 1000
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    
    return f"{minutes}:{remaining_seconds:02d}"

def time_difference(time1, time2):
    # Convert each time to seconds
    def to_seconds(time_str):
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    
    seconds1 = to_seconds(time1)
    seconds2 = to_seconds(time2)
    
    return abs(seconds2 - seconds1)

def get_songs():
    songs = []
    for file in os.listdir(folder_path):
        songs.append(file)
    if songs :
        return songs
    return None

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