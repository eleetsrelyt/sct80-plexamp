#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import requests
from dotenv import load_dotenv
import os

# load from .env
load_dotenv()
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
PLAYER_ID = os.getenv("PLAYER_NAME")
PORT = os.getenv("PLEXAMP_PORT", 32500)


# GPIO pins for SW5 (B2–B5)
OUT_PIN = 12  # B3
IN_PIN = 16   # B5

# === Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(OUT_PIN, GPIO.OUT)
GPIO.output(OUT_PIN, GPIO.HIGH)  # Inactive by default
GPIO.setup(IN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def send_playpause():
    url = f'http://localhost:{PORT}/player/playback/playPause?machineIdentifier={PLAYER_ID}'
    headers = {
        'X-Plex-Token': PLEX_TOKEN
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("Sent play/pause toggle to Plexamp.")
    except requests.RequestException as e:
        print(f"Error: {e}")

print("Watching for SW5 press... (Ctrl+C to exit)")

try:
    while True:
        GPIO.output(OUT_PIN, GPIO.LOW)  # Activate row
        time.sleep(0.01)

        if GPIO.input(IN_PIN) == GPIO.LOW:
            print("SW5 pressed. Toggling Plexamp.")
            send_playpause()
            while GPIO.input(IN_PIN) == GPIO.LOW:
                time.sleep(0.05)  # Wait for release
        GPIO.output(OUT_PIN, GPIO.HIGH)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Goodbye.")
finally:
    GPIO.cleanup()
