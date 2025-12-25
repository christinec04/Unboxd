from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from collections import defaultdict
import requests
import bs4
import itertools 
import time 
import sys
import os

def init_headless_chrome_webdriver() -> webdriver.Chrome:
    """Returns a Chrome webdriver that operates without a GUI and limits unnecessary requests"""
    chrome_options = webdriver.ChromeOptions()
    # do not fetch images or css stylesheets
    prefs = {
            "profile.default_content_setting_values.images": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options)
    return driver

def scrape_reviews(username: str, print_status: bool = False) -> pd.DataFrame:
    """Returns the scraped Letterboxd reviews of `username` with a Chrome webdriver"""
    if print_status: print("starting scraping reviews")
    driver = init_headless_chrome_webdriver()
    data = defaultdict(list)
    for page_number in itertools.count(start=1, step=1):
        if print_status: print(f"scraping page {page_number}...")
        driver.get(f"https://letterboxd.com/{username}/reviews/films/page/{page_number}/")
        time.sleep(2)
        reviews = driver.find_elements(By.CSS_SELECTOR, "[data-object-name=\"review\"]")
        # clicks `element` regardless of whether it is visible on the page 
        click_element = lambda element: driver.execute_script("arguments[0].click();", element)
        reveal_spoiler_buttons = driver.find_elements(By.CSS_SELECTOR, "[data-js-trigger=\"spoiler.reveal\"]")
        for button in reveal_spoiler_buttons: 
            click_element(button)
        show_more_buttons = driver.find_elements(By.CLASS_NAME, "reveal")
        for button in show_more_buttons: 
            click_element(button)
        for review in reviews:
            try:
                user_rating_symbols = review.find_element(By.CLASS_NAME, "rating").text.strip()
                user_rating = user_rating_symbols.count("★") + \
                        0.5 * user_rating_symbols.count("½")
            except NoSuchElementException:
                # skip reviews without ratings
                continue
            data["user_rating"].append(user_rating)
            name_parent_element = review.find_element(By.CLASS_NAME, "name")
            name = name_parent_element.find_element(By.TAG_NAME, "a").text
            data["original_title"].append(name)
            release_year = review.find_element(By.CLASS_NAME, "releasedate").text
            data["release_year"].append(release_year)
            user_review_element = review.find_element(By.CLASS_NAME, "js-review-body")
            user_review = user_review_element.text
            data["user_review"].append(user_review)
        page_numbers = driver.find_elements(By.CLASS_NAME, "paginate-page")
        # should not happen
        if len(page_numbers) == 0:
            break
        last_page_number = int(page_numbers.pop().text.strip())
        if page_number == last_page_number:
            break;
    if print_status: print("finished scraping")
    driver.quit()
    return pd.DataFrame.from_dict(data)

def scrape_ratings(username: str, print_status: bool = False) -> pd.DataFrame:
    """Returns the scraped Letterboxd ratings of `username`"""
    if print_status: print("starting scraping ratings")
    data = defaultdict(list)
    for page_number in itertools.count(start=1, step=1):
        if print_status: print(f"scraping page {page_number}...")
        page_url = f"https://letterboxd.com/{username}/films/page/{page_number}/"
        try:
            response = requests.get(page_url)
            time.sleep(2)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # choosing not to retry to limit number of requests 
            if print_status: print(f"failed to get {page_url} because {e}")
            continue
        html = response.text
        soup = bs4.BeautifulSoup(markup=html, features="html.parser")
        films = soup.find_all(name="li", class_="griditem")
        for film in films:
            poster = film.find(name="div", attrs={"data-component-class":"LazyPoster"})
            # should not happen
            if poster is None:
                continue
            original_title_and_release_year = poster.get(key="data-item-full-display-name")
            # should not happen, but there is also no point in scraping an unknown film
            if not isinstance(original_title_and_release_year, str):
                continue
            example_suffix = " (2099)"
            split_index = len(original_title_and_release_year) - len(example_suffix)
            original_title = original_title_and_release_year[:split_index]
            data["original_title"].append(original_title)
            # remove whitespace and parentheses from release year suffix and parse as int
            release_year = int(original_title_and_release_year[split_index+2:-1])
            data["release_year"].append(release_year)
            user_rating_element = film.find(name="span", attrs={"class":"rating"})
            if user_rating_element is None:
                # handling None is left up to the preprocessing stage, e.g. via imputation by mean 
                user_rating = None
            else:
                user_rating_symbols = user_rating_element.get_text()
                user_rating = user_rating_symbols.count("★") + 0.5 * user_rating_symbols.count("½")
            data["user_rating"].append(user_rating)
        page_numbers = soup.find_all(name="li", class_="paginate-page")
        # should not happend
        if len(page_numbers) == 0:
            break
        last_page_number = int(page_numbers.pop().get_text())
        if page_number == last_page_number:
            break;
    if print_status: print("finished scraping")
    return pd.DataFrame.from_dict(data)

def scrape_pfp_url(username: str) -> str:
    """Returns the scraped Letterboxd profile picture url `username`"""
    page_url = f"https://letterboxd.com/{username}/"
    try:
        response = requests.get(page_url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return ""
    html = response.text
    soup = bs4.BeautifulSoup(markup=html, features="html.parser")
    try:
        pfp_grandparent = soup.find(name="div", class_="profile-avatar")
        pfp_element = pfp_grandparent.find(name="img")
        return pfp_element.get("src");
    except AttributeError:
        return ""
    except Exception:
        return ""

if __name__ == "__main__":
    from paths import Path
    username = sys.argv[1]
    if "reviews" in sys.argv:
        data = scrape_reviews(username, print_status=True)
        os.makedirs(Path.REVIEWS_FOLDER, exist_ok=True)
        data.to_csv(os.path.join(Path.REVIEWS_FOLDER, f"{username}.csv"), index=False)
    if "ratings" in sys.argv:
        data = scrape_ratings(username, print_status=True)
        os.makedirs(Path.RATINGS_FOLDER, exist_ok=True)
        data.to_csv(os.path.join(Path.RATINGS_FOLDER, f"{username}.csv"), index=False)
    if "pfp" in sys.argv:
        print('pfp url:', scrape_pfp_url(username))
