# Spin motor W2 (outer wheel)

import RPi.GPIO as GPIO
import time

# Motor W2 pins
STEP_PIN = 22
DIR_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# Spin counter-clockwise
GPIO.output(DIR_PIN, GPIO.LOW)

# Make it spin slower than W1
for _ in range(600):  # 3 rotations
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(0.007)
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(0.007)

GPIO.cleanup()
print("W2 spun 3 times")
