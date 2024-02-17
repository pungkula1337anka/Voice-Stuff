
<h1 align="center">
<br>

Random Music

</h1><br>
<br><br>

Searches music library and creates a temporary playlist containing 300 random generated songs. <br> 
Starts the playback on your connected speakers. <br>
This script assumes your music is mounted at /media/Music<br>

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
import sys
import subprocess
import random

def find_closest_directory(directory):
    if os.path.isdir(directory):
        return directory
    else:
        return None

if __name__ == "__main__":
    # Kill any existing VLC process
    subprocess.run(["pkill", "vlc"])

    # Run the shell command to install VLC and modify vlc binary
    vlc_install_command = "apk add vlc && sed -i 's/geteuid/getppid/' /usr/bin/vlc"
    subprocess.run(vlc_install_command, shell=True)
    
    directory = '/media/Music/'  # Change this to the desired music directory

    closest_directory = find_closest_directory(directory)
    if closest_directory:
        # Initialize a list to hold the selected files
        selected_files = []

        # Iterate through the directory and add files to the list
        for root, dirs, files in os.walk(closest_directory):
            for file in files:
                if len(selected_files) >= 300:
                    break  # Stop if we have reached the limit
                selected_files.append(os.path.join(root, file))

        # Shuffle the selected files
        random.shuffle(selected_files)

        # Write shuffled playlist to a temporary file
        temp_playlist_file = "/tmp/shuffled_playlist.m3u"
        with open(temp_playlist_file, 'w') as f:
            for file in selected_files:
                f.write(file + '\n')
        
        # Generate the command to load the playlist into VLC
        command = "cvlc --playlist-enqueue '{}' &".format(temp_playlist_file)
        
        print("Executing command:", command)
        
        # Execute the command
        subprocess.run(command, shell=True)
    else:
        print("Music directory not found.")
```

<br><br>
