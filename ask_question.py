# Ask user about their values

import random

values = [
    "Money",
    "Career Success",
    "Recognition",
    "Family Obligations",
    "Social Status",
    "Physical Appearance",
    "Romantic Validation",
    "Academic Achievement",
    "Power/Control",
    "Possessions/Luxury",
    "Others' Approval",
    "Competition/Winning"
]

# Pick 3 random values
picked = random.sample(values, 3)
picked.append("Freedom")
random.shuffle(picked)

print("\nWhat are your values?")
for i, val in enumerate(picked, 1):
    print(f"{i}. {val}")

choice = input("\nEnter 1-4: ")
print(f"You chose: {picked[int(choice)-1]}")
