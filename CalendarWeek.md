
<h1 align="center">
<br>

Calendar Week

</h1><br>
<br><br>

Lists upcoming calendar entries, for 170 hours forward, in a really nice human readable _(if you know swedish)_ format.   
No duplicate entries allowed.

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

Create the file 'shell_command.yaml'  in your /config dir and paste in the code below.
This will allow you to call the script easily later.
Include the file in your`configuration.yaml` like ths `shell_command: !include shell_command.yaml` 

- **4: Python script** <br>

This is where the magic happends. <br>
Within your /config dir, create a file called `kalender.py` <br>
Paste in the code at the bottom of this page. <br>

<br>
Your all set, try it out!<br><br>


<br><br>



## **⚠️⚠️ _WARNING_ ⚠️⚠️** <br><br><br>

_DO NOT RENAME_ the python script,  
If you have a file called calendar.py in your config folder, your home assistant will _CRASH!_  
__Having  a swedish Kalender aint so bad after all..__



## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: shell_command.py_calendar
      data: {}
      response_variable: result   
    - service: notify.mobile_app_YOUR_iPHONE
      data:
        message: "{{ result['stdout'] }}"
        title: "Kalender"
        data:
          push:
            sound:
              name: default
              critical: 1
              volume: 1         
  speech:
    text: "{{ result['stdout'] }}"
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
          - "vad händer"
          - "[min] (kalender|kalendern)"
          - "[mitt] schema"
```

<br><br>


## 🦆 /config/shell_command.yaml <br>


<br>


```
  py_calendar: "python kalender.py"
```

<br><br>



## 🦆 /config/kalender.py <br>


<br>


```
import requests
from datetime import datetime, timedelta

### DEFINE CALENDAR ENTITY_IDs HERE!
CALENDAR_ENTITY_IDS = [
    "calendar.anniversaries",
    "calendar.ha",
    "calendar.hem",
    "calendar.kalender"
]

def get_calendar_events(duration):
    all_events = []
    for calendar_entity_id in CALENDAR_ENTITY_IDS:
### --> 	DEFINE YOUR IP HERE
        endpoint = f"http://YOUR_HOME_ASSISTANT_IP:8123/api/calendars/{calendar_entity_id}?start={datetime.now().isoformat()}&end={(datetime.now() + duration).isoformat()}"

        try:
####    ----->  	            ------>           ----->            ----->         LONG_LIVED_TOKEN HERE 
            response = requests.get(endpoint, headers={'Authorization': 'Bearer YOUR_LONG_LIVED_ACCESS_TOKEN'}, timeout=10)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            events = response.json()
            all_events.extend(events)
        except requests.RequestException as e:
            print(f"Error fetching calendar events: {e}")

    return all_events

def format_event(event):
    start_time_str = event.get('start', {}).get('date') or event.get('start', {}).get('dateTime')
    if start_time_str:
        try:
            start_time = datetime.fromisoformat(start_time_str)
        except ValueError:
            print("Error: Unable to parse start time.")
            return ""

        formatted_start_time = format_date(start_time)
        return f"{formatted_start_time}: {event.get('summary', 'No summary')}"
    else:
        print("Error: ingen start tid.")
        return ""

def format_date(date):

    swedish_date = date.strftime("%A den %d %B")

    swedish_date = swedish_date.replace("Monday", "måndag").replace("Tuesday", "tisdag").replace("Wednesday", "onsdag") \
        .replace("Thursday", "torsdag").replace("Friday", "fredag").replace("Saturday", "lördag").replace("Sunday", "söndag") \
        .replace("January", "januari").replace("February", "februari").replace("March", "mars").replace("April", "april") \
        .replace("May", "maj").replace("June", "juni").replace("July", "juli").replace("August", "augusti") \
        .replace("September", "september").replace("October", "oktober").replace("November", "november").replace("December", "december")
    return swedish_date

if __name__ == "__main__":
    duration = timedelta(days=7)  

    calendar_events = get_calendar_events(duration)

    if calendar_events:
       
        unique_events = {}

        for event in calendar_events:
            event_key = event.get('start', {}).get('date') or event.get('start', {}).get('dateTime')
            if event_key:
                if event_key not in unique_events:
                    unique_events[event_key] = event

        today = datetime.now().strftime("%Y-%m-%d")
        events_today = []
        upcoming_events = []
        for event in unique_events.values():
            start_time_str = event.get('start', {}).get('date') or event.get('start', {}).get('dateTime')
            if start_time_str == today:
                events_today.append(event)
            else:
                upcoming_events.append(event)

        if events_today:
            print("Idag:")
            for event in events_today:
                print(format_event(event))
            print()

        print("Kommande evenemang:")
        sorted_events = sorted([event for event in upcoming_events if event.get('start', {}).get('dateTime') is not None], key=lambda x: x.get('start', {}).get('dateTime'))
        for event in sorted_events:
            print(format_event(event))
    else:
        print("Misslyckades.")
```

<br><br>

