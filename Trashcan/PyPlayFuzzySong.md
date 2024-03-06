
<h1 align="center">
<br>
Play Fuzzy Song
</h1><br>
<br><br>
Searches /media/Music for chosen song and starts playback on your connected speakers.<br><br>
Sadly this one does have room to improve, it does its job, but would prefer to have more fuzz in it, if you got any ideas please dont be a strange...  <br><br><br>
The beuty about doing, whats called an "fuzzy search" like this, is that it allows you to (most likely) call a song name which is not in your native language.<br> 
Even if the STT generates the wrong word, the python script will still point you to the right directory path.<br><br>
Just network mount your music to `/media/Music` and run the py,<br> 
it will take care of the installation process of VLC and modify the binaries so it can be run safely.  

And if you like the song playing, you can just say ["add this to my playlist"](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/PyAddSongToPlaylist.md)   

<br>

_Not sure what to listen to? Take a look at [RandomMusic](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/PyRandomMusic.md)_

<br><br>

- **1: Create the shell commands.** <br>

Create the file 'shell_command.yaml' file in your /config dir and paste in the code below.
This will allow you to call the script easily later.

- **2: Intent Script** <br>

Create the file 'intent_script.yaml' file in the /config dir and fill in the code below.


- **3: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.
In that folder you create a file called `IntentName.yaml` and fill in the code from below. 

- **4: The fuzzy search python script** <br>

This is where the magic happends. <br>
Within your /config dir, create a file called `play_fuzzy_song.py` <br>
Paste in the code at the bottom of this page. <br>

<br>
Your all set, try it out!<br><br>



## **⚠️⚠️ You can get a media player entity ⚠️⚠️** <br>

Settings > Devices & Integrations > VideoLAN > VLC with Telnet  
and fill in your local ip and default port.  
If you did not change the password in the pyscript, the password is `test123`.  


    
<br><br>


## 🦆 /config/shell_command.yaml <br>


<br>


```
  play_fuzzy_song: "python play_fuzzy_song.py '{{ song }}' /media/Music"
```

<br><br>


## 🦆 /config/intent_script.yaml <br>


<br>

```
IntentName:
  action:
    - service: shell_command.play_fuzzy_song
      data: 
        song: "{{song}}"
```

<br><br>


## 🦆 /custon_sentences/sv/PlayArtist.yaml <br>


<br>

```
language: "sv"
intents:
  IntentName:
    data:
      - sentences:
          - "spela upp låten {song}"
lists:
  song:
    wildcard: true   
```

<br><br>



## 🦆 /config/play_fuzzy_song.py <br>


<br>

```
import os
import subprocess
import re
import sys

def clean_search_query(query):

    query = re.sub(r'[.,]', '', query)

    query = query.lower()
    return query

def fuzzy_search(root_dir, query):
    closest_file = None
    min_distance = float('inf')

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)


            distance = abs(len(filename) - len(query))
            if distance < min_distance and query in filename.lower():
                min_distance = distance
                closest_file = file_path

    return closest_file

def play_file(file_path):

    subprocess.run(["pkill", "vlc"])

    subprocess.run(["apk", "add", "vlc"])
    subprocess.run(["sed", "-i", "s/geteuid/getppid/", "/usr/bin/vlc"])

    subprocess.Popen(["cvlc", "add", file_path, "-I", "telnet", "--telnet-password=test123", "--telnet-port=4212", "--alsa-audio-device=hw:1,0"])

def main():
    if len(sys.argv) != 3:
        print("Usage: python play_fuzzy_song.py SEARCH_QUERY /path/to/music")
        sys.exit(1)

    search_query = sys.argv[1]
    root_dir = sys.argv[2]
    search_query = clean_search_query(search_query)
    closest_file = fuzzy_search(root_dir, search_query)
    if closest_file:
        print("Found closest file:", closest_file)
        play_file(closest_file)
    else:
        print("Please try again.")

if __name__ == "__main__":
    main()
```


<br><br>
