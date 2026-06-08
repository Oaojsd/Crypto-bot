from strategies.base_strategy import BaseStrategy
from utils.indicators import simple_moving_average


class PriceConfirmationFilter(BaseStrategy):
    def __init__(self, long_window=26):
        self.long_window = long_window

    def generate_signal(self, candles):
        closes = []

        for candle in candles:
            closes.append(candle["close"])

        long_average = simple_moving_average(closes, self.long_window)
        current_price = closes[-1]

        if long_average is None:
            return {
                "strategy": "price_confirmation_filter",
                "signal": "BLOCK_BUY",
                "strength": 1.0,
                "reason": "NOT_ENOUGH_DATA"
            }

        if current_price < long_average:
            return {
                "strategy": "price_confirmation_filter",
                "signal": "BLOCK_BUY",
                "strength": 1.0,
                "reason": "PRICE_BELOW_LONG_AVERAGE",
                "current_price": current_price,
                "long_average": long_average
            }

        return {
            "strategy": "price_confirmation_filter",
            "signal": "ALLOW",
            "strength": 0.0,
            "reason": "PRICE_ABOVE_LONG_AVERAGE",
            "current_price": current_price,
            "long_average": long_average
        }