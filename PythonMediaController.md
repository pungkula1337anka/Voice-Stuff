
<h1 align="center">
<br>

__Python Media Controller__

<img src="https://raw.githubusercontent.com/pungkula1337anka/Voice-Stuff/main/asset/pythonmedia.png">


</h1><br>

<br><br><br>


# __Full media control in one Python script.__ <br>

The beuty about doing, whats called an "fuzzy search" like this, is that it allows you to (most likely) call an artists name which are not in your native language.
Even if the STT generates the wrong word, the python script will still _(try to)_ point you to the right directory path.<br>


__Available types:__

1. 🎙️ __Podcast__  <br>
Fuzzy searches a Podcast directory, lists all files in that directory, orders them after creation date. Sends them to your HA media player for playback.
I use the container based service [Podgrab](https://github.com/akhilrex/podgrab) to automatically download new episodes.  
And this [PyPodCleanup](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/PyPodCleanup.md) script to automatically  remove old episodes.  

2. 🔀 __Jukebox__  <br>
Shuffles & randomizes 150 songs from your music directory. <br>
Sends them back to your HA media player for playback. <br>

3. 🎵 __Music__ <br>
Fuzzy searches your music directory for an artist (folder) of your choice. <br>
Lists all files in that folder and creates a temporary playlist which are shuffled and sent back to your HA media player. <br>

4. 🎵 __Song__  <br>
Fuzzy searches your music directory and all its subdirectories for an song. <br>
Song is sent back to your media player to enjoy. <br>

5. 📽️ __Movie__ <br>
Fuzzy searches for a movie title (folder in your movie directory). <br>
Lists all file inside that folder, order them after filepath name, and sends them back to your media player. <br>

6. 📖 __Audiobook__  <br>
Fuzzy searches your audiobook directory for a folder. <br>
Lists all files in that folder, order them by filepath name and sends to media player.

6. 📹 __OtherVideos__ <br>
Fuzzysearches for a file in your othervideos directory. <br> 
File is played on your media player.

7. 🎵 __Musicvideos__ <br>
Searches your musicvideo directory, for an artist (folder). <br>
list all files, shuffles & randomizes before playback. <br>

8. 📺 __TV__ <br>
Searches your TV directory for a TV Show (folder).
Lists all files in that directory and all its subdirectories, shuffles them all and randomizes order. <br>
Sends them all to your media_player.  

9. 🎼 __Playlist__  <br>
Specify full filepath in search query.
Playlist is played on media_player in argument when running the script.
I use [this](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/PyAddSongToPlaylist.md) script to add sobgs to my playlist.  


10. 🗞️ __News__ <br>
Define your newscasts RESTful API's in the Python file. <br>
If the newscast items has not been heard before, they will be played. _(if played before, they are skipped)_ <br>
The script stores some data about played items in a .txt file in your config directory, <br>
dont worry though, the script wont let it get big and strong. <br>

11. 📡 __Live-TV__ <br>
_???_
 
<br> 

I __strongly__ recommend creating an presence media player sensor with a template, for full automation support. <br>
Start by creating a template sensor that simply states what room you are in. <br> 
I did this with the attributes of my motion sensors. <br>
If you need help I suggest asking nicely [here](https://discord.com/channels/330944238910963714/672223497736421388).  <br>

<br>


- **1: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **2: Custom Sentences** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it `MediaController.yaml`<br>
I will use `IntentName.yaml` as an example here, fill this yaml file with the code from below, edit for your language. <br>

- **3: Shell command** <br>

If you dont have it already, create the file `shell_command.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `shell_command: !include shell_command.yaml`<br> 

- **4: Python Script** <br>

Create the file `media_controller.py` inside your /config folder. <br>
Paste in wall of text at bottom. <br>


<br><br>




## 🦆 /config/intent_script.yaml <br>

You can define your playlist path in the template.

<br>


```
MediaController:
  action:
    - service: shell_command.media_controller
      data: 
        search: >
          "{% if typ == 'playlist' %}/media/MyPlaylist2.m3u{% else %}'{{ search | default(0) }}'{% endif %}"
        typ: "{{typ}}"
```

<br><br>


## 🦆 /config/custom_sentences/sv/MediaController.yaml <br>

Before you hastly delete my words and insert your own, take a look at how I did this. <br>
This setup & with the search defaulting to `0`, enables me to skip the search part and just say `spela upp musik` to trigger the jukebox intent. <br>
and also say `spela upp spellistan` for insant playlist playback. <br>

<br>


```
language: "sv"
intents:
  MediaController:
    data:
      - sentences:
          - "kör igång {typ} {search}"
          - "(spel|spela) [upp] {typ} {search}"
          - "jag vill se {typ} {search}"
          - "spela [upp] {typ} "
          - "jag vill höra {typ} {search}"
lists:
  search:
    wildcard: true
  typ:
    values:
      - in: "(serie|serien|tvserien|tv-serien|tv serien)"
        out: "tv"  
      - in: "(podd|pod|podcast|podcost|poddan|podden)"
        out: "podcast"
      - in: "(slump|slumpa|random|musik)"
        out: "jukebox"
      - in: "(artist|artisten|band|bandet|grupp|gruppen)"
        out: "music"        
      - in: "(låt|låten|sång|sången)"
        out: "song" 
      - in: "(film|filmen)"
        out: "movie"        
      - in: "(ljudbok|ljudboken)"
        out: "audiobook"       
      - in: "video"
        out: "othervideo"       
      - in: "(musik video|music video)"
        out: "musicvideo"              
      - in: "(spellista|spellistan|spel lista|spel listan|playlist)"
        out: "playlist"        
      #- in: ""
      #  out: "livetv"   
```

<br><br>


## 🦆 /config/shell_command.yaml <br>

You can define your media player at the end of the shell command. <br>
_(or preferbly presence media player)_

<br>

```
    media_controller: 'python media_controller.py "{{ search }}" {{ typ }} {{ states("sensor.presence_media_player") }}'
```

<br><br>


## 🦆 /config/media_controller.py <br>

Don't forget to define your Home Assistant IP, long lived acess token, media directories.<br>
Also in case you want your own local newscasts, please define their RESTful API's in this file aswell.
<br>


```
import os
import sys
import random
import time
import requests
import difflib
from difflib import get_close_matches

###########################################################
#### Define your shit here please. #####
HOME_ASSISTANT_IP = "YOUR_IP:YOUR_PORT"
ACCESS_TOKEN = "YOUR_LONG_LIVED_ACESS_TOKEN"
SEARCH_FOLDERS = {
    "tv": "/media/TV",
    "music": "/media/Music",
    "movie": "/media/Movies",
    "podcast": "/media/Podcasts",
    "musicvideo": "/media/Music_Videos",
    "audiobooks": "/media/Audiobooks",
    "othervideos": "/media/Other_Videos",
    "livetv": "/media/IPTV",
    "jukebox": "/media/Music",
    "song": "/media/Music"
}
NEWS_MEDIA_PLAYER = "media_player.ha"
PLAYED_NEWS_FILE = "played_news.txt"
MAX_PLAYED_NEWS_ENTRIES = 350
NEWS_API_LIST = [
    "http://api.sr.se/api/v2/news/episodes?format=json",
    "http://api.sr.se/api/v2/podfiles?programid=178&format=json",
    "http://api.sr.se/api/v2/podfiles?programid=5524&format=json",
    "http://api.sr.se/api/v2/podfiles?programid=5413&format=json"
]
DELAY_BETWEEN_SERVICE_CALLS = 0
###########################################################

news_list = []
def clean_search_query(query):
    """
    This function removes punctuation from the search query.
    """
    cleaned_query = query.replace('.', '').replace(',', '')
    return cleaned_query

def template_directory_path(directory_path):
    """
    This function templates the directory path.
    """
    return "media-source://media_source/local" + os.path.abspath(directory_path).split("/media")[-1]

def list_files(directory):
    """
    This function lists all files recursively in the given directory.
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(('.nfo', '.png', '.gif', '.m3u', '.jpg', '.jpeg')):
                file_list.append(os.path.join(root, file))
    return file_list

def find_closest_directory(query, directories):
    """
    This function finds the closest directory match for the given query.
    """
    closest_match = get_close_matches(query, directories, n=1)
    if closest_match:
        return closest_match[0]
    else:
        return None

def find_closest_file(query, files):
    """
    This function finds the closest file match for the given query.
    """
    closest_match = None
    max_ratio = 0
    for file in files:
        filename = os.path.splitext(os.path.basename(file))[0]  
        ratio = difflib.SequenceMatcher(None, query, filename).ratio()
        if ratio > max_ratio:
            max_ratio = ratio
            closest_match = file
    
    if closest_match:
        return closest_match
    else:
        return None

def send_service_call(media_content_id, enqueue, media_player_entity_id):
    """
    This function sends a service call to Home Assistant.
    """
    url = f"http://{HOME_ASSISTANT_IP}/api/services/media_player/play_media"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "entity_id": media_player_entity_id,
        "media_content_id": media_content_id,
        "media_content_type": "music",
        "extra": {
            "enqueue": enqueue
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Service call successful.")
    else:
        print(f"Service call failed with status code: {response.status_code}")

def read_m3u_file(file_path):
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return []

    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if not line.startswith('#')]

    return lines

def fetch_news():
    global news_list
    news_list.clear()

    for api in NEWS_API_LIST:
        response = requests.get(api)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("episodes", []) + data.get("podfiles", []):
                url = item.get("downloadpodfile", {}).get("url") or item.get("url")
                if url:
                    news_list.append(url)
    print("Fetched news:", news_list)

def send_news_service_call(media_content_id, enqueue=False):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "entity_id": NEWS_MEDIA_PLAYER,
        "media_content_id": media_content_id,
        "media_content_type": "music",
        "extra": {"enqueue": enqueue}
    }
    response = requests.post(f"http://{HOME_ASSISTANT_IP}/api/services/media_player/play_media", headers=headers,
                             json=data)
    print("Service call response:", response.text)
    return response.status_code

def load_played_news():
    if os.path.exists(PLAYED_NEWS_FILE):
        with open(PLAYED_NEWS_FILE, "r") as f:
            return set(f.read().splitlines()[:MAX_PLAYED_NEWS_ENTRIES])
    return set()

def save_played_news():
    with open(PLAYED_NEWS_FILE, "w") as f:
        f.write("\n".join(played_news))

def mainnews():
    global played_news
    played_news = load_played_news()
    fetch_news()
    if len(news_list) == 0:
        print("No new newscasts available.")
        return

    if news_list[0] not in played_news:
        status_code = send_news_service_call(news_list[0], enqueue=False)
        if status_code == 200:
            print(f"Sent service call for {news_list[0]}")
            played_news.add(news_list[0])
        else:
            print(f"Failed to send service call for {news_list[0]}")

    for news_item in news_list[1:]:
        if news_item not in played_news:
            time.sleep(1)  
            status_code = send_news_service_call(news_item, enqueue=True)
            if status_code == 200:
                print(f"Sent service call for {news_item}")
                played_news.add(news_item)
            else:
                print(f"Failed to send service call for {news_item}")

    save_played_news()

    if len(played_news) > MAX_PLAYED_NEWS_ENTRIES:
        played_news = set(list(played_news)[-MAX_PLAYED_NEWS_ENTRIES:])
        save_played_news()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python media_controller.py <search_query/m3u_file> <type> <media_player_entity_id>")
        sys.exit(1)

    query_or_file = sys.argv[1]
    directory_type = sys.argv[2].lower()
    media_player_entity_id = sys.argv[3]

    if directory_type == "news":
        mainnews()
    else:
        if directory_type == "playlist":
            lines = read_m3u_file(query_or_file)

            clear_playlist_url = f"http://{HOME_ASSISTANT_IP}/api/services/media_player/clear_playlist"
            clear_playlist_data = {}
            clear_playlist_headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            requests.post(clear_playlist_url, json=clear_playlist_data, headers=clear_playlist_headers)

            if lines:
                send_service_call(media_content_id=lines[0], enqueue=False, media_player_entity_id=media_player_entity_id)
                time.sleep(DELAY_BETWEEN_SERVICE_CALLS) 

            for line in lines[1:]:
                send_service_call(media_content_id=line, enqueue=True, media_player_entity_id=media_player_entity_id)
                time.sleep(DELAY_BETWEEN_SERVICE_CALLS)  
        else:
            search_query = clean_search_query(query_or_file)


            if directory_type == "musicvideo":
                if directory_type not in SEARCH_FOLDERS:
                    print("Invalid directory type.")
                    sys.exit(1)

                search_directory = SEARCH_FOLDERS[directory_type]
                directories = [d for d in os.listdir(search_directory) if os.path.isdir(os.path.join(search_directory, d))]
                
                closest_directory = find_closest_directory(search_query, directories)
                if not closest_directory:
                    print("No directory matching the search query found.")
                    sys.exit(1)

                search_directory = os.path.join(search_directory, closest_directory)
                files = list_files(search_directory)

                clear_playlist_url = f"http://{HOME_ASSISTANT_IP}/api/services/media_player/clear_playlist"
                clear_playlist_data = {}
                clear_playlist_headers = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                }
                requests.post(clear_playlist_url, json=clear_playlist_data, headers=clear_playlist_headers)

                files.sort()

                for i, file in enumerate(files):
                    media_content_id = template_directory_path(file)
                    if i == 0:
                        send_service_call(media_content_id, False, media_player_entity_id)
                    else:
                        send_service_call(media_content_id, True, media_player_entity_id)
                    time.sleep(DELAY_BETWEEN_SERVICE_CALLS)




            if directory_type == "movie":
                if directory_type not in SEARCH_FOLDERS:
                    print("Invalid directory type.")
                    sys.exit(1)

                search_directory = SEARCH_FOLDERS[directory_type]
                directories = [d for d in os.listdir(search_directory) if os.path.isdir(os.path.join(search_directory, d))]
                
                closest_directory = find_closest_directory(search_query, directories)
                if not closest_directory:
                    print("No directory matching the search query found.")
                    sys.exit(1)

                search_directory = os.path.join(search_directory, closest_directory)
                files = list_files(search_directory)

                clear_playlist_url = f"http://{HOME_ASSISTANT_IP}/api/services/media_player/clear_playlist"
                clear_playlist_data = {}
                clear_playlist_headers = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                }
                requests.post(clear_playlist_url, json=clear_playlist_data, headers=clear_playlist_headers)

                files.sort()

                for i, file in enumerate(files):
                    media_content_id = template_directory_path(file)
                    if i == 0:
                        send_service_call(media_content_id, False, media_player_entity_id)
                    else:
                        send_service_call(media_content_id, True, media_player_entity_id)
                    time.sleep(DELAY_BETWEEN_SERVICE_CALLS)
            elif directory_type == "jukebox":
                search_directory = SEARCH_FOLDERS[directory_type]
                files = list_files(search_directory)
                random.shuffle(files)
                for i, file in enumerate(files[:100]):
                    media_content_id = template_directory_path(file)
                    if i == 0:
                        send_service_call(media_content_id, False, media_player_entity_id)
                    else:
                        send_service_call(media_content_id, True, media_player_entity_id)
                    time.sleep(DELAY_BETWEEN_SERVICE_CALLS)
            elif directory_type == "livetv":
                trigger_home_assistant_automation(search_query)
            elif directory_type == "song":
                search_directory = SEARCH_FOLDERS[directory_type]
                files = list_files(search_directory)
                closest_file = find_closest_file(search_query, files)
                if closest_file:
                    media_content_id = template_directory_path(os.path.join(search_directory, closest_file))
                    send_service_call(media_content_id, False, media_player_entity_id)
                else:
                    print("No closest match found.")
            elif directory_type == "othervideos":
                if directory_type not in SEARCH_FOLDERS:
                    print("Invalid directory type.")
                    sys.exit(1)

                search_directory = SEARCH_FOLDERS[directory_type]
                files = list_files(search_directory)
                
                closest_file = find_closest_file(search_query, files)
                if closest_file:
                    media_content_id = template_directory_path(closest_file)
                    send_service_call(media_content_id, False, media_player_entity_id)
                else:
                    print("No closest match found.")
            else:
                if directory_type not in SEARCH_FOLDERS:
                    print("Invalid directory type.")
                    sys.exit(1)

                search_directory = SEARCH_FOLDERS[directory_type]
                directories = [d for d in os.listdir(search_directory) if os.path.isdir(os.path.join(search_directory, d))]

                closest_directory = find_closest_directory(search_query, directories)
                if closest_directory:
                    templated_directory_path = template_directory_path(os.path.join(search_directory, closest_directory))
                    files = list_files(os.path.join(search_directory, closest_directory))
                    if directory_type in ["music", "tv"]:
                        random.shuffle(files)
                    else:
                        files.sort()

                    clear_playlist_url = f"http://{HOME_ASSISTANT_IP}/api/services/media_player/clear_playlist"
                    clear_playlist_data = {}
                    clear_playlist_headers = {
                        "Authorization": f"Bearer {ACCESS_TOKEN}",
                        "Content-Type": "application/json"
                    }
                    requests.post(clear_playlist_url, json=clear_playlist_data, headers=clear_playlist_headers)

                    for i, file in enumerate(files[:150]):
                        media_content_id = template_directory_path(file)
                        if i == 0:
                            send_service_call(media_content_id, False, media_player_entity_id)
                        else:
                            send_service_call(media_content_id, True, media_player_entity_id)
                        time.sleep(DELAY_BETWEEN_SERVICE_CALLS)
                else:
                    print("Sorry, try again.")

```

<br><br>

