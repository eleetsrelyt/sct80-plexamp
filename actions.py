import time
import threading
import RPi.GPIO as GPIO
from plexamp_api import get_player_state, play_pause, next_track, previous_track, toggle_star
from gpio_config import LED_PINS, LED_COMMON, POWER_GPIO
from led_control import led_boot_sequence, led_on, led_off, all_leds_off

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

_power_on = False

def set_power_state(state):
    global _power_on
    _power_on = state
    print(f"[power] Power state set to: {'ON' if _power_on else 'OFF'}")

# LED setup is now handled in led_control.setup_leds()
# GPIO.setup(LED_COMMON, GPIO.OUT)
# GPIO.output(LED_COMMON, GPIO.LOW)
# for pin in LED_PINS.values():
#     GPIO.setup(pin, GPIO.OUT)
#     GPIO.output(pin, GPIO.HIGH)

def set_led(label, state):
    if state:
        led_on(label)
    else:
        led_off(label)

def update_leds_from_status():
    if not _power_on:
        return

    state = get_player_state()

    # Play LED: ON only when playing
    set_led("D415", state == "playing")

    # Pause LED: ON when not playing (paused or stopped)
    set_led("D416", state != "playing")

    # Placeholder values — can be updated with actual PMS fields later
    set_led("D422", False)  # Auto Spacing LED
    set_led("D421", False)  # Repeat LED

def run_led_polling(interval=1):
    def loop():
        while True:
            update_leds_from_status()
            time.sleep(interval)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()

def monitor_power_and_backlight():
    GPIO.setup(POWER_GPIO["POWER_DETECT"], GPIO.IN)
    GPIO.setup(POWER_GPIO["RELAY_CONTROL"], GPIO.OUT)
    GPIO.output(POWER_GPIO["RELAY_CONTROL"], GPIO.LOW)

    def loop():
        powered = False
        while True:
            if GPIO.input(POWER_GPIO["POWER_DETECT"]) == GPIO.HIGH and not powered:
                GPIO.output(POWER_GPIO["RELAY_CONTROL"], GPIO.HIGH)
                print("[power] ON")
                led_boot_sequence()
                powered = True
            elif GPIO.input(POWER_GPIO["POWER_DETECT"]) == GPIO.LOW and powered:
                GPIO.output(POWER_GPIO["RELAY_CONTROL"], GPIO.LOW)
                print("[power] OFF")
                all_leds_off()
                powered = False
            time.sleep(0.5)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()

def handle_press(button):
    print(f"[button] Pressed: {button['label']}")

    match button["action"]:
        case "play_pause":
            play_pause()
        case "next":
            next_track()
        case "previous":
            previous_track()
        case "star":
            toggle_star()
        case _:
            print(f"[warn] Unknown action: {button['action']}")