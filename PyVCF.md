
<h1 align="center">
<br>

Python vCard Helper

</h1><br>
<br><br>

Ask for a contact from your adressbooks personal information and you will get the phone number on TTS, <br>
and all their contact information will be displayed on your android TV along with their contact picture. <br>

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

- **4: Python script** <br>

Within your /config dir, create a file called `vcfhelper.py`
Paste in the code further down this page and save.

<br><br>



## **⚠️⚠️ NOTE ⚠️⚠️** <br><br><br>

Have your phone backup contact pictures to `/config/www/contacts/CONTACTNAME.png`.

<br><br>

## 🦆 /config/intent_script.yaml <br>


<br>


```
IntentName:
  action:
    - service: shell_command.vcf_helper
      data: 
        contact: "{{contact}}"
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
          - "(contact|kontakt) info {contact} "  
lists:
  contact:
    wildcard: true
```

<br><br>


## 🦆 /config/shell_command.yaml <br>


<br>


```
  vcf_helper: "python vcfhelper.py '{{ contact }}.vcf'"
```

<br><br>


## 🦆 /config/vcfhelper.py <br>


<br>


```
import os
import re
import sys
import json
import time
import requests

# Define your global variables here
HOME_ASSISTANT_IP = "HOME_ASSISTANT_IP:HOME_ASSISTANT_PORT"
LONG_LIVED_ACCESS_TOKEN = "LONG_LIVED_ACESS_TOKEN"
VCF_FILES_DIRECTORY = "/share/contacts"
MEDIA_PLAYER_TTS = "media_player.tts"
TTS_ENTITY_ID = "tts.piper"
DEBUG_MODE = False
COUNTRY_CODE = "+46"


def extract_contact_info(file_path):
    with open(file_path, 'r') as file:
        contact_data = file.read()

    name_match = re.search(r'FN:(.*?)\n', contact_data)
    email_matches = re.findall(r'EMAIL;.*?:(.*?)\n', contact_data)
    phone_matches = re.findall(r'TEL;.*?:(.*?)\n', contact_data)
    address_match = re.search(r'ADR;.*?:(.*?)\n', contact_data)
    birthday_match = re.search(r'BDAY:(.*?)\n', contact_data)
    notes_match = re.search(r'NOTE:(.*?)\n', contact_data)

    name = name_match.group(1) if name_match else ""
    emails = email_matches if email_matches else []
    phones = phone_matches if phone_matches else []
    address = address_match.group(1) if address_match else ""
    birthday = birthday_match.group(1) if birthday_match else ""
    notes = notes_match.group(1) if notes_match else ""

    return name, emails, phones, address, birthday, notes


def send_to_android_tv(contact_name, contact_info):

    title = contact_name
    message = "\n".join(contact_info)
    

    service_payload = {
        "title": title,
        "message": message,
        "data": {
            "fontsize": "max",
            "position": "center",
            "duration": 60,
            "transparency": "0%",
            "color": "red",
            "interupt": "1",
            "image": {
                "url": f"https://{HOME_ASSISTANT_IP}/local/contacts/{contact_name}.png"
            }
        }
    }

    response = requests.post(f"http://{HOME_ASSISTANT_IP}/api/services/notify/shield_notification", 
                             headers={"Authorization": f"Bearer {LONG_LIVED_ACCESS_TOKEN}", 
                                      "Content-Type": "application/json"},
                             json=service_payload)
    if DEBUG_MODE:
        print("Sending to Android TV:")
        print(json.dumps(service_payload, indent=4))
        print(response.text)

def read_out_contact_info(contact_name, contact_info):

    formatted_contact_numbers = []
    for info in contact_info:
        if re.match(r'^\+\d{2}', info):
            contact_number = info.replace(COUNTRY_CODE, "0")
            formatted_contact_number = f"{contact_number[:3]} . {contact_number[3:5]} . {contact_number[5:7]} . {contact_number[7:]}"
            formatted_contact_numbers.append(formatted_contact_number)


    message = f"{contact_name} . Telefon nummer .  {' . . . '.join(formatted_contact_numbers)}"
    

    service_payload = {
        "entity_id": TTS_ENTITY_ID,
        "language": "sv_SE",
        "message": message,
        "media_player_entity_id": MEDIA_PLAYER_TTS  
    }

    response = requests.post(f"http://{HOME_ASSISTANT_IP}/api/services/tts/speak", 
                             headers={"Authorization": f"Bearer {LONG_LIVED_ACCESS_TOKEN}", 
                                      "Content-Type": "application/json"},
                             json=service_payload)
    if DEBUG_MODE:
        print("Reading out contact info:")
        print(json.dumps(service_payload, indent=4))
        print(response.text)
    
    time.sleep(5)
    
    response = requests.post(f"http://{HOME_ASSISTANT_IP}/api/services/tts/speak", 
                             headers={"Authorization": f"Bearer {LONG_LIVED_ACCESS_TOKEN}", 
                                      "Content-Type": "application/json"},
                             json=service_payload)
    if DEBUG_MODE:
        print("Reading out contact info (Second TTS call):")
        print(json.dumps(service_payload, indent=4))
        print(response.text)


def process_vcf_files(directory, contact_name):
    if contact_name.lower().endswith(".vcf"):
        contact_name = contact_name[:-4]

    for filename in os.listdir(directory):
        if filename.lower().endswith(".vcf"):
            file_path = os.path.join(directory, filename)
            contact_name_vcf, emails, phones, address, birthday, notes = extract_contact_info(file_path)
            if contact_name_vcf.lower() == contact_name.lower():
                contact_info = []
                if emails:
                    contact_info.extend(emails)
                if phones:
                    contact_info.extend(phones)
                if address:
                    contact_info.append(address)
                if birthday:
                    contact_info.append(f"Birthday: {birthday}")
                if notes:
                    contact_info.append(f"Notes: {notes}")

                send_to_android_tv(contact_name_vcf, contact_info)

                read_out_contact_info(contact_name_vcf, contact_info)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py <contact_name>")
        sys.exit(1)

    contact_name_arg = sys.argv[1]

    process_vcf_files(VCF_FILES_DIRECTORY, contact_name_arg)

```

<br><br>


