class BaseStrategy:
    def generate_signal(self, candles):
        raise NotImplementedError(
            "Toda estratégia deve implementar generate_signal()"
        )