
<h1 align="center">
<br>

Random Music

</h1><br>
<br><br>

Searches music library and creates a temporary playlist containing 300 random generated songs. <br> 
Starts the playback on your connected speakers. <br>
Just network mount your music to `/media/Music` and run the py,<br> 
it will take care of the installation process of VLC and modify the binaries so it can be run safely.<br><br>

And if you like the song playing, you can just say ["add this to my playlist"](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/AddSongToPlaylist.md)     

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

Create a file called `random_music.py` in your `config` directory. Paste in the code from below. <br>


<br><br>

You are done, try it out! <br><br>


## **⚠️⚠️ You can get a media player entity ⚠️⚠️** <br>

Settings > Devices & Integrations > VideoLAN > VLC with Telnet  
and fill in your local ip and default port.  
If you did not change the password in the pyscript, the password is `test123`.  

<br><br>




## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: shell_command.random_music
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
          - "spela upp musik"
          - "slumpa musik"
          - "musik slumpa"
          - "jag vill höra musik"
```

<br><br>


## 🦆 /config/shell_command.yaml <br>


<br>


```
  random_music: "python random_music.py"
```

<br><br>


## 🦆 /config/random_music.py <br>


<br>


```
import os
import subprocess
import random

def select_files(directory, limit=300):
    selected_files = []
    artists = set()  # Keep track of artists already selected
    for root, dirs, files in os.walk(directory):
        random.shuffle(files)
        for file in files:
            if len(selected_files) >= limit:
                break
            file_path = os.path.join(root, file)
            artist = os.path.basename(os.path.dirname(file_path))
            if artist not in artists:
                selected_files.append(file_path)
                artists.add(artist)
    return selected_files

if __name__ == "__main__":
    subprocess.run(["pkill", "vlc"])

    vlc_install_command = "apk add vlc && sed -i 's/geteuid/getppid/' /usr/bin/vlc"
    subprocess.run(vlc_install_command, shell=True)
    
    directory = '/media/Music/'  # Change this to the desired music directory

    selected_files = select_files(directory)

    random.shuffle(selected_files)  # Shuffle the list of selected files

    temp_playlist_file = "/tmp/shuffled_playlist.m3u"
    with open(temp_playlist_file, 'w') as f:
        for file in selected_files:
            f.write(file + '\n')

    # YOU PROBABLY WANT TO CHANGE THE PASSWORD HERE!!
    command = "cvlc -I telnet --telnet-password=test123 --telnet-port=4212 --alsa-audio-device=hw:1,0 '{}' &".format(temp_playlist_file)
    
    print("Executing command:", command)
    
    subprocess.run(command, shell=True)
```

<br><br>
