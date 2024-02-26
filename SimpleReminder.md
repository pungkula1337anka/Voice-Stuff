
<h1 align="center">
<br>

Simple Reminder

</h1><br>
<br><br>

Sinple reminder, sets an calendar entry with a title of your choice, for tomorrow.  
Nuff said. 🐷   

<br><br><br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>


- **3: Dont forget!** <br>

You probably already have an automation to remind you about upcoming events. <br>
Example automation at the bottom of this page, in case you dont. <br>

  

<br><br>



## **⚠️⚠️ NOTE ⚠️⚠️** <br><br><br>

_These are just examples, you should make configurations that fit your usecase._



## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: calendar.create_event
      target:
        entity_id: calendar.ha
      data:
        summary: "{{reminder}}"
        start_date_time: "{{ today_at('18:00') + timedelta(hours=24) }}"
        end_date_time: "{{ today_at('20:00') + timedelta(hours=24) }}"
  speech:
    text: " Jag Ser till att du inte glömmer bort {{reminder}} . Jag kommer påminna dig imorgon . "
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
          - "påminn mig (att|om) {reminder}"
          - "glöm (ej|inte) [att] {reminder}"
          . "kom ihåg [att] {reminder}"
          
lists:
  reminder:
    wildcard: true     
```          

<br><br>




## 🦆 Example automation <br>



<br>


```
alias: Pass Song to HomePod Automation
description: "If Pass to Homepod toggle is on, everytime a new song is played on VLC, the song gets sent to Homepod"
mode: single
trigger:
  - platform: calendar
    event: start
    offset: "-4:0:0"	# Send notification 4 hours BEFORE event is schedueled
    entity_id: calendar.ha
  - platform: calendar
    event: start
    offset: "-4:0:0"
    entity_id: calendar.kalender
action:    
  - service: calendar.get_events
    target:
      entity_id:
        - calendar.ha
        - calendar.anniversaries
        - calendar.ALL_YOUR
        - calendar.CALENDARS_HERE
    data:
      duration:
        hours: 24
    response_variable: agenda
  - service: notify.mobile_app_antons_iphonetest
    data:
      message: >
        {% for event in agenda["calendar.ha"]["events"] %} {{ event.start}}: {{
        event.summary }}<br> {% endfor %} {% for event in
        agenda["calendar.anniversaries"]["events"] %} {{ event.summary }}<br> {%
        endfor %} {% for event in agenda["calendar.ALL_YOUR"]["events"] %} {{
        event.summary }}<br> {% endfor %} {% for event in
        agenda["calendar.CALENDARS_HERE"]["events"] %} {{ event.summary }}<br> {%
        endfor %}
      title: Kalender
      data:
        push:
          sound:
            name: default
            critical: 1
            volume: 1
mode: single
```

<br><br>

