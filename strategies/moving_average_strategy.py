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
            return "HOLD"

        print(f"Preço atual: {current_price}")
        print(f"Média móvel {self.window}: {average}")

        if current_price > average:
            return "BUY"

        if current_price < average:
            return "SELL"

        return "HOLD"