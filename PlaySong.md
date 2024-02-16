
<h1 align="center">
<br>

Play Song

</h1><br>
<br><br>

Plays the song you asked for on your desired media player.

<br><br><br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>


- **3: Helpers** <br>

Create the helpers by adding the code below to your `configuration.yaml` file.

- **4: Command Line Sensor** <br>

Create the command line sensor by adding the code below to your `command_line.yaml` file.<br>
Dont forget to include it in your `configuration.yaml` file by adding `command_line: !include command_line.yaml`<br>


<br><br>




## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: input_text.set_value
      data: 
        value: {{song}}
      target:
        entity_id: input_text.search1
    - delay:
        hours: 0
        minutes: 0
        seconds: 2	# <-- You can change this, depending on the size of your media library.
        milliseconds: 0
    - service: media_player.play_media
      metadata: {}
      data:
        media_content_type: music
        media_content_id: "{{states('sensor.search_song')}}"
      target:
        entity_id: media_player.ha # <-- Change
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
          - "spela upp låten {song}"
lists:
  song:
    wildcard: true
```

<br><br>


## 🦆 /config/configuration.yaml <br>


<br>


```
input_text:
  search1:
    name: search1
    initial: The Rolling Stones
```

<br><br>


## 🦆 /config/command_line.yaml <br>


<br>


```
  - sensor:
      name: search_song
      command: "find /media/Music | grep -i {{states('input_text.search1')}}"
      value_template: '{{ value |replace("/media/Music/", "media-source://media_source/local/Music/") }}'
```

<br><br>
