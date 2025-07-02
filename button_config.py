# Configuration for each button in the SCT-80 matrix.
# Each entry maps:
# - a matrix switch ID (e.g. SW5)
# - to its row/col GPIOs
# - the label shown in logs
# - associated LED by label (mapped in led_control)
# - action string (handled in actions.py)
# - LED mode ("on_when_playing", "blink_when_paused", etc.)

BUTTON_CONFIG = {
    "SW4": {
        "label": "Record",
        "row": 12,  # B3
        "col": 9,   # B4
        "led": "D414",
        "action": "star",
        "led_mode": "momentary_register",
        "sanity_check": "all_leds_test"
    },
    "SW5": {
        "label": "Play",
        "row": 12,  # B3
        "col": 16,  # B5
        "led": "D415",
        "action": "play_pause",
        "led_mode": "on_when_playing",
        "sanity_check": "all_leds_test"
    },
    "SW6": {
        "label": "Rewind",
        "row": 12,
        "col": 20,  # B6
        "led": None,
        "action": "previous",
        "led_mode": None,
        "sanity_check": "all_leds_test"
    },
    "SW7": {
        "label": "Stop",
        "row": 12,
        "col": 21,  # B7
        "led": None,
        "action": "play_pause",
        "led_mode": None,
        "sanity_check": "all_leds_test"
    },
    "SW8": {
        "label": "Pause",
        "row": 6,   # B2
        "col": 9,  # B4
        "led": "D416",
        "action": "play_pause",
        "led_mode": "blink_when_paused",
        "sanity_check": "all_leds_test"
    },
    "SW9": {
        "label": "Fast Forward",
        "row": 6,   # B2
        "col": 16,  # B5
        "led": None,
        "action": "next",
        "led_mode": None,
        "sanity_check": "all_leds_test"
    },
    "SW10": {
        "label": "Auto Spacing",
        "row": 6,
        "col": 20,  # B6
        "led": "D422",
        "action": "shuffle",
        "led_mode": "on_when_shuffle",
        "sanity_check": "all_leds_test"
    },
    "SW11": {
        "label": "Direction",
        "row": 6,
        "col": 21,  # B7
        "led": None,
        "action": "random_album_radio",
        "led_mode": "blink_D418_D419",
        "sanity_check": "all_leds_test"
    },
    "SW12": {
        "label": "Reverse",
        "row": 5,   # B1
        "col": 9,   # B4
        "led": None,
        "led_mode": None,
        "sanity_check": "all_leds_test"
    },
    "SW13": {
        "label": "Repeat",
        "row": 5,
        "col": 16,  # B5
        "led": "D421",
        "action": "toggle_repeat",
        "led_mode": "on_when_repeat",
        "sanity_check": "all_leds_test"
    },
    "POWER": {
        "label": "Power",
        "row": None,
        "col": 17,  # D616 power detect
        "led": None,
        "action": "toggle_hdmi_backlight",
        "led_mode": None,
        "relay_control_gpio": 7,
        "sanity_check": "all_leds_test"
    }
}