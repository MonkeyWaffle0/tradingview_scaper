import csv
from time import sleep


def compare(price_list, sar_list):
    sar_bullish_signal = False
    sar_bearish_signal = False
    bullish_klinger = False
    bearish_klinger = False

    if (sar_list[0] > price_list[0]) and (sar_list[1] > price_list[1]) and (sar_list[2] > price_list[2]):
        sar_bearish_signal = True

    elif (sar_list[0] < price_list[0]) and (sar_list[1] < price_list[1]) and (sar_list[2] < price_list[2]):
        sar_bullish_signal = True

    if klinger1 > klinger2:
        bullish_klinger = True
    elif klinger1 < klinger2:
        bearish_klinger = True

    return sar_bullish_signal, sar_bearish_signal, bullish_klinger, bearish_klinger


def buy(price):
    global wallet
    fee = wallet * 0.001
    wallet -= fee
    amount = wallet / price
    wallet = 0

    print("You bought {0} ETH for {1}".format(amount, price, wallet))
    return amount


def sell(price, amount):
    global wallet
    if wallet != 0:
        return None

    fee = amount * price * 0.001
    wallet += amount * price
    wallet -= fee

    print("You sold {0}ETH for {1}, You have {2}BTC".format(amount, price, wallet))


with open("csv.csv", "r") as read_file:
    reader = csv.reader(read_file)
    lines = list(reader)

long = False
short = False
bought = 0
index = 4
wallet = 1
stop_loss = 0
stop_loss_rate = 0.05

while True:
    sleep(0.005)

    try:
        price_list = [
            float(lines[index - 2][0]),
            float(lines[index - 1][0]),
            float(lines[index][0])
        ]

        sar_list = [
            float(lines[index - 2][1]),
            float(lines[index - 1][1]),
            float(lines[index][1])
        ]
    except IndexError:
        break

    price = float(lines[index][0])
    klinger1 = float(lines[index][2])
    klinger2 = float(lines[index][3])

    bullish_sar, bearish_sar, bullish_klinger, bearish_klinger = compare(price_list, sar_list)

    if bullish_sar and bullish_klinger:
        if not long:
            bought = buy(price)
            long = True
            short = False
            stop_loss = price * (1 - stop_loss_rate)

    elif bearish_sar and bearish_klinger:
        if not short:
            sell(price, bought)
            short = True
            long = False
            stop_loss = price * (1 + stop_loss_rate)

    if stop_loss != 0:
        if long and price <= stop_loss:
            print("stop loss")
            sell(price, bought)
            short = True
            long = False
            stop_loss = price * (1 + stop_loss_rate)

        elif short and price >= stop_loss:
            print("stop loss")
            bought = buy(price)
            long = True
            short = False
            stop_loss = price * (1 - stop_loss_rate)

    index += 1

print("\n")
gain = (1 - wallet) * 100
gain = round(gain, 2)
if wallet > 1:
    print("You made a {}% profit.".format(gain))
else:
    print("You made a {}% loss.".format(gain))