# main.py

import RPi.GPIO as GPIO
import time
import signal
import sys
from gpio_config import B_PINS, SWITCH_MATRIX, LED_PINS, LED_COMMON
from actions import handle_press
from led_control import setup_leds, all_leds_off, led_on, led_off, led_boot_sequence
from button_config import BUTTON_CONFIG

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
setup_leds()

from plexamp_api import get_status, play_pause

POWER_GPIO = 17
RELAY_GPIO = 7
GPIO.setup(POWER_GPIO, GPIO.IN)
GPIO.setup(RELAY_GPIO, GPIO.OUT)

def set_backlight(on: bool):
    GPIO.output(RELAY_GPIO, GPIO.HIGH if on else GPIO.LOW)

set_backlight(False)  # Ensure off at start


# Setup B pins
for pin in B_PINS.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


from state_manager import run_led_polling, set_power_state, update_led_states
all_leds_off()
run_led_polling()

# Switch label by pin pair lookup (reverse mapping)
PIN_PAIR_TO_SWITCH = {
    (B_PINS[p1], B_PINS[p2]): sw
    for sw, (p1, p2) in SWITCH_MATRIX.items()
}

# Track previously detected switches to debounce manually
pressed_cache = set()

previous_power_state = GPIO.input(POWER_GPIO)

print("Monitoring power state...")

# Force initial power state sync
if previous_power_state == GPIO.HIGH:
    print("Power ON detected (initial)")
    set_backlight(True)
    led_boot_sequence()
    update_led_states()
    set_power_state(True)
else:
    print("Power OFF detected (initial)")
    set_backlight(False)
    all_leds_off()
    set_power_state(False)
    if get_status() == "playing":
        play_pause()

def shutdown_handler(sig, frame):
    print("[shutdown] Cleaning up GPIO and exiting...")
    set_backlight(False)
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

print("Scanning for button presses... (Ctrl+C to exit)")

while True:
    current_power_state = GPIO.input(POWER_GPIO)

    if current_power_state != previous_power_state:
        if current_power_state == GPIO.HIGH:
            print("Power ON detected")
            set_backlight(True)
            led_boot_sequence()
            update_led_states()
            set_power_state(True)
        else:
            print("Power OFF detected")
            set_backlight(False)
            all_leds_off()
            set_power_state(False)
            if get_status() == "playing":
                play_pause()

        previous_power_state = current_power_state

    if current_power_state == GPIO.HIGH:
        for row_label, row_pin in B_PINS.items():
            # Set current row to output LOW
            GPIO.setup(row_pin, GPIO.OUT)
            GPIO.output(row_pin, GPIO.LOW)

            for col_label, col_pin in B_PINS.items():
                if row_pin == col_pin:
                    continue  # Skip same pin

                # Set current column to input with pull-up
                GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

                if GPIO.input(col_pin) == GPIO.LOW:
                    key = (row_pin, col_pin)
                    alt_key = (col_pin, row_pin)
                    sw = PIN_PAIR_TO_SWITCH.get(key) or PIN_PAIR_TO_SWITCH.get(alt_key)
                    if sw and sw not in pressed_cache:
                        button = BUTTON_CONFIG.get(sw)
                        if button:
                            print(f"[DEBUG] Button {sw} pressed, action: {button['action']}")
                            handle_press(button)
                        pressed_cache.add(sw)
                else:
                    key = (row_pin, col_pin)
                    alt_key = (col_pin, row_pin)
                    sw = PIN_PAIR_TO_SWITCH.get(key) or PIN_PAIR_TO_SWITCH.get(alt_key)
                    if sw in pressed_cache:
                        pressed_cache.remove(sw)

            # Reset row to input with pull-up
            GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    time.sleep(0.05)