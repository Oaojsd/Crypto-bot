class BacktestReport:
    def calculate_max_drawdown(self, equity_curve):
        if len(equity_curve) == 0:
            return 0.0

        peak = equity_curve[0]["equity"]
        max_drawdown = 0.0

        for point in equity_curve:
            equity = point["equity"]

            if equity > peak:
                peak = equity

            drawdown = ((equity - peak) / peak) * 100

            if drawdown < max_drawdown:
                max_drawdown = drawdown

        return max_drawdown

    def generate(self, result):
        trades = result["trades"]

        buy_trades = []
        sell_trades = []

        for trade in trades:
            if trade["action"] == "BUY":
                buy_trades.append(trade)

            elif trade["action"] == "SELL":
                sell_trades.append(trade)

        winning_trades = []
        losing_trades = []

        for trade in sell_trades:
            profit = trade.get("profit", 0)

            if profit > 0:
                winning_trades.append(trade)

            elif profit < 0:
                losing_trades.append(trade)

        total_profit = result["final_value"] - result["initial_balance"]
        total_profit_percent = (total_profit / result["initial_balance"]) * 100

        total_wins = len(winning_trades)
        total_losses = len(losing_trades)
        total_closed_trades = len(sell_trades)

        if total_closed_trades > 0:
            win_rate = (total_wins / total_closed_trades) * 100
        else:
            win_rate = 0.0

        total_profit_from_winners = 0.0

        for trade in winning_trades:
            total_profit_from_winners += trade.get("profit", 0)

        total_loss_from_losers = 0.0

        for trade in losing_trades:
            total_loss_from_losers += trade.get("profit", 0)

        if total_wins > 0:
            average_win = total_profit_from_winners / total_wins
        else:
            average_win = 0.0

        if total_losses > 0:
            average_loss = total_loss_from_losers / total_losses
        else:
            average_loss = 0.0

        if total_loss_from_losers < 0:
            profit_factor = total_profit_from_winners / abs(total_loss_from_losers)
        else:
            profit_factor = 0.0

        max_drawdown = self.calculate_max_drawdown(result["equity_curve"])

        return {
            "initial_balance": result["initial_balance"],
            "final_value": result["final_value"],
            "total_profit": total_profit,
            "total_profit_percent": total_profit_percent,
            "cash_balance": result["cash_balance"],
            "asset_balance": result["asset_balance"],
            "total_trades": len(trades),
            "buy_trades": len(buy_trades),
            "sell_trades": len(sell_trades),
            "winning_trades": total_wins,
            "losing_trades": total_losses,
            "win_rate": win_rate,
            "average_win": average_win,
            "average_loss": average_loss,
            "profit_factor": profit_factor,
            "max_drawdown": max_drawdown,
            "regime_counts": result.get("regime_counts", {})
        }