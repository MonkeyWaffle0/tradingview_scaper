import csv
from time import sleep

import matplotlib.pyplot as plt


def compare(price, boillinger_top, boillinger_bottom, rsi):
    bullish_klinger = False
    bearish_klinger = False
    bullish_boillinger = False
    bearish_boillinger = False
    bullish_rsi = False
    bearish_rsi = False

    if klinger > 0:
        bullish_klinger = True
    elif klinger < 0:
        bearish_klinger = True

    if price >= boillinger_top * 1.0015:
        bullish_boillinger = True
    elif price <= boillinger_bottom * 0.9985:
        bearish_boillinger = True

    if rsi >= 65:
        bearish_rsi = True
    elif rsi <= 35:
        bullish_rsi = True

    return bullish_klinger, bearish_klinger, bullish_boillinger, bearish_boillinger, bullish_rsi, bearish_rsi


def buy(price):
    global wallet, stop_loss, buy_list
    fee = wallet * 0.001
    wallet -= fee
    amount = wallet / price
    wallet = 0
    stop_loss = price * (1 - stop_loss_rate)

    buy_list[index] = price * 100


    print("You bought {0} ETH for {1}".format(amount, price, wallet))
    return amount


def sell(price, amount):
    global wallet, stop_loss, sell_list
    if wallet != 0:
        return None

    stop_loss = price * (1 + stop_loss_rate)
    fee = amount * price * 0.001
    wallet += amount * price
    wallet -= fee

    sell_list[index] = price * 100

    print("You sold {0}ETH for {1}, You have {2}BTC".format(amount, price, wallet))


with open("csv.csv", "r") as read_file:
    reader = csv.reader(read_file)
    lines = list(reader)

long = False
short = False
long_boillinger = False
short_boillinger = False

short_stop_loss = False
long_stop_loss = False

bought = 0
index = 4
wallet = 1
stop_loss = 0
stop_loss_rate = 0.005

buy_list = [1.5 for x in range(709)]
sell_list = [1.5 for x in range(709)]

while True:
    sleep(0.005)

    try:
        price = float(lines[index][0])
        boillinger_top = float(lines[index][1])
        boillinger_bottom = float(lines[index][2])
        klinger = float(lines[index][3])
        rsi = float(lines[index][4])
    except IndexError:
        break

    bullish_klinger, bearish_klinger, bullish_boillinger, bearish_boillinger, bullish_rsi, bearish_rsi = compare(price, boillinger_top, boillinger_bottom, rsi)

    # Top boillinger bounce
    if boillinger_top * 0.999 <= price <= boillinger_top * 1.001:
        if not short and not long_boillinger and not short_stop_loss:
                sell(price, bought)
                short = True
                long = False
                long_boillinger = False
                short_boillinger = False
                long_stop_loss = False
                short_stop_loss = False

    # Bottom boillinger bounce
    elif boillinger_bottom * 0.999 <= price <= boillinger_bottom * 1.001:
        if not long and not short_boillinger and not long_stop_loss:
                bought = buy(price)
                long = True
                short = False
                long_boillinger = False
                short_boillinger = False
                long_stop_loss = False
                short_stop_loss = False

    # Top boillinger breakout
    elif bullish_boillinger:
        if bullish_rsi and bullish_klinger:
            if not long_boillinger and not long and not long_stop_loss:
                bought = buy(price)
                long_boillinger = True
                long = False
                short = False
                short_boillinger = False
                long_stop_loss = False
                short_stop_loss = False

    # Bottom boillinger breakout
    elif bearish_boillinger:
        if bearish_rsi and bearish_klinger:
            if not short_boillinger and not short and not short_stop_loss:
                sell(price, bought)
                short_boillinger = True
                long = False
                short = False
                long_boillinger = False
                long_stop_loss = False
                short_stop_loss = False

    if long_boillinger and price <= boillinger_top * 0.998:
        sell(price, bought)
        short = True
        short_boillinger = False
        long = False
        long_boillinger = False
        long_stop_loss = False
        short_stop_loss = False

    if short_boillinger and price >= boillinger_bottom * 1.002:
        bought = buy(price)
        long = True
        short = False
        short_boillinger = False
        long_boillinger = False
        long_stop_loss = False
        short_stop_loss = False

    if stop_loss != 0:
        if long or long_boillinger:
            if price <= stop_loss:
                print("stop loss")
                sell(price, bought)
                short = False
                long = False
                short_boillinger = False
                long_boillinger = False
                long_stop_loss = False
                short_stop_loss = True

        elif short or short_boillinger:
            if price >= stop_loss:
                print("stop loss")
                bought = buy(price)
                long = False
                short = False
                short_boillinger = False
                long_boillinger = False
                long_stop_loss = True
                short_stop_loss = False

    if long_stop_loss:
        if bearish_klinger and bearish_rsi:
            if price <= boillinger_top * 0.999:
                sell(price, bought)
                short = True
                long = False
                short_boillinger = False
                long_boillinger = False
                long_stop_loss = False
                short_stop_loss = False

    if short_stop_loss:
        if bullish_klinger and bullish_rsi:
            if price >= boillinger_bottom * 1.001:
                bought = buy(price)
                long = True
                short = False
                short_boillinger = False
                long_boillinger = False
                long_stop_loss = False
                short_stop_loss = False

    index += 1


print("\n")
gain = (1 - wallet) * 100
gain = round(gain, 2)
if wallet > 1:
    print("You made a {}% profit.".format(gain))
else:
    print("You made a {}% loss.".format(gain))


prices = []
tops = []
bottoms = []
for line in lines:
    if "price" not in line[0]:
        price = float(line[0]) * 100
        prices.append(price)
        top = float(line[1]) * 100
        tops.append(top)
        bottom = float(line[2]) * 100
        bottoms.append(bottom)


plt.plot(prices)
plt.plot(tops)
plt.plot(bottoms)
plt.plot(buy_list, "gs")
plt.plot(sell_list, "ro")
plt.show()