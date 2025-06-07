from gpiozero import LED
import RPi.GPIO as GPIO
from time import sleep

# GPIO mode
GPIO.setmode(GPIO.BCM)

# Define LEDs (gpiozero controls only the sink pin)
led_map = {
    "D414": 25,
    "D415": 24,
    "D416": 23,
    "D417": 22,
    "D418": 4,
    "D419": 26,
    "D420": 19,
    "D421": 13,
    "D422": 27,  # Custom handling (uses GPIO 10 as source)
    "D407": 14,
    "D406": 15,
    "D405": 18,
}

# LEDs with active-high logic
active_high_leds = {"D407", "D406", "D405"}

# Special case: D422 needs GPIO 10 HIGH as source
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, GPIO.HIGH)

# Initialize LEDs, exclude D422 from gpiozero
leds = {
    label: LED(pin, active_high=(label in active_high_leds))
    for label, pin in led_map.items()
    if label != "D422"
}

# Manually control D422's sink pin (GPIO 27)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)  # Start OFF

# Track on/off states
states = {label: False for label in led_map}

print("Type D### to toggle (e.g. D414). Type 'exit' to quit.\n")

while True:
    cmd = input("LED> ").strip().upper()

    if cmd == "EXIT":
        print("Exiting. Turning all LEDs off.")
        for label, led in leds.items():
            led.off()
        # Turn off regular LEDs
        for label, led in leds.items():
            led.off()

        # Turn off D422 safely
        print("Turning off D422 and cleaning up GPIO...")
        GPIO.output(27, GPIO.HIGH)   # Stop sinking current
        GPIO.output(10, GPIO.LOW)    # Stop sourcing current
        GPIO.cleanup([10, 27])       # Release both pins
        break

    elif cmd in leds:
        if states[cmd]:
            leds[cmd].off()
            states[cmd] = False
            print(f"{cmd} is now OFF")
        else:
            leds[cmd].on()
            states[cmd] = True
            print(f"{cmd} is now ON")

    elif cmd == "D422":
        if states["D422"]:
            GPIO.output(27, GPIO.HIGH)
            states["D422"] = False
            print("D422 is now OFF")
        else:
            GPIO.output(27, GPIO.LOW)
            states["D422"] = True
            print("D422 is now ON")

    else:
        print(f"Unknown LED '{cmd}'. Try again.")