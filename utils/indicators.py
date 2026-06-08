def simple_moving_average(values, window):
    if len(values) < window:
        return None

    recent_values = values[-window:]
    return sum(recent_values) / window


def rsi(values, period=14):
    if len(values) <= period:
        return None

    gains = []
    losses = []

    recent_values = values[-(period + 1):]

    for i in range(1, len(recent_values)):
        difference = recent_values[i] - recent_values[i - 1]

        if difference > 0:
            gains.append(difference)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(difference))

    average_gain = sum(gains) / period
    average_loss = sum(losses) / period

    if average_loss == 0:
        return 100

    relative_strength = average_gain / average_loss

    return 100 - (100 / (1 + relative_strength))


def percentage_difference(value_a, value_b):
    if value_b == 0:
        return 0

    return ((value_a - value_b) / value_b) * 100


def average_candle_range_percent(candles, period=14):
    if len(candles) < period:
        return None

    recent_candles = candles[-period:]
    ranges = []

    for candle in recent_candles:
        high = candle["high"]
        low = candle["low"]
        close = candle["close"]

        if close == 0:
            continue

        range_percent = ((high - low) / close) * 100
        ranges.append(range_percent)

    if len(ranges) == 0:
        return None

    return sum(ranges) / len(ranges)