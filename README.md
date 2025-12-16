# Unboxd
A recommendation system for Letterboxd movies.\
To see screenshots of the prototype and how the classification system works, read `paper.pdf`

## Setup
\! For further development setup see `DEVELOPMENT.md`

### Backend 
- Install [Google Chrome](https://www.google.com/chrome/) to use for scraping
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for handling python versions, packages, and virtual environments
- `cd backend`
- Download the [(international) movies dataset](https://drive.google.com/file/d/1dwHwCoIjesnRsvrOr_MbSBNcz6vOvaCU/view?usp=sharing) and move it to `data` as `movies.csv`
- Create virtual environment (one time only): `uv venv`
- Prior to running scripts, activate the venv
    - MacOS/Linux: `source .venv/bin/activate`
    - Windows: `source .venv\Scripts\activate`
- Run the server: `uv run main.py`
- Deactivate the venv when done: `deactivate`

### Frontend Setup
- Install [Node.js](https://nodejs.org/en/download) to get npm
- `cd frontend`
- Install all dependencies: `npm install`
- Run the frontend: `npm run dev`
