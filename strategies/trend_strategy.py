from strategies.base_strategy import BaseStrategy
from utils.indicators import simple_moving_average, percentage_difference


class TrendStrategy(BaseStrategy):
    def __init__(self, short_window=9, long_window=21):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, candles):
        closes = []

        for candle in candles:
            closes.append(candle["close"])

        short_average = simple_moving_average(closes, self.short_window)
        long_average = simple_moving_average(closes, self.long_window)

        if short_average is None or long_average is None:
            return {
                "strategy": "trend",
                "signal": "HOLD",
                "strength": 0.0
            }

        difference = percentage_difference(short_average, long_average)

        if difference > 0.15:
            return {
                "strategy": "trend",
                "signal": "BUY",
                "strength": 0.75
            }

        if difference < -0.15:
            return {
                "strategy": "trend",
                "signal": "SELL",
                "strength": 0.75
            }

        return {
            "strategy": "trend",
            "signal": "HOLD",
            "strength": 0.20
        }