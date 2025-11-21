# Project-ez2-ermili-cch8-dvchavan

## Backend Setup
- Install [Google Chrome](https://www.google.com/chrome/) to use for scraping
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for handling python versions, packages, and virtual environments
- `cd backend`
- To run the backend: `uv run uvicorn main:app`

### Scraping Letterboxd Reviews

- To run the scraper: `uv run scrape_reviews.py username`, where `username` is the letterboxd username to use for scraping
- After the program terminates, find the scraped reviews at `./reviews/username.csv`, where `username` is the same letterboxd username used earlier

## Frontend Setup
- Install [Node.js](https://nodejs.org/en/download) to get npm
- `cd frontend`
- To install all dependencies `npm install`
- To run the frontend `npm run dev`
