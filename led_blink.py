# Blink different colored LEDs

import RPi.GPIO as GPIO
import time

# LED pins
GREEN_LED = 5
BLUE_LED = 6
WHITE_LED = 13
RED_LED = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(WHITE_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

# Blink green 3 times
for _ in range(3):
    GPIO.output(GREEN_LED, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(GREEN_LED, GPIO.LOW)
    time.sleep(0.5)

# Turn on blue
GPIO.output(BLUE_LED, GPIO.HIGH)
time.sleep(2)
GPIO.output(BLUE_LED, GPIO.LOW)

# Flash white
GPIO.output(WHITE_LED, GPIO.HIGH)
time.sleep(1)
GPIO.output(WHITE_LED, GPIO.LOW)

GPIO.cleanup()
print("LEDs blinked")
