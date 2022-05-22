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
        movie_list = []
        movie_search_result = driver.find_elements_by_xpath("//div[@class='sc-crrsfI iDhzRL imdb-header__search-menu']/div/ul/li")
        if len(movie_search_result) > 0:
            for i in range(len(movie_search_result)):
                movie_title = movie_search_result[i].find_elements_by_class_name("searchResult__constTitle")
                if len(movie_title) > 0: 
                    movie_list.append((movie_search_result[i], movie_title[0].text))
                    print(f"index: {len(movie_list) - 1} -> {movie_title[0].text}")

        # Select the movie from the above search list
        ind = int(input("Enter movie index: "))
        movie_name = movie_list[ind][1]
        time.sleep(1)

        counter = 5
        while 0 < counter:
            try:  
                movie_list[ind][0].click()
                break
            except:
                counter -= 1

        # Click on the review button
        try:
            driver.find_element_by_xpath("//div[@data-testid='reviews-header']/a").click()
        except:
            print("No reviews available")
            driver.quit()
            return

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