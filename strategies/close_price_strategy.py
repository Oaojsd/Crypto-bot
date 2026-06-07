from strategies.base_strategy import BaseStrategy


class ClosePriceStrategy(BaseStrategy):
    def generate_signal(self, candles):
        last_candle = candles[-1]

        current_price = last_candle["close"]

        print(f"Preço atual: {current_price}")

        return "HOLD"