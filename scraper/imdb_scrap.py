from shutil import move
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import os.path

movieFileName = lambda movie: "_".join(movie.split())

def scrapReviews(movie_name: str) -> None:
    try:
        if os.path.exists(f"data/{movieFileName(movie_name)}.json"):
            print("Already exists")
            return

        CHROME_DRIVER_BINARY = "scraper/chromedriver"
        options = webdriver.ChromeOptions()
        options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        driver = webdriver.Chrome(CHROME_DRIVER_BINARY, chrome_options=options)

        # Go to the URL
        driver.maximize_window()
        url = "https://www.imdb.com/"
        driver.get(url)

        # Write on the search text field
        driver.find_element_by_id("suggestion-search").send_keys(movie_name)
        time.sleep(2)
        
        # Click on the first search result
        result_movie_name = driver.find_element_by_xpath("//div[@class='sc-crrsfI iDhzRL imdb-header__search-menu']/div/ul/li/a")
        movie_name = result_movie_name.text.split("\n")[0]
        result_movie_name.click()

        # Click on the search button
        #driver.find_element_by_id("suggestion-search-button").click()

        # Go to the first movie in the list
        #driver.find_element_by_xpath("//table[@class='findList']/tbody/tr/td[@class='result_text']/a").click()

        # Click on the review button
        driver.find_element_by_xpath("//div[@data-testid='reviews-header']/a").click()

        # Get all the reviews
        reviews_obj = []
        while True:
            try:
                driver.find_element_by_class_name("ipl-load-more__button").click()
                time.sleep(3)
            except:
                reviews_obj = driver.find_elements_by_xpath("//div[@class='text show-more__control']")
                break
        
        reviews = []
        for review in reviews_obj:
            if review.text != "":
                reviews.append(review.text)
        
        # Export reviews
        data = {'reviews': reviews}
        with open(f'data/{movieFileName(movie_name)}.json', 'w') as jsonfile:
            json.dump(data, jsonfile)

        # Quit the driver
        driver.quit()
    except Exception as e:
        print(str(e))

scrapReviews("Bhool")