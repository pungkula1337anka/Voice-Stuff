
<h1 align="center">
<br>
PlayArtist
</h1><br>
<br><br>
Searches /media/Music for chosen artist and plays the entire folder through your connected speakers.<br><br>
The good thing about doing, whats called an "fuzzy search" like this, is that it allows you to (most likely) call artist names that are not in your native language.<br> 
Even if the STT generates the wrong word, the python script will still point you to the right directory path.<br>
<br><br>

- 1: Add the SSH integration <br>

Settings > Devices and services > add integration & search for SSH.<br>

I found this to be the easiest way to run VLC through your connected speakers.<br>

- 2: Install VLC <br>

VLC is a media player that supports playback of entire folders.
Create the file 'install_vlc.sh' inside your /config directory and paste in the code below.
This script will install VLC package, and run a command which allows you to control it with an root priveledged user.
HA limitations to install packages, will require you to run this after each update, but this can easily be done through an automation.<br>

- 3: Create the shell commands. <br>

Create the file 'shell_command.yaml' file in your /config dir and paste in the code below.
This will allow you to call the scripts easily later.

- 4: Intent Script <br>

Create the file 'intent_script.yaml' file in the /config dir and fill in the code below.
Dont forget to add your credentials to the 'secrets.yaml' file!

- 5: Custom Sentence <br>

Create a folder called 'custom_sentences' inside your /config dir.
Inside that folder, once again create a folder named with your language code. 'sv' for swedish, 'en' for english.
In that folder you create a file called 'PlayArtist.yaml' and fill in the code from below. 

- 6: The fuzzy search python script <br>

This is where the magic happends. 
Within your /config dir, create a file called 'find_closest_directory.py'
Paste in the code at the bottom of this page. 

<br><br>
Your all set, try it out!<br><br>

## 🦆 /config/shell_command.yaml <br>


<br>
<br>

```
  py_find_closest_directory: "python find_closest_directory.py '{{ artist }}' /media/Music" <br>
  install_vlc: "sh install_vlc.sh"<br>
```

<br><br>


## 🦆 /config/intent_script.yaml <br>


<br><br>

```
PlayArtist:
  action:
    - service: shell_command.py_find_closest_directory
      data: 
        artist: "{{band}}"
      response_variable: search_result
    - service: ssh_command.exec_command
      data:
        host: !secret haos_ip
        port: 22
        user: !secret haos_user
        pass: !secret haos_auth
        command: "{{ search_result['stdout'] }}"
```

<br><br>


## 🦆 /custon_sentences/sv/PlayArtist.yaml <br>


<br><br>

```
language: "sv"
intents:
  PlayArtist:
    data:
      - sentences:
          - "spela upp (gruppen|bandet|artisten) {band}"
lists:
  band:
    wildcard: true   
```

<br><br>


## 🦆 /config/install_vlc.sh <br>


<br><br>

```
apk add vlc && sed -i 's/geteuid/getppid/' /usr/bin/vlc
```

<br><br>


## 🦆 /config/find_closest_directory.py <br>


<br><br>

```
import os
import sys
from difflib import get_close_matches

def find_closest_directory(query, directory):
    directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    closest_match = get_close_matches(query, directories, n=1)
    if closest_match:
        closest_dir = os.path.join(directory, closest_match[0])
        if not closest_dir.endswith('/'):
            closest_dir += '/'
        return closest_dir
    else:
        return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <search_query> <directory>")
        sys.exit(1)

    search_query = sys.argv[1]
    directory = sys.argv[2]

    closest_directory = find_closest_directory(search_query, directory)
    if closest_directory:
        print("cvlc add '{}' vlc://quit &".format(closest_directory))
    else:
        print("")
```


<br><br>
