# Rotate both motors at the same time

import RPi.GPIO as GPIO
import time

# Motor pins
W1_STEP = 17
W1_DIR = 27
W2_STEP = 22
W2_DIR = 23
BLUE_LED = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(W1_STEP, GPIO.OUT)
GPIO.setup(W1_DIR, GPIO.OUT)
GPIO.setup(W2_STEP, GPIO.OUT)
GPIO.setup(W2_DIR, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)

# Set directions
GPIO.output(W1_DIR, GPIO.HIGH)  # W1 clockwise
GPIO.output(W2_DIR, GPIO.LOW)   # W2 counter-clockwise

# Turn on blue LED during motion
GPIO.output(BLUE_LED, GPIO.HIGH)

# Rotate both for 3 seconds
steps = 0
while steps < 300:
    # Step both motors
    GPIO.output(W1_STEP, GPIO.HIGH)
    GPIO.output(W2_STEP, GPIO.HIGH)
    time.sleep(0.003)
    GPIO.output(W1_STEP, GPIO.LOW)
    GPIO.output(W2_STEP, GPIO.LOW)
    time.sleep(0.007)
    steps += 1

GPIO.output(BLUE_LED, GPIO.LOW)
GPIO.cleanup()
print("Both wheels rotated")
