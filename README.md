# Project-ez2-ermili-cch8-dvchavan

## how to scrape letterboxd reviews

- install chrome
- download selenium: `pip install selenium`
- run `scrape-reviews.py`
- when prompted, enter a letterboxd username to use for scraping
- wait till the program terminates
- find the scraped reviews in `./reviews/username.csv`, where username is the same letterboxd username from earlier

## Setup
- Setup virtual environment: run `python -m venv venv`
- Activate virtual environment:
  - Windows: `.\venv\Script\activate`
  - Mac/Linux: `source ./venv/bin/activate`
- Download requirements: `pip install -r requirements.txt`
- Install `npm install axios`
`npm install tailwindcss @tailwindcss/vite`

## To run
- Cd into `frontend` and run `npm run dev`
- Cd into `backend` and run `python main.py`
