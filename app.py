from flask import Flask, jsonify, request, send_from_directory, redirect, url_for
from flask_cors import CORS
import os
import pygame
import threading
import signal
import sys
import time

app = Flask(__name__)
CORS(app)

# Initialize pygame mixer
pygame.mixer.init()

# Globals
folder_path = "./songs"
songs = []
current_index = 0
current_time = 0
song_length = 0
is_looping = False
playback_active = True

def song_finished_callback():
    """Callback function when a song finishes playing"""
    if is_looping:
        # Replay the current song
        pygame.mixer.music.play()
    else:
        # Play next song
        next_song(auto=True)

# Background thread to monitor playback and handle song completion
def monitor_playback():
    global current_time, playback_active
    last_pos = 0
    while playback_active:
        time.sleep(0.1)  # Check every 100ms
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000
            last_pos = current_time
        else:
            # If music isn't playing and we were previously playing (last_pos > 0),
            # then the song has finished
            if last_pos > 0:
                last_pos = 0
                song_finished_callback()

# Start monitoring thread
def start_monitor():
    threading.Thread(target=monitor_playback, daemon=True).start()

start_monitor()

# Graceful shutdown handler
def shutdown_handler(sig, frame):
    global playback_active
    print("Shutting down gracefully...")
    playback_active = False
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'image.png', mimetype='image/png')

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/load', methods=['GET'])
def load_songs():
    global songs, current_index
    if not os.path.isdir(folder_path):
        return jsonify({"error": "Songs folder not found"}), 404

    songs = [f for f in os.listdir(folder_path) if f.endswith(".mp3")]
    if not songs:
        return jsonify({"error": "No songs found in the folder"}), 404

    current_index = 0
    pygame.mixer.music.load(os.path.join(folder_path, songs[current_index]))
    return jsonify({"songs": songs, "current_song": songs[current_index]})

@app.route('/play', methods=['POST'])
def play():
    global song_length
    pygame.mixer.music.play()
    song_length = pygame.mixer.Sound(os.path.join(folder_path, songs[current_index])).get_length()
    return jsonify({"status": "playing"})

@app.route('/pause', methods=['POST'])
def pause():
    pygame.mixer.music.pause()
    return jsonify({"status": "paused"})

@app.route('/unpause', methods=['POST'])
def unpause():
    pygame.mixer.music.unpause()
    return jsonify({"status": "unpaused"})

@app.route('/next', methods=['POST'])
def next_song(auto=False):
    global current_index, song_length
    if songs:
        current_index = (current_index + 1) % len(songs)
        pygame.mixer.music.load(os.path.join(folder_path, songs[current_index]))
        pygame.mixer.music.play()
        song_length = pygame.mixer.Sound(os.path.join(folder_path, songs[current_index])).get_length()
    return jsonify({"current_song": songs[current_index]})

@app.route('/previous', methods=['POST'])
def previous_song():
    global current_index, song_length
    if songs:
        current_index = (current_index - 1) % len(songs)
        pygame.mixer.music.load(os.path.join(folder_path, songs[current_index]))
        pygame.mixer.music.play()
        song_length = pygame.mixer.Sound(os.path.join(folder_path, songs[current_index])).get_length()
    return jsonify({"current_song": songs[current_index]})

@app.route('/set_position', methods=['POST'])
def set_position():
    position = request.json.get("position", 0)
    pygame.mixer.music.play(start=position)
    return jsonify({"status": "position set", "position": position})

@app.route('/toggle_loop', methods=['POST'])
def toggle_loop():
    global is_looping
    is_looping = request.json.get("loop", False)
    return jsonify({"looping": is_looping})

@app.route('/play_song', methods=['POST'])
def play_song():
    global current_index, song_length
    song_name = request.json.get("song_name")
    if song_name in songs:
        current_index = songs.index(song_name)
        pygame.mixer.music.load(os.path.join(folder_path, song_name))
        pygame.mixer.music.play()
        song_length = pygame.mixer.Sound(os.path.join(folder_path, song_name)).get_length()
        return jsonify({"current_song": song_name})
    return jsonify({"error": "Song not found"}), 404

@app.route('/current_position', methods=['GET'])
def current_position():
    return jsonify({"position": current_time, "length": song_length})

@app.route('/song/<filename>')
def get_song(filename):
    return send_from_directory(folder_path, filename)

if __name__ == '__main__':
    print("Starting Flask server... Press Ctrl+C to exit.")
    app.run(debug=True)