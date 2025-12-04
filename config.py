# pin numbers
MOTOR1_PINS = [2, 3, 17, 14] # motor 1 pins (inner wheel)
MOTOR2_PINS = [5, 6, 26, 16] # motor 2 pins (outer wheel)
SENSOR1_PIN = 1   # W1 Buddha - inner wheel
SENSOR2_PIN = 15  # W2 Prayer figure - outer wheel
# STEP_DELAY = 0.002 # UNUSED: motor timing is hardcoded in motor functions instead
STEPS_PER_REV = 200  # steps for one full revolution (NEMA 17 stepper, 1.8° per step)
MAX_ALIGNMENT_STEPS = 1600 # maximum steps before giving up on sensor alignment
STEP_SEQUENCE = [[1, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 1], [1, 0, 0, 1]]
