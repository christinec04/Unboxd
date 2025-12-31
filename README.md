# Unboxd
A recommendation system for Letterboxd movies.\
You can download the recommended movies list and import it to your Letterboxd watchlist. See [here](https://letterboxd.com/about/importing-data/) for the Letterboxd guide on importing data.

[Protoype demo](https://www.linkedin.com/posts/christinechen04_just-wanted-to-share-what-dhruv-chavan-eric-activity-7409682403075522560-uDkS)

## Setup
\! For further development setup see `DEVELOPMENT.md`

### Backend 
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
