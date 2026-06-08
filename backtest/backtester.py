from config.settings import settings
from risk.portfolio import Portfolio


class Backtester:
    def __init__(
        self,
        strategies,
        decision_engine,
        minimum_hold_candles=3,
        avoid_last_candles=30
    ):
        self.strategies = strategies
        self.decision_engine = decision_engine
        self.portfolio = Portfolio()
        self.trades = []
        self.equity_curve = []
        self.regime_counts = {
            "BULL": 0,
            "BEAR": 0,
            "SIDEWAYS": 0,
            "UNKNOWN": 0
        }
        self.minimum_hold_candles = minimum_hold_candles
        self.avoid_last_candles = avoid_last_candles
        self.entry_index = None

    def should_stop_loss(self, current_price):
        if not self.portfolio.has_position():
            return False

        price_change_percent = (
            (current_price - self.portfolio.entry_price)
            / self.portfolio.entry_price
        ) * 100

        return price_change_percent <= -settings.STOP_LOSS_PERCENT

    def should_take_profit(self, current_price):
        if not self.portfolio.has_position():
            return False

        price_change_percent = (
            (current_price - self.portfolio.entry_price)
            / self.portfolio.entry_price
        ) * 100

        return price_change_percent >= settings.TAKE_PROFIT_PERCENT

    def calculate_equity(self, current_price):
        return (
            self.portfolio.cash_balance
            + self.portfolio.asset_balance * current_price
        )

    def update_regime_count(self, final_decision):
        market_regime = final_decision.get("market_regime", "UNKNOWN")

        if market_regime not in self.regime_counts:
            market_regime = "UNKNOWN"

        self.regime_counts[market_regime] += 1

    def run(self, candles):
        last_buy_index = len(candles) - self.avoid_last_candles

        for index in range(30, len(candles)):
            historical_candles = candles[:index + 1]
            current_price = historical_candles[-1]["close"]

            trade = None
            final_decision = None

            if self.should_stop_loss(current_price):
                trade = self.portfolio.sell(current_price)

                if trade is not None:
                    trade["exit_reason"] = "STOP_LOSS"
                    self.entry_index = None

            elif self.should_take_profit(current_price):
                trade = self.portfolio.sell(current_price)

                if trade is not None:
                    trade["exit_reason"] = "TAKE_PROFIT"
                    self.entry_index = None

            else:
                strategy_results = []

                for strategy in self.strategies:
                    result = strategy.generate_signal(historical_candles)
                    strategy_results.append(result)

                final_decision = self.decision_engine.decide(strategy_results)
                self.update_regime_count(final_decision)

                if final_decision["decision"] == "BUY":
                    if not self.portfolio.has_position() and index < last_buy_index:
                        trade = self.portfolio.buy(current_price)
                        self.entry_index = index

                        if trade is not None:
                            trade["exit_reason"] = None
                            trade["decision"] = final_decision

                elif final_decision["decision"] == "SELL":
                    if self.portfolio.has_position():
                        candles_held = index - self.entry_index

                        if candles_held >= self.minimum_hold_candles:
                            trade = self.portfolio.sell(current_price)
                            self.entry_index = None

                            if trade is not None:
                                trade["exit_reason"] = "SIGNAL"
                                trade["decision"] = final_decision

            if trade is not None:
                trade["index"] = index

                if "decision" not in trade:
                    trade["decision"] = {
                        "decision": "SELL",
                        "confidence": None,
                        "buy_score": None,
                        "sell_score": None,
                        "strategies": len(self.strategies),
                        "market_regime": "UNKNOWN",
                        "blocked_by": []
                    }

                self.trades.append(trade)

            equity = self.calculate_equity(current_price)

            self.equity_curve.append({
                "index": index,
                "equity": equity,
                "price": current_price
            })

        last_price = candles[-1]["close"]
        final_value = self.calculate_equity(last_price)

        return {
            "initial_balance": self.portfolio.initial_balance,
            "final_value": final_value,
            "cash_balance": self.portfolio.cash_balance,
            "asset_balance": self.portfolio.asset_balance,
            "trades": self.trades,
            "equity_curve": self.equity_curve,
            "regime_counts": self.regime_counts
        }