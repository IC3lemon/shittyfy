# `shittyfy`
Spotify premium is a nono. pls dont diss, a literal toddler is learning scraping, scripting and having fun. \
Mini mini project because im too jobless and wish to eradicate spotify premium, and the need to pay for downloading songs while maintaining a good playlist.
Also my github barren.<br><br>
idk if this legal honestly btw<br>
<img src="https://github.com/user-attachments/assets/4afda5b1-12a8-442e-a44c-757ffcf17e8a" width="50%" height="50%">

***
## WHAT IS THIS SHIT :
basically \
makes use of spotify api (spotipy) to scrape a playlist \
searches the songs on the playlist on youtube \
downloads them from youtube once found, \
and launches a music player for u to enjoy that playlist for free, \
So u get downloading songs, maintaining a playlist, streaming it with ease, pausing, playing, using the slider - \
everything. EVERYTHING THAT SPOTIFY ASKS U TO PAY MONEY FOR

## DEPENDENCIES : 
```
pygame scrapetube python-dotenv spotipy pytube yt-dlp ffmpeg flask
```
***
## INSTRUCTIONS :
- clone this repo
- make a client ID and client secret from <a href="https://developer.spotify.com/dashboard">`here`</a>
- create a "premium playlist" (temporary, aiming to make all playlists a user has available offline automatic). You save songs to this playlist, it becomes available offline because the script(should setup a periodic cronjob for the script).
- generate link for the playlist. u get smth like this `https://open.spotify.com/playlist/REDACTED1?si=REDACTED2`. `REDACTED1` is your playlist ID.
- update the `.env` with the variables `client ID` `client SECRET` `playlist ID` `username`
- run the <a href="https://github.com/IC3lemon/shittyfy/blob/main/main.py">`thing`</a>
- once the script's running with no errors, goto http://127.0.0.1:5000 to access shittyfy fr.
***
## SCREENSHOT(S) :
![image](https://github.com/user-attachments/assets/b74539c1-a949-4233-91b4-fd331f924baf)
***
## TODO's :
- [ ] make shittyfy a true pseudo spotify premium. 
- [ ] make it so that it grabs all playlists from a user. 
- [x] give it a UI when playing songs. *** 
- [ ] lyrics 
- [x] looking up an artist.
- [x] make shit loop 
- [ ] get the godforsaken slider to stop tweaking
- [ ] pausing is tweaking the slider, fix it
