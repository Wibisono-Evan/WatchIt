from datetime import datetime


def get_time_based_greeting():
    # Fetch the current hour (0 to 23) from the local system time
    current_hour = datetime.now().hour

    # Check time ranges to determine the correct greeting
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"
