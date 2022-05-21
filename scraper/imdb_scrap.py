from selenium import webdriver
import json
import time
import os.path

def scrap_reviews(movie_name: str) -> None:
    try:
        if os.path.exists(f"data/{movie_name}.json"):
            print("Already exists")
            return

        MOVIE_NAME = movie_name
        CHROME_DRIVER_BINARY = "scraper/chromedriver"
        options = webdriver.ChromeOptions()
        options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        driver = webdriver.Chrome(CHROME_DRIVER_BINARY, chrome_options=options)

        # Go to the URL
        driver.maximize_window()
        url = "https://www.imdb.com/"
        driver.get(url)

        # Write on the search text field
        search_area = driver.find_element_by_id("suggestion-search").send_keys(MOVIE_NAME)
        time.sleep(2)

        # Click on the search button
        driver.find_element_by_id("suggestion-search-button").click()

        # Go to the first movie in the list
        driver.find_element_by_xpath("//table[@class='findList']/tbody/tr/td[@class='result_text']/a").click()

        # Click on the review button
        driver.find_element_by_xpath("//div[@data-testid='reviews-header']/a").click()

        # Get all the reviews
        reviews_obj = []
        while True:
            load_more = driver.find_element_by_class_name("ipl-load-more__button")
            if load_more.text == 'Load More':
                load_more.click()
                time.sleep(3)
            else:
                reviews_obj = driver.find_elements_by_xpath("//div[@class='text show-more__control']")
                break
        
        reviews = []
        for review in reviews_obj:
            if review.text != "":
                reviews.append(review.text)
        
        # Export reviews
        data = {'reviews': reviews}
        with open(f'data/{MOVIE_NAME}.json', 'w') as jsonfile:
            json.dump(data, jsonfile)

        # Quit the driver
        driver.quit()
    except Exception as e:
        print(str(e))