from backtest.buy_and_hold import BuyAndHold
from data.market_data import MarketData
from optimization.walk_forward import WalkForwardValidator


def print_result(title, result):
    print("")
    print(title)
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


def print_buy_and_hold(result):
    print("")
    print("===== BUY AND HOLD =====")
    print(f"Preço inicial: {result['first_price']:.2f}")
    print(f"Preço final: {result['last_price']:.2f}")
    print(f"Valor final: {result['final_value']:.2f}")
    print(f"Lucro/prejuízo: {result['total_profit']:.2f}")
    print(f"Resultado percentual: {result['total_profit_percent']:.2f}%")


def run():
    market_data = MarketData()
    validator = WalkForwardValidator()
    buy_and_hold = BuyAndHold()

    timeframes = [
        "15m",
        "1h",
        "4h"
    ]

    for timeframe in timeframes:
        print("")
        print("=" * 50)
        print(f"TIMEFRAME: {timeframe}")
        print("=" * 50)

        candles = market_data.fetch_ohlcv(
            limit=500,
            timeframe=timeframe
        )

        hold_result = buy_and_hold.run(candles)
        print_buy_and_hold(hold_result)

        result = validator.run(candles)

        if result["status"] == "NO_APPROVED_CONFIG":
            print("")
            print("Nenhuma configuração aprovada no período de treino.")
            continue

        best_config = result["best_config"]
        validation_result = result["validation_result"]

        print_result("===== MELHOR CONFIGURAÇÃO NO TREINO =====", best_config)
        print_result("===== RESULTADO NA VALIDAÇÃO =====", validation_result)

        bot_vs_hold = (
            validation_result["total_profit_percent"]
            - hold_result["total_profit_percent"]
        )

        print("")
        print("===== COMPARAÇÃO BOT VS BUY AND HOLD =====")
        print(f"Diferença percentual: {bot_vs_hold:.2f}%")

        if bot_vs_hold > 0:
            print("Resultado: o bot superou o buy and hold nesse período.")
        else:
            print("Resultado: o bot NÃO superou o buy and hold nesse período.")

        if validation_result["approved"]:
            print("Validação: configuração aprovada fora da amostra.")
        else:
            print("Validação: configuração reprovada fora da amostra.")


if __name__ == "__main__":
    run()