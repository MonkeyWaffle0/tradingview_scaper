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

    sar = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div/div"
    ).text

    dif_sar = float(price) - float(sar)

    rsi = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[3]/div/div/div"
    ).text

    macd = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[5]/td[2]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[1]/div"
    ).text

    macd = macd.replace("−", "-")
    macd = float(macd) * 1000

    values = {
        "price": price,
        "sar": dif_sar,
        "rsi": rsi,
        "macd": macd
    }

    return values


def create_csv(data_id, values):
    """Create the csv file and add the first row if the file does not exist yet."""
    row = [key for key in values.keys()]
    if not os.path.exists("data_training/data_training_" + data_id + ".csv"):
        with open("data_training_" + data_id + ".csv", "w", newline="") as write_file:
            writer = csv.writer(write_file)
            writer.writerow(row)


def edit_csv(values):
    """Add a new line to the csv file."""
    row = [val for val in values.values()]
    with open("data_training/data_training_" + data_id + ".csv", "a", newline="") as write_file:
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
    previous_price = 0
    input("""Log in Tradingview, get you chart ready, go to your starting point and press any key to start. \n
    Once you started, put your cursor on the chart, the chart will move to the right and gather the data from your starting point. 
    \n""")
    while True:
        # Once the loop is started, will press the right arrow key to go to the next candle, and add the data to the
        # csv.
        pyautogui.press("right")
        # Some errors may occur if the chart is moving too fast.
        sleep(0.01)
        # Gets the values you want.
        values = get_values()
        create_csv(data_id, values)
        if values.get("price") == "n/a":
            continue
        # Add the new line to the csv file.
        if values.get("price") != previous_price:
            edit_csv(values)
            previous_price = values.get("price")