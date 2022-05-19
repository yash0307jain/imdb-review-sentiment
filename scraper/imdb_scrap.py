from pathlib import Path
import selenium
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time

try:
    PATH = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(PATH)

    url = "https://www.imdb.com/"
    driver.get(url)
    time.sleep(5)
    print(driver)
except Exception as e:
    print(str(e))