# Project-ez2-ermili-cch8-dvchavan

## Backend Setup
- Install [Google Chrome](https://www.google.com/chrome/) to use for scraping
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for handling python versions, packages, and virtual environments
- Download the [Trending Movies Dataset](https://www.kaggle.com/datasets/amitksingh2103/trending-movies-over-the-years) and move it to `backend/data/trending_movies.csv`
- Download the [International Movies Dataset](https://www.kaggle.com/datasets/pavan4kalyan/imdb-dataset-of-600k-international-movies) and move its inner `movie_datset` folder to `backend/data/movie_dataset`
- `cd backend`
- Create virtual environment (one time only): `uv venv`
- Activate the venv: `source .venv/bin/activate`
- Initialize the datasets (one time only): `uv run helpers/initialize_datasets.py`
- Run the backend: `uv run main.py`
- Deactivate the venv: `deactivate`

### Scraping Letterboxd Reviews

- `cd helpers`
- Run the scraper: `uv run scrape_reviews.py username`, where `username` is the letterboxd username to use for scraping
- After the program terminates, find the scraped reviews at `../data/reviews/username.csv`, where `username` is the same one from above

### Performing Sentiment Analysis

- `cd helpers`
- Ensure the reviews to perform analysis on are at `./data/reviews/username.csv` 
- Run the analysis: `uv run sentiment.py username`, where `username` is the same one from above
- After the program terminates, find the reviews and their sentiment analysis at `../data/sentiment_reviews/username.csv`, where `username` is the same one from above

### Merging Analyzed Reviews with the International Movies Dataset

- `cd helpers`
- Ensure the analyzed reviews are at `./data/processed_reviews/username.csv` 
- Run the merger: `uv run movieswreviews.py username`, where `username` is the same one from above
- After the program terminates, find the merged, analyzed reviews `../data/merged_reviews/username.csv`, where `username` is the same one from above

## Frontend Setup
- Install [Node.js](https://nodejs.org/en/download) to get npm
- `cd frontend`
- Install all dependencies: `npm install`
- Run the frontend: `npm run dev`

## File architecture
`root`
- `backend` backend folder
  - `data` all datasheets
  - `helpers` helper methods
    - `models.py` type modelling
    - `movieswreviews.py` merges movie dataset with reviews
    - `initialize_datasets.py` initializes movie dataset and trending movies dataset
    - `recommender.py` cosine similarity, knn and recommender methods
    - `scrape_reviews.py` Letterboxd scraper
    - `scrape_trailer_ids.py` YouTube scraper
    - `sentiment.py` sentiment analysis on reviews
  - `main.py` main backend file to run
- `frontend` frontend folder
  - `app`
    - `api`
      - `index.ts` backend api setup
    - `recommendations`
      - `page.tsx` recommendations page ("/recommendations")
    - `globals.css` global css file
    - `layout.tsx` main layout
    - `page.tsx` main landing page ("/")
    - `types.tsx` type modelling
  - `components`
    - `ui` shadcn ui components
    - `error.tsx` error component
    - `movie-card.tsx` movie card component
    - `nav-bar.tsx` navigation bar component
    - `progress.tsx` progress bar component
    - `result.tsx` result component that shows on loaded results page
    - `theme-provider.tsx` dark/light mode theme provider
    - `theme-toggle.tsx` dark/light mode toggle component
