# gpio_config.py

# GPIO pin mapping for B wires (used in switch matrix)
# Row pins (outputs)
B_OUTPUT_PINS = {
    "B1": 5,
    "B2": 6,
    "B3": 12
}

# Column pins (inputs)
B_INPUT_PINS = {
    "B4": 9,
    "B5": 16,
    "B6": 20,
    "B7": 21
}

# Switch matrix connections: SW -> (Pin1, Pin2)
# Labels: Record, Play, Rewind, Stop, Pause, Fast Forward, Auto Spacing, Direction, Reverse, Repeat
SWITCH_MATRIX = {
    "SW4": ("B3", "B4"),   # Record
    "SW5": ("B3", "B5"),   # Play
    "SW6": ("B3", "B6"),   # Rewind
    "SW7": ("B3", "B7"),   # Stop
    "SW8": ("B2", "B4"),   # Pause
    "SW9": ("B2", "B5"),   # Fast Forward
    "SW10": ("B2", "B6"),  # Auto Spacing
    "SW11": ("B2", "B7"),  # Direction
    "SW12": ("B1", "B4"),  # Reverse
    "SW13": ("B1", "B5")   # Repeat
}

# LED GPIO mapping
LED_PINS = {
    "D414": 25,  # Record (red)
    "D415": 24,  # Play
    "D416": 23,  # Pause
    "D417": 22,  # ASMS
    "D418": 4,   # > Direction
    "D419": 26,  # < Direction
    "D420": 19,  # Reverse
    "D421": 13,  # Repeat
    "D422": 10,  # Auto Spacing
    "D407": 14,  # Normal (red)
    "D406": 15,  # CrO2 (red)
    "D405": 18   # Metal (red)
}

# Common anode for LED sinking
LED_COMMON = 27

# Power and backlight control GPIOs
POWER_GPIO = {
    "POWER_DETECT": 17,     # Reads HIGH when SCT powered
    "RELAY_CONTROL": 7      # Controls backlight relay
}
