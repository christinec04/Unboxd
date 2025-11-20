from selenium import webdriver
from selenium.webdriver.common.by import By
import sys

def convert_to_csv_string(string: str):
    string = string.replace('"', "'")
    return f'"{string}"'

def click_element(driver, element):
    driver.execute_script('arguments[0].click();', element)

def get_url(username, page_number):
    return f'https://letterboxd.com/{username}/reviews/films/page/{page_number}/'

def init_dataset(username):
    dataset = open(f'./reviews/{username}.csv', 'a', encoding='utf-8')
    col_headers = 'name,user rating,user review\n'
    dataset.write(col_headers)
    return dataset

def update_dataset(dataset, name, user_rating, user_review):
    data = (name, user_rating, user_review)
    dataset.write(f"{','.join(str(value) for value in data)}\n")

def scrape_reviews(username):
    print('starting scraping')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options)

    dataset = init_dataset(username)
    page_number = 1
    while True:
        print(f'scraping page {page_number}...')
        driver.get(get_url(username, page_number))
        reviews = driver.find_elements(By.CSS_SELECTOR, '[data-object-name="review"]')
        if len(reviews) == 0:
            break
        for review in reviews:
            # press all 'more' links to expand all the reviews 
            while True:
                try:
                    button = review.find_element(By.CLASS_NAME, 'reveal')
                    click_element(driver, button)
                except:
                    break  
            name_parent_element = review.find_element(By.CLASS_NAME, 'name')
            name = convert_to_csv_string(name_parent_element.find_element(By.TAG_NAME, 'a').text)
            # scrape the user's rating if given
            try:
                user_rating_symbols = review.find_element(By.CLASS_NAME, 'rating').text.strip()
                user_rating = user_rating_symbols.count('★') + \
                        0.5 * user_rating_symbols.count('½')
            except:
                user_rating = ''
            # TODO deal with spoiler warning in review - username: maorimovies
            user_review_element = review.find_element(By.CLASS_NAME, 'js-review-body')
            user_review = convert_to_csv_string(user_review_element.text)
            update_dataset(dataset, name, user_rating, user_review)
        page_number += 1
    print('finished scraping')
    driver.quit()
    dataset.close()


if __name__ == "__main__":
    scrape_reviews(sys.argv[1])
