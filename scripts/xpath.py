close_price = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[2]/div/div[4]/div[2]"
    ).text

    open_price = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]"
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

    dif_sar = float(close_price) - float(sar)
    dif_sar = round(dif_sar, 5)

    """klinger1 = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[1]/div"
    ).text

    klinger2 = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div"
    ).text

    klinger = float(klinger1) - float(klinger2)"""

    rsi = driver.find_element_by_xpath(
        "/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[3]/div/div/div"
    ).text