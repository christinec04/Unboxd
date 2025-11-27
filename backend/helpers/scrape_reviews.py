from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import pandas as pd
import os
from utils import create_path
import requests
from bs4 import BeautifulSoup

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
    columns = ['name', 'user rating', 'user review', 'date', 'description']
    data = {}
    for column in columns:
        data[column] = []
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
            poster = review.find_element(By.CLASS_NAME, 'film-poster')
            movie_link = poster.find_element(By.TAG_NAME, 'a').get_attribute('href')
            description = None
            if movie_link:
                response = requests.get(movie_link)
                soup = BeautifulSoup(response.text, 'html.parser')
                description_element = soup.find(attrs={'class':'truncate'})
                if description_element:
                    description = description_element.text.strip()
            data['description'].append(description)
            name_parent_element = review.find_element(By.CLASS_NAME, 'name')
            name = name_parent_element.find_element(By.TAG_NAME, 'a').text
            data['name'].append(name)
            user_review_element = review.find_element(By.CLASS_NAME, 'js-review-body')
            user_review = user_review_element.text
            data['user review'].append(user_review)
            release_date = review.find_element(By.CLASS_NAME, 'releasedate').text
            data['date'].append(release_date)
        page_number += 1
    if print_status:
        print('finished scraping')
    driver.quit()
    return pd.DataFrame.from_dict(data)

if __name__ == "__main__":
    username = sys.argv[1]
    data = scrape_reviews(username, print_status=True)
    data.to_csv(create_path([os.getcwd(), '..', 'data', 'reviews', f'{username}.csv']), index=False)
