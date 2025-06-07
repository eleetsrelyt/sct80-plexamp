#!/usr/bin/env python3

# status_test.py
# 
# Successful reference script for single-button GPIO control of Plexamp playback.
# Features:
# - Optimistic LED toggling on button press
# - Polling Plex Media Server every few seconds to confirm/correct state
# - LED wired so LOW = ON, HIGH = OFF
# - Debounce/toggle logic using software-tracked LED state
# - Intended as a working template for expanding to additional buttons

import RPi.GPIO as GPIO
import time
import requests
from dotenv import load_dotenv
import os
import urllib3
import xml.etree.ElementTree as ET
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

# load from .env
load_dotenv()
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
PLAYER_ID = os.getenv("PLEXAMP_PLAYER")
PORT = os.getenv("PLEXAMP_PORT", 32500)
PLEX_SERVER = os.getenv("PLEX_SERVER")
PLEX_PORT = os.getenv("PLEX_PORT", "32400")

BUTTON_STATUS_POLL_INTERVAL = 1
POLL_INITIAL_DELAY = 3


# GPIO pins for SW5 (B2–B5)
BUTTON_ROW_PIN = 12  # B3
BUTTON_COL_PIN = 16  # B5

# === Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_ROW_PIN, GPIO.OUT)
GPIO.output(BUTTON_ROW_PIN, GPIO.HIGH)  # Inactive by default
GPIO.setup(BUTTON_COL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
BUTTON_PRESS_LED_PIN = 24  # D415

# NOTE: LED is wired such that LOW = ON and HIGH = OFF
# So we turn it LOW to light up when button is pressed, and HIGH to turn it off
GPIO.setup(BUTTON_PRESS_LED_PIN, GPIO.OUT)
GPIO.output(BUTTON_PRESS_LED_PIN, GPIO.HIGH)  # Start with LED OFF

# === State tracking ===
assumed_state = None
poll_until = 0
next_poll_time = 0
led_should_be_on = False  # Tracks intended LED state

# Polls the Plex Media Server for playback state of the target player.
# Updates LED to match playing/paused state.
def poll_and_update_led():
    global led_should_be_on
    try:
        url = f"https://{PLEX_SERVER}:{PLEX_PORT}/status/sessions"
        headers = {
            'X-Plex-Token': PLEX_TOKEN
        }
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        xml = response.text

        root = ET.fromstring(xml)
        for player in root.findall(".//Player"):
            title = player.attrib.get("title", "")
            state = player.attrib.get("state", "")
            if title == PLAYER_ID:
                log(state)
                led_should_be_on = (state == "playing")
                GPIO.output(BUTTON_PRESS_LED_PIN, GPIO.LOW if led_should_be_on else GPIO.HIGH)
                return

        GPIO.output(BUTTON_PRESS_LED_PIN, GPIO.HIGH)

    except Exception as e:
        GPIO.output(BUTTON_PRESS_LED_PIN, GPIO.HIGH)

def send_playpause():
    url = f'http://localhost:{PORT}/player/playback/playPause?machineIdentifier={PLAYER_ID}'
    headers = {
        'X-Plex-Token': PLEX_TOKEN
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        log("Sent play/pause toggle to Plexamp.")
    except requests.RequestException as e:
        log(f"Error: {e}")

log("Watching for SW5 press... (Ctrl+C to exit)")

poll_until = time.time() + POLL_INITIAL_DELAY + 10

try:
    while True:
        GPIO.output(BUTTON_ROW_PIN, GPIO.LOW)
        time.sleep(0.01)

        # === Button press handling ===
        # When button is pressed:
        # - Turn LED on immediately
        # - Toggle Plexamp playback
        # - Flip the software-tracked LED state
        # - Update the physical LED accordingly
        # - Start/resume polling window to confirm state later
        if GPIO.input(BUTTON_COL_PIN) == GPIO.LOW:
            GPIO.output(BUTTON_PRESS_LED_PIN, GPIO.LOW)  # LED ON while pressed
            log("SW5 pressed. Toggling Plexamp.")
            send_playpause()
            while GPIO.input(BUTTON_COL_PIN) == GPIO.LOW:
                time.sleep(0.05)
            led_should_be_on = not led_should_be_on
            GPIO.output(BUTTON_PRESS_LED_PIN, GPIO.LOW if led_should_be_on else GPIO.HIGH)
            poll_until = time.time() + POLL_INITIAL_DELAY + 10
            next_poll_time = time.time() + POLL_INITIAL_DELAY
            continue  # Skip polling in this cycle

        GPIO.output(BUTTON_ROW_PIN, GPIO.HIGH)

        # === Polling logic ===
        # Check Plex Media Server status periodically within a polling window
        # LED state is updated to reflect confirmed playback status
        if time.time() < poll_until and time.time() >= next_poll_time:
            poll_and_update_led()
            next_poll_time = time.time() + BUTTON_STATUS_POLL_INTERVAL

        time.sleep(0.1)

    # === Cleanup on exit ===
except KeyboardInterrupt:
    log("Goodbye.")
finally:
    GPIO.cleanup()
