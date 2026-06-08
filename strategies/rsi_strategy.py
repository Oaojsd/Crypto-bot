from strategies.base_strategy import BaseStrategy
from utils.indicators import rsi


class RsiStrategy(BaseStrategy):
    def __init__(self, period=14):
        self.period = period

    def generate_signal(self, candles):
        closes = []

        for candle in candles:
            closes.append(candle["close"])

        current_rsi = rsi(closes, self.period)

        if current_rsi is None:
            return {
                "strategy": "rsi",
                "signal": "HOLD",
                "strength": 0.0
            }

        if current_rsi < 30:
            return {
                "strategy": "rsi",
                "signal": "BUY",
                "strength": 0.70
            }

        if current_rsi > 70:
            return {
                "strategy": "rsi",
                "signal": "SELL",
                "strength": 0.70
            }

        return {
            "strategy": "rsi",
            "signal": "HOLD",
            "strength": 0.20
        }