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

    search_area = driver.find_element_by_id("suggestion-search").send_keys("Doctor Strange")

    search_button = driver.find_element_by_id("suggestion-search-button").click()

    movie_table = driver.find_element_by_xpath("//table[@class='findList']/tbody/tr/td[@class='result_text']/a").click()
    print(movie_table.get_attribute('innerHTML'))

    time.sleep(2)
except Exception as e:
    print(str(e))