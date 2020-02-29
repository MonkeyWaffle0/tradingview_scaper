from selenium import webdriver

import csv
import os
from time import sleep


def create_csv():
    row = ["price", "ema", "volume", "volume_ema", "klinger", "rsi", "signal"]
    if not os.path.exists("csv.csv"):
        with open('csv.csv', 'w', newline="") as write_file:
            writer = csv.writer(write_file)
            writer.writerow(row)


def edit_csv(price, ema, vol, vol_ema, klinger, rsi, signal):
    row = [price, ema, vol, vol_ema, klinger, rsi, signal]
    with open('csv.csv', 'a', newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerow(row)


def get_csv():
    with open("csv.csv", "r") as read_file:
        reader = csv.reader(read_file)
        lines = list(reader)

    price_list = []
    sar_list = []
    lenght = len(lines)
    if lenght > 4:
        price_list = [
            lines[lenght - 3][0],
            lines[lenght - 2][0],
            lines[lenght - 1][0]
                      ]
        sar_list = [
            lines[lenght - 3][1],
            lines[lenght - 2][1],
            lines[lenght - 1][1]
        ]
    return price_list, sar_list


def get_values():
    price = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[3]/div[1]/div/span[4]/span[2]"
    ).text

    sar = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[3]/div[3]/div/span[1]/span"
    ).text

    volume = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[3]/div[2]/div/span[1]/span"
    ).text

    volume_ema = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[3]/div[2]/div/span[2]/span"
    ).text

    klinger1 = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[3]/div[1]/div/span[1]/span"
    ).text
    if "K" in klinger1:
        klinger1 = klinger1[:len(klinger1) - 1]

    klinger2 = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[3]/div[1]/div/span[2]/span"
    ).text
    if "K" in klinger2:
        klinger2 = klinger2[:len(klinger2) - 1]

    rsi = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[5]/td[2]/div/div[3]/div[1]/div/span[1]/span"
    ).text

    return price, sar, volume, volume_ema, klinger1, klinger2, rsi


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
    fee = wallet * 0.1
    wallet -= fee
    amount = wallet / price
    wallet = 0

    print("You bought {0} ETH for {1}".format(amount, price, wallet))
    return amount


def sell(price, amount):
    global wallet
    if wallet != 0:
        return None

    fee = amount * price * 0.1
    wallet += amount * price
    wallet -= fee

    print("You sold {0}ETH for {1}, You have {2}BTC".format(amount, price, wallet))


if __name__ == "__main__":

    create_csv()
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.tradingview.com/#signin")
    except Exception as e:
        print('+ Error Involving Chrome Driver + \n')
        quit()

    wallet = 1

    long = False
    short = False
    bought = 0




    input()
    while True:
        sleep(300)

        price, sar, volume, volume_ema, klinger1, klinger2, rsi = get_values()
        # print("Price:", price, "\n" + "SAR:", sar, "\n" + "Klinger 1:", klinger1, "\n" + "Klinger 2:", klinger2, "\n")

        edit_csv(price, sar, klinger1, klinger2)
        price_list, sar_list = get_csv()

        if len(price_list) == 3:
            bullish_sar, bearish_sar, bullish_klinger, bearish_klinger = compare(price_list, sar_list)

            # print(price_list, "\n", sar_list, "\n", bullish_sar, bearish_sar, "\n", bullish_klinger, bearish_klinger)

            if bullish_sar and bullish_klinger:
                if not long:
                    bought = buy(price)
                    long = True
                    short = False

            elif bearish_sar and bearish_klinger:
                if not short:
                    sell(price, bought)
                    short = True
                    long = False





