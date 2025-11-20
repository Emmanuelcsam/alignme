# Save session data to CSV file

import csv
from datetime import datetime

def save_data():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"alignme_session_{timestamp}.csv"

    data = {
        'session_id': '001',
        'timestamp': datetime.now().isoformat(),
        'seed': 42,
        'choices_before_freedom': 'Money,Career',
        'num_questions': 3,
        'W1_speed_rpm': 75,
        'W1_rotations': 3,
        'W2_speed_rpm': 60,
        'W2_rotations': 2,
        'alignment_error_deg': 3.5,
        'affirmation_index': 2,
        'affirmation_text': 'Each rotation brings clarity to your centered self.',
        'duration_sec': 75
    }

    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)

    print(f"Data saved to {filename}")

save_data()
