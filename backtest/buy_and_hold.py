from config.settings import settings


class BuyAndHold:
    def run(self, candles):
        first_price = candles[0]["close"]
        last_price = candles[-1]["close"]

        fee = settings.INITIAL_BALANCE * settings.TRADING_FEE
        net_amount_to_invest = settings.INITIAL_BALANCE - fee

        asset_amount = net_amount_to_invest / first_price

        final_gross_value = asset_amount * last_price
        final_fee = final_gross_value * settings.TRADING_FEE
        final_value = final_gross_value - final_fee

        total_profit = final_value - settings.INITIAL_BALANCE
        total_profit_percent = (
            total_profit / settings.INITIAL_BALANCE
        ) * 100

        return {
            "initial_balance": settings.INITIAL_BALANCE,
            "first_price": first_price,
            "last_price": last_price,
            "final_value": final_value,
            "total_profit": total_profit,
            "total_profit_percent": total_profit_percent
        }