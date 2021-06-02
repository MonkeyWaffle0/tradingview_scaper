from Constants import SHORT, LONG


class Trader:
    def __init__(self):
        self.wallet = 1000.0
        self.previous_wallet = self.wallet
        self.crypto_wallet = 1000.0
        self.previous_crypto_wallet = self.crypto_wallet
        self.bought = 0
        self.sold = 0

        self.fees_rate = 0.001
        self.stop_loss_rate = 0.01
        self.goal_rate = self.stop_loss_rate * 1.5

        self.current_state = None
        self.losses = []
        self.gains = []

        self.stop_loss = 0
        self.goal = 0

    def update_stop_loss(self, price, action):
        if action == LONG:
            self.stop_loss = price * (1 - self.stop_loss_rate)
            self.goal = price * (1 + self.goal_rate)
        elif action == SHORT:
            self.stop_loss = price * (1 + self.stop_loss_rate)
            self.goal = price * (1 - self.goal_rate)

    def enter_long(self, price):
        previous_wallet = self.wallet
        trading_wallet = self.wallet / 2
        self.handle_fees(trading_wallet, LONG)
        self.bought = self.convert_to_crypto(trading_wallet, price)
        self.wallet -= self.bought * price
        self.crypto_wallet += self.bought
        self.log_entered(self.bought, price, 'Bought')
        self.current_state = LONG
        self.update_stop_loss(price, LONG)
        self.previous_wallet = previous_wallet

    def enter_short(self, price):
        previous_crypto_wallet = self.crypto_wallet
        trading_wallet = self.crypto_wallet / 2
        self.handle_fees(trading_wallet, SHORT)
        self.sold = self.convert_to_money(trading_wallet, price)
        self.crypto_wallet -= self.sold / price
        self.wallet += self.sold
        self.log_entered(self.sold, price, 'Sold')
        self.current_state = SHORT
        self.update_stop_loss(price, SHORT)
        self.previous_crypto_wallet = previous_crypto_wallet

    def buy_back(self, price):
        previous_wallet = self.wallet
        self.handle_fees(self.sold, LONG)
        buying_amount = self.convert_to_crypto(self.sold, price)
        self.wallet -= buying_amount * price
        self.crypto_wallet += buying_amount
        diff = self.crypto_wallet / self.previous_crypto_wallet
        self.log_diff(buying_amount * price, price, diff, 'Bought')
        self.current_state = None
        self.sold = 0
        self.previous_wallet = previous_wallet

    def sell_back(self, price):
        previous_crypto_wallet = self.crypto_wallet
        self.handle_fees(self.bought, SHORT)
        selling_amount = self.convert_to_money(self.bought, price)
        self.wallet += selling_amount
        self.crypto_wallet -= selling_amount / price
        diff = self.wallet / self.previous_wallet
        self.log_diff(selling_amount / price, price, diff, 'Sold')
        self.current_state = None
        self.bought = 0
        self.previous_crypto_wallet = previous_crypto_wallet

    def check_trade(self, price):
        if self.current_state == LONG and (price >= self.goal or price <= self.stop_loss):
            self.sell_back(price)
        elif self.current_state == SHORT and (price <= self.goal or price >= self.stop_loss):
            self.buy_back(price)

    def log_entered(self, amount, price, action):
        if action == "Bought":
            print(
                f"\nEntered long position by buying {'{:.2f}'.format(amount)} BTC at {price}.\nCurrent wallet : {'{:.2f}'.format(self.wallet)}\nCurrent BTC wallet: {'{:.2f}'.format(self.crypto_wallet)}\n")
        elif action == "Sold":
            print(
                f"\nEntered short position by selling {'{:.2f}'.format(amount)} BTC at {price}.\nCurrent wallet : {'{:.2f}'.format(self.wallet)}\nCurrent BTC wallet: {'{:.2f}'.format(self.crypto_wallet)}\n")

    def log_diff(self, amount, price, diff, action):
        print(
            f"\n{action} back {'{:.2f}'.format(amount)} BTC at {price}.\nCurrent wallet : {'{:.2f}'.format(self.wallet)}\nCurrent BTC wallet: {'{:.2f}'.format(self.crypto_wallet)}\n")
        if diff > 1.0:
            self.gains.append((diff - 1) * 100)
            print(f"Gained {(diff - 1) * 100}%")
        elif diff < 1.0:
            self.losses.append((1 - diff) * 100)
            print(f"Lost {(1 - diff) * 100}%")
        else:
            print("No loss / gain.")
        print("\n\n")

    def convert_to_crypto(self, money, price):
        return money / price

    def convert_to_money(self, crypto, price):
        return crypto * price

    def handle_fees(self, amount, action):
        fees = amount * self.fees_rate
        if action == LONG:
            self.wallet -= fees
        elif action == SHORT:
            self.crypto_wallet -= fees

    def calculate_total_gain(self):
        return sum(self.gains) - sum(self.losses)
