
<h1 align="center">
<br>

Next Bus

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


## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: homeassistant.update_entity
      target:
        entity_id: "{{ states.sensor | selectattr('object_id', 'match', 'resrobot_') | map(attribute='entity_id') | list }}"
      data: {}  
  speech:
    text: " {% set next_bus_time_str = states('sensor.resrobot_sensor_1') %}
{% set current_time_str = states('sensor.time') %}

{% if next_bus_time_str != 'unavailable' %}
    {% set next_bus_time = strptime(next_bus_time_str, '%H:%M') %}
    {% set current_time = strptime(current_time_str, '%H:%M') %}
    {% set time_difference = next_bus_time - current_time %}
    {% set minutes_left = time_difference.total_seconds() / 60 %}
    {% if minutes_left > 0 %}
        Nästa buss till Vasaplan avgår om {{ minutes_left | round(0) }} minuter
    {% elif minutes_left == 0 %}
        Bussen går just nu. Nästa avgår {{states('sensor.resrobot_sensor_2')}}
    {% else %}
        Nästa buss har redan gått.
    {% endif %}
{% else %}
    Buss tabellen är tydligen inte tillgänglig just nu.
{% endif %}

    
    Sedan avgår bussen  . . {{states('sensor.resrobot_sensor_2')}}"       
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
          - "när går [nästa} buss[en} till STOPID2"
          - "vilken tid går bussen till STOPID2"
```

<br><br>


## 🦆 /config/sensors.yaml <br>


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

