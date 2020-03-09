import matplotlib.pyplot as plt
import csv

import pandas as pd
import numpy as np


class MacdTrader():
    def __init__(self, data):
        self.currency = "BTC"  # Currency we are trading
        self.wallet = 100.0  # 100.0 Current money
        self.starting_wallet = self.wallet  # Money the trader started with
        self.previous_wallet = 0  # Money before buying
        self.fee_rate = 0.001  # Rate of the transaction fees
        self.bought = 0.0  # Amount bought
        self.data = data  # Trading data
        self.transaction_rate = 0.5
        self.wants_to = "BUY"  # Action the trader is looking to do
        # Signals used to decide wether buy or sell
        self.signals = {
            "macd": None,
            "rsi": None,
            "sar": None
        }
        self.prices = []  # List of all the prices to display with matplotlib
        # List of all buy/sell points to display with matplotlib
        self.buy_list = [1.7 for x in range(len(data))]
        self.sell_list = [1.7 for x in range(len(data))]

    def update_signals(self, values):
        """Changes signals to bull or bear depending of their value."""
        for key, value in values.items():
            value = float(value)
            if key == "sar" or key == "macd":
                if value > 0:
                    self.signals[key] = "bull"
                else:
                    self.signals[key] = "bear"
            elif key == "rsi":
                if value <= 30:
                    self.signals[key] = "bull"
                elif value >= 70:
                    self.signals[key] = "bear"
                else:
                    self.signals[key] = None

    def read_signal(self, index, price):
        """Returns a buy action if there is a majority of bullish signals, or a sell action if there is a majority of bearish signals."""
        bullish = 0
        bearish = 0
        for signal in self.signals.values():
            if signal == "bull":
                bullish += 1
            elif signal == "bear":
                bearish += 1
        if bullish > bearish:
            return self.buy(index, price)
        elif bearish > bullish:
            return self.sell(index, price)

    def buy(self, index, price):
        "Returns nothing if we are looking to sell, else buys the maximum amount minus the transaction fee."
        if self.wants_to == "SELL":
            return None
        price = float(price)
        self.wants_to = "SELL"
        self.previous_wallet = self.wallet
        fee = self.wallet * self.fee_rate
        self.wallet -= fee
        self.bought = self.wallet / price
        self.bought = round(self.bought, 2)
        self.wallet = 0
        self.buy_list[index] = price * 100
        print(f"Bought {self.bought}{self.currency} for {price}.")

    def sell(self, index, price):
        "Returns nothing if we are looking to buy, else sells the maximum amount minus the transaction fee."
        if self.wants_to == "BUY":
            return None
        self.wants_to = "BUY"
        price = float(price)
        fee = self.bought * price * self.fee_rate
        self.wallet += self.bought * price
        self.wallet -= fee
        self.sell_list[index] = price * 100
        print(f"Sold {self.wallet}{self.currency} for {price}.")

    def add_price(self, price):
        """Appends the price to the price list. (* 100 for readability with matplotlib)"""
        self.prices.append(price * 100)

    def get_results(self):
        """Returns a percentage of gain/loss."""
        if self.wants_to == "SELL":
            self.wallet = self.previous_wallet
        gain = self.wallet - self.starting_wallet
        gain = round(gain, 2)
        if gain > 0:
            print(f"You made a {gain}% gain.")
        elif gain < 0:
            print(f"You made a {gain}% loss.")
        else:
            print("You didn't trade or made any profit.")
        return gain

    def show_results(self):
        """Shows a graph with the prices and buy and sell points."""
        data = pd.read_csv("data_training_0903-macd.csv")
        data = data[["price", "sar", "rsi", "macd"]]
        X = np.array(data)
        prices = []
        for i in range(len(X)):
            prices.append(X[i][0] * 100)
        plt.plot(prices)
        plt.plot(self.buy_list, "gs")
        plt.plot(self.sell_list, "ro")
        plt.show()

    def trade(self):
        i_price = 0
        i_sar = 1
        i_rsi = 2
        i_macd = 3

        for i, line in enumerate(self.data):
            if i == len(self.data) - 2:
                break
            self.add_price(line[i_price])
            values = {
                "sar": line[i_sar],
                "rsi": line[i_rsi],
                "macd": line[i_macd]
            }
            self.update_signals(values)
            self.read_signal(i, line[i_price])
        print("")
        self.get_results()
        self.show_results()


with open("data_training_0903-macd.csv", "r") as read_file:
    read = csv.reader(read_file)
    next(read)
    data = [item for item in read]
trader = MacdTrader(data)
trader.trade()