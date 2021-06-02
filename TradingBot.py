import csv

from Constants import BUY, SELL, LONG, SHORT
from DataAnalyzer import DataAnalyzer
from Trader import Trader


class TradingBot:
    def __init__(self, data):
        self.data = data
        self.data_analyzer = DataAnalyzer()
        self.trader = Trader()

    def analyze_data(self):
        for data in self.data:
            current_price = float(data['price'])
            self.data_analyzer.update_indicators(data)
            signal = self.data_analyzer.get_signal()
            if signal == BUY and not self.trader.current_state:
                self.trader.enter_short(current_price)
            elif signal == SELL and not self.trader.current_state:
                self.trader.enter_long(current_price)
            elif self.trader.current_state == LONG or self.trader.current_state == SHORT:
                self.trader.check_trade(current_price)
        print(f"\n{len(self.trader.gains)} gain, {len(self.trader.losses)} loss.\n")
        print(f"Total gain : {'{:.2f}'.format(self.trader.calculate_total_gain())}%")


if __name__ == "__main__":
    with open('data_training/data_training_0530_supertrend.csv') as file:
        readCSV = csv.reader(file, delimiter=',')
        data = []
        for line in csv.DictReader(file):
            data.append(line)
    bot = TradingBot(data)
    bot.analyze_data()
