from strategies.base_strategy import BaseStrategy
from utils.indicators import simple_moving_average, percentage_difference


class MarketRegimeFilter(BaseStrategy):
    def __init__(
        self,
        short_window=50,
        long_window=200,
        min_trend_percent=0.50
    ):
        self.short_window = short_window
        self.long_window = long_window
        self.min_trend_percent = min_trend_percent

    def generate_signal(self, candles):
        closes = []

        for candle in candles:
            closes.append(candle["close"])

        short_average = simple_moving_average(closes, self.short_window)
        long_average = simple_moving_average(closes, self.long_window)

        if short_average is None or long_average is None:
            return {
                "strategy": "market_regime_filter",
                "signal": "BLOCK_BUY",
                "strength": 1.0,
                "regime": "UNKNOWN",
                "reason": "NOT_ENOUGH_DATA"
            }

        difference = percentage_difference(short_average, long_average)

        if difference > self.min_trend_percent:
            return {
                "strategy": "market_regime_filter",
                "signal": "ALLOW",
                "strength": 0.0,
                "regime": "BULL",
                "difference": difference
            }

        if difference < -self.min_trend_percent:
            return {
                "strategy": "market_regime_filter",
                "signal": "BLOCK_BUY",
                "strength": 1.0,
                "regime": "BEAR",
                "difference": difference
            }

        return {
            "strategy": "market_regime_filter",
            "signal": "ALLOW",
            "strength": 0.0,
            "regime": "SIDEWAYS",
            "difference": difference
        }