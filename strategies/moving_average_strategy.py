from strategies.base_strategy import BaseStrategy
from utils.indicators import simple_moving_average


class MovingAverageStrategy(BaseStrategy):
    def __init__(self, window=20):
        self.window = window

    def generate_signal(self, candles):
        closes = []

        for candle in candles:
            closes.append(candle["close"])

        average = simple_moving_average(closes, self.window)
        current_price = closes[-1]

        if average is None:
            return {
                "strategy": "moving_average",
                "signal": "HOLD",
                "strength": 0.0
            }

        print(f"Preço atual: {current_price}")
        print(f"Média móvel {self.window}: {average}")

        if current_price > average:
            return {
                "strategy": "moving_average",
                "signal": "BUY",
                "strength": 0.60
            }

        if current_price < average:
            return {
                "strategy": "moving_average",
                "signal": "SELL",
                "strength": 0.60
            }

        return {
            "strategy": "moving_average",
            "signal": "HOLD",
            "strength": 0.0
        }