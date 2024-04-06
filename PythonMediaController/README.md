
<h1 align="center">
<br>
 
__Python Media Controller__ _v0.2_

<img src="https://raw.githubusercontent.com/pungkula1337anka/Voice-Stuff/main/asset/pythonmedia.png">


</h1><br>

<br><br><br>


# __Full media control in one Python script.__ <br>

__UPDATED__
This script now has __FULL__ video codec support! Play __ANY__ media files! __NO TRANSCODING NEEDED!__

Python Media Controller utilizes the portability of Chromecast and the power of LibVLC to broadcast your local media to your devices.
The difflib module is used to maximize your search potential and to create an "fuzzywuzzy" alike search effect, which can be clearvly used especially when spaking in a language other than your Assist pipeline defaults.
This allows for (most likely) calling an artists name or song title thats not in your native language.
Even if the STT generates the wrong word, the python script will still _(try to)_ point you to the right directory path.<br>
A correction function is also implemented as fallback to ensure as high success rate as possible for your voice commands.
All search results are stored in temporary .m3u files when being sent to your media player to simplify the playback process as much as possible.
The python comes with custom sentence, combined these has every possible command you could ever need to control your TV's or Media boxes.

5 simple steps to control all your media by voice. <br>

<br>

_Example usage:_
```
- "play tvshow family guy"
- "play movie godzilla"
- "play channel 6"
- "play artist the rolling stones"
- "playing song death to all but metal"
- "play music"
- "play youtube funny cats"
- "play podcast self hosted"
- "add this song to my playlist"
[...] and many more.
```
<br>

__Available Media Types:__

1. 🎬 __YouTube__  <br> 
Plays <search_query>'s closeest match on YouTube. <br>
Specify a `remote.*` entity. _(not `media_player.*`)_ <br>
_Requires API key._ <br>

2. 🎙️ __Podcast__  <br>
Fuzzy searches a Podcast directory, lists all files in that directory, orders them after creation date. Sends them to your HA media player for playback.
I use the container based service [Podgrab](https://github.com/akhilrex/podgrab) to automatically download new episodes.  
And this [PythonPodCleanup](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/PythonPodCleanup.md) script to automatically  remove old episodes.  

3. 🔀 __Jukebox__  <br>
Shuffles & randomizes 150 songs from your music directory. <br>
Sends them back to your media player remote for playback. <br>

4. 🎵 __Music__ <br>
Fuzzy searches your music directory for an artist (folder) of your choice. <br>
Lists all files in that folder and creates a temporary playlist which are shuffled and sent back to your HA media players remote entity. <br>

5. 🎵 __Song__  <br>
Fuzzy searches your music directory and all its subdirectories for a song. <br>
The closest matches compared to your search query is stored in order of closest_match ratio. <br>

6. 📽️ __Movie__ <br>
Fuzzy searches for a movie title (folder in your movie directory). <br>
Lists all file inside that folder, order them after filepath name, path gets stored in the temp file sent to remote entity id. <br>

7. 📖 __Audiobook__  <br>
Fuzzy searches your audiobook directory for a folder. <br>
Lists all files in that folder, order them by filepath name and stores in a temporary playlist file casted to your media player.<br>

8. 📹 __OtherVideos__ <br>
Searches for a file in your othervideos directory. <br> 
Just like everything else its processed into a m3u file and sent to a `remote.`

9. 🎵 __Musicvideos__ <br>
Searches your musicvideo directory, for an artist (folder). <br>
list all files, shuffles & randomizes the m3u order before sending for playback. <br>

10. 📺 __TV__ <br>
Searches your TV directory for a TV Show (folder).
Lists all files in that directory and all its subdirectories, shuffles them all and randomizes order. <br>
Sends them all in a .m3u file to your `remote` entity id.

11. 🎼 __Playlist__  <br>
Specify full playlist filepath in search query. _(or define default playlist)_ <br>

12. 🎼 __Add__  <br>
Add currently playing song to your default playlist. <br>


13. 🗞️ __News__ <br>
Define your newscasts RESTful API's in the Python file. <br>
If the newscast items has not been heard before, they will be played. _(if played before, they are skipped)_ <br>
The script stores some data about played items in a .txt file in your config directory, <br>
dont worry though, the Python wont let it get big and grow strong. <br>

14. 📡 __Live-TV__ <br>
Edit your `.m3u` file and split your channels into separate `.m3u` files. <br>
Name each file by channel word you want to use and place it inside the directory `/config/www/live/` <br>

 
<br> 

__Additional Media Player Commands:__

__Volume Control__  <br> 
Increase/Decrease volume by saying `up` or `down`.<br>

__Next Track/Episode__  <br> 
Simply say `Next`.<br>

__Previous Track/Episode__  <br> 
`Previous` is the word. <br>

<br>


## 🦆 __getting started__ <br>


- **1: Download the files** <br>
Add the content of the files into your already existing files.<br>
Make sure they are in the correct path.

- **2: Reverse Proxy Media Directory** <br>
Running Chromecast like this requires TLS HTTPS and a domain. <br>
If you are running Home Assistant OS and are not familiar with these kinds of network setups, I would reccomend <br>
network mounting your media to `/media`. <br>
And downloading the `Caddy 2` Reverse Proxy addon. [Repo URL]() <br>
Register a couple duckdns domains and grab your API Key. <br>
Place the files`caddy` and `Caddyfile` in your /share/caddy directory. <br>
Define your `IP` and `duckdns domains` and `API key` in the `Caddyfile`. <br>
Use the DuckDNS addon to dynamically update your IP to duckdns. <br>
Congratulations, after restarting the addons your reverse proxy should be up and running. <br>

- **3: Custom Sentences** <br>
If you want to edit and use your own sentences you edit the `MediaController.yaml` file. <br>

- **4: Python Script** <br>
Edit the top section in `media_controller.py` to unlock all available features. <br>

YouTube API Key can be created [here](https://developers.google.com/youtube/registering_an_application). You probably need to connect the key to a project aswell. <br>

Dont forget to define your stuff _and .........._ <br>

__yay__ <br>
  - 🎉 _congratulations! 🎉 you can now control_ <br>
    - _your media like a pro voice ninja!_  <br>
<br><br>



<br>


<br><br>


<h1 align="center">
<br>
 
 __🎈 enjoy 🎈__ 

</h1><br><br>
