
<h1 align="center">
<br>

Python Ask Wikipedia

</h1><br>
<br><br>

Ask Wiki an question, get an answer.

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

If you dont have it already, create the file `shell_command.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `shell_command: !include shell_command.yaml`<br> 

- **4: Python Script** <br>

Create the file `ask_wiki.py` inside your /config folder. <br>
Paste in at bottom of this page, and fill in your Home Assistant information. <br>


<br><br>




## 🦆 /config/shell_command.yaml <br>


<br>


```
  ask_wiki: "python ask_wiki.py {{ question | urlencode }} "
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
          - "vad är {question} "
lists:
  question:
    wildcard: true
```

<br><br>


## 🦆 /config/intent_script.yaml <br>


<br>

```
IntentName:
  action:
    - service: shell_command.ask_wiki
      data: 
        question: "{{question}}"
```

<br><br>




## 🦆 /config/ask_wiki.py <br>


<br>


```
import sys
import json
import requests

# Define your Wiki language & HA Host information here
WIKIPEDIA_API_URL = 'https://sv.wikipedia.org/w/api.php'
HOME_ASSISTANT_IP = 'YOUR_HOME_ASSISTANT_IP'
HOME_ASSISTANT_PORT = 'YOUR_HOME_ASSISTANT_PORT'
LONG_LIVED_ACCESS_TOKEN = 'YOUR_LONG_LIVED_ACESS_TOKEN'

# Define TTS Variables here
MEDIA_PLAYER_ENTITY_ID = 'media_player.ha'
LANGUAGE = 'sv_SE'
ENTITY_ID = 'tts.piper'


def search_wikipedia(query):
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
        'titles': query
    }
    try:
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        data = response.json()
        page_id = next(iter(data['query']['pages'])) 
        if page_id == '-1':
            print("No Wikipedia page found for the query:", query)
            return None
        else:
            return data['query']['pages'][page_id]['extract']
    except Exception as e:
        print("Failed to get Wikipedia snippet:", e)
        return None

def send_tts_message(message):
    service_payload = {
        "entity_id": ENTITY_ID,
        "language": LANGUAGE,
        "message": message,
        "media_player_entity_id": MEDIA_PLAYER_ENTITY_ID
    }

    response = requests.post(f"http://{HOME_ASSISTANT_IP}:{HOME_ASSISTANT_PORT}/api/services/tts/speak",
                             headers={"Authorization": f"Bearer {LONG_LIVED_ACCESS_TOKEN}",
                                      "Content-Type": "application/json"},
                             json=service_payload)
    if response.status_code == 200:
        print("TTS message sent successfully.")
    else:
        print("Failed to send TTS message to Home Assistant:", response.text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <search_query>")
        sys.exit(1)

    search_query = sys.argv[1]
    snippet = search_wikipedia(search_query)
    if snippet:
        send_tts_message(snippet)
```

<br><br>

