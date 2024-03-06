
<h1 align="center">
<br>

__Ask__

</h1><br>
<br><br>

Ask your customized search engine a question & get the answer. <br>
The power of Google is in your voice. <br>
The results you get from this script, is very much about how you customize the search engine. <br>
Use your imagination, about what this can do. <br>


 
<br><br>

- **1: Create a search engine** <br>

Go to Google developer, create and customize an search engine. <br>
Get the search engine ID & API key. <br>
 
- **2: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **3: Custom Sentences** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it `MediaController.yaml`<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below, edit for your language. <br>

- **4: Shell command** <br>

If you dont have it already, create the file `shell_command.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `shell_command: !include shell_command.yaml`<br> 

- **5: Python Script** <br>

Create the file `ask.py` inside your /config folder. <br>
Paste in at bottom of this page, and fill in your Google Search engine ID & API key. <br>
And your Home Assistant information. <br>


<br><br>




## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: shell_command.ask
      data: 
        question: "{{question}}"
```

<br><br>


## 🦆 /config/custom_sentences/sv/MediaController.yaml <br>


<br>


```
language: "sv"
intents:
  IntentName:
    data:
      - sentences:
          - "fråga {question} "
          - "jag har en (fråga|fundering) {question} "
          - "jag undrar {question} "
          - "har du någon aning om {question}"
lists:
  question:
    wildcard: true

```

<br><br>


## 🦆 shell_command.yaml <br>


<br>

```
  ask: "python ask.py {{ question | urlencode }} "
```

<br><br>


## 🦆 /config/media_controller.py <br>


<br>


```
import sys
import json
import urllib.request
import urllib.error
import requests
import time
import difflib

# Define your Google Search & HA Host information here
GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
SEARCH_ENGINE_ID = 'YOUR_GOOGLE_SEARCH_ENGINE_ID'
HOME_ASSISTANT_IP = 'YOUR_HOME_ASSISTANT_IP'
HOME_ASSISTANT_PORT = 'YOUR_HOME_ASSISTANT_PORT'
LONG_LIVED_ACCESS_TOKEN = 'YOUR_LONG_LIVED_ACESS_TOKEN'

# Define TTS Variables here
MEDIA_PLAYER_ENTITY_ID = 'media_player.ha'
LANGUAGE = 'sv_SE'
ENTITY_ID = 'tts.piper'

def search_google(query):
    url = f'https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}'
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except urllib.error.URLError as e:
        print("Failed to get search results from Google Custom Search API:", e)
        return None

def extract_snippet(response_json, search_query):
    if 'items' in response_json and len(response_json['items']) > 0:
        snippets = [item['snippet'] for item in response_json['items']]
        best_match = difflib.get_close_matches(search_query, snippets, n=1, cutoff=0.6)
        if best_match:
            return best_match[0]
        else:
            print("No close match found.")
            return None
    else:
        print("No search results found.")
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
    response = search_google(search_query)
    if response:
        snippet = extract_snippet(response, search_query)
        if snippet:
            send_tts_message(snippet)
            time.sleep(20)  
            send_tts_message(snippet)  
```¨

<br><br>

