# Slow approach for final alignment

import RPi.GPIO as GPIO
import time

# Pins
W2_STEP = 22
W2_DIR = 23
PHOTO2 = 25
WHITE_LED = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(W2_STEP, GPIO.OUT)
GPIO.setup(W2_DIR, GPIO.OUT)
GPIO.setup(PHOTO2, GPIO.IN)
GPIO.setup(WHITE_LED, GPIO.OUT)

# Set direction
GPIO.output(W2_DIR, GPIO.LOW)

print("Starting slow alignment approach (20 RPM)...")

# Move slowly until sensor triggered
aligned = False
for _ in range(100):  # Max 100 steps
    if GPIO.input(PHOTO2):
        aligned = True
        print("ALIGNMENT DETECTED!")
        GPIO.output(WHITE_LED, GPIO.HIGH)
        break

    # Single step at slow speed (20 RPM)
    GPIO.output(W2_STEP, GPIO.HIGH)
    time.sleep(0.015)
    GPIO.output(W2_STEP, GPIO.LOW)
    time.sleep(0.015)

if not aligned:
    print("Alignment not achieved in slow approach")

time.sleep(2)
GPIO.cleanup()
