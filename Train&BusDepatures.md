
<h1 align="center">
<br>

Python Travel Robot

</h1><br>
<br><br>

Text to Speech Departure Tunes.

<br><br>


## 🦆 getting started <br>

- **1: Get API Key** <br>

Create a new project for ResRobot 2.1 on Trafiklab to get your API key. <br>

- **2: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **3: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>

- **4: Shell command** <br>

- **5: Python script** <br>

Create the file `resrobot.py` inside your /config directory. <br>
Paste in the code below and dont forget to define your HA information & long lived, and Trafiklab API. <br>

- **6: Get your stop id's** <br>

Run your shell command like this:
<br>

```
# lookup stop ID:
service: shell_command.resrobot
data: 
  departure: search
  destination: göteborg
```

<br>

```
# add stop id
service: shell_command.resrobot
data: 
  departure: add PICK_A_STOP_NAME
  destination: STOP_ID_FROM_SEARCH
``` 
<br>
This will the stop ID to your list, but you will still need to include the stop name in your custom sentence list. <br>








<br><br>





## 🦆 /config/shell_commands.yaml <br>


<br>

```
  resrobot: "python resrobot.py {{ departure }} {{ destination }}"
```

<br><br>



## 🦆 /config/intent_script.yaml <br>


<br>


```
BussDepartures:
  action:
    - service: shell_command.resrobot
      data: 
        departure: "{{departure}}"
        destination: "{{destination}}"  
```

<br><br>


## 🦆 /custon_sentences/sv/IntentName.yaml <br>


<br>

```
language: "sv"
intents:
  BussDepartures:
    data:
      - sentences:
          - "när går bussen från {departure} till {destination}"
          - "vilken tid går bussen från {departure} till {destination}"
          - "när går nästa buss från {departure} till {destination}"
          - "vilken tid går nästa buss från {departure} till {destination}"
          - "hur lång tid är det till nästa buss från {departure} till {destination}"
          - "när går nästa {departure} till {destination}"
          - "vilken tid går nästa {departure} till {destination}"
          - "hur lång tid är det till nästa {departure} till {destination}"

lists:
  departure:
    values:
      - in: "(stop5|stop 5)"
        out: "stop5"   
      - in: "(stop5|stop 5)"
        out: "stop5"   
      - in: "(stop5|stop 5)"
        out: "stop5"   
      - in: "(stop5|stop 5)"
        out: "stop5"   
      - in: "(stop5|stop 5)"
        out: "stop5"   
      - in: "(stop5|stop 5)"
        out: "stop5"    
  destination:
    values:
      - in: "(stop5|stop 5)"
        out: "stop5"   
      - in: "(stop5|stop 5)"
        out: "stop5"   
      - in: "(stop5|stop 5)"
        out: "stop5"   
      - in: "(stop5|stop 5)"
        out: "stop5"   
      - in: "(stop5|stop 5)"
        out: "stop5"   
      - in: "(stop5|stop 5)"
        out: "stop5"        
```

<br><br>


## 🦆 /config/sensors.yaml <br>

Only uf you want them on dashboard.
<br>


```
  - platform: rest
    resource: https://api.resrobot.se/v2.1/departureBoard?id=STOPID1&direction=STOPID2&duration=700&format=json&accessId=YOURAPIKEY
    name: "Sensor 1 Name"
    value_template: "{{ value_json.Departure[0].time[0:5] }}"
    unique_id: sensor.resrobot_sensor_1
    force_update: false   # change at your own risk
    icon: mdi:bus
    scan_interval: 86400  # change at your own risk
    
  - platform: rest
    resource: https://api.resrobot.se/v2.1/departureBoard?id=STOPID1&direction=STOPID2&duration=700&format=json&accessId=YOURAPIKEY
    name: "Sensor 2 Name"
    value_template: "{{ value_json.Departure[1].time[0:5]  }}"
    unique_id: sensor.resrobot_sensor_2
    force_update: false   # change at your own risk
    icon: mdi:bus
    scan_interval: 86400  # change at your own risk
```

<br><br>

## 🦆 /config/resrobot.py <br>

<br>

```
#  resrobot.py
import sys
import requests
import time
import os

##########################################################
# Please define your shit here.
API_KEY = 'TRAFIKLAB_API_KEY'
ENTITY_ID = 'tts.piper'
LANGUAGE = 'sv_SE'
MEDIA_PLAYER_ENTITY_ID = 'media_player.tts'
HOME_ASSISTANT_IP = 'HOME_ASSISTANT_IP:8123'
LONG_LIVED_ACCESS_TOKEN = 'LONG_LIVED_ACESS_TOKEN'
STOP_IDS_FILE = 'stop_ids.py'

##########################################################

def get_stop_ids():
    stop_ids = {}
    stop_ids_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), STOP_IDS_FILE)
    if os.path.exists(stop_ids_path):
        try:
            from stop_ids import STOP_IDS as stop_ids
        except Exception as e:
            print(f"Error reading stop IDs file: {e}")
    return stop_ids

STOP_IDS = get_stop_ids()

def get_departure_times(departure_stop, destination_stop):
    departure_stop = departure_stop.lower()
    destination_stop = destination_stop.lower()
    
    if not departure_stop in STOP_IDS or not destination_stop in STOP_IDS:
        return "Invalid stop ID"

    departure_id = STOP_IDS[departure_stop]
    destination_id = STOP_IDS[destination_stop]

    url = f'https://api.resrobot.se/v2.1/departureBoard?id={departure_id}&direction={destination_id}&duration=700&format=json&accessId={API_KEY}'
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return "Timeout error"
    except requests.exceptions.RequestException:
        return "Request error"

    data = response.json()
    departure_times = [dep['time'][:5] for dep in data.get('Departure', [])[:4]]
    
    if not departure_times:
        return "No departure times available"
    
    next_bus_time_str = departure_times[0]
    current_time_str = time.strftime('%H:%M')
    
    try:
        next_bus_time = time.strptime(next_bus_time_str, '%H:%M')
        current_time = time.strptime(current_time_str, '%H:%M')
    except ValueError:
        return "Invalid time format"
    
    time_difference = (time.mktime(next_bus_time) - time.mktime(current_time)) / 60
    minutes_left = round(time_difference)

    if minutes_left > 0:
        return f"Nästa buss till {destination_stop} avgår om {minutes_left} minuter. Sedan har den avgångstid: {', '.join(departure_times[1:])}"
    elif minutes_left == 0:
        return f"Bussen går just nu. Nästa avgångstid är: {', '.join(departure_times[1:])}"
    else:
        return "Nästa buss har redan gått."

def send_tts_message(message):
    url = f'http://{HOME_ASSISTANT_IP}/api/services/tts/speak'
    headers = {
        'Authorization': f'Bearer {LONG_LIVED_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    service_payload = {
        "entity_id": ENTITY_ID,
        "language": LANGUAGE,
        "message": message,
        "media_player_entity_id": MEDIA_PLAYER_ENTITY_ID
    }
    try:
        response = requests.post(url, headers=headers, json=service_payload)
        response.raise_for_status()
        return "TTS message sent successfully"
    except requests.exceptions.RequestException as e:
        return f"Error sending TTS message: {e}"

def fuzzy_search_stop(search_query):
    url = f'https://api.resrobot.se/v2.1/location.name?input={search_query}?&format=json&accessId={API_KEY}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        stop_locations = data.get('stopLocationOrCoordLocation', [])
        if not stop_locations:
            print("No stop locations found.")
        else:
            for location in stop_locations:
                stop_location = location.get('StopLocation', {})
                name = stop_location.get('name', 'N/A')
                ext_id = stop_location.get('extId', 'N/A')
                print(f"Name: {name}, ID: {ext_id}")
    except requests.exceptions.Timeout:
        print("Timeout error")
    except requests.exceptions.RequestException:
        print("Request error")

def add_stop_id_to_globals(stop_name, stop_id):
    global STOP_IDS
    STOP_IDS[stop_name.lower()] = stop_id

    stop_ids_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), STOP_IDS_FILE)

    with open(stop_ids_path, 'r') as file:
        lines = file.readlines()
    with open(stop_ids_path, 'w') as file:
        file.writelines(lines[:-1])

    with open(stop_ids_path, 'a') as file:
        file.write(f"\n    '{stop_name.lower()}': '{stop_id}',")
        file.write("\n}")

    print(f"Stop ID {stop_id} added for {stop_name}")


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == 'add':
        stop_name = sys.argv[2]
        stop_id = sys.argv[3]
        add_stop_id_to_globals(stop_name, stop_id)
    elif len(sys.argv) == 3 and sys.argv[1] == 'search':
        search_query = sys.argv[2]
        fuzzy_search_stop(search_query)
    elif len(sys.argv) == 3:
        departure_stop = sys.argv[1]
        destination_stop = sys.argv[2]
        departure_times = get_departure_times(departure_stop, destination_stop)
        tts_result = send_tts_message(departure_times)
        print(tts_result)
    else:
        print("Usage:")
        print("python resrobot.py search <search_query>")
        print("python resrobot.py add <stop_name> <stop_id>")
        print("python resrobot.py <departure_stop> <destination_stop>")
        sys.exit(1)

```
<br><br>
