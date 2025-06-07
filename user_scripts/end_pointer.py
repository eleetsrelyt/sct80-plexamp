import requests
from dotenv import load_dotenv
import os

load_dotenv()
PORT = os.getenv("PLEXAMP_PORT", 32500)
TOKEN = os.getenv("PLEX_TOKEN")

base_url = f"http://localhost:{PORT}"

headers = {
    "X-Plex-Token": TOKEN
}

def try_endpoint(path):
    url = f"{base_url}{path}"
    try:
        r = requests.get(url, headers=headers)
        print(f"{url} --> {r.status_code}")
        print(r.text[:500])
        if r.status_code == 200 and "application/json" in r.headers.get("Content-Type", ""):
            print(r.json())
    except Exception as e:
        print(f"{url} --> ERROR: {e}")

# try likely endpoints
paths = [
    "/player/playback/status",
    "/player/playback/playQueues",
    "/player/playback",
    "/player/playback/playing",
    "/player/playback/nowPlaying",
    "/player/playback/playPause",
    "/player/playback/state",
    "/player/playQueues",
    "/status/sessions",
    "/status",
    "/"
]

for path in paths:
    try_endpoint(path)