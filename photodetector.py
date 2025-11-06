import RPi.GPIO as GPIO

PHOTO1_PIN = 24  # For W1
PHOTO2_PIN = 25  # For W2

GPIO.setmode(GPIO.BCM)
GPIO.setup(PHOTO1_PIN, GPIO.IN)
GPIO.setup(PHOTO2_PIN, GPIO.IN)

sensor1 = GPIO.input(PHOTO1_PIN)
sensor2 = GPIO.input(PHOTO2_PIN)

if sensor1:
    print("W1 Buddha detected")
else:
    print("W1 Buddha not detected")
