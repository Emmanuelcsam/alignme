# Show welcome message

import RPi.GPIO as GPIO
import time

GREEN_LED = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_LED, GPIO.OUT)

print("\n" + "="*60)
print("           WELCOME TO ALIGNME")
print("     Align your values, find your freedom")
print("="*60)
print("\nA mindfulness experience by Team Insight")
print("\nReady to explore what matters most to you?")
print("="*60 + "\n")

# Turn on green LED
GPIO.output(GREEN_LED, GPIO.HIGH)
time.sleep(3)
GPIO.output(GREEN_LED, GPIO.LOW)

GPIO.cleanup()
print("Press ENTER to begin...")
