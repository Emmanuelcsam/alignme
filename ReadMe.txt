1: Hardware Initialization & Calibration

Session Reset (reset_session):

Clears previous user choices.

Re-initializes the Pseudo-Random Number Generator (PRNG) with a null seed.

Physical Homing (find_center):

Calibration: The system runs calibrate_both_wheels. It spins wheels until sensors trigger, moves off them, spins back, and counts the steps. This dynamically calculates the hardware's specific STEPS_PER_REV (handling belt tension/motor variance).

Alignment: Wheels move to the sensor trigger point.

Zeroing: Logical coordinate system (motors.py/WheelPosition) is set to (0, 0) at this physical location.

2: The Awakening 

Animation (opening_sequence):

Motors perform a fixed, choreographed set of movements (spirals, large rotations).

The sequence deliberately ends with the wheels misaligned from home (non-zero coordinates).

Difficulty Calculation (calculate_proportional_movement):

System snapshots the final "misaligned" coordinates (e.g., Inner: +400, Outer: -200).

Determines the maximum offset and divides by required_correct_answers (3).

Defines exactly how many stepper motor steps constitute one "unit" of progress for this specific session.

3: The Interaction Loop (gameplay)

Condition: Loops continuously while wheel positions are outside the alignment threshold (+/- 5 steps).

Progress Display: Calculates percentage based on (Current Offset / Starting Offset).

Input Generation:

Selects a question using seeded RNG.

Generates 3 choices: 2 Distractions (from list), 1 "Freedom".

Shuffles positions.

User Input:

Polls touchscreen for taps (1, 2, or 3). Falls back to keyboard if no touchscreen found.

Logic Branch:

IF "Freedom" (Correct):

Motor Driver: Calls move_toward_home.

Action: Wheels rotate towards (0,0) by the calculated "step unit".

UI: Displays "Aligned" message.

IF Distraction (Incorrect):

Motor Driver: Calls move_away_from_home.

Action: Wheels rotate away from (0,0) by half of a "step unit" (penalty).

UI: Displays "Misaligned" message.

State Update: New positions are recorded. Loop repeats.

4: Resolution & Termination

Alignment Detection: Loop breaks when position abs(inner) < 5 and abs(outer) < 5.

Celebration (celebration_and_center):

Performs "victory" spirals.

Safety Check: Calls return_to_center() to force a physical sensor check, ensuring the machine ends exactly at the home position regardless of calculation rounding errors.

Logging: Prints session statistics (choices made, calibration data, final offsets).



