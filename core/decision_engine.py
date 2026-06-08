class DecisionEngine:
    def __init__(
        self,
        minimum_confidence=65.0,
        minimum_score=1.0,
        sideways_minimum_score=1.5,
        bear_sell_minimum_score=0.6
    ):
        self.minimum_confidence = minimum_confidence
        self.minimum_score = minimum_score
        self.sideways_minimum_score = sideways_minimum_score
        self.bear_sell_minimum_score = bear_sell_minimum_score

    def get_filters(self, strategy_results):
        blocking_filters = []
        block_buy_filters = []
        market_regime = "UNKNOWN"

        for result in strategy_results:
            if result["signal"] == "BLOCK":
                blocking_filters.append(result)

            elif result["signal"] == "BLOCK_BUY":
                block_buy_filters.append(result)

            if result["strategy"] == "market_regime_filter":
                market_regime = result.get("regime", "UNKNOWN")

        return blocking_filters, block_buy_filters, market_regime

    def get_required_score(self, market_regime, decision):
        if market_regime == "SIDEWAYS":
            return self.sideways_minimum_score

        if market_regime == "BEAR" and decision == "SELL":
            return self.bear_sell_minimum_score

        return self.minimum_score

    def decide(self, strategy_results):
        blocking_filters, block_buy_filters, market_regime = self.get_filters(
            strategy_results
        )

        if len(blocking_filters) > 0:
            return {
                "decision": "HOLD",
                "confidence": 0.0,
                "buy_score": 0.0,
                "sell_score": 0.0,
                "strategies": len(strategy_results),
                "market_regime": market_regime,
                "blocked_by": blocking_filters
            }

        buy_score = 0.0
        sell_score = 0.0

        for result in strategy_results:
            signal = result["signal"]
            strength = result["strength"]

            if signal == "BUY":
                buy_score += strength

            elif signal == "SELL":
                sell_score += strength

        total_score = buy_score + sell_score

        if total_score == 0:
            return {
                "decision": "HOLD",
                "confidence": 0.0,
                "buy_score": buy_score,
                "sell_score": sell_score,
                "strategies": len(strategy_results),
                "market_regime": market_regime,
                "required_score": self.minimum_score,
                "blocked_by": []
            }

        if buy_score > sell_score:
            confidence = (buy_score / total_score) * 100
            decision = "BUY"
            winning_score = buy_score

        elif sell_score > buy_score:
            confidence = (sell_score / total_score) * 100
            decision = "SELL"
            winning_score = sell_score

        else:
            return {
                "decision": "HOLD",
                "confidence": 50.0,
                "buy_score": buy_score,
                "sell_score": sell_score,
                "strategies": len(strategy_results),
                "market_regime": market_regime,
                "required_score": self.minimum_score,
                "blocked_by": []
            }

        confidence = round(confidence, 2)

        required_score = self.get_required_score(
            market_regime=market_regime,
            decision=decision
        )

        if confidence < self.minimum_confidence:
            decision = "HOLD"

        if winning_score < required_score:
            decision = "HOLD"

        if decision == "BUY" and len(block_buy_filters) > 0:
            decision = "HOLD"

        return {
            "decision": decision,
            "confidence": confidence,
            "buy_score": buy_score,
            "sell_score": sell_score,
            "required_score": required_score,
            "strategies": len(strategy_results),
            "market_regime": market_regime,
            "blocked_by": block_buy_filters
        }