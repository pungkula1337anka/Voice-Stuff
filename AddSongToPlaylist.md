
<h1 align="center">
<br>

Add Song To Playlist

</h1><br>
<br><br>

Checks what song is currently being played, takes the song title and does a search, grabs file & netadata and saves it for a rainy day on your playlist. <br>

To play the playlist, you can use [PlayPlaylist](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/PlayPlaylist.md). <br>
<br><br><br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the `/config` dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>

- **3: Shell Command** <br>

Create a file called `shell_commands.yaml` in your `config` directory. <br>
Dont forget to include it in your `configuration.yaml` file. `shell_command: !include shell_commands.yaml` <br>

- **4: Add the Python script** <br>

Create a file called `add_song_to_playlist.py` in your `config` directory. Paste in the code from below. <br>

<br><br>



## **⚠️⚠️ NOTE ⚠️⚠️** <br><br>


This script grabs the currently playing song title from a media_player. <br> 
You can either use [my other script](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/RandomMusicLoop.md) to setup VLC with telnet or edit accordingly. <br>

<br><br>


## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: shell_command.add_song_to_playlist
      data: {}
```

<br><br>


## 🦆 /custon_sentences/sv/IntentName.yaml <br>


<br>

```
language: "sv"
intents:
  IntentName:
    data:
      - sentences:
          - "lägg till i spellistan"
          - "lägg till den här låten i spellistan"
          - "musik lägg till"
          - "musik lägg till [i] (listan|spellista|spellistan)"
```

<br><br>


## 🦆 /config/shell_command.yaml <br>


<br>


```
  add_song_to_playlist: 'python add_song_to_playlist.py /media/MyPlaylist.m3u'
```

<br><br>


## 🦆 /config/add_song_to_playlist.py <br>


<br>


```
import os
import sys
import requests
from mutagen import File as MFile

# GLOBAL VARIABLES
# CHANGE THESE!! 
HOME_ASSISTANT_IP = 'YOUR_IP'
HOME_ASSISTANT_PORT = 'YOUR_PORT'
ENTITY_ID = 'media_player.YOUR_TELNET_PLAYER'
ATTRIBUTE_NAME = 'media_title' 
ACCESS_TOKEN = 'YOUR_LONG_LIVED_ACESS_TOKEN'

def get_entity_attribute(entity_id, attribute_name):
    url = f'http://{HOME_ASSISTANT_IP}:{HOME_ASSISTANT_PORT}/api/states/{entity_id}'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        state_obj = response.json()
        if 'attributes' in state_obj and attribute_name in state_obj['attributes']:
            return state_obj['attributes'][attribute_name]
        else:
            print(f"Attribute '{attribute_name}' not found for entity '{entity_id}'.")
            sys.exit(1)
    else:
        print("Failed to get entity state:", response.text)
        sys.exit(1)

def get_song_file_path(media_title):
    media_directory = '/media/Music'
    for root, dirs, files in os.walk(media_directory):
        for file in files:
            if media_title.lower() in file.lower():
                return os.path.join(root, file)
    return None

def create_m3u_from_file(filepath):
    metadata_list = []
    audio = MFile(filepath)
    if audio and hasattr(audio, 'tags'):
        artist = audio.get('artist', [''])[0]
        title = audio.get('title', [''])[0]
        if artist and title:
            metadata_list.append(f"#EXTINF:-1,{artist} - {title}")
        else:
            print("Missing metadata (artist or title) for file:", filepath)
    metadata_list.append(filepath)
    return metadata_list

def main(playlist_file):
    media_title = get_entity_attribute(ENTITY_ID, ATTRIBUTE_NAME)
    if media_title:
        song_file = get_song_file_path(media_title)
        if song_file:
            mode = 'a' if os.path.exists(playlist_file) else 'w'
            with open(playlist_file, mode) as playlist:
                metadata_list = create_m3u_from_file(song_file)
                if metadata_list:
                    if mode == 'a':
                        playlist.write('\n')
                    playlist.write('\n'.join(metadata_list) + '\n')
            print(f"Song {song_file} added to playlist {playlist_file} successfully!")
        else:
            print(f"Song with title '{media_title}' not found in the music directory.")
    else:
        print(f"Failed to retrieve media title from attribute '{ATTRIBUTE_NAME}' of entity '{ENTITY_ID}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <playlist_file>")
        sys.exit(1)
    playlist_file = sys.argv[1]
    main(playlist_file)
```

<br><br>


