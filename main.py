from data.market_data import MarketData
from strategies.moving_average_strategy import MovingAverageStrategy


def main():
    market_data = MarketData()
    candles = market_data.fetch_ohlcv(limit=100)

    strategy = MovingAverageStrategy(window=20)
    signal = strategy.generate_signal(candles)

    print(f"Sinal gerado: {signal}")


if __name__ == "__main__":
    main()