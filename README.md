# Project-ez2-ermili-cch8-dvchavan

## Backend Setup
- Install [Google Chrome](https://www.google.com/chrome/) to use for scraping
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for handling python versions, packages, and virtual environments
- `cd backend`
- Create virtual environment (one time only): `uv venv`
- Prior to running scripts, activate the venv: `source .venv/bin/activate`
- Run the server: `uv run main.py`
- Deactivate the venv when done: `deactivate`

## Backend Setup for Development (Optional)

### Creating Datasets

- Download the [(international) movies dataset](https://www.kaggle.com/datasets/pavan4kalyan/imdb-dataset-of-600k-international-movies) and move inner the `movie_dataset` to `data/movie_dataset`
- Download the [trending movies dataset](https://www.kaggle.com/datasets/amitksingh2103/trending-movies-over-the-years) and move it to `data/trending_movies.csv`
- Initialize the movies dataset and merged trending movies dataset: `uv run helpers/initialize_datasets.py`
- Preprocess the movies dataset: `uv run helpers/preprocess_features.py`
- Split the preprocessed movies dataset: `uv run helpers/split_csv.py`
- Retrieve the preprocessed features of the trending movies dataset: `uv run helpers/retrieve_preprocessed.py`
- **(Very slow ~ 6 hrs)** Scrape movie trailer YouTube video ids for the merged trending movies dataset: `uv run helpers/scrape_trailer_ids.py`

### Scraping, Sentiment Analysis, and Merging of Letterboxd Data

- Select a Letterboxd user's `username` to use 

#### Scraping 

- `uv run helpers/scrape_reviews.py username`
- Find the scraped reviews at `data/reviews/username.csv`

#### Sentiment Analysis

- `uv run helpers/sentiment.py username`
- Find the scraped reviews and their sentiment analysis at `data/sentiment_reviews/username.csv`

#### Merging

- `uv run helpers/movieswreviews.py username`
- Find the reviews and their sentiment analysis at `data/merged_reviews/username.csv` 

## Frontend Setup
- Install [Node.js](https://nodejs.org/en/download) to get npm
- `cd frontend`
- Install all dependencies: `npm install`
- Run the frontend: `npm run dev`

## File architecture
`root`
- `backend` backend folder
  - `main.py` fastapi server 
  - `data` all datasheets
  - `helpers` helper methods
    - `models.py` type modelling
    - `paths.py` enumerates the paths of the contents of `data`
    - `initialize_datasets.py` initializes the movies dataset and the merged trending movies dataset
    - `scrape_reviews.py` provides method for scraping Letterboxd user data 
    - `scrape_trailer_ids.py` scrapes YouTube for merged trending movie trailer ids
    - `sentiment.py` provides method for sentiment analysis on scraped Letterboxd user data 
    - `movieswreviews.py` provides method for merging the movies dataset with post sentiment analysis Letterboxd user data
    - `recommender.py` provides cosine similarity and knn recommender methods
    - `preprocess_features.py` preprocesses the movies dataset
    - `split_csv.py` splits the preprocessed movies dataset into multiple files
    - `retrieve_preprocessed.py` provides methods for retrieving the preprocessed versions of movie data
    - `test.py` tests the recommendation system on mock data
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
