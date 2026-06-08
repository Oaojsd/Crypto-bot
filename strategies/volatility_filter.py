from strategies.base_strategy import BaseStrategy
from utils.indicators import average_candle_range_percent


class VolatilityFilter(BaseStrategy):
    def __init__(
        self,
        period=14,
        min_volatility_percent=0.25,
        max_volatility_percent=4.0
    ):
        self.period = period
        self.min_volatility_percent = min_volatility_percent
        self.max_volatility_percent = max_volatility_percent

    def generate_signal(self, candles):
        volatility = average_candle_range_percent(
            candles=candles,
            period=self.period
        )

        if volatility is None:
            return {
                "strategy": "volatility_filter",
                "signal": "BLOCK",
                "strength": 1.0,
                "reason": "NOT_ENOUGH_DATA"
            }

        if volatility < self.min_volatility_percent:
            return {
                "strategy": "volatility_filter",
                "signal": "BLOCK",
                "strength": 1.0,
                "reason": "LOW_VOLATILITY",
                "volatility": volatility
            }

        if volatility > self.max_volatility_percent:
            return {
                "strategy": "volatility_filter",
                "signal": "BLOCK",
                "strength": 1.0,
                "reason": "HIGH_VOLATILITY",
                "volatility": volatility
            }

        return {
            "strategy": "volatility_filter",
            "signal": "ALLOW",
            "strength": 0.0,
            "reason": "NORMAL_VOLATILITY",
            "volatility": volatility
        }