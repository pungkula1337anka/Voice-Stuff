
<h1 align="center">
<br>

Play Playlist

</h1><br>
<br><br>

Makes sure VLC is installed, then starts playing a playlist. <br> 
Playback is started on your HA connected speakers. <br>
I use [this](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/AddSongToPlaylist.md) to add songs to the playlist by voice. <br> 

<br><br><br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>

- **3: Shell command** <br>

Create a file called `shell_commands.yaml` in your `config` directory. <br>
Dont forget to include it in your `configuration.yaml` file. `shell_command: !include shell_commands.yaml` <br>

- **4: Python script** <br>

Create a file called `play_playlist.py` in your `config` directory. Paste in the code from below. <br>


<br><br>



## **⚠️⚠️ TO STOP THE PLAYBACK⚠️⚠️** <br>


The terminal command `pkill vlc` will stop the music.<br><br>
For volume control, one option is to use<br>

mute
```
curl -X POST -H "Authorization: Bearer $SUPERVISOR_TOKEN" -d '{"index": 0,"volume": 0}' http://supervisor/audio/volume/output
```

<br><br>

100%
```
curl -X POST -H "Authorization: Bearer $SUPERVISOR_TOKEN" -d '{"index": 0,"volume": 1}' http://supervisor/audio/volume/output
```





## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: shell_command.play_playlist
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
          - "spela upp spellistan"
```

<br><br>


## 🦆 /config/shell_command.yaml <br>


<br>


```
  play_playlist: "python play_playlist.py '/media/MyPlaylist.m3u'"
```

<br><br>


## 🦆 /config/play_playlist.py <br>


<br>


```
import subprocess
import sys

def play_playlist(playlist_file):
    # Install VLC and modify the binary
    subprocess.run(["apk", "add", "vlc"])
    subprocess.run(["sed", "-i", "s/geteuid/getppid/", "/usr/bin/vlc"])

    subprocess.run(["cvlc", playlist_file, "vlc://quit"])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python play_playlist.py <playlist_file>")
        sys.exit(1)

    playlist_file = sys.argv[1]
    play_playlist(playlist_file)
```

<br><br>
