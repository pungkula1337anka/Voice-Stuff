
<h1 align="center">
<br>

Set Timer

</h1><br>
<br><br>

Simple, sets a timer.

<br><br><br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>





<br><br>



## **⚠️⚠️ Dont forget to create the timer.timer ⚠️⚠️** <br><br><br>





## 🦆 /config/intent_script.yaml <br>


<br>


```
SetTimer:
  action:
    - service: timer.start
      data:
          duration: "00:{{minutes}}:00"
      target:
          entity_id: timer.timer
  speech:
    text: "räknar ned från {{ minutes }} minuter"   
 
SetHourTimer:
  action:
    - service: timer.start
      data:
          duration: "{{hours}}:{{minutes}}:00"
      target:
          entity_id: timer.timer             
  speech:
    text: "räknar ned från {{ hours }} timmar och {{ minutes }} minuter"  
```

<br><br>


## 🦆 /custon_sentences/sv/IntentName.yaml <br>


<br>

```
language: "sv"
intents:
  SetTimer:
    data:
      - sentences:
          - "(starta|ställ|sätt)  [en] timer [på] {minutes} minuter"       
lists:
  minutes:
    range:
      from: 0
      to: 60
```


```	
language: "sv"
intents:
  SetHourTimer:
    data:
      - sentences:
          - "(starta|ställ|sätt)  [en] timer [på] {hours} (timma|timme|timmar) [och] {minutes} minuter"          
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


## 🦆 Example Automation <br>


<br>

```
alias: timer_finish
description: "When the timer finishes, blinks a light and send notification to phone and play sound on media player."
trigger:
  - platform: event
    event_type: timer.finished
    event_data:
      entity_id: timer.timer
action:
  - parallel:
      - service: light.turn_on
        data:
          flash: long
        target:
          entity_id:
            - light.min_lampa                     #<- change
      - service: notify.mobile_app_min_telefon     #<- change
        data:
          message: TIMER
      - service: media_player.play_media
        target:
          entity_id: media_player.min_media_spelare     #<- change
        data:
          media_content_id: http://homeassistant.local:8123/local/sound/timer.mp3       #<- change
          media_content_type: music
```



