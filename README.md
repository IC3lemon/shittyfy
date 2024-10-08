# `shittyfy`
Spotify premium is a nono. pls dont diss, a literal toddler is learning scraping, scripting and having fun. \
Mini mini project because im too jobless and wish to eradicate spotify premium, and the need to pay for downloading songs while maintaining a good playlist.
Also my github barren.<br><br>idk if this legal honestly btw
***
## DEPENDENCIES : 
```
pygame scrapetube python-dotenv spotipy pytube yt-dlp ffmpeg
```
***
## INSTRUCTIONS :
- clone this repo
- make a client ID and client secret from <a href="https://developer.spotify.com/dashboard">`here`</a>
- create a "premium playlist" (temporary, aiming to make all playlists a user has available offline automatic). You save songs to this playlist, it becomes available offline because the script(should setup a periodic cronjob for the script).
- generate link for the playlist. u get smth like this `https://open.spotify.com/playlist/REDACTED1?si=REDACTED2`. `REDACTED1` is your playlist ID.
- update the `.env` with the variables `client ID` `client SECRET` `playlist ID` `username`
- run the <a href="https://github.com/IC3lemon/shittyfy/blob/main/main.py">`thing`</a>
***
## TODO's :
- [ ] make shittyfy a true pseudo spotify premium. 
- [ ] make it so that it grabs all playlists from a user. 
- [ ] give it a UI when playing songs. *** 
- [ ] lyrics 
- [ ] looking up an artist.
- [x] make shit loop
