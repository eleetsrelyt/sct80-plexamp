# state_manager.py

import time
import threading
import RPi.GPIO as GPIO
from plexamp_api import get_player_state
from gpio_config import LED_PINS, LED_COMMON, POWER_GPIO
from led_control import led_boot_sequence, led_on, led_off, all_leds_off
from button_config import BUTTON_CONFIG

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

_power_on = False

def set_power_state(state):
    global _power_on
    _power_on = state

def get_power_state():
    return _power_on

def set_led(label, state):
    if state:
        led_on(label)
    else:
        led_off(label)

def update_leds_from_status():
    if not _power_on:
        return

    state = get_player_state()

    for config in BUTTON_CONFIG.values():
        label = config.get("led")
        mode = config.get("led_mode")

        if not label or not mode:
            continue

        match mode:
            case "on_when_playing":
                set_led(label, state == "playing")
            case "blink_when_paused":
                set_led(label, state != "playing")
            case "momentary_register":
                pass  # handled at press time
            case "r2d2_blink":
                set_led(label, time.time() % 1 < 0.1)
            case _:
                pass


def run_led_polling(interval=1):
    def loop():
        while True:
            if not _power_on:
                time.sleep(interval)
                continue
            update_leds_from_status()
            time.sleep(interval)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()

# Temporary alias for legacy import in main.py
update_led_states = update_leds_from_status