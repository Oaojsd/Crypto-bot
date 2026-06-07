def simple_moving_average(values, window):
    if len(values) < window:
        return None

    recent_values = values[-window:]
    return sum(recent_values) / window