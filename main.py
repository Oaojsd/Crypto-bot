from core.decision_engine import DecisionEngine
from data.market_data import MarketData
from strategies.moving_average_strategy import MovingAverageStrategy
from strategies.rsi_strategy import RsiStrategy


def main():
    market_data = MarketData()
    candles = market_data.fetch_ohlcv(limit=100)

    strategies = [
        MovingAverageStrategy(window=20),
        RsiStrategy(period=14)
]

    strategy_results = []

    for strategy in strategies:
        result = strategy.generate_signal(candles)
        strategy_results.append(result)

    decision_engine = DecisionEngine()
    final_decision = decision_engine.decide(strategy_results)

    print("Resultados das estratégias:")
    print(strategy_results)

    print("Decisão final:")
    print(final_decision)


if __name__ == "__main__":
    main()