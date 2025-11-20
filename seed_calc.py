# Calculate seed from user choices

def calc_seed(choices):
    seed = 0
    value_ids = {
        "Money": 1,
        "Career Success": 2,
        "Recognition": 3,
        "Family Obligations": 4,
        "Social Status": 5,
        "Physical Appearance": 6,
        "Romantic Validation": 7,
        "Academic Achievement": 8,
        "Power/Control": 9,
        "Possessions/Luxury": 10,
        "Others' Approval": 11,
        "Competition/Winning": 12
    }

    for choice in choices:
        if choice in value_ids:
            seed = (seed * 13 + value_ids[choice]) % 256

    return seed

# Example usage
my_choices = ["Money", "Career Success", "Recognition"]
result = calc_seed(my_choices)
print(f"Seed: {result}")
