import time
import random
from config import MOTOR1_PINS, MOTOR2_PINS, STEPS_PER_REV
from motors import (smooth_spin_both, move_toward_home, move_away_from_home, get_position, get_offset_from_home, calculate_proportional_movement, get_steps_for_correct, get_steps_for_wrong, is_aligned)
from interface import clear_screen, typewriter
from sensors import return_to_center

def opening_sequence():
    clear_screen()
    print()
    print()
    typewriter("  awakening...", 0.08)
    time.sleep(0.5)

    smooth_spin_both("cw", "cw", 30, 0.006, 0.003)  # Initial stir - the lock senses something 30 steps, .006 delay inner, .003 delay outer
    time.sleep(0.3)
    smooth_spin_both("ccw", "ccw", 30, 0.006, 0.003)
    time.sleep(0.4)

    smooth_spin_both("cw", "cw", 150, 0.004, 0.002)  # First larger movement
    time.sleep(0.5)

    smooth_spin_both("ccw", "ccw", 180, 0.004, 0.002)  # Second larger movement
    time.sleep(0.5)

    smooth_spin_both("cw", "cw", 40, 0.005, 0.003)  # Fine tuning adjustments
    time.sleep(0.3)
    smooth_spin_both("ccw", "ccw", 50, 0.005, 0.003)
    time.sleep(0.4)

    smooth_spin_both("cw", "cw", 200, 0.003, 0.002)  # Both wheels engage
    time.sleep(0.3)

    smooth_spin_both("cw", "cw", STEPS_PER_REV, 0.002, 0.001)  # First full rotation - the mechanism releases
    time.sleep(0.2)

    smooth_spin_both("ccw", "ccw", STEPS_PER_REV, 0.002, 0.001)  # Second full rotation - confirming the unlock
    time.sleep(0.3)

    smooth_spin_both("cw", "cw", 60, 0.005, 0.003)  # Final settling - leave wheels offset from home
    time.sleep(0.2)

    movement_info = calculate_proportional_movement()  # Calculate proportional movement based on where we ended up

    print()
    typewriter("  ready", 0.06)
    time.sleep(1)

    return movement_info


def celebration_and_center():
    clear_screen()
    print()
    print()
    typewriter("  acknowledge your center", 0.06)
    time.sleep(0.5)

    for i in range(3):  # Graceful spirals - celebrating the achievement
        smooth_spin_both("cw", "ccw", 80 + i * 40, 0.005, 0.002)
        time.sleep(0.15)
        smooth_spin_both("ccw", "cw", 40, 0.004, 0.002)
        time.sleep(0.15)

    smooth_spin_both("cw", "cw", 150, 0.004, 0.002)  # Harmonious convergence - beginning the return
    time.sleep(0.25)
    smooth_spin_both("ccw", "ccw", 150, 0.004, 0.002)
    time.sleep(0.25)

    smooth_spin_both("cw", "ccw", 100, 0.005, 0.003)  # Gentle settling motion
    time.sleep(0.3)

    return_to_center()  # Smoothly return to center (sensor alignment)
    time.sleep(0.5)

def move_closer():
    steps = get_steps_for_correct()  # Uses proportional steps calculated from awakening sequence
    actual_steps = move_toward_home(steps)
    return actual_steps

def move_away():
    steps = get_steps_for_wrong()  # Uses proportional steps 
    actual_steps = move_away_from_home(steps)
    return actual_steps
