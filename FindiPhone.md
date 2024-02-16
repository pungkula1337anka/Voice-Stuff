
<h1 align="center">
<br>
Find My iPhone
</h1><br>
<br><br>
Pings the iPhone.<br>
<br><br>


- **1: Intent Script** <br>

Create the file 'intent_script.yaml' file in the /config dir and fill in the code below.


- **2: Custom Sentence** <br>

Create a folder called 'custom_sentences' inside your /config dir.
Inside that folder, once again create a folder named with your language code. 'sv' for swedish, 'en' for english.
In that folder you create a file called 'FindiPhone.yaml' and fill in the code from below. 

<br><br>





## 🦆 /config/intent_script.yaml <br>


<br>

```
FindiPhone:
  action:
    - service: notify.mobile_app_antons_iphonetest
      data:
        message: Här är jag!
        title: Find My Phone
        data:
          push:
            sound:
              name: default
              critical: 1
              volume: 1
    - delay:
        hours: 0
        minutes: 0
        seconds: 10
        milliseconds: 0
    - service: notify.mobile_app_antons_iphonetest
      data:
        message: Här är jag!
        title: Find My Phone
        data:
          push:
            sound:
              name: default
              critical: 1
              volume: 1
```

<br><br>


## 🦆 /custon_sentences/sv/PlayArtist.yaml <br>


<br>

```
language: "sv"
intents:
  FindiPhone:
    data:
      - sentences:
          - "var är min telefon"

```

<br><br>




