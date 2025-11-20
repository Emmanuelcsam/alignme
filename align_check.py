import RPi.GPIO as GPIO

# Photodiode pins
PHOTO1_PIN = 24  # Buddha sensor
PHOTO2_PIN = 25  # Prayer sensor
WHITE_LED = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(PHOTO1_PIN, GPIO.IN)
GPIO.setup(PHOTO2_PIN, GPIO.IN)
GPIO.setup(WHITE_LED, GPIO.OUT)

def is_aligned():
    buddha = GPIO.input(PHOTO1_PIN)
    prayer = GPIO.input(PHOTO2_PIN)

    if buddha and prayer:
        return True
    return False

# Check alignment
if is_aligned():
    print("ALIGNED! Buddha and Prayer figure are together!")
    GPIO.output(WHITE_LED, GPIO.HIGH)
else:
    print("Not aligned yet")
    GPIO.output(WHITE_LED, GPIO.LOW)

GPIO.cleanup()
