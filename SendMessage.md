
<h1 align="center">
<br>

Send Messages

</h1><br>
<br><br>

Sends encrypted SMS from your phone. _(without your phone..)_   
I use [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) to set up a container with a rest API, that makes it possible to send and receive encrypted text messages.  

<br><br><br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentence** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it whatever you want, but remember it, cause it will be referencesd later.<br>
I will use `SendMessage.yaml` as an example here, fill this yaml file with the code from below. <br>


- **3: Setup the container** <br>

Use docker compose to throw up a signal-cli container with REST API support.  

- **4: Shell commands** <br>

Create the file 'shell_command.yaml' file in your /config dir and paste in the code below.  
Fill in your own phone number, and your contacts phone numbers.  
This will allow you to call the commands easily later.

<br><br>




## 🦆 /config/intent_script.yaml <br>


<br>


```
SendMessage:
  action:
    - service: shell_command.send_message
      data: 
        text: "{{text}}"
        number: "{{number}}"
  speech:
    text: "det är skickat bruschan"
```

<br><br>


## 🦆 /custon_sentences/sv/SendMessage.yaml <br>


<br>

```
language: "sv"
intents:
  SendMessage:
    data:
      - sentences:
          - "skriv till {number} {text}"
                    
lists:
  number:
    values:
      - in: "friend1"
        out: "+46111111111"
      - in: "friend2"
        out: "+46222222222" 
  text:
    wildcard: true
```

<br><br>


## 🦆 signal-cli-rest-api <br>

Link to [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api).  

<br>

signal-cli-rest-api  docker-compose

```
# [Stack Signal] - (signal-cli-rest-api)
# --- >> SIGNAL << --- #
version: "3"
services:
  signal-cli-rest-api:
    image: bbernhard/signal-cli-rest-api:latest
    environment:
      - MODE=normal #supported modes: json-rpc, native, normal
      #- AUTO_RECEIVE_SCHEDULE=0 22 * * * #enable this parameter on demand (see description below)
    ports:
      - "8080:8080" #map docker port 8080 to host port 8080.
    volumes:
      - "./signal-cli-config:/home/.local/share/signal-cli" #map "signal-cli-config" folder on host system into docker container. the folder contains the password and cryptographic keys when a new number is registered
```

<br>
When the container is up and running, from your Phone <br>
open Signal app and go to settings > link device > Scan QR <br>

and visit [localhost:8080/v1/qrcodelink?device_name=signal-api](http://localhost:8080/v1/qrcodelink?device_name=signal-api) and scan the QR code. <br>
  
__Bonus__ <br>


_If you want to be extra sneaky_ <br>

you could stop the signal container, remove the ports docker-compose and instead add `network_mode: "container:gluetun"` <br>

throw up a [Gluetun](https://github.com/qdm12/gluetun) container and start the containers.  

gluetun docker-compose _(edit for your prefered vpn)_

```
# [Stack VPN] - (Gluetun)
# --- >> GLUETUN << --- #
version: "3"
services:
  gluetun:
    image: qmcgaw/gluetun
    container_name: gluetun
    hostname: gluetun
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    ports:
      - 8888:8888/tcp  		# HTTP proxy
      - 8388:8388/tcp        	# Shadowsocks
      - 8388:8388/udp  	        # Shadowsocks
      - 8000:8000/tcp  		# Built-in HTTP control server
 #CONNECTED CONTAINERS  >>> ADD THIS TO THE CONTAINER > network_mode: "container:gluetun" <<<< <<<
      - 8080:8080               # signal-cli-rest-api
    volumes:
    #use this path if you are on HAOS
      - /mnt/data/supervisor/addons/local/gluetun/config:/gluetun
    environment:
      # See https://github.com/qdm12/gluetun/wiki
      - VPN_SERVICE_PROVIDER=PROVIDER
      - VPN_TYPE=openvpn
      # OpenVPN:
      - OPENVPN_USER=USER
      - OPENVPN_PASSWORD=PASSWORD
      #- SERVER_REGIONS=Gothenburg
      - FIREWALL_OUTBOUND_SUBNETS=255.255.255.0/24,192.168.1.0/24,192.168.65.0/24
      - HTTPPROXY=on
      - SHADOWSOCKS=on
      - SHADOWSOCKS_LOG=on
      - SHADOWSOCKS_CIPHER=chacha20-ietf-poly1305
      - SHADOWSOCKS_PASSWORD=PASSWORD123
      
      # Wireguard:
      #- WIREGUARD_PRIVATE_KEY=KEY
      #- WIREGUARD_ADDRESSES=ADESS
      
      # Timezone for accurate log times
      - TZ=Europe/Stockholm
      
  #### PRIVATE INTERNET ACESS EXAMPLE  #####  
      #- PRIVATE_INTERNET_ACCESS_VPN_PORT_FORWARDING=off
      #- OPENVPN_USER=USER
      #- OPENVPN_PASSWORD=PASSWORD
      #- SERVER_REGIONS=SE Stockholm
    
  #### PROTON VPN EXAMPLE #####  
      - VPN_SERVICE_PROVIDER=protonvpn
      - OPENVPN_USER=USER
      - OPENVPN_PASSWORD=PASSWORD
      - SERVER_COUNTRIES=COUNTRY
      #- VPN_PORT_FORWARDING=off
      #- VPN_PORT_FORWARDING_PROVIDER=protonvpn
    restart: always
```

## 🦆 /config/shell_command.yaml <br>


<br>


```
  send_message: >
    curl -X POST -H "Content-Type: application/json" 'http://YOUR_IP:YOUR_PORT/v2/send' \
       -d '{"message": "{{ text }}", "number": "+46YOUR_PHONE_NUMBER", "recipients": [ "{{ number }}" ]}' 
```

<br><br>

