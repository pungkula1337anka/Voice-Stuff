
<h1 align="center">
<br>

__Guest Arrival__

</h1><br>
<br><br>

Knock Knock, who's there? <br>
This will notify you before your guests arrive __(If they are auto connecting to your WiFi)__ <br>
Also sends notification with MAC when unknown device connects. 

 
<br><br>



- **1: Python script** <br>

If you dont have it already, add `python_script:` to your `configuration.yaml` file. 
Create the file `guest_arrival.py` in `config/python_scripts` _(create the folder if you dont have it)_
Paste in the python script below, and start defining your devices, and then your guests devices.
Add your own actions.

- **2: Automation to trigger** <br>

You will ofcourse have to have some way of getting the MAC adresses.  <br>
Im sure you can find a integration that does that for you. _(I use AsusWRT integration)_ <br>
Then create an automation that looks something similiar to below. <br>

<br><br>




## 🦆 /config/python_scripts/guest_arrival.py <br>

Dont forget to define your own and your guests devices.  
<br>


```
# define your devices here
my_devices = {
    #"Your_Device1": "XX:XX:XX:XX:XX:XX",
    #"Your_Device2": "XX:XX:XX:XX:XX:XX",
    #"Your_Device3": "XX:XX:XX:XX:XX:XX",
    # ...
}

# define friends devices here.
friends_devices = {
    "friend1": "XX:XX:XX:XX:XX:XX",    
    "friend2": "XX:XX:XX:XX:XX:XX",   
    "friend3": "XX:XX:XX:XX:XX:XX",   
    # ...
}

mac_addresses = data.get("mac_addresses", [])
print("Received MAC addresses:", mac_addresses)


for mac_address in mac_addresses:
    if not mac_address or mac_address == '00:00:00:00:00:00':
        print("Invalid MAC address:", mac_address)
        continue

    if mac_address in friends_devices.values():

        print("Friend's device MAC address:", mac_address)
        friendly_device_name = [name for name, mac in friends_devices.items() if mac == mac_address][0]
        print("Friendly device name:", friendly_device_name)
        
######## define actions for friend device connected 
        friendly_device_message = f"oj nu kommer . . {friendly_device_name} vilken ära. . nu kommer {friendly_device_name} "
        hass.services.call("tts", "speak", {
            "entity_id": "tts.piper",
            "message": friendly_device_message,
            "cache": True,
            "media_player_entity_id": "media_player.tts",
            "language": "sv_SE"
        })
    elif mac_address in my_devices.values():
        print("Your device MAC address:", mac_address)

    else:
        print("Stranger's device MAC address:", mac_address)
        
####### define actions for unknown device connected 
        hass.services.call("notify", "mobile_app_YOUR_iPHONE", {
            "title": "Unknown Device Connected",
            "message": f"A device with MAC address {mac_address} has connected to your network.",
            "data": {
                "push": {
                    "sound": {
                        "name": "default",
                        "critical": 1,
                        "volume": 0.7
                    }
                },
                "tag": "mac"
            }
        })
```

<br><br>



## 🦆 Example automation <br>


<br>


```
alias: Guest Arrival Notification
trigger:
  - platform: state
    entity_id: sensor.router_connected_devices
condition: []
action:
  - service: python_script.guest_arrival
    data_template:
      mac_addresses: >-
        {{ trigger.from_state.attributes.devices | map(attribute='mac') | list
        }}
mode: single
```

<br><br>

