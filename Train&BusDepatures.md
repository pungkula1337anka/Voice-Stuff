
<h1 align="center">
<br>

Train & Bus Depatures

</h1><br>
<br><br>

Tells you when the chosen bus is depaturing.

<br><br><br>



- **1: Get API Key** <br>

Create a new project for ResRobot 2.1 on Trafiklab to get your API key. <br>

- **2: Find your stop ids** <br>

Find your stop ID's, you will need them to create the RESTful sensors. <br>
Here is the docs on how to find them.<br>
https://www.trafiklab.se/sv/api/trafiklab-apis/resrobot-v21/stop-lookup/ <br>

- **3: RESTful sensors** <br>

Fill in the code below in your `sensors.yaml` file, and change the ID's to match your stop ID's and API key. <br>
STOPID1 is where your bus/train is leaving from.<br>
STOPID2 is where your bus/train is arriving.<br>

- **4: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **5: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>






<br><br>



## **⚠️⚠️ Important ⚠️⚠️** <br><br>

DO NOT FORGET to turn off the force_update and set a very high scan_interval on the REST sensors!!<br>
Or else your sensors will break very, very quickly, and you might get a possible ban from Trafiklab! <br>
If you are planning to have the sensors on a dashboard, i suggest making a button to update them.<br>

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
import sys
import requests
import time

# Global variables
API_KEY = 'TRAFIKLAB_TOKEN'
ENTITY_ID = 'tts.piper'
LANGUAGE = 'sv_SE'
MEDIA_PLAYER_ENTITY_ID = 'media_player.tts'
HOME_ASSISTANT_IP = 'HOME_ASSISTANT_IP'
LONG_LIVED_ACCESS_TOKEN = 'LONG_LIVED_ACESS_TOKEN'
STOP_IDS = {
    'stop1': 'XXXXXXXXX',
    'stop2': 'XXXXXXXXX',
    'stop3': 'XXXXXXXXX',
    'stop4': 'XXXXXXXXX',
    'stop5': 'XXXXXXXXX',
    'stop6': 'XXXXXXXXX'
}



def get_departure_times(departure_stop, destination_stop):
    departure_stop = departure_stop.lower()
    destination_stop = destination_stop.lower()
    
    departure_id = STOP_IDS.get(departure_stop)
    destination_id = STOP_IDS.get(destination_stop)
    if not departure_id or not destination_id:
        return "Invalid stop ID"

    url = f'https://api.resrobot.se/v2.1/departureBoard?id={departure_id}&direction={destination_id}&duration=700&format=json&accessId={API_KEY}'
    try:
        response = requests.get(url, timeout=10)  # Adjust timeout as needed
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
    url = f'http://{HOME_ASSISTANT_IP}:8123/api/services/tts/speak'
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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python get_departure_times.py <departure_stop> <destination_stop>")
        sys.exit(1)
    
    departure_stop = sys.argv[1]
    destination_stop = sys.argv[2]

    departure_times = get_departure_times(departure_stop, destination_stop)
    tts_result = send_tts_message(departure_times)
    print(tts_result)
```
<br><br>
