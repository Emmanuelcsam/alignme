# Spin motor W1 (inner wheel)

import RPi.GPIO as GPIO
import time

# Motor W1 pins
STEP_PIN = 17
DIR_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# Spin clockwise
GPIO.output(DIR_PIN, GPIO.HIGH)

# Make it spin (200 steps = 1 rotation)
for _ in range(400):  # 2 rotations
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(0.005)
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(0.005)

GPIO.cleanup()
print("W1 spun 2 times")
