
class Strategy:
    # Constant for the overall risk level in percentage
    RISK_LEVEL_PERCENTAGE = 0.0075  # Example risk level: 2%

    def __init__(self, equity_value):
        self.equity_value = equity_value

    def calculate_position_size(self, stock_price):
        # Calculate the maximum amount of equity to risk per trade
        max_equity_risk = (self.equity_value * self.RISK_LEVEL_PERCENTAGE)

        # Calculate the number of stocks to buy based on the maximum equity risk
        position_size = max_equity_risk / stock_price

        return position_size