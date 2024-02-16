
<h1 align="center">
<br>

Time

</h1><br>
<br><br>

Tells current time, date and month. 

<br><br><br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>




## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
  speech:
    text: Klockan är {{ states('sensor.time')| replace(":", "  ") }} .  Det är{% if now().weekday() in (0,) %} Måndag {% elif now().weekday() in (1,) %} Tisdag {% elif now().weekday() in (2,) %} Måndag {% elif now().weekday() in (3,) %} Tisdag {% elif now().weekday() in (4,) %} Måndag {% elif now().weekday() in (5,) %} Tisdag {% elif now().weekday() in (6,) %} Söndag {% endif %} {{  as_timestamp(now())| timestamp_custom('%-d')}} {% if now().month in (1,) %}Januari {% elif now().month in (2,) %} Februari {% elif now().month in (3,) %} Mars {% elif now().month in (4,) %} April {% elif now().month in (5,) %} Maj {% elif now().month in (6,) %} Juni {% elif now().month in (7,) %} Juli {% elif now().month in (8,) %} Augusti {% elif now().month in (9,) %} September {% elif now().month in (10,) %} Oktober {% elif now().month in (11,) %} November {% elif now().month in (12,) %} December{% endif %}
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
          - "[vad är] klockan"
          - "vad är det för dag"
          - "vilken dag är det"
```

<br><br>




