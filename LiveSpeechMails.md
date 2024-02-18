
<h1 align="center">
<br>

Live TTS eMail

</h1><br>
<br><br>

When you get an email, you'll hear a mailmotherfucker and he will read your email for you.<br>
*with voice command to turn all live TTS off.*
<br><br><br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>


- **3: Helper** <br>

Simple. A boolean helper to toggle the live TTS.<br>
Create the helper yourself or copy pasta the code into your `configuration.yaml` file.<br>

- **4: Setup forwarding** <br>

For security, you can, and probably should(?) have a seperate email account for this. <br>
Setup automatic forwarding off the emails you want to that account. <br>

- **5: Setup IMAP** <br>

Settings > Devices & Services > Add integration > Search for IMAP. <br>

- **6: Create the automation** <br>

You can pasta the code below if you want. <br>

<br><br>





## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: input_boolean.turn_off
      target:
        entity_id: input_boolean.babbla
      data: {}
  speech:
    text: "ja ska va tyst.."
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
          - "[sluta] babbla"
          - "sluta prata"
```

<br><br>


## 🦆 /config/configuration.yaml <br>


<br>


```
input_boolean:
  name: babbla
  icon: mdi:car
```

<br><br>


## 🦆 /config/automation.yaml <br>


<br>


```
alias: imap_tts
description: ""
trigger:
  - platform: event
    event_type: imap_content
    event_data: {}
condition:
  - condition: state
    entity_id: input_boolean.babbla
    state: "on"
action:
  - service: media_player.play_media
    target:
      entity_id: media_player.ha
    data:
      media_content_id: mailmotherfucker.mp3
      media_content_type: music
  - delay:
      hours: 0
      minutes: 0
      seconds: 4
      milliseconds: 0
  - service: tts.speak
    metadata: {}
    data:
      cache: false
      media_player_entity_id: media_player.ha
      message: >-
        From {{ trigger.event.data['sender'] }} . Subject {{
        trigger.event.data['subject'] }} - 
    target:
      entity_id: tts.piper
mode: single
```

<br><br>
