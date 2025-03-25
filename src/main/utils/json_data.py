import json
import os


# Define the path to the JSON file
USER_ACCESS_FILE = os.path.join('data', 'user_access.json')

def load_user_access():
    """Load user access information from the JSON file."""
    if os.path.exists(USER_ACCESS_FILE):
        with open(USER_ACCESS_FILE, 'r') as f:
            return json.load(f)

    data = {
            "last_acess": " ",
            "daily_sequence": 0,
            "total_victories": {
                "main": 0,
                "chinease": 0,
                "crazy": 0,
                "gnome": 0
            }
        }
    save_user_access(data)
    return data

def save_user_access(data):
    """Save user access information to the JSON file."""
    with open(USER_ACCESS_FILE, 'w') as f:
        json.dump(data, f, indent=4)