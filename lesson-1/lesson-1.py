import json
import os
from urllib.parse import urljoin, urlencode

import requests


def path_collector(path, id, key):
    BASE_URL = os.environ.get("BASE_URL", path)
    query = "?" + urlencode(
        dict(id=id, key=key))  # формируем набор key=value из коллекции словарь
    return urljoin(BASE_URL, query)


username = 'Sebkd'
token = os.environ.get('GITHUB_TOKEN')

response = requests.get('https://api.github.com/user/repos', auth=(username, token))

with open('lesson-1/github.json', 'a') as github_json_file:
    json.dump(response.json(), github_json_file)  # файл в .gitignore

youtube_id = os.environ.get('ID_YOUTUBE')
youtube_key = os.environ.get('API_KEY_YOUTUBE')
path_to_youtube = f"https://www.googleapis.com/youtube/v3/videos"  # путь до youtube без параметров

print(path_collector(path_to_youtube, youtube_id, youtube_key))
response = requests.get(path_collector(path_to_youtube, youtube_id, youtube_key))

with open('lesson-1/youtube.json', 'a') as youtube_json_file:
    json.dump(response.json(), youtube_json_file)

