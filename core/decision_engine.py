class DecisionEngine:
    def decide(self, strategy_results):
        buy_score = 0
        sell_score = 0

        for result in strategy_results:
            signal = result["signal"]
            strength = result["strength"]

            if signal == "BUY":
                buy_score += strength

            if signal == "SELL":
                sell_score += strength

        if buy_score > sell_score:
            return {
                "decision": "BUY",
                "confidence": buy_score
            }

        if sell_score > buy_score:
            return {
                "decision": "SELL",
                "confidence": sell_score
            }

        return {
            "decision": "HOLD",
            "confidence": 0.0
        }