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
    """Send a 1-star rating to the currently playing track using the PMS API."""
    url = f"{PMS_URL}/status/sessions"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        for track in root.findall("Track"):
            player = track.find("Player")
            if player is not None and (
                player.get("machineIdentifier") == PLAYER_ID or
                player.get("title") == PLAYER_ID
            ):
                rating_key = track.get("ratingKey")
                if rating_key:
                    rate_url = f"{PMS_URL}/:/rate?key={rating_key}&rating=10"
                    rate_response = requests.put(rate_url, headers=HEADERS)
                    rate_response.raise_for_status()
                    print(f"[star] Rated item {rating_key} with 1 star.")
                return
        print("[star] No active track found to rate.")
    except requests.RequestException as e:
        print(f"[star] API error: {e}")
    except ET.ParseError as e:
        print(f"[star] XML parse error: {e}")

def set_repeat(repeat_mode='repeat'):
    print("Repeat toggle not available in local API")

def get_status():
    url = f"{PMS_URL}/status/sessions"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        for track in root.findall("Track"):
            player = track.find("Player")
            if player is not None and (
                player.get("machineIdentifier") == PLAYER_ID or
                player.get("title") == PLAYER_ID
            ):
                return player.get("state")
    except requests.RequestException as e:
        print(f"get_status error: {e}")
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
    return None


# --- Additional functions for full session status and player polling ---

def get_all_players():
    """Returns a list of all active players with their titles and states."""
    url = f"{PMS_URL}/status/sessions"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        players = []
        for track in root.findall("Track"):
            player = track.find("Player")
            if player is not None:
                players.append({
                    "title": player.get("title"),
                    "machineIdentifier": player.get("machineIdentifier"),
                    "state": player.get("state")
                })
        return players
    except requests.RequestException as e:
        print(f"get_all_players error: {e}")
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
    return []


def get_player_state(player_title=None):
    """Returns state of a specific player, defaults to PLAYER_ID."""
    player_title = player_title or PLAYER_ID
    players = get_all_players()
    for player in players:
        if player["title"] == player_title or player["machineIdentifier"] == player_title:
            return player["state"]
    return None

def next_track():
    skip()

def previous_track():
    previous()

def toggle_star():
    star()