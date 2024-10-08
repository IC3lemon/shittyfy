# `shittyfy`
Spotify premium is a nono. pls dont diss, a literal script baby is learning scraping, scripting and having fun.
Made this because im too jobless and wish to eradicate spotify premium, and the need to pay for downloading songs while maintaining a good playlist.
***
## dependencies : 
`pygame``scrapetube``python-dotenv``spotipy``pytube``yt-dlp``ffmpeg`
***
## Instructions :
- clone this repo
- make a client ID and client secret from <a href="https://developer.spotify.com/dashboard">`here`</a>
- create a "premium playlist" (temporary, aiming to make all playlists a user has available offline automatic). You save songs to this playlist, it becomes available offline because the script(should setup a periodic cronjob for the script).
- generate link for the playlist. u get smth like this `https://open.spotify.com/playlist/REDACTED1?si=REDACTED2`. `REDACTED1` is your playlist ID.
- update the `.env` with the variables `client ID` `client SECRET` `playlist ID` `username`
- run the thing
***
