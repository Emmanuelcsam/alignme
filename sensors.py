import RPi.GPIO as GPIO
import time
from config import MOTOR1_PINS, MOTOR2_PINS, SENSOR1_PIN, SENSOR2_PIN
from config import STEP_SEQUENCE, MAX_ALIGNMENT_STEPS
from motors import stop_motor, reset_position, set_calibration
from interface import clear_screen, typewriter

def find_sensor(motor_pins, sensor_pin, direction):
    if GPIO.input(sensor_pin) == 1: #checks if already on sensor
        time.sleep(2)
        if GPIO.input(sensor_pin) == 1:
            return 0
    steps = 0     # Initialize step counter to track how far motor has moved
    while GPIO.input(sensor_pin) == 0: # steps % 4 gives us 0, 1, 2, 3, 0...
        if direction == "cw":
            pattern = STEP_SEQUENCE[steps % 4]
        else:
            pattern = STEP_SEQUENCE[-(steps % 4) - 1] #[3], [2], [1], [0], [3]...
        for j, pin in enumerate(motor_pins):
            GPIO.output(pin, pattern[j])  # (index, pin) set each pin HIGH (1) or LOW (0)
        time.sleep(0.003)
        steps += 1  # Increment step counter to move to next pattern in sequence
        if steps > MAX_ALIGNMENT_STEPS: #stop if too many steps taken
            stop_motor(motor_pins)
            return -1
    stop_motor(motor_pins)
    time.sleep(2)  # Hold position
    return steps


def align_both_wheels():
    result1 = find_sensor(MOTOR1_PINS, SENSOR1_PIN, "cw")     # Align inner wheel
    time.sleep(0.3)
    result2 = find_sensor(MOTOR2_PINS, SENSOR2_PIN, "ccw")     # Align outer wheel
    time.sleep(0.3)

    if result1 >= 0 and result2 >= 0:
        reset_position()     # Reset position tracking - this is now home (0, 0)
        return True
    else:
        typewriter("  alignment incomplete", 0.04)
        time.sleep(1)
        return False

def return_to_center():
    find_sensor(MOTOR1_PINS, SENSOR1_PIN, "cw")
    time.sleep(0.3)
    find_sensor(MOTOR2_PINS, SENSOR2_PIN, "ccw")
    reset_position()

def calibrate_full_rotation(motor_pins, sensor_pin, direction):
    if GPIO.input(sensor_pin) != 1: # Move to find sensor first
        steps = 0
        while GPIO.input(sensor_pin) == 0 and steps < MAX_ALIGNMENT_STEPS:
            if direction == "cw":
                pattern = STEP_SEQUENCE[steps % 4]
            else:
                pattern = STEP_SEQUENCE[-(steps % 4) - 1]
            for j, pin in enumerate(motor_pins):
                GPIO.output(pin, pattern[j])
            time.sleep(0.003)
            steps += 1
        stop_motor(motor_pins)
        time.sleep(0.5)
    off_steps = 0 # move move OFF the sensor
    while GPIO.input(sensor_pin) == 1 and off_steps < 100:
        if direction == "cw":
            pattern = STEP_SEQUENCE[off_steps % 4]
        else:
            pattern = STEP_SEQUENCE[-(off_steps % 4) - 1]
        for j, pin in enumerate(motor_pins):
            GPIO.output(pin, pattern[j])
        time.sleep(0.003)
        off_steps += 1
    stop_motor(motor_pins)
    time.sleep(0.2)
    revolution_steps = 0 #steps for a full rotation back to sensor
    while GPIO.input(sensor_pin) == 0 and revolution_steps < MAX_ALIGNMENT_STEPS:
        if direction == "cw":
            pattern = STEP_SEQUENCE[revolution_steps % 4]
        else:
            pattern = STEP_SEQUENCE[-(revolution_steps % 4) - 1]
        for j, pin in enumerate(motor_pins):
            GPIO.output(pin, pattern[j])
        time.sleep(0.003)
        revolution_steps += 1
    stop_motor(motor_pins)
    time.sleep(0.3)
    total_steps = off_steps + revolution_steps
    return total_steps

def calibrate_both_wheels():
    inner_steps = calibrate_full_rotation(MOTOR1_PINS, SENSOR1_PIN, "cw")
    time.sleep(0.3)
    outer_steps = calibrate_full_rotation(MOTOR2_PINS, SENSOR2_PIN, "ccw")
    time.sleep(0.3)
    set_calibration(inner_steps, outer_steps) # Store calibration data
    reset_position()
    return {"inner": inner_steps, "outer": outer_steps}


def find_center():
    clear_screen()
    print()
    print()
    typewriter("  finding center...", 0.05)
    time.sleep(0.5)
    calibration_data = calibrate_both_wheels() #(measure steps per revolution)
    time.sleep(0.3)
    result = align_both_wheels() # Align to sensors
    time.sleep(0.3)
    if result:
        typewriter("  centered", 0.06)
        time.sleep(1)
        return calibration_data
    else:
        return None
