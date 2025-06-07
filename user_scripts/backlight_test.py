import RPi.GPIO as GPIO
import time

RELAY_GPIO = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_GPIO, GPIO.OUT)
GPIO.output(RELAY_GPIO, GPIO.LOW)  # Relay off initially

print("Type 'on', 'off', or 'q' to quit.\n")

try:
    while True:
        cmd = input("Relay> ").strip().lower()

        if cmd == "on":
            GPIO.output(RELAY_GPIO, GPIO.HIGH)
            print("Relay ON – screen should be on.")
        elif cmd == "off":
            GPIO.output(RELAY_GPIO, GPIO.LOW)
            print("Relay OFF – screen should be off.")
        elif cmd == "q":
            break
        else:
            print("Unknown command.")
except KeyboardInterrupt:
    pass
finally:
    GPIO.output(RELAY_GPIO, GPIO.LOW)
    GPIO.cleanup()
    print("Clean exit.")