from data.market_data import MarketData
from strategies.close_price_strategy import ClosePriceStrategy


def main():
    market_data = MarketData()

    candles = market_data.fetch_ohlcv(limit=100)

    strategy = ClosePriceStrategy()

    signal = strategy.generate_signal(candles)

    print(f"Sinal gerado: {signal}")


if __name__ == "__main__":
    main()