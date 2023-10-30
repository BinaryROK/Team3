import pandas as pd
import numpy as np
import os
import params as pa
import time
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
pd.set_option('display.Width', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)


def driversetting(DownloadPath):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": pa.DownloadPath,
                                              "download.prompt_for_download": False,
                                              "download.directory_upgrade": True,
                                              "safebrowsing_for_trusted_source_enabled": False,
                                              "safebrowsing.enabled": False})

    #options.add_argument("headless") # 켜두면 크롬창이 뜨지않고 실행됨
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shn-usage')
    driver = webdriver.Chrome(executable_path='C:\Team3\Crawl\chromedriver_win32\chromedriver.exe',options=options)
    driver.implicitly_wait(pa.waitseconds)

    return driver

def gen():

    driver = driversetting(pa.DownloadPath)

    driver.get(pa.gonggong)
    print('run website')
    time.sleep(pa.waitseconds)

    # Click the first element
    try:
        element1 = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[1]/div[3]/div/a')
        element1.click()
        print('Clicked the first element')
    except:
        print('Failed to click the first element')

    time.sleep(2)  # Wait for download to complete

    # Click the second element
    try:
        element2 = driver.find_element(By.XPATH, '//*[@id="tab-layer-file"]/div[9]/div[3]/ul/li[1]/div[1]/a')
        element2.click()
        print('Clicked the second element')
    except:
        print('Failed to click the second element')

    time.sleep(2)  # Wait for the operation to complete

    # Click the third element
    try:
        element3 = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[5]/div[3]/ul/li[1]/div[1]/a')
        element3.click()
        print('Clicked the third element')
    except:
        print('Failed to click the third element')

    time.sleep(2)  # Wait for the operation to complete

    # Click the fourth element
    try:
        element4 = driver.find_element(By.XPATH, '//*[@id="layer_data_infomation"]/div[3]/table/tbody/tr[13]/td/a[1]')
        element4.click()
        print('Clicked the fourth element')
    except:
        print('Failed to click the fourth element')

    time.sleep(2)  # Wait for the operation to complete

    # Click the 5th element

    try:
        element5 = driver.find_element(By.XPATH, '//*[@id="layer_data_infomation"]/div[4]/div/a')
        element5.click()
        print('Clicked the fifth element')
    except:
        print('Failed to click the fifth element')

    time.sleep(2)  # Wait for the operation to complete

    try:
        element6 = driver.find_element(By.XPATH, '//*[@id="data-type-recommendData"]/a')
        element6.click()
        print('Clicked the sixth element')
    except:
        print('Failed to click the sixth element')

    time.sleep(2)  # Wait for the operation to complete


    try:
        element7 = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[5]/div[3]/ul/li[2]/div[1]/a')
        element7.click()
        print('Clicked the seventh element')
    except:
        print('Failed to click the seventh element')

    time.sleep(2)  # Wait for the operation to complete

    try:
        element8 = driver.find_element(By.XPATH, '//*[@id="layer_data_infomation"]/div[3]/table/tbody/tr[13]/td/a[1]')
        element8.click()
        print('Clicked the eighth element')
    except:
        print('Failed to click the eighth element')

    time.sleep(2)  # Wait for the operation to complete

    try:
        element9 = driver.find_element(By.XPATH, '//*[@id="layer_data_infomation"]/div[4]/div/a')
        element9.click()
        print('Clicked the ninth element')
    except:
        print('Failed to click the ninth element')

    time.sleep(2)  # Wait for the operation to complete

    try:
        element6 = driver.find_element(By.XPATH, '//*[@id="data-type-recommendData"]/a')
        element6.click()
        print('Clicked the sixth element')
    except:
        print('Failed to click the sixth element')

    time.sleep(2)  # Wait for the operation to complete

    try:
        element10 = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[5]/div[3]/ul/li[3]/div[1]/a')
        element10.click()
        print('Clicked the 10th element')
    except:
        print('Failed to click the 10th element')

    time.sleep(2)  # Wait for the operation to complete

    try:
        element11 = driver.find_element(By.XPATH, '//*[@id="layer_data_infomation"]/div[3]/table/tbody/tr[13]/td/a[1]')
        element11.click()
        print('Clicked the 11th element')
    except:
        print('Failed to click the 11th element')

    time.sleep(2)  # Wait for the operation to complete

    return []


if __name__ == '__main__':
    gen()