import RPi.GPIO as GPIO
import time

# GPIO setup
output_pins = {
    5: "B1",
    6: "B2",
    12: "B3"
}
input_pins = {
    9: "B4",
    16: "B5",
    20: "B6",
    21: "B7"
}

GPIO.setmode(GPIO.BCM)

# Setup output pins
for pin in output_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Default HIGH (inactive)

# Setup input pins with pull-ups
for pin in input_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Scanning for button presses... (Ctrl+C to exit)")

try:
    while True:
        for out_pin, out_label in output_pins.items():
            GPIO.output(out_pin, GPIO.LOW)  # Activate this row
            time.sleep(0.01)  # Short delay for stability

            for in_pin, in_label in input_pins.items():
                if GPIO.input(in_pin) == GPIO.LOW:
                    print(f"Button press between {out_label} (GPIO{out_pin}) and {in_label} (GPIO{in_pin})")

            GPIO.output(out_pin, GPIO.HIGH)  # Deactivate row
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting.")
finally:
    GPIO.cleanup()
