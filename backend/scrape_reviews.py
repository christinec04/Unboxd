from selenium import webdriver
from selenium.webdriver.common.by import By

def convert_to_csv_string(string: str):
    string = string.replace('"', "'")
    return f'"{string}"'

def click_element(driver, element):
    driver.execute_script('arguments[0].click();', element)

def get_url(username, page_number):
    return f'https://letterboxd.com/{username}/reviews/films/page/{page_number}/'

def scrape_reviews(username):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options)

    data = []
    page_number = 1
    while True:
        print(f'scraping page {page_number}...')
        driver.get(get_url(username, page_number)) # need to check if username exists
        reviews = driver.find_elements(By.CSS_SELECTOR, '[data-object-name="review"]')
        if not reviews:
            break
        for review in reviews:
            # reveal all spoilers / truncated text
            while True:
                try:
                    button = review.find_element(By.CLASS_NAME, 'reveal')
                    click_element(driver, button)
                except:
                    break  # no more reveal buttons in this review

            name_parent_element = review.find_element(By.CLASS_NAME, 'name')
            name = convert_to_csv_string(name_parent_element.find_element(By.TAG_NAME, 'a').text)
            try:
                user_rating_symbols = review.find_element(By.CLASS_NAME, 'rating').text.strip()
                user_rating = user_rating_symbols.count('★') + \
                        0.5 * user_rating_symbols.count('½')
            except:
                user_rating = ''
            # TODO deal with spoiler warning in review - username: maorimovies
            user_review_element = review.find_element(By.CLASS_NAME, 'js-review-body')
            user_review = convert_to_csv_string(user_review_element.text)
            data.append((name, user_rating, user_review))
        page_number += 1
    driver.quit()

    print('saving data...')
    with open(f'./reviews/{username}.csv', 'w', encoding='utf-8') as dataset:
        col_headers = 'name,user rating,user review\n'
        dataset.write(col_headers)
        for row in data:
            dataset.write(f"{','.join(str(value) for value in row)}\n")
