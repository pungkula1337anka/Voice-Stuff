
<h1 align="center">
<br>

Play News

</h1><br>
<br><br>

Plays the latest news (Swedish Radio) on a chosen media player.

<br><br><br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>


- **3: RESTful sensor** <br>

Create the REST sensor by adding the code below to your `sensors.yaml` file.





<br><br>




## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: media_player.play_media
      data:
        media_content_id: "{{ states('sensor.sveriges_radio_news') }}"
        media_content_type: music
      target:
         entity_id: media_player.ha		# <--- Change this to your chosen media player
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
          - "(starta|spela upp|sätt på|berätta) nyheterna"       
          - "jag vill höra nyheterna" 
          - "nyheter"

```

<br><br>


## 🦆 /config/sensors.yaml <br>


<br>


```
- platform: rest
  resource: http://api.sr.se/api/v2/news/episodes?format=json
  name: "SR Ekot Nyheter"
  value_template: "{{ value_json.episodes[0].downloadpodfile.url }}"
  unique_id: sensor.sveriges_radio_news
  force_update: true
```

<br><br>

