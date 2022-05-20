from pathlib import Path
import selenium
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time

try:
    CHROME_DRIVER_BINARY = "scraper/chromedriver"
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    driver = webdriver.Chrome(CHROME_DRIVER_BINARY, chrome_options=options)

    url = "https://www.imdb.com/"
    driver.get(url)
    time.sleep(5)
    print(driver)
except Exception as e:
    print(str(e))