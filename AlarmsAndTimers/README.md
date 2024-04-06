
<h1 align="center">
<br>

Alarms And Timers<br>
<br>

![image](https://github.com/pungkula1337anka/Voice-Stuff/assets/105579081/b034fb2d-28a3-4564-aa55-ad5ed24a4d99)


</h1><br>
<br><br>

A single, feature packed, intent_script for all your timer needs! <br>

<br><br>

__Features:__
Start

<br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>


- **3: Add helpers ** <br>

Add the helpers by adding the code down below to your `configuration.yaml` file. 

- **4: ** <br>



<br><br>



## **⚠️⚠️ NOTE ⚠️⚠️** <br><br><br>





## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: input_datetime.set_datetime
      data:
          time: "{{hours}}:{{minutes | default(00)}}:00"
      target:
          entity_id: >
            {% set wakeupalarm1_state = states('input_boolean.wakeupalarm1') %}
            {% set wakeupalarm2_state = states('input_boolean.wakeupalarm2') %}
            {% set wakeupalarm3_state = states('input_boolean.wakeupalarm3') %}

            {% if wakeupalarm1_state == 'on' %}
              {% if wakeupalarm2_state == 'on' %}
                input_datetime.wakeupalarm3
              {% else %}
                input_datetime.wakeupalarm2
              {% endif %}
            {% else %}
              input_datetime.wakeupalarm1
            {% endif %} 
    - service: input_boolean.turn_on
      data: {}
      target:
          entity_id: >input_boolean.switch_wake_up_alarm
            {% set wakeupalarm1_state = states('input_boolean.wakeupalarm1') %}
            {% set wakeupalarm2_state = states('input_boolean.wakeupalarm2') %}
            {% set wakeupalarm3_state = states('input_boolean.wakeupalarm3') %}

            {% if wakeupalarm1_state == 'on' %}
              {% if wakeupalarm2_state == 'on' %}
                input_boolean.wakeupalarm3
              {% else %}
                input_boolean.wakeupalarm2
              {% endif %}
            {% else %}
              input_boolean.wakeupalarm1
            {% endif %} 
  speech:
    text: "ställde väckarklockan på {{ hours }}  {{ minutes }}"     
```

<br><br>


## 🦆 /custon_sentences/sv/IntentName.yaml <br>


<br>

```
language: "sv"
intents:
  SetWakeUpTime:
    data:
      - sentences:
          - "(starta|ställ|sätt) väckarklockan på {hours} [och] {minutes} "          
          - "väck mig klockan {hours} {minutes} "    
          - "väck mig {hours} {minutes} "       
          - "väck mig klockan {hours}"    
lists:
  minutes:
    range:
      from: 0
      to: 60
  hours:
    range:
      from: 0
      to: 24
```

<br><br>


## 🦆 /config/configuration.yaml <br>


<br>


```
input_datetime:
  wakeupalarm1:
    name: Wake Up Alarm1
    has_date: true
    has_time: true
  wakeupalarm2:
    name: Wake Up Alarm2
    has_date: true
    has_time: true
  wakeupalarm3:
    name: Wake Up Alarm3
    has_date: true
    has_time: true

input_boolean:
  wakeupalarm1:
    name: Wake Up Alarm1
  wakeupalarm2:
    name: Wake Up Alarm2
  wakeupalarm3:
    name: Wake Up Alarm3

timer:
  wakeup:
    duration: "00:00:01"
    restore: true
```

<br><br>


## 🦆 Example Automation <br>


<br>


```
alias: wake_up_alarm
description: ""
trigger:
  - platform: time
    at: input_datetime.wakeupalarm
  - platform: event
    event_type: timer.finished
    event_data:
      entity_id: timer.wakeup    
condition:
  - condition: time
    weekday:
      - fri
      - thu
      - wed
      - tue
      - mon
action:
  - service: timer.start
    data: {}
    target:
      entity_id: timer.wakeup
  - service: media_player.volume_set
    data:
      volume_level: 1
    target:
      entity_id: media_player.ha
  - service: media_player.play_media
    data:
      media_content_id: /local/sound/wakeup.mp3
      media_content_type: music
    target:
      entity_id: media_player.ha
  - service: notify.mobile_app_iPhone
    data:
      data:
        push:
          sound:
            name: default
            critical: 1
            volume: 1
      title: "⚠️ "
      message: VAKNA
  - delay:
      hours: 0
      minutes: 0
      seconds: 4
      milliseconds: 0
  - service: notify.mobile_app_iPhone
    data:
      data:
        push:
          sound:
            name: default
            critical: 1
            volume: 1
      title: "⚠️ "
      message: VAKNA
```

<br><br>
