from config.settings import settings


class Portfolio:
    def __init__(self):
        self.initial_balance = settings.INITIAL_BALANCE
        self.cash_balance = settings.INITIAL_BALANCE
        self.asset_balance = 0.0
        self.entry_price = 0.0

    def has_position(self):
        return self.asset_balance > 0

    def buy(self, price):
        amount_to_invest = self.cash_balance * settings.RISK_PER_TRADE
        fee = amount_to_invest * settings.TRADING_FEE
        net_amount_to_invest = amount_to_invest - fee

        if net_amount_to_invest <= 0:
            return None

        asset_amount = net_amount_to_invest / price

        self.cash_balance -= amount_to_invest
        self.asset_balance += asset_amount
        self.entry_price = price

        return {
            "action": "BUY",
            "price": price,
            "amount": asset_amount,
            "fee": fee,
            "cash_balance": self.cash_balance,
            "asset_balance": self.asset_balance
        }

    def sell(self, price):
        if not self.has_position():
            return None

        gross_sale_value = self.asset_balance * price
        fee = gross_sale_value * settings.TRADING_FEE
        net_sale_value = gross_sale_value - fee

        invested_value = self.asset_balance * self.entry_price
        profit = net_sale_value - invested_value

        trade = {
            "action": "SELL",
            "price": price,
            "amount": self.asset_balance,
            "fee": fee,
            "profit": profit,
            "cash_balance": self.cash_balance + net_sale_value,
            "asset_balance": 0.0
        }

        self.cash_balance += net_sale_value
        self.asset_balance = 0.0
        self.entry_price = 0.0

        return trade