from data.market_data import MarketData
from strategies.moving_average_strategy import MovingAverageStrategy


def main():
    market_data = MarketData()
    candles = market_data.fetch_ohlcv(limit=100)

    strategy = MovingAverageStrategy(window=20)
    result = strategy.generate_signal(candles)

    print(result)


if __name__ == "__main__":
    main()