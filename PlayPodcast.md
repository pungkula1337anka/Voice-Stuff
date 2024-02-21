
<h1 align="center">
<br>
Play Podcast
</h1><br>
<br><br>
Searches /media/Podcasts/ for chosen podcast and creates an temporary playlist of the entire found subdirectory, starts   playback on your connected speakers, after it sorts the podcasts by release date, playing the newest first..<br><br>
The beuty about doing, whats called an "fuzzy search" like this, is that it allows you to (most likely) call a Podcasts name which are not in your native language.<br> 
Even if the STT generates the wrong word, the python script will still point you to the right directory path.<br>

The Python script will take care of the installation process of VLC and modify the binaries so it can be run safely.  
  
I use the [Podgrab](http://#) container to automatically download new episodes.  
And my [PyPodCleanup](http://#) script to remove old episodes.  
   

<br>



<br><br>

- **1: Create the shell commands.** <br>

Create the file 'shell_command.yaml' file in your /config dir and paste in the code below.
This will allow you to call the script easily later.

- **2: Intent Script** <br>


If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 
If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 


- **3: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>

- **4: The fuzzy search python script** <br>

This is where the magic happends. <br>
Within your /config dir, create a file called `play_fuzzy_podcast.py` <br>
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
  play_fuzzy_podcast: "python play_fuzzy_podcast.py '{{ podcast }}' "
```

<br><br>


## 🦆 /config/intent_script.yaml <br>


<br>

```
# Plays specified Podcast
IntentName:
  action:
    - service: shell_command.play_fuzzy_podcast
      data: 
        podcast: "{{podcast}}"
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
          - "spela [upp] (pod|podd|podden|podcast|poddcast|poddkast) {podcast}"
          - "(pod|podd|podcast|podkast) spela [upp] {podcast}"
                    
lists:
  podcast:
    wildcard: true
```

<br><br>



## 🦆 /config/play_fuzzy_podcast.py <br>


<br>

```
import os
import sys
import subprocess
from difflib import get_close_matches

PODCASTS_DIRECTORY = "/media/Podcasts/"

def clean_search_query(query):
    cleaned_query = query.replace('.', '').replace(',', '')
    return cleaned_query

def find_closest_podcast(query):
    podcasts = [p for p in os.listdir(PODCASTS_DIRECTORY) if os.path.isdir(os.path.join(PODCASTS_DIRECTORY, p))]
    closest_match = get_close_matches(query, podcasts, n=1)
    if closest_match:
        closest_podcast = os.path.join(PODCASTS_DIRECTORY, closest_match[0])
        return closest_podcast
    else:
        return None

def get_podcast_files_sorted_by_date(directory):
    podcast_files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    podcast_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return podcast_files

if __name__ == "__main__":
    subprocess.run(["pkill", "vlc"])

    vlc_install_command = "apk add vlc && sed -i 's/geteuid/getppid/' /usr/bin/vlc"
    subprocess.run(vlc_install_command, shell=True)

    if len(sys.argv) != 2:
        print("Usage: python script.py <search_query>")
        sys.exit(1)

    search_query = sys.argv[1]
    cleaned_search_query = clean_search_query(search_query)

    closest_podcast_directory = find_closest_podcast(cleaned_search_query)
    if closest_podcast_directory:
        podcast_files = get_podcast_files_sorted_by_date(closest_podcast_directory)

        if podcast_files:
            temp_playlist_file = "/tmp/podcast_playlist.m3u"
            with open(temp_playlist_file, 'w') as f:
                for file in podcast_files:
                    f.write(file + '\n')
##### ---->        YOU PROBABLY WANT TO CHANGE THE PASSWORD!
            command = "cvlc -I telnet --telnet-password=test123 --telnet-port=4212 --alsa-audio-device=hw:1,0 --playlist-enqueue '{}' &".format(temp_playlist_file)

            print("Executing command:", command)

            subprocess.run(command, shell=True)
        else:
            print("No podcasts found in the directory.")
    else:
        print("No closest match found for the podcast.")

```


<br><br>
