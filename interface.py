import os
import sys
import time
import threading
import select
import evdev
from evdev import ecodes
from messages import get_random_question, get_choices
def clear_screen(): # clear terminal screen
    os.system('clear')
def intro_sequence():
    clear_screen()
    print()
    print()
    time.sleep(1)
    typewriter_slow("  College life can get out of control...", 0.06)
    time.sleep(1.5)
    clear_screen()
    print()
    print()
    typewriter_slow("  You become consumed...", 0.07)
    time.sleep(1.2)
    clear_screen()
    print()
    print()
    typewriter_slow("  Overwhelmed...", 0.08)
    time.sleep(0.8)
    typewriter_slow("  Out. Of. Balance.", 0.12)
    time.sleep(2)
    clear_screen()
    print()
    print()
    print()
    time.sleep(0.5)
    typewriter("  WELCOME TO ALIGN ME", 0.08)
    time.sleep(2)
def typewriter(text, delay=0.04): # typewriter effect
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
def typewriter_slow(text, delay=0.07): # slow down typewriter effect
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
def show_progress(percent): #alignment percent
    clear_screen()
    print()
    print()
    typewriter(f"  {percent}% aligned", 0.03)
def ask_question(): #drandom question
    question = get_random_question()
    print()
    typewriter(f"  {question}", 0.05)
    print()
def show_choices(choices): #the choice options
    for i, choice in enumerate(choices, 1):
        typewriter(f"    {i}. {choice}", 0.02)
        time.sleep(0.1)
def get_user_choice(): #touchscreen input
    print()
    typewriter("  tap screen: 1x, 2x, or 3x", 0.02)
    print()
    tap_count = 0
    last_tap_time = 0
    tap_timeout = 0.8
    try:
        touch_device = None
        for path in evdev.list_devices():
            device = evdev.InputDevice(path)
            if 'ft5' in device.name.lower():
                touch_device = device
                break
        if touch_device:
            touch_device.grab()
            while True:
                r, w, x = select.select([touch_device.fd], [], [], 0.1)
                if r:
                    for event in touch_device.read():
                        if event.type == ecodes.EV_KEY and event.code == ecodes.BTN_TOUCH and event.value == 1:
                            tap_count += 1
                            last_tap_time = time.time()
                            sys.stdout.write(f"\r  taps: {tap_count}   ")
                            sys.stdout.flush() #
                if tap_count > 0 and (time.time() - last_tap_time) > tap_timeout: # Wait for tap timeout after last tap
                    break
            touch_device.ungrab()
            print()
            if tap_count >= 1 and tap_count <= 3: # Valid tap counts
                return tap_count - 1 # return 0, 1, or 2
            else:
                typewriter("  please tap 1, 2, or 3 times", 0.02)
                time.sleep(1)
                return None
        else:
            raise Exception("No touchscreen found")
    except Exception as e:
        print(f"  (touchscreen unavailable, using keyboard)")
        answer = input("  choose (1-3): ").strip()

        if answer not in ["1", "2", "3"]:
            typewriter("  please enter 1, 2, or 3", 0.02)
            time.sleep(1)
            return None
        return int(answer) - 1
def show_response(message): #message and pause
    clear_screen()
    print()
    print()
    typewriter(f"    {message}", 0.04)
    time.sleep(2)
    clear_screen()

def show_final_message(): #freedom message
    clear_screen()
    print()
    print()
    print()
    time.sleep(0.5)
    typewriter_slow("  you are free", 0.12)
    print()
    print()
