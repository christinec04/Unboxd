from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from typing import List, Tuple

def click_element(driver, element):
    driver.execute_script('arguments[0].click();', element)

def get_url(username: str, page_number: int):
    return f'https://letterboxd.com/{username}/reviews/films/page/{page_number}/'

def to_csv_string(string: str):
    string = string.replace('"', "'")
    return f'"{string}"'

def save_data_to_csv(username: str, data: List[Tuple[str, int, str]]):
    dataset = open(f'./reviews/{username}.csv', 'w', encoding='utf-8')
    col_headers = 'name,user rating,user review\n'
    dataset.write(col_headers)
    for row in data:
        new_row = (to_csv_string(val) if isinstance(val, str) else str(val) for val in row)
        dataset.write(f"{','.join(new_row)}\n")
    dataset.close()

def scrape_reviews(username: str) -> List[Tuple[str, int, str]]:
    print('starting scraping')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options)
    data = []
    page_number = 1
    while True:
        print(f'scraping page {page_number}...')
        driver.get(get_url(username, page_number))
        reviews = driver.find_elements(By.CSS_SELECTOR, '[data-object-name="review"]')
        if len(reviews) == 0:
            break
        for review in reviews:
            # press all 'more' links to expand all the reviews 
            for button in review.find_elements(By.CLASS_NAME, 'reveal'):
                try:
                    click_element(driver, button)
                except:
                    continue
            name_parent_element = review.find_element(By.CLASS_NAME, 'name')
            name = name_parent_element.find_element(By.TAG_NAME, 'a').text
            # scrape the user's rating if given
            try:
                user_rating_symbols = review.find_element(By.CLASS_NAME, 'rating').text.strip()
                user_rating = user_rating_symbols.count('★') + \
                        0.5 * user_rating_symbols.count('½')
            # default to 0 which cannot be used as a rating in letterboxd
            except:
                user_rating = 0
            # TODO deal with spoiler warning in review - username: maorimovies
            user_review_element = review.find_element(By.CLASS_NAME, 'js-review-body')
            user_review = user_review_element.text
            data.append((name, user_rating, user_review))
        page_number += 1
    print('finished scraping')
    driver.quit()
    return data

if __name__ == "__main__":
    username = sys.argv[1]
    data = scrape_reviews(username)
    save_data_to_csv(username, data)

