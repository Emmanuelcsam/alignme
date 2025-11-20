# Calculate motor speeds from seed

def get_speeds(seed):
    # W1: 60-90 RPM
    w1_speed = 60 + (seed % 31)

    # W2: 45-75 RPM
    w2_speed = 45 + ((seed * 7) % 31)

    # Rotations: 2-4
    w1_rotations = 2 + (seed % 3)
    w2_rotations = 2 + ((seed * 3) % 3)

    return w1_speed, w2_speed, w1_rotations, w2_rotations

# Test with a seed
test_seed = 142
w1_rpm, w2_rpm, w1_rot, w2_rot = get_speeds(test_seed)

print(f"Seed: {test_seed}")
print(f"W1: {w1_rpm} RPM, {w1_rot} rotations")
print(f"W2: {w2_rpm} RPM, {w2_rot} rotations")
