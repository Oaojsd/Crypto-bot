from backtest.backtester import Backtester
from backtest.buy_and_hold import BuyAndHold
from backtest.report import BacktestReport
from core.decision_engine import DecisionEngine
from data.market_data import MarketData
from strategies.market_regime_filter import MarketRegimeFilter
from strategies.moving_average_strategy import MovingAverageStrategy
from strategies.price_confirmation_filter import PriceConfirmationFilter
from strategies.rsi_strategy import RsiStrategy
from strategies.trend_strategy import TrendStrategy
from strategies.trend_strength_filter import TrendStrengthFilter
from strategies.volatility_filter import VolatilityFilter


def print_report(report):
    print("===== RELATÓRIO DO BACKTEST =====")
    print(f"Saldo inicial: {report['initial_balance']:.2f}")
    print(f"Valor final: {report['final_value']:.2f}")
    print(f"Lucro/prejuízo: {report['total_profit']:.2f}")
    print(f"Resultado percentual: {report['total_profit_percent']:.2f}%")
    print(f"Drawdown máximo: {report['max_drawdown']:.2f}%")
    print(f"Saldo em caixa: {report['cash_balance']:.2f}")
    print(f"Quantidade de ativo: {report['asset_balance']}")
    print(f"Regimes: {report['regime_counts']}")

    print("")
    print("===== OPERAÇÕES =====")
    print(f"Total de operações: {report['total_trades']}")
    print(f"Compras: {report['buy_trades']}")
    print(f"Vendas: {report['sell_trades']}")
    print(f"Trades vencedores: {report['winning_trades']}")
    print(f"Trades perdedores: {report['losing_trades']}")
    print(f"Taxa de acerto: {report['win_rate']:.2f}%")
    print(f"Lucro médio: {report['average_win']:.4f}")
    print(f"Prejuízo médio: {report['average_loss']:.4f}")
    print(f"Profit factor: {report['profit_factor']:.2f}")


def print_buy_and_hold(result):
    print("")
    print("===== BUY AND HOLD =====")
    print(f"Preço inicial: {result['first_price']:.2f}")
    print(f"Preço final: {result['last_price']:.2f}")
    print(f"Valor final: {result['final_value']:.2f}")
    print(f"Lucro/prejuízo: {result['total_profit']:.2f}")
    print(f"Resultado percentual: {result['total_profit_percent']:.2f}%")


def run():
    timeframe = "1h"
    limit = 500

    market_data = MarketData()

    candles = market_data.fetch_ohlcv(
        limit=limit,
        timeframe=timeframe
    )

    strategies = [
        MarketRegimeFilter(
            short_window=20,
            long_window=80,
            min_trend_percent=0.50
        ),
        VolatilityFilter(
            period=14,
            min_volatility_percent=0.25,
            max_volatility_percent=4.0
        ),
        TrendStrengthFilter(
            short_window=12,
            long_window=26,
            min_difference_percent=0.20
        ),
        PriceConfirmationFilter(long_window=26),
        MovingAverageStrategy(window=20),
        RsiStrategy(period=14),
        TrendStrategy(short_window=12, long_window=26)
    ]

    decision_engine = DecisionEngine()

    backtester = Backtester(
        strategies=strategies,
        decision_engine=decision_engine
    )

    result = backtester.run(candles)

    report_generator = BacktestReport()
    report = report_generator.generate(result)

    print("")
    print("===== BACKTEST ÚNICO =====")
    print(f"Timeframe: {timeframe}")
    print(f"Candles: {limit}")
    print("Configuração:")
    print("MA: 20")
    print("RSI: 14")
    print("Trend: 12 x 26")
    print("Regime: 20 x 80")
    print("Price confirmation: close > MA 26")
    print("")

    print_report(report)

    buy_and_hold = BuyAndHold()
    hold_result = buy_and_hold.run(candles)
    print_buy_and_hold(hold_result)

    bot_vs_hold = (
        report["total_profit_percent"]
        - hold_result["total_profit_percent"]
    )

    print("")
    print("===== COMPARAÇÃO BOT VS BUY AND HOLD =====")
    print(f"Diferença percentual: {bot_vs_hold:.2f}%")

    if bot_vs_hold > 0:
        print("Resultado: o bot superou o buy and hold nesse período.")
    else:
        print("Resultado: o bot NÃO superou o buy and hold nesse período.")

    print("")
    print("===== ÚLTIMAS OPERAÇÕES =====")

    for trade in result["trades"][-5:]:
        print(trade)


if __name__ == "__main__":
    run()