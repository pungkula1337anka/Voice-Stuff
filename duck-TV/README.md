
<h1 align="center">
<br>
 

<img src="https://github.com/pungkula1337anka/Voice-Stuff/blob/main/asset/ducktv6.jpeg?raw=true" width="350" height="350"  />

</h1><br>

</h1><br>

<br><br>

<img src="https://github.com/pungkula1337anka/Voice-Stuff/blob/main/asset/banner-dark.png?raw=true" width="300" height="150"  />

<br>

# __What is 🦆 duck-TV? 📺__

duck-TV is a super easy way to power-up your Chromecast and give it voice controlling capabilities. <br>
The duck-TV script can be used to control all kinds of media! <br> <br>
<br>

__2 quick and simple steps to control all your media by voice.__ <br>

<br>

🦆 Quack and play, no delay, <br>
🗑️ Clicks and taps? A thing of the past, <br>
🎙 Just speak up, and have a blast! <br>

<br><br>


# __Full media control in one Python script.__ <br>

<br>
duck-TV Voice Controller utilizes the portability of Chromecast and the power of LibVLC to broadcast your local media to your devices. <br>
The difflib module is used to maximize your search potential and to create an __lightning fast__ "fuzzywuzzy" alike search effect, which can be clearvly used
especially when spaking in a language other than your Assist pipeline defaults. <br>
This allows for calling an artists name or song title thats not in your native language. <br>
Even if the STT generates the wrong word, the python script will still _(try to)_ point you to the right directory path.<br>
A correction function is also implemented as fallback to ensure as high success rate as possible for your voice commands. <br>
All search results are stored in temporary .m3u files when being sent to your media player to simplify the playback process as much as possible. <br><br>
The script comes with custom sentence, combined these has every possible command you could ever think off, when controlling your TV's or Media boxes. <br>
<br>
Upon first usage, you will prompted for your samba password. This will only happen once.<br>


<br>

_Example usage:_
```
- "play tvshow family guy"
- "play movie godzilla"
- "play channel 6"
- "play artist the rolling stones"
- "play song death to all but metal"
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
Simply define your Live-TV http URLs in the python file. <br>
You can then call a channel by saying `play channel 5`. <br>

 
<br> 

__Additional Media Player Commands:__

__Volume Control__  <br> 
Increase/Decrease volume by saying `up` or `down`.<br>

__Next Track/Episode__  <br> 
Simply say `Next`.<br>

__Previous Track/Episode__  <br> 
`Previous` is the word. <br>

__Power On/Off your TV__  <br> 
Turn on/off your TV's & media box by saying `on` or `off`.<br>

<br>


## 🦆 __getting started__ <br>


- **1: Download the files** <br>
Download and the files in this repo to your `/config` directory. <br>
If the files already exist in your /config directory, simply add the content of the files and save.<br>

- **2: Python Script** <br>
Edit the top section in `media_controller.py` to unlock all available features. <br>
YouTube API Key can be created [here](https://developers.google.com/youtube/registering_an_application). You probably need to connect the key to a project aswell. <br>

- **OPTIONAL: Custom Sentences** <br>
If your language is not included in the `/custom_sentences` directory, simply create a folder with your language code and copy the yaml file and edit it to your preferences. <br>

- **OPTIONAL BONUS: Continued Conversation** <br>
If you want the Voice Assistant to automatically start upon failed intent (not having to say the wake word again) add the code below to your ESP devices yaml. <br>

```
api:
# -> CREATES SERVICE CALL <- #  
  services:
    - service: wait_and_start_va
      then:
        - script.execute: wait_and_start_va

script:
# -> WAIT AND START VA <- #  
  - id: wait_and_start_va
    then:
      - delay: 10s 
      - switch.turn_off: use_wake_word
      - wait_until:
          not:
            voice_assistant.is_running:
      - delay: 100ms
      - voice_assistant.start:
      - delay: 250ms  
      - wait_until:
          not:
            voice_assistant.is_running:
      - switch.turn_on: use_wake_word

switch:
# -> USE WAKE WORD <- #
  - platform: template
    name: Use wake word
    id: use_wake_word
    optimistic: true
    restore_mode: RESTORE_DEFAULT_OFF
    entity_category: config
    on_turn_on:
      - lambda: id(va).set_use_wake_word(true);
      - if:
          condition:
            not:
              - voice_assistant.is_running
          then:
            - voice_assistant.start_continuous
    on_turn_off:
      - voice_assistant.stop
      - lambda: id(va).set_use_wake_word(false);
```

__yay__ <br>
  - 🎉 _congratulations! 🎉 you can now control_ <br>
    - _your media like a pro voice ninja!_  <br>
<br><br>



<br>


<br><br>


<h1 align="center">
<br>
 
 __🎈 enjoy 🎈__ 

</h1><br><br><br><br>

<img src="https://github.com/pungkula1337anka/Voice-Stuff/blob/main/asset/ducktv.png?raw=true" width="250" height="250"  />


# __Troubleshooting__

Make sure you rebooted your Home Assistant after installing everything.

Make sure you have Samba (SMB) on your HA instance. There is an official Addon you can use. <br>

Make sure you have the Android TV Remote integration installed and properly configurated on your HA instance. <br> 

Make sure you have defined everything in the top section of the python file correctly. <br> 

For best performance, I recommend having the VLC app installed on your TV/Android box. <br>

Still having issues? Go to Developer Tools > Services abd try sending a service call to start a movie: <br>

```
service: shell_command.media_controller
data: 
  search: MOVIE_TITLE_HERE
  typ: movie
  player: remote.YOUR_REMOTE
```
<br>
Make sure you have the movie your searching for in a folder in the directory you defined in the `media_controller.py` file.  <br>

If the service call is successful, there problem is probably in the custom sentence file, try adjusting it. <br>
<br>
<br>

__Still having problems? Feel free to create an issue here or contact me-__ 

<br><br>
