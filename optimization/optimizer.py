from backtest.backtester import Backtester
from backtest.report import BacktestReport
from core.decision_engine import DecisionEngine
from strategies.market_regime_filter import MarketRegimeFilter
from strategies.moving_average_strategy import MovingAverageStrategy
from strategies.rsi_strategy import RsiStrategy
from strategies.trend_strategy import TrendStrategy
from strategies.trend_strength_filter import TrendStrengthFilter
from strategies.volatility_filter import VolatilityFilter


class Optimizer:
    def __init__(self):
        self.report_generator = BacktestReport()

    def calculate_score(self, report):
        profit_score = report["total_profit_percent"]
        drawdown_penalty = abs(report["max_drawdown"])
        win_rate_score = report["win_rate"] / 100
        profit_factor_score = report["profit_factor"]

        total_trades = report["total_trades"]

        if total_trades < 6:
            trade_penalty = 1.0
        else:
            trade_penalty = 0.0

        score = (
            profit_score
            + win_rate_score
            + profit_factor_score
            - drawdown_penalty
            - trade_penalty
        )

        return score

    def is_approved(self, report):
        if report["total_profit"] <= 0:
            return False

        if report["profit_factor"] < 1.10:
            return False

        if report["total_trades"] < 6:
            return False

        if report["max_drawdown"] < -1.0:
            return False

        return True

    def build_strategies(self, config):
        return [
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
                short_window=config["trend_short"],
                long_window=config["trend_long"],
                min_difference_percent=0.20
            ),
            MovingAverageStrategy(window=config["ma_window"]),
            RsiStrategy(period=config["rsi_period"]),
            TrendStrategy(
                short_window=config["trend_short"],
                long_window=config["trend_long"]
            )
        ]

    def test_config(self, candles, config):
        strategies = self.build_strategies(config)
        decision_engine = DecisionEngine()

        backtester = Backtester(
            strategies=strategies,
            decision_engine=decision_engine
        )

        result = backtester.run(candles)
        report = self.report_generator.generate(result)
        score = self.calculate_score(report)

        return {
            "ma_window": config["ma_window"],
            "rsi_period": config["rsi_period"],
            "trend_short": config["trend_short"],
            "trend_long": config["trend_long"],
            "score": score,
            "final_value": report["final_value"],
            "total_profit": report["total_profit"],
            "total_profit_percent": report["total_profit_percent"],
            "max_drawdown": report["max_drawdown"],
            "total_trades": report["total_trades"],
            "win_rate": report["win_rate"],
            "average_win": report["average_win"],
            "average_loss": report["average_loss"],
            "profit_factor": report["profit_factor"],
            "regime_counts": report["regime_counts"],
            "approved": self.is_approved(report)
        }

    def run(self, candles):
        approved_results = []
        rejected_results = []

        moving_average_windows = [10, 20, 30, 40]
        rsi_periods = [10, 14, 21]
        trend_configs = [
            {"short_window": 5, "long_window": 20},
            {"short_window": 7, "long_window": 21},
            {"short_window": 9, "long_window": 21},
            {"short_window": 12, "long_window": 26},
            {"short_window": 20, "long_window": 50}
        ]

        for ma_window in moving_average_windows:
            for rsi_period in rsi_periods:
                for trend_config in trend_configs:
                    config = {
                        "ma_window": ma_window,
                        "rsi_period": rsi_period,
                        "trend_short": trend_config["short_window"],
                        "trend_long": trend_config["long_window"]
                    }

                    item = self.test_config(candles, config)

                    if item["approved"]:
                        approved_results.append(item)
                    else:
                        rejected_results.append(item)

        approved_results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        rejected_results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return {
            "approved": approved_results,
            "rejected": rejected_results,
            "total_tested": len(approved_results) + len(rejected_results)
        }