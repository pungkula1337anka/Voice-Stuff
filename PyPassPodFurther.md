
<h1 align="center">
<br>

Pass Pod Further

</h1><br>
<br><br>

Grabs the pod title from the VLC telnet integrations media player entity media_title attribute, searches for the full file path, templates it to a correct media source url, then sends it back to another media player entity. This is not nearly fast enough to use as multiroom functionallity, and some may argue the use case for this, but it should do the trick if you just want to listen in a different room.  
Assumes you are doing the playback on VLC with telnet integration installed, but it could be edited for different scenarios if you wish.  

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

Create the file 'shell_command.yaml' file in your /config dir and paste in the code below.  
This will allow you to call the script easily later.  

- **4: Python script** <br>

Within your /config dir, create a file called `py_pass_pod_further.py` <br>
Paste in the code further down this page. <br>

- **5: Example automation** <br>

Example use case.  

<br><br>



## **⚠️⚠️ NOTE ⚠️⚠️** <br><br><br>

_These are just examples, you should make configurations that fit your usecase._



## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: input_boolean.toggle
      data: {}
      target:
        entity_id: input_boolean.pass_to_homepod
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
          - "jag är i sovrummet"
          - "jag vill höra i sovrummet"
```

<br><br>


## 🦆 /config/shell_command.yaml <br>


<br>


```
  pass_pod_further: "python py_pass_pod_further.py /media/Podcasts" 
```

<br><br>


## 🦆 /config/py_pass_song_further.py <br>


<br>


```
import os
import sys
import requests


def fuzzy_search(target, query):
    target = target.lower()
    query = query.lower()
    
    score = 0
    i, j = 0, 0

    while i < len(target) and j < len(query):
        if target[i] == query[j]:
            score += 1
            j += 1
        i += 1

    return score / max(len(target), len(query)) * 100


def fuzzy_search_in_directory(media_title, directory):
    best_match = None
    best_score = 0

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)

            score = fuzzy_search(file, media_title)
            if score > best_score:
                best_match = filepath
                best_score = score

    return best_match

# Home Assistant configuration
HA_IP = "YOUR_HOME_ASSISTANT_IP"
HA_PORT = "8123"
ACCESS_TOKEN = "YOUR_LONG_LIVED_ACESS_TOKEN"

# Define your VLC Telnet media player entity ID
entity_id = "media_player.vlc_telnet"

headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
response = requests.get(f"http://{HA_IP}:{HA_PORT}/api/states/{entity_id}", headers=headers)
media_title = response.json()["attributes"]["media_title"]


if len(sys.argv) != 2:
    print("Usage: python script.py <directory>")
    sys.exit(1)
directory = sys.argv[1]


result_filepath = fuzzy_search_in_directory(media_title, directory)


templated_filepath = result_filepath.replace(f"{directory}/", 'media-source://media_source/local/Podcasts/')

# Define where you wish to send the audio
service_data = {
    "entity_id": "media_player.homepod",
    "media_content_type": "music",
    "media_content_id": templated_filepath
}

requests.post(f"http://{HA_IP}:{HA_PORT}/api/services/media_player/play_media", headers=headers, json=service_data)

print("Service call sent:", templated_filepath)

```

<br><br>



## 🦆 Example automation <br>


You could for example, create an helper boolean in your `configuration.yaml` file.  
```
input_boolean:
  pass_to_homepod:
    name: Pass the Podcast to Homepod
    initial: false
    icon: mdi:music
```  

<br><br>


```
alias: Pass Podcast to HomePod Automation
description: "If Pass to Homepod toggle is on, everytime a new Podcast is played on VLC, the song gets sent to Homepod"
mode: single
trigger:
  - platform: state
    entity_id:
      - media_player.vlc_telnet
    attribute: media_title
  - platform: state
    entity_id:
      - input_boolean.pass_to_homepod    
condition:
  - condition: state
    entity_id: input_boolean.pass_to_homepod
    state: "on"
action:
  - service: shell_command.pass_pod_further
    data: {}
```

<br><br>

