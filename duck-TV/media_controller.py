### -->  duck-TV Voice Controller  <--   ###
##################################    
##### -> README <- ######
# https://github.com/pungkula1337anka/Voice-Stuff/tree/main/duck-TV
##################################
# Be sure to place this file inside your /config directory.
import os
import sys
import random
import time
import requests
import datetime
import difflib
import tempfile
import secrets
import string
from difflib import get_close_matches
from urllib.parse import urlencode
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### --> Define your shit here please <-- ###

# ~~~> REQUIRED <~~~ #
# Define your Home Assistant connection. 
HOME_ASSISTANT_IP = "YOUR_HOME_ASSISTANT_IP:8123"
ACCESS_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"

# Define your /media folders here. 
SEARCH_FOLDERS = {
    "tv": "/media/TV",
    "music": "/media/Music",
    "movie": "/media/Movies",
    "podcast": "/media/Podcasts",
    "musicvideo": "/media/Music_Videos",
    "audiobooks": "/media/Audiobooks",
    "othervideos": "/media/Other_Videos",
    "jukebox": "/media/Music",
}

# ~~~> REQUIRED for saving songs to playlist<~~~ #
# Define media_player & attribute for grabbing currently playing data.
ENTITY_ID = "media_player.shield"
ATTRIBUTE_NAME = "media_title"

# ~~~> REQUIRED for YouTube <~~~ #
# Grab your API Key from Google Developer.
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'

# ~~~> REQUIRED for Live-TV <~~~ #
# Define oyur Live-TV channels here.
livetv_channels = {
    "1": "http://example.com:1233/asdko23/291dmasi/93213",
    "2": "http://example.com:1233/asdko23/291dmasi/93213",
    "3": "http://example.com:1233/asdko23/291dmasi/93213",
    "4": "http://example.com:1233/asdko23/291dmasi/93213",
    "5": "http://example.com:1233/asdko23/291dmasi/93213",
}

# ~~~> REQUIRED for Newscasts <~~~ #
# Define your local News casts REST API's here.
NEWS_API_LIST = [
    "http://api.sr.se/api/v2/news/episodes?format=json",
    "http://api.sr.se/api/v2/podfiles?programid=178&format=json",
    "http://api.sr.se/api/v2/podfiles?programid=5524&format=json",
    "http://api.sr.se/api/v2/podfiles?programid=5413&format=json"
]

# ~~~> OPTIONAL FEATURES<~~~ #

# If you are having issues with Speech to Text translating or generating wrong words, you can correct them here, before they are processed into the script.
# You can also use this to create aliases for your live-TV channels and such.
CORRECTIONS = {
    "wrong word": "right word",
    "wrong word2": "right word2",
}


# Defining your default playlist to simplify automations.
DEFAULT_PLAYLIST = "/media/Playlists/MyPlaylist2.m3u"

# Stores recently played news data to avoid hearing duplicates.
PLAYED_NEWS_FILE = "played_news.txt"
MAX_PLAYED_NEWS_ENTRIES = 350
INTRO_URL = "https://drive.proton.me/urls/GF9374B97R#ZMSv2jz9JPBY"

# Only chnage if you know what you are doing. Default = "smb://"
WEBSERVER = "smb://"
### --> Thank you! <-- ###
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

news_list = []

def apply_corrections(query):
    """
    This function applies corrections to the search query.
    """
    corrected_query = CORRECTIONS.get(query, query)
    return corrected_query
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def preprocess_search_query():
    """
    This function preprocesses the search query before executing the main script.
    """
    if len(sys.argv) > 1:
        search_query = sys.argv[1]
        corrected_query = apply_corrections(search_query)
        sys.argv[1] = corrected_query

if __name__ == "__main__":
    preprocess_search_query()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def clean_search_query(query):
    """
    This function removes punctuation from the search query.
    """
    cleaned_query = query.replace('.', '').replace(',', '').replace('!', '')
    return cleaned_query
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def call_media_next_track_service(entity_id):
    service_data = {}
    call_service("media_player/media_next_track", service_data, entity_id)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def call_media_previous_track_service(entity_id):
    service_data = {}
    call_service("media_player/media_previous_track", service_data, entity_id)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def call_media_play_pause_service(entity_id):
    service_data = {}
    call_service("media_player/media_play_pause", service_data, entity_id)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def call_volume_up_service(entity_id):
    service_data = {}
    call_service("media_player/volume_up", service_data, entity_id)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def call_volume_down_service(entity_id):
    service_data = {}
    call_service("media_player/volume_down", service_data, entity_id)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def call_power_on_service(file_name):
    """
    This function sends a service call to Home Assistant to power on TV.
    """
    url = f"http://{HOME_ASSISTANT_IP}/api/services/remote/turn_on"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "entity_id": sys.argv[3]  
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("qwack")
    else:
        print(f"")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def call_power_off_service(file_name):
    """
    This function sends a service call to Home Assistant to power on TV.
    """
    url = f"http://{HOME_ASSISTANT_IP}/api/services/remote/turn_off"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "entity_id": sys.argv[3]  
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("qwack qwack.")
    else:
        print(f"")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def call_service(service, data, entity_id):
    url = f"http://{HOME_ASSISTANT_IP}/api/services/{service}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    service_data = {"entity_id": entity_id, **data}
    response = requests.post(url, json=service_data, headers=headers)
    if response.status_code == 200:
        print(f"Service call '{service}' successful.")
    else:
        print(f"")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def call_template_service():
    """
    This function gets the current Assist device.
    """
    template = """
    {% set sensor_states = namespace(last_sensor='', last_changed=None) %}
    {% for entity_id in states | selectattr('entity_id', 'match', 'binary_sensor.*assist_in_progress$') | map(attribute='entity_id') | list %}
        {% set state_obj = states[entity_id] %}
        {% if sensor_states.last_changed is none or state_obj.last_changed > sensor_states.last_changed %}
            {% set sensor_states.last_sensor = entity_id %}
            {% set sensor_states.last_changed = state_obj.last_changed %}
        {% endif %}
    {% endfor %}
    {{ sensor_states.last_sensor if sensor_states.last_sensor else 'None' }}
    """
    url = f"http://{HOME_ASSISTANT_IP}/api/template"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {"template": template}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.text  
    else:
        return None  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def template_directory_path(directory_paths):
    """
    This function templates the directory paths.
    """
    urls = []
    for directory_path in directory_paths:
        url = f"{WEBSERVER}{HOME_ASSISTANT_IP.split(':')[0]}/media{os.path.abspath(directory_path).split('/media')[-1]}"
        urls.append(url)
    return urls
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def save_media_content_urls(media_content_urls, file_name):
    """
    This function saves the media content URLs to a text file.
    """
    with open(f"www/playlist.m3u", "w") as file:
        file.write(INTRO_URL + '\n')
        for media_content_url in media_content_urls:
            file.write(media_content_url + '\n')
    send_service_call(file_name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def find_closest_directory(query, directories):
    """
    This function finds the closest directory match for the given query.
    """
    closest_match = get_close_matches(query, directories, n=1)
    if closest_match:
        return closest_match[0]
    else:
        return None
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def find_closest_files(query, directory, n=5):
    """
    This function finds the closest file matches for the given query within the directory and its subdirectories.
    """
    closest_matches = []
    ratios = []
    for root, _, files in os.walk(directory):
        for file in files:
            filename = os.path.splitext(file)[0]  
            ratio = difflib.SequenceMatcher(None, query, filename).ratio()
            closest_matches.append((os.path.join(root, file), ratio))
            ratios.append(ratio)

    closest_matches.sort(key=lambda x: x[1], reverse=True)

    return closest_matches[:n]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def save_media_content_ids(media_content_ids, file_name):
    """
    This function saves the media content IDs to a text file.
    """

    with open(f"www/playlist.m3u", "w") as file:
        file.write(INTRO_URL + '\n')
        media_content_ids = [str(item) for item in media_content_ids]
        file.writelines('\n'.join(media_content_ids) + '\n')

    send_service_call(file_name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def read_m3u_file(file_path):
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return []

    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if not line.startswith('#')]

    return lines
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def start_va(name):
    """
    This function sends a service call to Home Assistant to start Voice Assistant on targeted device.
    """
    url = f"http://{HOME_ASSISTANT_IP}/api/services/esphome/{name}_wait_and_start_va"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("")
    else:
        print("")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def send_livetv_call(channel_name):
    """
    This function sends a service call to Home Assistant to start playing the playlist.
    """
    if channel_name not in livetv_channels:
        print("Channel not found in the list.")
        return

    channel_url = livetv_channels[channel_name]

    with open("www/tmp/playlist.m3u", "w") as tmp_file:
        tmp_file.write(channel_url)

    url = f"http://{HOME_ASSISTANT_IP}/api/services/remote/turn_on"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "activity": f"http://{HOME_ASSISTANT_IP}/local/tmp/playlist.m3u",
        "entity_id": sys.argv[3]  
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("")
    else:
        print(f"det låter som du har en kötte bulle i käften. tugga klart middagen och försök sedan igen. Status code: {response.status_code}")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def get_entity_attribute(entity_id, attribute_name):
    url = f'http://{HOME_ASSISTANT_IP}/api/states/{entity_id}'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        state_obj = response.json()
        if 'attributes' in state_obj and attribute_name in state_obj['attributes']:
            return state_obj['attributes'][attribute_name]
        else:
            print(f"Attribute '{attribute_name}' not found for entity '{entity_id}'.")
            sys.exit(1)
    else:
        print("Failed to get entity state:", response.text)
        sys.exit(1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def create_m3u_from_file(filepath):
    metadata_list = []
    metadata_list.append(filepath)
    return metadata_list
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def add_song_to_playlist(playlist_file):
    song_path = get_entity_attribute(ENTITY_ID, ATTRIBUTE_NAME)
    if song_path:
        mode = 'a' if os.path.exists(playlist_file) else 'w'
        with open(playlist_file, mode) as playlist:
            metadata_list = create_m3u_from_file(song_path)
            if metadata_list:
                if mode == 'a':
                    playlist.write('\n')
                playlist.write('\n'.join(metadata_list) + '\n')
        print(f"Song {song_path} added to the playlist {playlist_file} successfully!")
    else:
        print(f"Failed to extract song path from the media player '{ATTRIBUTE_NAME}' attribute '{ENTITY_ID}'.")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def send_mp3playlist_call(search_query):
    """
    This function sends a service call to Home Assistant to start playing the playlist.
    """
    url = f"http://{HOME_ASSISTANT_IP}/api/services/remote/turn_on"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "activity": sys.argv[1],
        "entity_id": sys.argv[3]  
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Sure thing.")
    else:
        print(f"It sounds like you have a meat ball in your mouth. Finish your dinner before trying again. Status code: {response.status_code}")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def send_service_call(file_name):
    """
    This function sends a service call to Home Assistant to start playing the playlist.
    """
    url = f"http://{HOME_ASSISTANT_IP}/api/services/remote/turn_on"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "activity": f"http://{HOME_ASSISTANT_IP}/local/playlist.m3u",
        "entity_id": sys.argv[3]  
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("No problem.")
    else:
        print(f"It sounds like you have a meat ball in your mouth. Finish your dinner before trying again. Status code: {response.status_code}")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def load_played_news():
    if os.path.exists(PLAYED_NEWS_FILE):
        with open(PLAYED_NEWS_FILE, "r") as f:
            return set(f.read().splitlines()[:MAX_PLAYED_NEWS_ENTRIES])
    return set()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def save_played_news():
    with open(PLAYED_NEWS_FILE, "w") as f:
        f.write("\n".join(played_news))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def mainnews(entity_id):
    global played_news
    played_news = load_played_news()
    fetch_news()
    if len(news_list) == 0:
        print("No new news casts available.")
        return

    new_news = [news_item for news_item in news_list if news_item not in played_news]
    if new_news:
        save_media_content_ids(new_news, "news")
        played_news.update(new_news)
        save_played_news()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Python usage: media_controller.py <search_query/m3u_file> <type> <remote.entity_id>")
        sys.exit(1)

    query_or_file = sys.argv[1]
    type_or_entity_id = sys.argv[2].lower()
    media_player_entity_id = sys.argv[3]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# News 
    if type_or_entity_id == "news":
        mainnews(media_player_entity_id)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Live-TV (TV Channels)
    elif type_or_entity_id == "livetv":
        send_livetv_call(query_or_file)        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Playlst (Play Playlist)
    elif type_or_entity_id == "playlist":
        query_or_file = sys.argv[1]   
        send_mp3playlist_call(query_or_file)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Add (Song to Playlist)
    elif type_or_entity_id == "add":
        playlist_file = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_PLAYLIST
        add_song_to_playlist(playlist_file)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Jukebox (Random Music)
    elif type_or_entity_id == "jukebox":
        search_directory = SEARCH_FOLDERS["music"]
        files = list_files(search_directory)
        random.shuffle(files)
        media_content_urls = template_directory_path(files)
        save_media_content_urls(media_content_urls, "jukebox")
        send_service_call("jukebox")  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Movies
    elif type_or_entity_id == "movie":
        closest_directory = find_closest_directory(query_or_file, os.listdir(SEARCH_FOLDERS["movie"]))
        if closest_directory:
            search_directory = os.path.join(SEARCH_FOLDERS["movie"], closest_directory)
            files = list_files(search_directory)
            media_content_urls = template_directory_path(files)
            save_media_content_urls(media_content_urls, "movie")
            send_service_call("movie")
        else:
            print("Could not find any movie with the title", sys.argv[1])
            print("Try again")
            entity_state = call_template_service()
            name = entity_state.replace('binary_sensor.', '').replace('_assist_in_progress', '')
            start_va(name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# TV (TV Shows)
    elif type_or_entity_id == "tv":
        closest_directory = find_closest_directory(query_or_file, os.listdir(SEARCH_FOLDERS["tv"]))
        if closest_directory:
            search_directory = os.path.join(SEARCH_FOLDERS["tv"], closest_directory)
            files = list_files(search_directory)
            random.shuffle(files)
            media_content_urls = template_directory_path(files)
            save_media_content_urls(media_content_urls, "tv")
            send_service_call("tv")
        else:
            print("Could not find any TV Show with the title", sys.argv[1])
            print("Try again")
            entity_state = call_template_service()
            name = entity_state.replace('binary_sensor.', '').replace('_assist_in_progress', '')
            start_va(name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Music (Artist)
    elif type_or_entity_id == "music":
        closest_directory = find_closest_directory(query_or_file, os.listdir(SEARCH_FOLDERS["music"]))
        if closest_directory:
            search_directory = os.path.join(SEARCH_FOLDERS["music"], closest_directory)
            files = list_files(search_directory)
            random.shuffle(files)
            media_content_urls = template_directory_path(files)
            save_media_content_urls(media_content_urls, "music")
            send_service_call("music")
        else:
            print("Could not find any music artist with the name", sys.argv[1])
            print("Try again")
            entity_state = call_template_service()
            name = entity_state.replace('binary_sensor.', '').replace('_assist_in_progress', '')
            start_va(name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Podcasts
    elif type_or_entity_id == "podcast":
        closest_directory = find_closest_directory(query_or_file, os.listdir(SEARCH_FOLDERS["podcast"]))
        if closest_directory:
            search_directory = os.path.join(SEARCH_FOLDERS["podcast"], closest_directory)
            files = list_files(search_directory)
            media_content_urls = template_directory_path(files)
            save_media_content_urls(media_content_urls, "podcast")
            send_service_call("podcast")
        else:
            print("Could not find any Podcast with the name", sys.argv[1])
            print("Try again")
            entity_state = call_template_service()
            name = entity_state.replace('binary_sensor.', '').replace('_assist_in_progress', '')
            start_va(name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Music Videos
    elif type_or_entity_id == "musicvideo":
        closest_directory = find_closest_directory(query_or_file, os.listdir(SEARCH_FOLDERS["musicvideo"]))
        if closest_directory:
            search_directory = os.path.join(SEARCH_FOLDERS["musicvideo"], closest_directory)
            files = list_files(search_directory)
            media_content_urls = template_directory_path(files)
            save_media_content_urls(media_content_urls, "musicvideo")
            send_service_call("musicvideo")
        else:
            print("Could not find any Music Video with the title", sys.argv[1])
            print("Try again")
            entity_state = call_template_service()
            name = entity_state.replace('binary_sensor.', '').replace('_assist_in_progress', '')
            start_va(name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Audiobooks            
    elif type_or_entity_id == "audiobooks":
        closest_directory = find_closest_directory(query_or_file, os.listdir(SEARCH_FOLDERS["audiobooks"]))
        if closest_directory:
            search_directory = os.path.join(SEARCH_FOLDERS["audiobooks"], closest_directory)
            files = list_files(search_directory)
            media_content_urls = template_directory_path(files)
            save_media_content_urls(media_content_urls, "audiobooks")
            send_service_call("audiobooks")
        else:
            print("Could not find any Audiobook with the title", sys.argv[1])
            print("Try again")
            entity_state = call_template_service()
            name = entity_state.replace('binary_sensor.', '').replace('_assist_in_progress', '')
            start_va(name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Other Videos
    elif type_or_entity_id == "othervideos":
        closest_directory = find_closest_directory(query_or_file, os.listdir(SEARCH_FOLDERS["othervideos"]))
        if closest_directory:
            search_directory = os.path.join(SEARCH_FOLDERS["othervideos"], closest_directory)
            files = list_files(search_directory)
            media_content_urls = template_directory_path(files)
            save_media_content_urls(media_content_urls, "othervideos")
            send_service_call("othervideos")
        else:
            print("Could not find any Video with the title", sys.argv[1])
            print("Try again")
            entity_state = call_template_service()
            name = entity_state.replace('binary_sensor.', '').replace('_assist_in_progress', '')
            start_va(name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Song (Music)
    elif type_or_entity_id == "song":
        closest_files = find_closest_files(query_or_file, SEARCH_FOLDERS["music"], n=5)
        if closest_files:
            files = [file for file, _ in closest_files]
            media_content_urls = template_directory_path(files)
            save_media_content_urls(media_content_urls, "song")
            send_service_call("song")
        else:
            print("Could not find any Song with the title", sys.argv[1])
            print("Try again")
            entity_state = call_template_service()
            name = entity_state.replace('binary_sensor.', '').replace('_assist_in_progress', '')
            start_va(name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# YouTube
    elif type_or_entity_id == "youtube":
        search_query = clean_search_query(query_or_file)
        video_url, video_title = search_youtube(search_query)

        if video_url:
            print(f"Starting to play video: {video_title}: {video_url}")
            save_media_content_ids([video_url], "youtube")
        else:
            print("Could not find any YouTube video with the title", sys.argv[1])
            print("Try again")
            entity_state = call_template_service()
            name = entity_state.replace('binary_sensor.', '').replace('_assist_in_progress', '')
            start_va(name)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Additional Media Control
    
# Play
    elif type_or_entity_id == "play":
        call_media_play_pause_service("all")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Pause
    elif type_or_entity_id == "pause":
        call_media_play_pause_service("all")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Next
    elif type_or_entity_id == "next":
        call_media_next_track_service("all")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Previous
    elif type_or_entity_id == "previous":
        call_media_previous_track_service("all")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Volume Up
    elif type_or_entity_id == "up":
        call_volume_up_service("all")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Volume Down
    elif type_or_entity_id == "down":
        call_volume_down_service("all")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Power On
    elif type_or_entity_id == "on":
        call_power_off_service("on")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Power Off
    elif type_or_entity_id == "off":
        call_power_off_service("off")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    else:
        if type_or_entity_id not in SEARCH_FOLDERS:
            print("Invalid directory type.")
            sys.exit(1)

        else:
            print("It sounds like you have a meat ball in your mouth. Finish your dinner before trying again.")
            
