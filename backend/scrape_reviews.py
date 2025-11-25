from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import pandas as pd
import os
from utils import create_path

def click_element(driver, element):
    driver.execute_script('arguments[0].click();', element)

def get_url(username: str, page_number: int):
    return f'https://letterboxd.com/{username}/reviews/films/page/{page_number}/'

def scrape_reviews(username: str, print_status: bool = False) -> pd.DataFrame:
    if print_status:
        print('starting scraping')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options)
    data = { 'name': [], 'user rating': [], 'user review': [] }
    page_number = 1
    while True:
        if print_status:
            print(f'scraping page {page_number}...')
        driver.get(get_url(username, page_number))
        reviews = driver.find_elements(By.CSS_SELECTOR, '[data-object-name="review"]')
        if len(reviews) == 0:
            break
        for review in reviews:
            try:
                reveal_spoiler_button = review.find_element(By.CSS_SELECTOR, '[data-js-trigger="spoiler.reveal"]')
                click_element(driver, reveal_spoiler_button)
            except:
                pass
            try:
                show_more_button = review.find_element(By.CLASS_NAME, 'reveal')
                click_element(driver, show_more_button)
            except:
                pass
            try:
                user_rating_symbols = review.find_element(By.CLASS_NAME, 'rating').text.strip()
                user_rating = user_rating_symbols.count('★') + \
                        0.5 * user_rating_symbols.count('½')
            except:
                # default to 0 which cannot be used as a rating in letterboxd
                user_rating = 0
            data['user rating'].append(user_rating)
            name_parent_element = review.find_element(By.CLASS_NAME, 'name')
            name = name_parent_element.find_element(By.TAG_NAME, 'a').text
            data['name'].append(name)
            user_review_element = review.find_element(By.CLASS_NAME, 'js-review-body')
            user_review = user_review_element.text
            data['user review'].append(user_review)
        page_number += 1
    if print_status:
        print('finished scraping')
    driver.quit()
    return pd.DataFrame.from_dict(data)

if __name__ == "__main__":
    username = sys.argv[1]
    data = scrape_reviews(username, print_status=True)
    data.to_csv(create_path([os.getcwd(), 'reviews', f'{username}.csv']), index=False)
