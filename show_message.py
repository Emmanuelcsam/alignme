# Show affirmation message

def get_message(seed):
    messages = [
        "Your inner compass points true. Trust your journey.",
        "What you release makes space for what matters most.",
        "Each rotation brings clarity to your centered self.",
        "Values aligned, peace defined. Breathe into this moment.",
        "The path inward illuminates the way forward.",
        "In letting go, you've found what cannot be taken.",
        "Thank you for choosing presence over pressure."
    ]

    index = seed % 7
    return messages[index]

# Pick message based on seed
my_seed = 42
msg = get_message(my_seed)

print("\n" + "="*50)
print("✨ ALIGNMENT ACHIEVED ✨")
print("="*50)
print(f"\n{msg}\n")
print("="*50)
