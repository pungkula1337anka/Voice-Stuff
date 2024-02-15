
<h1 align="center">
<br>
Play Artist
</h1><br>
<br><br>
Searches /media/Music for chosen artist and plays the entire folder through your connected speakers.<br><br>
The beuty about doing, whats called an "fuzzy search" like this, is that it allows you to (most likely) call an artists name which are not in your native language.<br> 
Even if the STT generates the wrong word, the python script will still point you to the right directory path.<br><br>
Just network mount your music to your instance and run the py,<br> 
it will take care of the installation process of VLC and modify the binaries so it can be run safely.<br><br>
<br>


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



## **⚠️⚠️ TO STOP THE PLAYBACK⚠️⚠️** <br>


The terminal command `pkill vlc` will stop the music.<br>
For volume control, one option is to use<br>

```mute
curl -X POST -H "Authorization: Bearer $SUPERVISOR_TOKEN" -d '{"index": 0,"volume": 0}' http://supervisor/audio/volume/output
```

<br>


```100%
curl -X POST -H "Authorization: Bearer $SUPERVISOR_TOKEN" -d '{"index": 0,"volume": 1}' http://supervisor/audio/volume/output
```



    
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
from difflib import get_close_matches

def clean_search_query(query):
    # Remove periods and commas from the query
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

if __name__ == "__main__":
    # Run the shell command to install VLC and modify vlc binary
    vlc_install_command = "apk add vlc && sed -i 's/geteuid/getppid/' /usr/bin/vlc"
    subprocess.run(vlc_install_command, shell=True)
    
    if len(sys.argv) != 3:
        print("Usage: python script.py <search_query> <directory>")
        sys.exit(1)

    search_query = sys.argv[1]
    directory = sys.argv[2]

    # Clean the search query
    cleaned_search_query = clean_search_query(search_query)

    closest_directory = find_closest_directory(cleaned_search_query, directory)
    if closest_directory:
        command = "cvlc add '{}' vlc://quit &".format(closest_directory)
        print("Executing command:", command)
        
        # Execute the command
        subprocess.run(command, shell=True)
    else:
        print("Sorry")
```


<br><br>
