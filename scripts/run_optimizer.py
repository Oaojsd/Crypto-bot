from data.market_data import MarketData
from optimization.optimizer import Optimizer


def print_result(index, result):
    print("")
    print(f"#{index}")
    print(f"Score: {result['score']:.4f}")
    print(f"MA window: {result['ma_window']}")
    print(f"RSI period: {result['rsi_period']}")
    print(f"Trend: {result['trend_short']} x {result['trend_long']}")
    print(f"Valor final: {result['final_value']:.2f}")
    print(f"Lucro/prejuízo: {result['total_profit']:.2f}")
    print(f"Resultado percentual: {result['total_profit_percent']:.2f}%")
    print(f"Drawdown máximo: {result['max_drawdown']:.2f}%")
    print(f"Total de operações: {result['total_trades']}")
    print(f"Taxa de acerto: {result['win_rate']:.2f}%")
    print(f"Lucro médio: {result['average_win']:.4f}")
    print(f"Prejuízo médio: {result['average_loss']:.4f}")
    print(f"Profit factor: {result['profit_factor']:.2f}")
    print(f"Aprovado: {result['approved']}")
    print(f"Regimes: {result.get('regime_counts', {})}")


def run():
    market_data = MarketData()
    optimizer = Optimizer()

    timeframe = "1h"

    candles = market_data.fetch_ohlcv(
        limit=500,
        timeframe=timeframe
    )

    optimization_result = optimizer.run(candles)

    approved = optimization_result["approved"]
    rejected = optimization_result["rejected"]
    total_tested = optimization_result["total_tested"]

    print("===== OTIMIZAÇÃO =====")
    print(f"Timeframe: {timeframe}")
    print(f"Total testado: {total_tested}")
    print(f"Configurações aprovadas: {len(approved)}")
    print(f"Configurações rejeitadas: {len(rejected)}")

    if len(approved) > 0:
        print("")
        print("===== TOP 5 CONFIGURAÇÕES APROVADAS =====")

        for index, result in enumerate(approved[:5], start=1):
            print_result(index, result)

    else:
        print("")
        print("Nenhuma configuração aprovada.")
        print("Melhor configuração rejeitada:")

        if len(rejected) > 0:
            print_result(1, rejected[0])


if __name__ == "__main__":
    run()