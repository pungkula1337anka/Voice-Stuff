
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

    subprocess.run(["pkill", "vlc"])

    vlc_install_command = "apk add vlc && sed -i 's/geteuid/getppid/' /usr/bin/vlc"
    subprocess.run(vlc_install_command, shell=True)
    
    directory = '/media/Music/'  # Change this to the desired music directory

    closest_directory = find_closest_directory(directory)
    if closest_directory:

        selected_files = []

        for root, dirs, files in os.walk(closest_directory):
            for file in files:
                if len(selected_files) >= 300:
                    break  # Stop if we have reached the limit
                selected_files.append(os.path.join(root, file))


        random.shuffle(selected_files)

        temp_playlist_file = "/tmp/shuffled_playlist.m3u"
        with open(temp_playlist_file, 'w') as f:
            for file in selected_files:
                f.write(file + '\n')
        
        # YOU PROBABLY WANT TO CHANGE THE PASSWORD!!
        command = "cvlc -I telnet --telnet-password=test123 --telnet-port=4212 --alsa-audio-device=hw:1,0 '{}' &".format(temp_playlist_file)
        
        print("Executing command:", command)
        
        subprocess.run(command, shell=True)
    else:
        print("Music directory not found.")
```

<br><br>
