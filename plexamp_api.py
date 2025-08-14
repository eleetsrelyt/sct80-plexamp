# plexamp_api.py

import os
import requests
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()

BASE_URL = f"http://localhost:{os.getenv('PLEXAMP_PORT', 32500)}"
PMS_URL = f"http://{os.getenv('PLEX_SERVER')}:{os.getenv('PLEX_PORT', 32400)}"
TOKEN = os.getenv("PLEXAMP_TOKEN")
PLAYER_ID = os.getenv("PLEXAMP_PLAYER")
HEADERS = {
    "X-Plex-Token": TOKEN
}


# --- Helper: Poll local Plexamp timeline endpoint and return XML root ---
def poll_local_timeline(include_metadata: bool = True, wait: int = 0, media_type: str = "music"):
    """Poll Plexamp's local timeline endpoint and return parsed XML.
    Defaults to include metadata and no long-poll wait for snappy LED/state updates.
    """
    url = f"{BASE_URL}/player/timeline/poll"
    params = {
        "wait": str(wait),
        "includeMetadata": "1" if include_metadata else "0",
        "commandID": "1",
        "type": media_type,
    }
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=5)
        response.raise_for_status()
        return ET.fromstring(response.content)
    except requests.RequestException as e:
        print(f"[poll_local_timeline] HTTP error: {e}")
    except ET.ParseError as e:
        print(f"[poll_local_timeline] XML parse error: {e}")
    return None

def play_pause():
    url = f"{BASE_URL}/player/playback/playPause?machineIdentifier={PLAYER_ID}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"play_pause error: {e}")

def skip():
    url = f"{BASE_URL}/player/playback/skipNext?machineIdentifier={PLAYER_ID}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"skip error: {e}")

def previous():
    url = f"{BASE_URL}/player/playback/skipPrevious?machineIdentifier={PLAYER_ID}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"previous error: {e}")

def star():
    """Send a 1-star rating to the currently playing item.
    We read ratingKey from LOCAL Plexamp timeline metadata, then call PMS once to rate.
    """
    root = poll_local_timeline(include_metadata=True)
    if root is None:
        print("[star] No timeline data available.")
        return
    # Try to find metadata for the current item; the container may nest <Timeline> and <Metadata>
    rating_key = None
    # Common layouts: <MediaContainer><Metadata ... ratingKey="..." /></MediaContainer>
    meta = root.find("Metadata")
    if meta is not None:
        rating_key = meta.get("ratingKey")
    if rating_key is None:
        # Some builds put Metadata under a second level
        for elem in root.iter("Metadata"):
            rk = elem.get("ratingKey")
            if rk:
                rating_key = rk
                break
    if not rating_key:
        print("[star] Could not find ratingKey in local metadata.")
        return
    # Rate via PMS
    try:
        rate_url = f"{PMS_URL}/:/rate?key={rating_key}&rating=10"
        rate_response = requests.put(rate_url, headers=HEADERS, timeout=5)
        rate_response.raise_for_status()
        print(f"[star] Rated item {rating_key} with 1 star.")
    except requests.RequestException as e:
        print(f"[star] PMS rate error: {e}")

def set_repeat(repeat_mode='repeat'):
    print("Repeat toggle not available in local API")

def get_status():
    """Return player state (e.g., 'playing', 'paused', 'stopped') from LOCAL Plexamp timeline."""
    root = poll_local_timeline(include_metadata=False)
    if root is None:
        return None
    # Expected structure: <MediaContainer> <Timeline state="playing" ... />
    timeline = root.find("Timeline")
    if timeline is not None:
        return timeline.get("state")
    return None


def get_all_players():
    """Return a single local player entry derived from the local timeline.
    The Plexamp local API doesn't enumerate *all* players; this returns just the current one.
    """
    state = get_status()
    return [{
        "title": PLAYER_ID,
        "machineIdentifier": PLAYER_ID,
        "state": state
    }]

def get_player_state(player_title=None):
    """Return state of the local Plexamp player using the local timeline poll."""
    return get_status()

def next_track():
    skip()

def previous_track():
    previous()

def toggle_star():
    star()

def start_radio(mode="randomAlbumRadio"):
    """Start a Plexamp radio session using the given mode."""
    url = f"{BASE_URL}/player/playRadio"
    payload = {
        "machineIdentifier": PLAYER_ID,
        "radioType": mode
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        print(f"[start_radio] Started radio with mode: {mode}")
    except requests.RequestException as e:
        print(f"[start_radio] API error: {e}")