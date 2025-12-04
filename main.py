#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from config import MOTOR1_PINS, MOTOR2_PINS, SENSOR1_PIN, SENSOR2_PIN
from sensors import find_center
from sequences import opening_sequence, celebration_and_center, move_closer, move_away
from messages import get_choices, get_aligned_message, get_misaligned_message, record_choice, print_session_summary, reset_session
from interface import show_progress, ask_question, show_choices, get_user_choice, show_final_message, show_response, clear_screen, intro_sequence
from motors import get_position, is_aligned

def setup(): #GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in MOTOR1_PINS + MOTOR2_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    GPIO.setup(SENSOR1_PIN, GPIO.IN)
    GPIO.setup(SENSOR2_PIN, GPIO.IN)

def cleanup(): #GPIO cleanup
    GPIO.cleanup()

def run_question_loop(movement_info):    #movement_info is calculated steps per answer from awakening
    freedom_count = 0
    while not is_aligned(threshold=5):  # Shows current progress based on actual position
        pos = get_position()
        max_offset = max(abs(pos["inner"]), abs(pos["outer"]))
        starting_offset = movement_info["max_offset"] # Calculates progress as percentage toward alignment
        if starting_offset > 0:
            actual_progress = int(100 * (1 - (max_offset / starting_offset)))
            actual_progress = max(0, min(100, actual_progress))
        else:
            actual_progress = 100
        show_progress(actual_progress)
        if is_aligned(threshold=5): # Check if we've achieved alignment
            break
        ask_question()
        choices = get_choices()
        show_choices(choices)
        choice_index = get_user_choice()
        if choice_index is None:
            continue  # Invalid input, ask again
        chosen = choices[choice_index]
        record_choice(chosen)
        if chosen == "freedom":
            freedom_count += 1
            show_response(get_aligned_message())
            move_closer()  # Uses proportional steps calculated from awakening
        else:
            show_response(get_misaligned_message())
            move_away()  # Uses half-proportional steps
    show_progress(100)  # Show full alignment


def main():
    setup()
    reset_session()  # Initialize fresh session state
    intro_sequence() # Step 1: Intro sequence - title page
    find_center() # Step 2: Find center - calibration and alignment
    movement_info = opening_sequence() # Step 3: Opening animation - tracks position, returns movement info
    run_question_loop(movement_info)# Step 4: Question loop with proportional movement
    celebration_and_center()# Step 5: Celebration and return to center
    show_final_message()# Step 6: Final message
    print_session_summary()
    time.sleep(3)
    cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        cleanup()
