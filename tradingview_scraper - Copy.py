"""Tradingview does not give us access to their data, the only accessible chart data are the current information
related to where the cursor is on the chart. This program will scrape those data using selenium and the data path."""

from selenium import webdriver
import pyautogui

import csv
import os
from time import sleep


def get_values():
    """The only way to get the data from Tradingview is to use xpath, here, you may want to custom this
    depending on which data you want to gather."""
    # Closing price
    price = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[2]/div/div[4]/div[2]"
    ).text

    ema20 = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div/div"
    ).text

    vol = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[3]/div[3]/div/div[1]/div"
    ).text

    vol_ema = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[3]/div[3]/div/div[2]/div"
    ).text

    if "K" in vol:
        vol = float(vol[:len(vol) - 1]) * 1000

    if "K" in vol_ema:
        vol_ema = float(vol_ema[:len(vol_ema) - 1]) * 1000

    sar = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[4]/div[3]/div/div/div"
    ).text

    dif_sar = float(price) - float(sar)

    rsi = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[3]/div/div/div"
    ).text

    return price, ema20, vol, vol_ema, dif_sar, rsi


def create_csv(data_id):
    """Create the csv file, you can custom this depending on tha data you need."""
    row = ["price", "ema20", "vol", "vol_ema", "sar", "rsi"]
    if not os.path.exists("data_training_" + data_id + ".csv"):
        with open("data_training_" + data_id + ".csv", "w", newline="") as write_file:
            writer = csv.writer(write_file)
            writer.writerow(row)


def edit_csv(price, ema20, vol, vol_ema, dif_sar, rsi):
    """Add a new line to the csv file."""
    row = [price, ema20, vol, vol_ema, dif_sar, rsi]
    with open("data_training_" + data_id + ".csv", "a", newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerow(row)


if __name__ == '__main__':
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.tradingview.com/#signin")
    except Exception as e:
        print("Error Involving Chrome Driver \n")
        quit()

    data_id = input("What is the data id ? \n")
    create_csv(data_id)
    previous_price = 0
    input("""Log in Tradingview, get you chart ready, go to your starting point and press any key to start. \n
    Once you started, put your cursor on the chart, the chart will move to the right and gather the data from your starting point. 
    \n""")
    while True:
        # Once the loop is started, will press the right arrow key to go to the next candle, and add the data to the
        # csv.
        pyautogui.press("right")
        # Some errors may occur if the chart is moving too fast.
        sleep(0.05)
        # Gets the values you want.
        price, ema20, vol, vol_ema, dif_sar, rsi = get_values()
        if price == "n/a":
            continue
        # Add the new line to the csv file.
        if price != previous_price:
            edit_csv(price, ema20, vol, vol_ema, dif_sar, rsi)
            previous_price = price




