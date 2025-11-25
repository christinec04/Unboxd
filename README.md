# Project-ez2-ermili-cch8-dvchavan

## Backend Setup
- Install [Google Chrome](https://www.google.com/chrome/) to use for scraping
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for handling python versions, packages, and virtual environments
- `cd backend`
- To run the backend: `uv run uvicorn main:app`

### Scraping Letterboxd Reviews

- To run the scraper: `uv run scrape_reviews.py username`, where `username` is the letterboxd username to use for scraping
- After the program terminates, find the scraped reviews at `./reviews/username.csv`, where `username` is the same one from above

### Performing Sentiment Analysis

- Ensure the reviews to perform analysis on are at `./reviews/username.csv` 
- To run the analysis: `uv run sent.py username`, where `username` is the same one from above
- After the program terminates, find the reviews and their sentiment analysis at `./processed_reviews/username.csv`, where `username` is the same one from above

## Frontend Setup
- Install [Node.js](https://nodejs.org/en/download) to get npm
- `cd frontend`
- To install all dependencies `npm install`
- To run the frontend `npm run dev`
