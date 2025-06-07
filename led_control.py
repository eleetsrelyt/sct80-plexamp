# led_control.py

import RPi.GPIO as GPIO
from gpio_config import LED_PINS, LED_COMMON
import time
import random

ACTIVE_HIGH_LEDS = {"D407", "D406", "D405"}
SPECIAL_D422 = "D422"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setup_leds():
    for pin in LED_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
    GPIO.setup(LED_COMMON, GPIO.OUT)
    GPIO.output(LED_COMMON, GPIO.LOW)
    if SPECIAL_D422 in LED_PINS:
        GPIO.setup(10, GPIO.OUT)
        GPIO.output(10, GPIO.HIGH)

    for label in LED_PINS:
        led_off(label)

def led_on(label):
    pin = LED_PINS[label]
    if label == SPECIAL_D422:
        GPIO.output(pin, GPIO.LOW)   # Sink
        GPIO.output(10, GPIO.HIGH)   # Source
    elif label in ACTIVE_HIGH_LEDS:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)

def led_off(label):
    pin = LED_PINS[label]
    if label == SPECIAL_D422:
        GPIO.output(pin, GPIO.HIGH)  # Stop sinking
        GPIO.output(10, GPIO.LOW)    # Stop sourcing
    elif label in ACTIVE_HIGH_LEDS:
        GPIO.output(pin, GPIO.LOW)
    else:
        GPIO.output(pin, GPIO.HIGH)

def all_leds_off():
    for label in LED_PINS:
        led_off(label)

def led_boot_sequence():
    for label in LED_PINS:
        led_on(label)
    time.sleep(1)
    for label in LED_PINS:
        led_off(label)


# Toggle the specified LED state.
def led_toggle(label):
    pin = LED_PINS[label]
    current_state = GPIO.input(pin)

    if label == SPECIAL_D422:
        GPIO.output(pin, GPIO.LOW if current_state else GPIO.HIGH)
        GPIO.output(10, GPIO.HIGH if current_state else GPIO.LOW)
    elif label in ACTIVE_HIGH_LEDS:
        GPIO.output(pin, GPIO.LOW if current_state else GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.HIGH if current_state == GPIO.LOW else GPIO.LOW)