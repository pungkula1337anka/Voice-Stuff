
<h1 align="center">
<br>

Lists All Custom Voice Commands

</h1><br>
<br><br>

Oh wow.. you have been working hard and adding new commands like crazy huh? <br>
Perhaps your mind is elsewhere sometimes and you forgot how to trigger your commands?  <br>
_I got you.._ Running this python will grab your custom sentences (6th line in all your yaml files) <br>
and send them back to you with an notification. <br>

<br><br><br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below. <br>


- **3: Shell command** <br>

Create the file 'shell_command.yaml' file in your /config dir and paste in the code below.
This will allow you to call the script easily later.

- **4: Python Script** <br>

Within your /config dir, create a file called `list_all_commands.py` <br>
Paste in the code from the bottom of this page. <br>
_Dont forget to change to your language code if your not a swetard._


<br><br>





## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: shell_command.list_voice_commands
      data: {}
      response_variable: result
    - service: notify.mobile_app_YOUR_iPHONE
      data:
        message: "{{ result['stdout'] }}"
        title: Voice Commands
        data:
          push:
            sound:
              name: default
              critical: 1
              volume: 1      
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
          - "vad ska jag säga" 
```

<br><br>


## 🦆 /config/shell_command.yaml <br>


<br>


```
  list_voice_commands: "python list_all_commands.py"
```

<br><br>



## 🦆 /config/list_all_commands.py <br>


<br>


```
import os
#      Define your language code here \/
directory = "/config/custom_sentences/sv/"

for filename in os.listdir(directory):
    if filename.endswith(".yaml") or filename.endswith(".yml"):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 6:
                print(lines[5].strip()) 
```

<br><br>

