
<h1 align="center">
<br>
Play Fuzzy Artist
</h1><br>
<br><br>
Searches /media/Music for chosen artist and creates an temporary playlist, starts playback on your connected speakers, after it shuffles all the songs in the playlist.<br><br>
The beuty about doing, whats called an "fuzzy search" like this, is that it allows you to (most likely) call an artists name which are not in your native language.<br> 
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
In that folder you create a file called `PlayArtist.yaml` and fill in the code from below. 

- **4: The fuzzy search python script** <br>

This is where the magic happends. <br>
Within your /config dir, create a file called `play_fuzzy_artist.py` <br>
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
  play_fuzzy_artist: "python play_fuzzy_artist.py '{{ artist }}' /media/Music"
```

<br><br>


## 🦆 /config/intent_script.yaml <br>


<br>

```
PlayArtist:
  action:
    - service: shell_command.play_fuzzy_artist
      data: 
        artist: "{{band}}"
```

<br><br>


## 🦆 /custon_sentences/sv/PlayArtist.yaml <br>


<br>

```
language: "sv"
intents:
  PlayArtist:
    data:
      - sentences:
          - "spela upp (gruppen|bandet|artisten) {band}"
lists:
  band:
    wildcard: true   
```

<br><br>



## 🦆 /config/play_fuzzy_artist.py <br>


<br>

```
import os
import sys
import subprocess
import random
from difflib import get_close_matches

def clean_search_query(query):
    cleaned_query = query.replace('.', '').replace(',', '')
    return cleaned_query

def find_closest_directory(query, directory):
    directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    closest_match = get_close_matches(query, directories, n=1)
    if closest_match:
        closest_dir = os.path.join(directory, closest_match[0])
        if not closest_dir.endswith('/'):
            closest_dir += '/'
        return closest_dir
    else:
        return None

def collect_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

if __name__ == "__main__":

    subprocess.run(["pkill", "vlc"])

    vlc_install_command = "apk add vlc && sed -i 's/geteuid/getppid/' /usr/bin/vlc"
    subprocess.run(vlc_install_command, shell=True)
    
    if len(sys.argv) != 3:
        print("Usage: python script.py <search_query> <directory>")
        sys.exit(1)

    search_query = sys.argv[1]
    directory = sys.argv[2]

    cleaned_search_query = clean_search_query(search_query)

    closest_directory = find_closest_directory(cleaned_search_query, directory)
    if closest_directory:
        files = collect_files(closest_directory)
        random.shuffle(files)

        temp_playlist_file = "/tmp/shuffled_playlist.m3u"
        with open(temp_playlist_file, 'w') as f:
            for file in files:
                f.write(file + '\n')
        
        # YOU PROBABLY WANT TO CHANGE THE PASSWORD!!
        command = "cvlc -I telnet --telnet-password=test123 --telnet-port=4212 --alsa-audio-device=hw:1,0 --playlist-enqueue '{}' &".format(temp_playlist_file)
        
        print("Executing command:", command)

        subprocess.run(command, shell=True)
    else:
        print("No closest match found.")
```


<br><br>
