
<h1 align="center">
<br>

Find Tv Remote

</h1><br>
<br><br>

Pings Nvidia Shield remote. 

<br><br><br>

- **1: Setup Android Debug Bridge Integration** <br>

Settings > Devices & Services > Add integration<br>

- **2: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **3: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>




<br><br>





## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: androidtv.adb_command
      target:
        entity_id: media_player.ADB
      data:
        command: am start -a android.intent.action.VIEW-d-n com.nvidia.remotelocator/.ShieldRemoteLocatorActivit
  speech:
    text: ""
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
          - "var är fjärrkontrollen"
          - "jag hittar inte fjärrkontrollen"
```

<br><br>




