from scripts.Constants import BUY, SELL


class DataAnalyzer:
    def __init__(self):
        self.ind_ema = None
        self.ind_supertrend = None
        self.ind_rsi = None
        self.last_three_rsi = [50, 50, 50]

    def update_indicators(self, data):
        price = float(data['price'])
        ema = float(data['ema'])
        rsi = float(data['rsi'])
        supertrend = data['supertrendBuy']

        self.update_ema(price, ema)
        self.update_rsi(rsi)
        self.update_supertrend(supertrend)

    def update_ema(self, price, ema):
        if price > ema:
            self.ind_ema = BUY
        elif price < ema:
            self.ind_ema = SELL
        else:
            self.ind_ema = None

    def update_rsi(self, rsi):
        del(self.last_three_rsi[0])
        self.last_three_rsi.append(rsi)
        if len([x for x in self.last_three_rsi if x >= 80]) > 0:
            self.ind_rsi = SELL
        elif len([x for x in self.last_three_rsi if x <= 20]) > 0:
            self.ind_rsi = BUY
        else:
            self.ind_rsi = None

    def update_supertrend(self, supertrend):
        if supertrend == "n/a":
            self.ind_supertrend = SELL
        else:
            self.ind_supertrend = BUY

    def get_signal(self):
        if self.ind_rsi == BUY and self.ind_ema == BUY and self.ind_supertrend == BUY:
            return BUY
        elif self.ind_rsi == SELL and self.ind_ema == SELL and self.ind_supertrend == SELL:
            return SELL
