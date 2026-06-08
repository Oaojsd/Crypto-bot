from strategies.base_strategy import BaseStrategy
from utils.indicators import simple_moving_average, percentage_difference


class TrendStrengthFilter(BaseStrategy):
    def __init__(
        self,
        short_window=12,
        long_window=26,
        min_difference_percent=0.20
    ):
        self.short_window = short_window
        self.long_window = long_window
        self.min_difference_percent = min_difference_percent

    def generate_signal(self, candles):
        closes = []

        for candle in candles:
            closes.append(candle["close"])

        short_average = simple_moving_average(closes, self.short_window)
        long_average = simple_moving_average(closes, self.long_window)

        if short_average is None or long_average is None:
            return {
                "strategy": "trend_strength_filter",
                "signal": "BLOCK",
                "strength": 1.0,
                "reason": "NOT_ENOUGH_DATA"
            }

        difference = abs(
            percentage_difference(short_average, long_average)
        )

        if difference < self.min_difference_percent:
            return {
                "strategy": "trend_strength_filter",
                "signal": "BLOCK",
                "strength": 1.0,
                "reason": "WEAK_TREND",
                "difference": difference
            }

        return {
            "strategy": "trend_strength_filter",
            "signal": "ALLOW",
            "strength": 0.0,
            "reason": "STRONG_ENOUGH_TREND",
            "difference": difference
        }