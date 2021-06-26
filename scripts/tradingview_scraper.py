"""Tradingview does not give us access to their data, the only accessible chart data are the current information
related to where the cursor is on the chart. This program will scrape those data using selenium and the data path."""

from selenium import webdriver
import pyautogui

import csv
import os
from time import sleep

from scripts.Constants import ID, PASSWORD


def get_values():
    """The only way to get the data from Tradingview is to use xpath, here, you may want to custom this
    depending on which data you want to gather."""

    factor = 10000

    # Closing price
    close_price = float(driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[5]/div[2]"
    ).text) * factor

    open_price = float(driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[2]"
    ).text) * factor

    high_price = float(driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[2]"
    ).text) * factor

    low_price = float(driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div[2]"
    ).text) * factor

    sar = float(driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div"
    ).text) * factor

    dif_sar = close_price - sar

    ema50 = float(driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[1]/div[2]/div[2]/div[3]/div[2]/div/div/div"
    ).text) * factor

    klinger1 = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[3]/td[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div"
    ).text

    klinger2 = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[3]/td[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div"
    ).text

    klinger1 = klinger1.replace("−", "-")
    klinger2 = klinger2.replace("−", "-")

    klinger1 = float(klinger1.replace("K", "")) * 1000 if "K" in klinger1 else int(klinger1)
    klinger2 = float(klinger2.replace("K", "")) * 1000 if "K" in klinger2 else int(klinger2)

    klinger = int(klinger1) - int(klinger2)

    return {
        "close_price": close_price,
        "open_price": open_price,
        "high_price": high_price,
        "low_price": low_price,
        "dif_sar": dif_sar,
        "ema50": ema50,
        "klinger": klinger
    }


def create_csv(data_id, values):
    """Create the csv file and add the first row if the file does not exist yet."""
    row = [key for key in values.keys()]
    if not os.path.exists("data_training/data_training_" + data_id + ".csv"):
        with open("data_training/data_training_" + data_id + ".csv", "w", newline="") as write_file:
            writer = csv.writer(write_file)
            writer.writerow(row)


def edit_csv(values):
    """Add a new line to the csv file."""
    print(values)
    row = [val for val in values.values()]
    with open("data_training/data_training_" + data_id + ".csv", "a", newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerow(row)


def log_in():
    email_button = driver.find_element_by_xpath("//*[@id='overlap-manager-root']/div/div[2]/div/div/div/div/div/div/div[1]/div[4]")
    email_button.click()
    sleep(1)
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.write(ID)
    pyautogui.press("tab")
    pyautogui.write(PASSWORD)
    pyautogui.press("tab")
    pyautogui.press("enter")
    sleep(1)
    chart_button = driver.find_element_by_xpath("/html/body/div[3]/div[4]/div/ul/li[1]/a")
    chart_button.click()


if __name__ == '__main__':
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.tradingview.com/#signin")
    except Exception as e:
        print("Error Involving Chrome Driver \n")
        quit()

    log_in()
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
        if values.get("close_price") == "n/a":
            continue
        # Add the new line to the csv file.
        if values.get("close_price") != previous_price:
            edit_csv(values)
            previous_price = values.get("close_price")
