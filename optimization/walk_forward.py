from optimization.optimizer import Optimizer


class WalkForwardValidator:
    def __init__(self):
        self.optimizer = Optimizer()

    def split_candles(self, candles):
        middle_index = len(candles) // 2

        training_candles = candles[:middle_index]
        validation_candles = candles[middle_index:]

        return training_candles, validation_candles

    def run(self, candles):
        training_candles, validation_candles = self.split_candles(candles)

        optimization_result = self.optimizer.run(training_candles)

        approved_configs = optimization_result["approved"]

        if len(approved_configs) == 0:
            return {
                "status": "NO_APPROVED_CONFIG",
                "training_result": optimization_result,
                "validation_result": None,
                "best_config": None
            }

        best_config = approved_configs[0]

        validation_result = self.optimizer.test_config(
            validation_candles,
            best_config
        )

        return {
            "status": "OK",
            "training_result": optimization_result,
            "validation_result": validation_result,
            "best_config": best_config
        }