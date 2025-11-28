from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import sys
import pandas as pd
import os
from itertools import count

def click_element(driver: webdriver.Chrome, element: WebElement) -> None:
    """Clicks `element`, regardless of whether is is obscured on the page, using `driver`"""
    driver.execute_script("arguments[0].click();", element)

def get_reviews_url(username: str, page_number: int) -> str:
    """Returns the url of the reviews on `page_number` of `username`'s reviews on Letterboxd"""
    return f"https://letterboxd.com/{username}/reviews/films/page/{page_number}/"

def reveal_hidden_reviews_content(driver: webdriver.Chrome, review: WebElement) -> None:
    """Reveals truncated content or content hidden by spoiler warnings on a Letterboxd reviews page"""
    try:
        reveal_spoiler_button = review.find_element(By.CSS_SELECTOR, "[data-js-trigger=\"spoiler.reveal\"]")
        click_element(driver, reveal_spoiler_button)
    except:
        pass
    try:
        show_more_button = review.find_element(By.CLASS_NAME, "reveal")
        click_element(driver, show_more_button)
    except:
        pass

def init_headless_chrome_webdriver() -> webdriver.Chrome:
    """Returns a Chrome webdriver that operates without a GUI"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options)
    return driver

def scrape_reviews(username: str, print_status: bool = False) -> pd.DataFrame:
    """Returns the scraped Letterboxd reviews of `username` with a Chrome webdriver"""
    if print_status: print("starting scraping")
    driver = init_headless_chrome_webdriver()
    columns = ["name", "year", "user_rating", "user_review"]
    data = { col:[] for col in columns }
    for page_number in count(start=1, step=1):
        if print_status: print(f"scraping page {page_number}...")
        driver.get(get_reviews_url(username, page_number))
        reviews = driver.find_elements(By.CSS_SELECTOR, "[data-object-name=\"review\"]")
        if len(reviews) == 0:
            break
        for review in reviews:
            reveal_hidden_reviews_content(driver, review)
            name_parent_element = review.find_element(By.CLASS_NAME, "name")
            name = name_parent_element.find_element(By.TAG_NAME, "a").text
            data["name"].append(name)
            release_year = review.find_element(By.CLASS_NAME, "releasedate").text
            data["year"].append(release_year)
            try:
                user_rating_symbols = review.find_element(By.CLASS_NAME, "rating").text.strip()
                user_rating = user_rating_symbols.count("★") + \
                        0.5 * user_rating_symbols.count("½")
            except:
                # default to 0 which cannot be used as a rating in letterboxd
                user_rating = 0
            data["user_rating"].append(user_rating)
            user_review_element = review.find_element(By.CLASS_NAME, "js-review-body")
            user_review = user_review_element.text
            data["user_review"].append(user_review)
    if print_status: print("finished scraping")
    driver.quit()
    return pd.DataFrame.from_dict(data)

if __name__ == "__main__":
    username = sys.argv[1]
    data = scrape_reviews(username, print_status=True)
    data.to_csv(os.path.join(os.getcwd(), "..", "data", "reviews", f"{username}.csv"), index=False)

