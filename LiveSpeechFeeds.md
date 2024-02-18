
<h1 align="center">
<br>

Live TTS RSS Feeds

</h1><br>
<br><br>

When an RSS feed gets an new post, you'll hear a pling and you'll get the feed read for you.  
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

- **3: Edit config file** <br>

Simple. A boolean helper to toggle the live TTS.  
Create the helper, and include a yaml file for feedreader by copying the code below into `configuration.yaml`  

- **4: Setup feedreader** <br>

Create a file called `feeds.yaml` inside your `config` directory. Use this file to fill in the feeds you want.  

- **6: Create the automation**  

You can use the code below as an example, but you'll have to edit accourdingly. <br>

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
feedreader: !include feeds.yaml
input_boolean:
  name: babbla
  icon: mdi:car
```

<br><br>


## 🦆 /config/feeds.yaml <br>


<br>


```
  urls:
    - https://www.example.com/rss
  scan_interval:
    minutes: 5
  max_entries: 15
```

<br><br>












## 🦆 /config/automation.yaml <br>


<br>


```
alias: Feedreader Automation
trigger:
  - platform: event
    event_type: feedreader
    event_data:
      feed_url: https://www.example.se/rss
    id: example
action:
  - if:
      - condition: trigger
        id:
          - example
    then:
      - condition: state
        entity_id: input_boolean.babbla
        state: "on"
      - service: media_player.play_media
        target:
          entity_id: media_player.yourmediaplayer
        data:
          media_content_id: pling.mp3
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
          message: Feedname {{trigger.event.data.title}}
          media_player_entity_id: media_player.yourmediaplayer
          language: sv_SE
        target:
          entity_id: tts.piper
```

<br><br>
