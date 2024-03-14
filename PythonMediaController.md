
<h1 align="center">
<br>
__Python Media Controller__

<img src="https://raw.githubusercontent.com/pungkula1337anka/Voice-Stuff/main/asset/pythonmedia.png">


</h1><br>

<br><br><br>


# __Full media control in one Python script.__ <br>

The beuty about doing, whats called an "fuzzy search" like this, is that it allows you to (most likely) call an artists name which are not in your native language.
Even if the STT generates the wrong word, the python script will still _(try to)_ point you to the right directory path.<br>
5 simple steps to control all your media by voice.. <br>

<br>

_Example usage:_

```
- "Start playing tvshow family guy"
- "Start playing movie godzilla"
- "Start playing channel 6"
- "Start playing artist the rolling stones"
- "Start playing song death to all but metal"
- "Start playing music"
- "Start playing youtube funny cats"
- "Start playing podcast self hosted"
[...]
```
<br>

__Available types:__

1. 🎬 __YouTube__  <br> 
Plays <search_query>'s closeest match on YouTube. <br>
Specify a `remote.*` entity. _(not `media_player.*`)_ <br>
_Requires API key._ <br>

2. 🎙️ __Podcast__  <br>
Fuzzy searches a Podcast directory, lists all files in that directory, orders them after creation date. Sends them to your HA media player for playback.
I use the container based service [Podgrab](https://github.com/akhilrex/podgrab) to automatically download new episodes.  
And this [PythonPodCleanup](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/PythonPodCleanup.md) script to automatically  remove old episodes.  

3. 🔀 __Jukebox__  <br>
Shuffles & randomizes 150 songs from your music directory. <br>
Sends them back to your HA media player for playback. <br>

4. 🎵 __Music__ <br>
Fuzzy searches your music directory for an artist (folder) of your choice. <br>
Lists all files in that folder and creates a temporary playlist which are shuffled and sent back to your HA media player. <br>

5. 🎵 __Song__  <br>
Fuzzy searches your music directory and all its subdirectories for an song. <br>
Song is sent back to your media player to enjoy. <br>

6. 📽️ __Movie__ <br>
Fuzzy searches for a movie title (folder in your movie directory). <br>
Lists all file inside that folder, order them after filepath name, and sends them back to your media player. <br>

7. 📖 __Audiobook__  <br>
Fuzzy searches your audiobook directory for a folder. <br>
Lists all files in that folder, order them by filepath name and sends to media player.

8. 📹 __OtherVideos__ <br>Fuzzysearches for a file in your othervideos directory. <br> 
File is played on your media player.

9. 🎵 __Musicvideos__ <br>
Searches your musicvideo directory, for an artist (folder). <br>
list all files, shuffles & randomizes before playback. <br>

10. 📺 __TV__ <br>
Searches your TV directory for a TV Show (folder).
Lists all files in that directory and all its subdirectories, shuffles them all and randomizes order. <br>
Sends them all to your media_player.  

11. 🎼 __Playlist__  <br>
Specify full filepath in search query.
Playlist is played on media_player in argument when running the script.
I use [this](https://github.com/pungkula1337anka/Voice-Stuff/blob/main/PythonSong2Playlist.md) script to add sobgs to my playlist.  

12. 🗞️ __News__ <br>
Define your newscasts RESTful API's in the Python file. <br>
If the newscast items has not been heard before, they will be played. _(if played before, they are skipped)_ <br>
The script stores some data about played items in a .txt file in your config directory, <br>
dont worry though, the Python wont let it get big and grow strong. <br>

13. 📡 __Live-TV__ <br>
Specify a `remote.*` entity. _(not `media_player.*`)_ <br>
Edit your `.m3u` file and split your channels so that each channel has its own `.m3u` file. <br>
Name each file by channel word you want to use and place it inside the directory `/config/www/live/`? <br>
_This only seems to work if the `*.m3u` is pPublicly accessible, so define your domain?_ <br>
 
<br> <br>


## 🦆 __getting started__ <br>


- **1: Presence Media Player** <br>

I __strongly__ recommend creating an presence media player sensor with a template, for full automation support. <br>
Amd the way we will do this will also enable auto switching between `media_player` and `remote` entity. <br>
Examples are below. <br>
If you need help I suggest asking nicely [here](https://discord.com/channels/330944238910963714/672223497736421388).  <br>

- **2: Intent Script** <br>

If you dont have it already, create the file `intent_script.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `intent_script: !include intent_script.yaml`<br> 

- **3: Custom Sentences** <br>

Create a folder called `custom_sentences` inside your /config dir.<br>
Inside that folder, once again create a folder named with your language code. `sv` for swedish, `en` for english.<br>
In that folder you create a file and name it `MediaController.yaml`<br>

- **4: Shell command** <br>

If you dont have it already, create the file `shell_command.yaml` in the /config dir and fill in the code below.<br>
(dont forget to reference it in `configuration.yaml` with `shell_command: !include shell_command.yaml`<br> 

- **5: Python Script** <br>

Create the file `media_controller.py` inside your /config folder. <br>
Paste in wall of text at bottom of this page. <br>
This scipt serves as is, if your looking for transcoding, this is not it. 
YouTube API Key can be created [here](https://developers.google.com/youtube/registering_an_application). <br>
Dont forget to define your stuff _and .........._ <br>
__yay__ <br>
  - 🎉 _congratulations! 🎉 you can now control_ <br>
    - _your media like a pro voice ninja!_  <br>
<br><br>


## 🦆 1 presence media player <br>

Jinja Time!
Start by creating a template sensor that simply states what room you are in. <br> 
I did this with the state and attributes of my motion sensors. <br>

_Example  templates_

```
# sensor.presence

{% set hall_state = states('binary_sensor.motion_sensor_hall_occupancy') %}
{% set kitchen_state = states('binary_sensor.motion_sensor_kok_occupancy') %}
{% set bedroom_state = states('binary_sensor.motion_sensor_sovrum_occupancy') %}
{% set YOU_state = states('device_tracker.YOU') %}

{% if YOU_state == 'away' %}
  Away
{% else %}
  {% if hall_state == 'off' and kitchen_state == 'off' and bedroom_state == 'off' %}
    {% set hall_last_seen = states('sensor.motion_sensor_hall_last_seen') %}
    {% set kitchen_last_seen = states('sensor.motion_sensor_kitchen_last_seen') %}
    {% set bedroom_last_seen = states('sensor.motion_sensor_sovrum_last_seen') %}
    
    {% set last_seen_times = [hall_last_seen, kitchen_last_seen, bedroom_last_seen] %}
    {% set latest_last_seen_time = last_seen_times | max %}
    
    {% if latest_last_seen_time == hall_last_seen %}
      Hallway
    {% elif latest_last_seen_time == kitchen_last_seen %}
      Kitchen
    {% elif latest_last_seen_time == bedroom_last_seen %}
      Bedroom
    {% endif %}
  {% else %}
    {% if hall_state == 'on' %}
      Hallway
    {% elif kitchen_state == 'on' %}
      Kitchen
    {% elif bedroom_state == 'on' %}
      Bedroom
    {% endif %}
  {% endif %}
{% endif %}


# sensor.presence_media_player
# only display entity name, entity type (remote/media_player) will be added by the intent script

{% set presence = states('sensor.presence') %}
 {% if presence == 'Kitchen' %}
   player1
 {% elif presence == 'Livingroom' %}
   player2
 {% elif presence == 'Bedroom' %}
   player3
 {% elif presence == 'Away' %}
   all
 {% elif presence == 'Unknown' %}
   all            
 {% endif %}
```
<br>

## 🦆 2 /config/intent_script.yaml <br>

You can define your music playlist path in the template.

<br>

```
MediaController:
  action:
    - service: shell_command.media_controller
      data: 
        search: >
          "{% if typ == 'playlist' %}/media/MyPlaylist2.m3u{% else %}'{{ search | default(0) }}'{% endif %}"
        typ: "{{typ}}"
        player: >
          "{% if typ == 'youtube' or typ == 'livetv' %}remote.{{ states('sensor.presence_media_player') }}{% else %}media_player.{{ states('sensor.presence_media_player') }}{% endif %}"
  speech:
    text: "inga problem ja fixar det mannen" 
```

<br>

## 🦆 3 /config/custom_sentences/sv/MediaController.yaml <br>

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
          - "(spel|spell|spela) [upp] {typ} {search}"
          - "(start|starta|startar) {typ} {search}"
          - "jag vill se {typ} {search}"
          - "(spel|spell|spela) [upp] {typ} "
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
      - in: "(nyheter|nyheterna|senaste nytt)"
        out: "news"   
      - in: "(kanal|kanalen|kannal)"
        out: "livetv"
      - in: "(youtube|yutube|yotub|tuben)"
        out: "youtube"
```

<br>

## 🦆 4 /config/shell_command.yaml <br>


<br>

```
    media_controller: 'python media_controller.py "{{ search }}" {{ typ }} {{ player }}'
```

<br>

## 🦆 5 /config/media_controller.py <br>

Don't forget to define your Home Assistant IP, long lived acess token, media directories.<br>
In case you want your own local newscasts, please define their RESTful API's in this file aswell. <br>
_API [key](https://developers.google.com/youtube/registering_an_application) is required for YouTube_ <br>
_Remote entity is required for live-TV & YouTube_ <br>


```
# media_controller.py

import os
import sys
import random
import time
import requests
import difflib
from difflib import get_close_matches
from urllib.parse import urlencode

##########################################################################
#### --> Define your shit here please <-- ####

HOME_ASSISTANT_IP = "YOUR_HOME_ASSISTANT_IP:8123"
ACCESS_TOKEN = "YOUR_LONG_LIVED_TOKEN_HERE"
YOUTUBE_API_KEY = 'YOUR_API_KEY_HERE'
YOUR_DOMAIN = "example.duckdns.org:8123"
PLAYED_NEWS_FILE = "played_news.txt"
MAX_PLAYED_NEWS_ENTRIES = 350
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
NEWS_API_LIST = [
    "http://api.sr.se/api/v2/news/episodes?format=json",
    "http://api.sr.se/api/v2/podfiles?programid=178&format=json",
    "http://api.sr.se/api/v2/podfiles?programid=5524&format=json",
    "http://api.sr.se/api/v2/podfiles?programid=5413&format=json"
]
DELAY_BETWEEN_SERVICE_CALLS = 0


##### --> Thank you! <-- ####
##########################################################################


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
        filename = os.path.splitext(os.path.basename(file))[0]  # Extracting filename without extension
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


def send_news_service_call(media_content_id, entity_id, enqueue=False):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "entity_id": entity_id,
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


def mainnews(entity_id):
    global played_news
    played_news = load_played_news()
    fetch_news()
    if len(news_list) == 0:
        print("No new newscasts available.")
        return

    for index, news_item in enumerate(news_list):
        if news_item not in played_news:
            if index == 0:
                # First news item, enqueue should be False
                status_code = send_news_service_call(news_item, entity_id, enqueue=False)
            else:
                status_code = send_news_service_call(news_item, entity_id, enqueue=True)

            if status_code == 200:
                print(f"Sent service call for {news_item}")
                played_news.add(news_item)
                save_played_news()
                time.sleep(1)  
            else:
                print(f"Failed to send service call for {news_item}")

    if len(played_news) > MAX_PLAYED_NEWS_ENTRIES:
        played_news = set(list(played_news)[-MAX_PLAYED_NEWS_ENTRIES:])
        save_played_news()


def search_youtube(query):
    params = {
        'q': query,
        'part': 'snippet',
        'type': 'video',
        'maxResults': 5, 
        'key': YOUTUBE_API_KEY
    }
    url = f'https://www.googleapis.com/youtube/v3/search?{urlencode(params)}'
    print("Request URL:", url)  

    response = requests.get(url)
    print("Response status code:", response.status_code)
    print("Response content:", response.content)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and data['items']:
            video_id = data['items'][0]['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            return video_url, data['items'][0]['snippet']['title']
        else:
            print("No videos found for the given search query.")
            return None, None
    else:
        print(f"Failed to retrieve videos. Status code: {response.status_code}")
        return None, None


def send_youtube_service_call(video_url, entity_id):
    service_data = {
        'activity': video_url,
        'entity_id': entity_id
    }

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    url = f'http://{HOME_ASSISTANT_IP}/api/services/remote/turn_on'

    response = requests.post(url, json=service_data, headers=headers)
    print("Service call response:", response.status_code)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("PythonMediaController usage: python media_controller.py <search_query/m3u_file> <type> <media_player/remote_entity_id>")
        sys.exit(1)

    query_or_file = sys.argv[1]
    type_or_entity_id = sys.argv[2].lower()
    media_player_entity_id = sys.argv[3]

    if type_or_entity_id == "news":
        mainnews(media_player_entity_id)
    elif type_or_entity_id == "playlist":
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
    elif type_or_entity_id == "youtube":
        search_query = clean_search_query(query_or_file)
        video_url, video_title = search_youtube(search_query)

        if video_url:
            print(f"Starting to play video: {video_title}: {video_url}")
            send_youtube_service_call(video_url, media_player_entity_id)
        else:
            print("No videos found for the given search query.")
    else:
        search_query = clean_search_query(query_or_file)

        if type_or_entity_id == "livetv":
            media_content_id = f"https://{YOUR_DOMAIN}/local/live/{search_query}/{search_query}.m3u"
            service_data = {
                "activity": media_content_id,
                "entity_id": media_player_entity_id
            }
            service_url = f"http://{HOME_ASSISTANT_IP}/api/services/remote/turn_on"
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            response = requests.post(service_url, json=service_data, headers=headers)
            if response.status_code == 200:
                print("Live TV service call successful.")
            else:
                print(f"Failed to send live TV service call with status code: {response.status_code}")
        elif type_or_entity_id == "jukebox":
            search_directory = SEARCH_FOLDERS[type_or_entity_id]
            files = list_files(search_directory)
            random.shuffle(files)
            for i, file in enumerate(files[:100]):
                media_content_id = template_directory_path(file)
                if i == 0:
                    send_service_call(media_content_id, False, media_player_entity_id)
                else:
                    send_service_call(media_content_id, True, media_player_entity_id)
                time.sleep(DELAY_BETWEEN_SERVICE_CALLS)
        else:
            if type_or_entity_id not in SEARCH_FOLDERS:
                print("Invalid directory type.")
                sys.exit(1)

            search_directory = SEARCH_FOLDERS[type_or_entity_id]
            directories = [d for d in os.listdir(search_directory) if
                           os.path.isdir(os.path.join(search_directory, d))]

            closest_directory = find_closest_directory(search_query, directories)
            if closest_directory:
                templated_directory_path = template_directory_path(
                    os.path.join(search_directory, closest_directory))
                files = list_files(os.path.join(search_directory, closest_directory))
                if type_or_entity_id in ["music", "tv"]:
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
                print("You must have meatballs in your mouth? Finish your dinner and try again.")
```

<br><br>


<h1 align="center">
<br>
 
# __🎈 thanks for coming this far 🎈__ 

</h1><br><br>
