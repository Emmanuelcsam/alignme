# Check emergency stop button

import RPi.GPIO as GPIO
import time

# E-stop button pin
ESTOP_PIN = 26
RED_LED = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(ESTOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RED_LED, GPIO.OUT)

print("Press E-STOP button to test...")

while True:
    if GPIO.input(ESTOP_PIN) == GPIO.LOW:
        print("EMERGENCY STOP PRESSED!")
        GPIO.output(RED_LED, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(RED_LED, GPIO.LOW)
        break
    time.sleep(0.1)

GPIO.cleanup()
print("E-stop test complete")
