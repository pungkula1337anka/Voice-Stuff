
<h1 align="center">
<br>

Random Music Loop

</h1><br>
<br><br>

Searches your music library and grabs a song by random. <br> 
After it starts a timer in HA with the duration of the song. And sets an input_text with the full file path of the song. <br>
So if you like the song you can just say ["add this to my playlist".](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/AddSongToPlaylist.md) <br>
Starts the playback on your connected speakers. <br>
When the timer finishes this all loops. <br>
This script assumes your music is mounted at /media/Music <br>

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
Fill in your local IP and Long lived acess token (x2). <br>

- **5: Create the helpers** <br>

Okay here you can just copy pasta the code below into your `configuration.yaml` file. <br>

- **6: Create the loop automation** <br>

You can copy paste everything down below into your `automations.yaml` file in your config folder.<br> 


<br><br>



## **⚠️⚠️ TO STOP THE PLAYBACK⚠️⚠️** <br>


The terminal command `pkill vlc` will stop the music.<br>
Dont forget to stop the timer aswell.<br><br>
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


<br><br><br>


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
import subprocess
import random
import requests
import time

def find_closest_directory(directory):
    if os.path.isdir(directory):
        return directory
    else:
        return None

def send_current_song_to_home_assistant(song_path):
    url = 'http://YOUR_HOME_ASSISTANT_IP:8123/api/services/input_text/set_value'  # Update with your Home Assistant IP
    headers = {
        'Authorization': 'Bearer YOUR_LONG_LIVED_ACCESS_TOKEN',  # Update with your access token
        'Content-Type': 'application/json',
    }
    data = {
        'entity_id': 'input_text.currentsong',
        'value': song_path
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Song information sent to Home Assistant successfully.")
    else:
        print("Failed to send song information to Home Assistant.")

def get_song_duration(song_path):
    duration_output = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", song_path])
    return int(float(duration_output))

def start_timer(duration):
    url = 'http://YOUR_HOME_ASSISTANT_IP:8123/api/services/timer/start'  # Update with your Home Assistant IP
    headers = {
        'Authorization': 'Bearer YOUR_LONG_LIVED_ACCESS_TOKEN',  # Update with your access token
        'Content-Type': 'application/json',
    }
    data = {
        'entity_id': 'timer.songtimer',
        'duration': duration
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Timer started successfully.")
    else:
        print("Failed to start timer.")

if __name__ == "__main__":
    # Kill any existing VLC process
    subprocess.run(["pkill", "vlc"])

    # Run the shell command to install VLC and modify vlc binary
    vlc_install_command = "apk add vlc && sed -i 's/geteuid/getppid/' /usr/bin/vlc"
    subprocess.run(vlc_install_command, shell=True)
    
    directory = '/media/Music/'  # Change this to the desired music directory

    closest_directory = find_closest_directory(directory)
    if closest_directory:
        
        selected_files = []

        # Iterate through the directory and add files to the list
        for root, dirs, files in os.walk(closest_directory):
            for file in files:
                if len(selected_files) >= 300:
                    break  # Stop if we have reached the limit
                selected_files.append(os.path.join(root, file))

        # Shuffle the selected files
        random.shuffle(selected_files)

        
        random_song = random.choice(selected_files)

       
        send_current_song_to_home_assistant(random_song)

        
        command = f"cvlc --playlist-enqueue '{random_song}' &"

        print("Executing command:", command)

        
        subprocess.run(command, shell=True)
        
        
        song_duration = get_song_duration(random_song)

        # Start the timer with the duration of the song
        start_timer(f"00:00:{song_duration}")  

    else:
        print("Music directory not found.")
```

<br><br>


## 🦆 /config/configuration.yaml <br>


<br>


```
timer:
  songtimer:
    duration: "00:00:00"

input_text:
  currentsong:
    name: Current Song 
    min: 8
    max: 250
    icon: mdi:music-box
```

<br><br>


## 🦆 /config/automations.yaml <br>


<br>


```
alias: Random Music Automation Loop
description: ""
trigger:
  - platform: event
    event_type: timer.finished
    event_data:
      entity_id: timer.songtimer
condition: []
action:
  - service: shell_command.random_music
    data: {}
mode: single
```

<br><br>
