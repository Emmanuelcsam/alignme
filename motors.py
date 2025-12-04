import RPi.GPIO as GPIO
import time
import threading
from config import MOTOR1_PINS, MOTOR2_PINS, STEP_SEQUENCE

class CalibrationData: # actual measured steps per full rotation
    def __init__(self):
        self.inner_steps_per_rev = 200
        self.outer_steps_per_rev = 200
        self.calibrated = False
    def set_calibration(self, inner_steps, outer_steps):
        """Store measured steps per revolution"""
        self.inner_steps_per_rev = inner_steps
        self.outer_steps_per_rev = outer_steps
        self.calibrated = True
    def get_calibration(self):
        return {"inner": self.inner_steps_per_rev, "outer": self.outer_steps_per_rev, "calibrated": self.calibrated}
calibration = CalibrationData()
class WheelPosition: # Position tracking (steps from home position), Positive = CW from home, Negative = CCW from home
    def __init__(self):
        self.inner = 0  # Motor 1 position
        self.outer = 0  # Motor 2 position
        self.starting_inner_offset = 0  # Movement calculation state, Offset after awakening sequence
        self.starting_outer_offset = 0
        self.steps_per_correct_answer = 0  # Calculated after awakening
        self.required_correct_answers = 3  # Need 3 freedom choices to align
    def reset(self): #Reset positions to home (0)
        self.inner = 0
        self.outer = 0
    def update(self, motor, direction, steps): # Update position after movement
        delta = steps if direction == "cw" else -steps
        if motor == "inner":
            self.inner += delta
        else:
            self.outer += delta
    def get_offset(self): # Get combined offset from home (absolute value sum)
        return abs(self.inner) + abs(self.outer)

    def get_positions(self):# Get current positions
        return {"inner": self.inner, "outer": self.outer}
    def calculate_movement_per_answer(self):
        self.starting_inner_offset = abs(self.inner)
        self.starting_outer_offset = abs(self.outer)
        max_offset = max(self.starting_inner_offset, self.starting_outer_offset) # Use the larger offset to ensure both wheels can align
        self.steps_per_correct_answer = max(1, (max_offset + 2) // self.required_correct_answers) # Each correct answer moves 1/3 of the way to alignment,Add a small buffer to ensure we reach home
        return { "inner_offset": self.starting_inner_offset, "outer_offset": self.starting_outer_offset, "max_offset": max_offset, "steps_per_answer": self.steps_per_correct_answer }
    def get_steps_for_correct(self): #Get steps to move toward home for a correct answer
        return self.steps_per_correct_answer
    def get_steps_for_wrong(self): #Get steps to move away from home for a wrong answer, Moving away by half the correct amount so player can recover.
        return max(1, self.steps_per_correct_answer // 2)
position = WheelPosition() # Global position tracker
def stop_motor(pins): #Turn off a motor
    for pin in pins:
        GPIO.output(pin, 0)
def spin_motor(pins, direction, steps, delay, track=True): #spin motor in specified direction for given steps at fixed delay
    for i in range(steps):
        if direction == "cw":
            pattern = STEP_SEQUENCE[i % 4]
        else:
            pattern = STEP_SEQUENCE[-(i % 4) - 1]
        for j, pin in enumerate(pins):
            GPIO.output(pin, pattern[j])
        time.sleep(delay)
    stop_motor(pins)
    if track: # Track position
        motor = "inner" if pins == MOTOR1_PINS else "outer"
        position.update(motor, direction, steps)
def smooth_spin(pins, direction, steps, start_delay=0.006, end_delay=0.002, track=True): #Spin with acceleration - starts slow, speeds up, then slows down
    if steps < 10:
        spin_motor(pins, direction, steps, (start_delay + end_delay) / 2, track)
        return
    ramp = steps // 4
    for i in range(ramp): # Speed up
        delay = start_delay - (start_delay - end_delay) * (i / ramp)
        if direction == "cw":
            pattern = STEP_SEQUENCE[i % 4]
        else:
            pattern = STEP_SEQUENCE[-(i % 4) - 1]
        for j, pin in enumerate(pins):
            GPIO.output(pin, pattern[j])
        time.sleep(delay)
    for i in range(ramp, steps - ramp): # Full speed
        if direction == "cw":
            pattern = STEP_SEQUENCE[i % 4]
        else:
            pattern = STEP_SEQUENCE[-(i % 4) - 1]
        for j, pin in enumerate(pins):
            GPIO.output(pin, pattern[j])
        time.sleep(end_delay)
    for i in range(steps - ramp, steps): # Slow down
        progress = (i - (steps - ramp)) / ramp
        delay = end_delay + (start_delay - end_delay) * progress
        if direction == "cw":
            pattern = STEP_SEQUENCE[i % 4]
        else:
            pattern = STEP_SEQUENCE[-(i % 4) - 1]
        for j, pin in enumerate(pins):
            GPIO.output(pin, pattern[j])
        time.sleep(delay)
    stop_motor(pins)
    if track: # Track position
        motor = "inner" if pins == MOTOR1_PINS else "outer"
        position.update(motor, direction, steps)
def smooth_spin_both(dir1, dir2, steps, start_delay=0.006, end_delay=0.002, track=True): #Spin both motors smoothly at the same time
    t1 = threading.Thread(target=smooth_spin, args=(MOTOR1_PINS, dir1, steps, start_delay, end_delay, track))
    t2 = threading.Thread(target=smooth_spin, args=(MOTOR2_PINS, dir2, steps, start_delay, end_delay, track))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
def reset_position(): #Reset position tracking to home
    position.reset()
def get_position(): #Get current wheel positions
    return position.get_positions()
def get_offset_from_home(): #Get total offset from home position
    return position.get_offset()
def set_calibration(inner_steps, outer_steps): #Store calibration data from measurement
    calibration.set_calibration(inner_steps, outer_steps)
def get_calibration(): #Get calibration data
    return calibration.get_calibration()
def calculate_proportional_movement():
    return position.calculate_movement_per_answer()
def get_steps_for_correct(): #Get calculated steps for a correct (freedom) answer
    return position.get_steps_for_correct()
def get_steps_for_wrong(): #Get calculated steps for a wrong (distraction) answer
    return position.get_steps_for_wrong()
def move_toward_home(steps):
    pos = position.get_positions() # Calculate direction needed to move toward 0 for each wheel
    inner_dir = "ccw" if pos["inner"] > 0 else "cw"
    outer_dir = "ccw" if pos["outer"] > 0 else "cw"
    inner_steps = min(steps, abs(pos["inner"])) #limit steps to current offset for each wheel
    outer_steps = min(steps, abs(pos["outer"]))
    if inner_steps == 0 and outer_steps == 0: # If a wheel is already at home, don't move it
        return 0
    # Move each wheel the appropriate amount,then use threaded movement but with different step counts
    if inner_steps > 0 and outer_steps > 0:
        # Both need movement
        actual_steps = max(inner_steps, outer_steps)
        t1 = threading.Thread(target=smooth_spin, args=(MOTOR1_PINS, inner_dir, inner_steps, 0.005, 0.003, True))
        t2 = threading.Thread(target=smooth_spin, args=(MOTOR2_PINS, outer_dir, outer_steps, 0.005, 0.003, True))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    elif inner_steps > 0:
        smooth_spin(MOTOR1_PINS, inner_dir, inner_steps, 0.005, 0.003, True)
        actual_steps = inner_steps
    else:
        smooth_spin(MOTOR2_PINS, outer_dir, outer_steps, 0.005, 0.003, True)
        actual_steps = outer_steps
    return actual_steps
def move_away_from_home(steps):  #Move wheels away from home position by specified steps, and continues in current direction (away from 0).
    pos = position.get_positions()
    # Use the starting offset direction if we're at or near 0
    if pos["inner"] > 0: # Continue in current direction (away from 0)
        inner_dir = "cw"  # Positive, keep going positive
    elif pos["inner"] < 0:
        inner_dir = "ccw"  # Negative, keep going negative
    else:
        inner_dir = "cw" if position.starting_inner_offset >= 0 else "ccw" #At zero - use original direction from awakening
    if pos["outer"] > 0:
        outer_dir = "cw"
    elif pos["outer"] < 0:
        outer_dir = "ccw"
    else:
        outer_dir = "cw" if position.starting_outer_offset >= 0 else "ccw"
    smooth_spin_both(inner_dir, outer_dir, steps, 0.005, 0.003)
    return steps
def is_aligned(threshold=5): #Check if both wheels are within threshold of home position
    pos = position.get_positions()
    return abs(pos["inner"]) <= threshold and abs(pos["outer"]) <= threshold
