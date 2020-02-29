from selenium import webdriver
from pynput.mouse import Controller


import csv
import os
from time import sleep


def create_csv():
    row = ["price", "boillinger_top", "boillinger_bottom", "klinger", "rsi"]
    if not os.path.exists("csv.csv"):
        with open('csv.csv', 'w', newline="") as write_file:
            writer = csv.writer(write_file)
            writer.writerow(row)


def edit_csv(price, boillinger_top, boillinger_bottom, klinger, rsi):
    row = [price, boillinger_top, boillinger_bottom, klinger, rsi]
    with open('csv.csv', 'a', newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerow(row)


def get_values():
    price = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[3]/div[1]/div/span[4]/span[2]"
    ).text

    boillinger_top = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[3]/div[2]/div/span[8]/span"
    ).text

    boillinger_bottom = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[3]/div[2]/div/span[9]/span"
    ).text

    klinger1 = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[3]/div[1]/div/span[1]/span"
    ).text
    try:
        if "K" in klinger1:
            klinger1 = klinger1[:len(klinger1) - 1]
            klinger1 = float(klinger1) * 1000
    except:
        pass

    klinger2 = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[3]/div[1]/div/span[2]/span"
    ).text
    try:
        if "K" in klinger2:
            klinger2 = klinger2[:len(klinger2) - 1]
            klinger2 = float(klinger2) * 1000


        klinger = float(klinger1) - float(klinger2)
    except:
        klinger = 0

    rsi = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[5]/td[2]/div/div[3]/div[1]/div/span[1]/span"
    ).text

    return price, boillinger_top, boillinger_bottom, klinger, rsi


def compare(price_list, sar_list):
    sar_bullish_signal = False
    sar_bearish_signal = False
    bullish_klinger = False
    bearish_klinger = False

    if (sar_list[0] > price_list[0]) and (sar_list[1] > price_list[1]) and (sar_list[2] > price_list[2]):
        sar_bearish_signal = True

    elif (sar_list[0] < price_list[0]) and (sar_list[1] < price_list[1]) and (sar_list[2] < price_list[2]):
        sar_bullish_signal = True

    if klinger > 0:
        bullish_klinger = True
    elif klinger < 0:
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


try:
    driver = webdriver.Chrome()
    driver.get("https://www.tradingview.com/#signin")
except Exception as e:
    print('+ Error Involving Chrome Driver + \n')
    quit()

wallet = 1
signal = 1
long = False
short = False
bought = 0
previous_price = 0
mouse = Controller()

create_csv()

input()
while True:
    sleep(0.5)
    mouse.move(1, 0)

    price, boillinger_top, boillinger_bottom, klinger, rsi = get_values()
    if price == "n/a":
        continue
    if price != previous_price:

        # print("Price:", price, "\n" + "SAR:", sar, "\n" + "Klinger 1:", klinger1, "\n" + "Klinger 2:", klinger2, "\n")

        edit_csv(price, boillinger_top, boillinger_bottom, klinger, rsi)

        previous_price = price






