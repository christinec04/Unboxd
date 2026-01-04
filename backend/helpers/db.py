from sqlalchemy import Engine, Row, create_engine, insert, text, Table, Column, Integer, Float, String, and_ , Index, ForeignKey, DateTime, select, Connection
from sqlalchemy.orm import Mapped, defer, mapped_column, Session
from typing import Sequence, Iterable
from heapq import nlargest
import os
import numpy as np

if os.getcwd().endswith("helpers"):
    from paths import Path
    from init_dataset import read_csvs_to_df
    from preprocessed_movie_model import Base, PreprocessedMovie
else:
    from helpers.paths import Path
    from helpers.init_dataset import read_csvs_to_df
    from helpers.preprocessed_movie_model import Base, PreprocessedMovie
        

class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    imdb_id: Mapped[str | None]
    poster_url: Mapped[str | None]
    runtime_seconds: Mapped[int | None]
    certificate_rating: Mapped[str | None]
    genres: Mapped[str]
    spoken_languages: Mapped[str]
    plot: Mapped[str | None]
    keywords: Mapped[str]
    directors: Mapped[str]
    writers: Mapped[str]
    actors: Mapped[str]
    companies: Mapped[str]


class Recommendation(Base):
    __tablename__ = "recommendation"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    expiration_date = mapped_column(DateTime, nullable=False)
    movie_id_1 = mapped_column(ForeignKey("movie.id"), nullable=False)
    movie_id_2 = mapped_column(ForeignKey("movie.id"), nullable=False)
    movie_id_3 = mapped_column(ForeignKey("movie.id"), nullable=False)
    movie_id_4 = mapped_column(ForeignKey("movie.id"), nullable=False)
    movie_id_5 = mapped_column(ForeignKey("movie.id"), nullable=False)
    movie_id_6 = mapped_column(ForeignKey("movie.id"), nullable=False)
    movie_id_7 = mapped_column(ForeignKey("movie.id"), nullable=False)
    movie_id_8 = mapped_column(ForeignKey("movie.id"), nullable=False)
    movie_id_9 = mapped_column(ForeignKey("movie.id"), nullable=False)
    movie_id_10 = mapped_column(ForeignKey("movie.id"), nullable=False)
    

class Trailer(Base):
    __tablename__ = "trailer"

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id = mapped_column(ForeignKey("movie.id"), nullable=False)
    trailer_id: Mapped[int]
    

def get_engine(echo: bool = False) -> Engine:
    return create_engine("sqlite+pysqlite:///" + Path.DATABASE, echo=echo)


def init_db():
    # Reset the db 
    if os.path.exists(Path.DATABASE):
        os.remove(Path.DATABASE)

    engine = get_engine(echo=True)

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        session.execute(text("PRAGMA journal_mode = WAL"))

        # session.execute(text("PRAGMA synchronous = normal"))
        # session.execute(text("PRAGMA temp_store = memory"))
        # session.execute(text("PRAGMA mmap_size = 30000000000"))
        # session.execute(text("PRAGMA journal_size_limit = 6144000"))
        # session.execute(text("PRAGMA page_size = 32768"))

        movies = read_csvs_to_df(Path.MOVIES_FOLDER)
        preprocessed_movies = read_csvs_to_df(Path.REDUCED_PREPROCESSED_MOVIES_FOLDER)

        # Two `original_title` values disappear into the abyss, so the rows 
        # they belonged to need to be dropped to adhere to the table schemas
        movies = movies.dropna(subset=["original_title"])
        preprocessed_movies = preprocessed_movies.dropna(subset=["original_title"])

        # Remove columns that exist in preprocessed_movies
        movies = movies.drop(columns=["original_title", "release_year"])

        session.execute(
                insert(Movie),
                [row._asdict() for row in movies.itertuples(index=False)]
                )
        session.execute(
                insert(PreprocessedMovie),
                [row._asdict() for row in preprocessed_movies.itertuples(index=False)]
                )

        preprocessed_movie_index = Index(
                "ix_original_title_release_year", 
                PreprocessedMovie.original_title, 
                PreprocessedMovie.release_year, 
                unique=True
                )
        preprocessed_movie_index.create(engine)
  
        # session.execute(text("PRAGMA vacuum"))
        # session.execute(text("PRAGMA optimize"))
                    
        session.commit()


"""
    - `expiration_date` set with timer proportional to the number of the user's rating
        - most pages of reviews i've seen is 79
        - on the next post /usernames/, if the timer expired:
            - update the recs, timer, and `UPDATE` the table
    - still store status in memory
        - delete from dict when done with system
        - for /status/ check in status first
            - if not there, check recommendations to see if shi already done
                - add new status: shi expired, you can run yo pockets again or just get the outdated recs
"""


test = [
        {"original_title": "Five Nights at Freddy's 2", "release_year": 2025, "rating": 3.0},
        {"original_title": "Avatar: Fire and Ash", "release_year": 2025, "rating": 3.0},
        {"original_title": "Marty Supreme", "release_year": 2025, "rating": 4.0},
        {"original_title": "Chainsaw Man – The Movie: Reze Arc", "release_year": 2025, "rating": 5.0},
        {"original_title": "The Conjuring: Last Rites", "release_year": 2025, "rating": 2.0},
        {"original_title": "Demon Slayer: Kimetsu no Yaiba Infinity Castle", "release_year": 2025, "rating": None},
        {"original_title": "The Fragrant Flower Blooms with Dignity", "release_year": 2025, "rating": 4.0},
        {"original_title": "Takopi's Original Sin", "release_year": 2025, "rating": 3.0},
        {"original_title": "KPop Demon Hunters", "release_year": 2025, "rating": 3.0},
        {"original_title": "F1", "release_year": 2025, "rating": None}
        ]


class create_temp_user_table:
    def __init__(
            self, 
            engine: Engine, 
            con: Connection, 
            username: str, 
            data: list[dict[str, str | int | float | None]]
                 ):
        self.engine = engine
        self.user_table = Table(
                username,
                Base.metadata,
                Column("id", Integer, primary_key=True),
                Column("original_title", String),
                Column("release_year", Integer),
                Column("rating", Float, nullable=True),
                prefixes=["TEMPORARY"]
                )
        self.data = data
        self.user_table.create(self.engine)
        con.execute(insert(self.user_table), data)
        con.commit()

    def __enter__(self) -> Table:
        return self.user_table

    def __exit__(self, exception_type, exception_val, exception_traceback):
        self.user_table.drop(self.engine)


def rated_preprocessed_movies(con: Connection, user_table: Table) -> Sequence[Row[tuple]]:
    """
    Args:
    `con`: sqlalchemy `Engine` `Connection`
    `user_table`: a sqlalchemy `Table` created using `create_temp_user_table`

    Returns:
    `(rating, id, feature_1, ..., feature_n)` 
    where `id` is an `int` < 700,000, and `rating` and `feature_x` are `float`s,
    for each user rated movie that could be matched with a movie from `preprocessed_movie`
    """
    cur = con.execute(
            select(user_table.c.rating, PreprocessedMovie)
            .join_from(
                user_table, 
                PreprocessedMovie, 
                and_(
                    user_table.c.original_title == PreprocessedMovie.original_title,
                    user_table.c.release_year == PreprocessedMovie.release_year
                    )
                )
            # Exclude movies that don't have ratings (i.e. were only liked on Letterboxd)
            .where(user_table.c.rating != None)
            # `PreprocessedMovie.id` is sufficient for matching with `movie`, so these aren't necessary
            .options(
                defer(PreprocessedMovie.original_title), 
                defer(PreprocessedMovie.release_year)
                )
            )
    return cur.fetchall() 


# def find_representative_movie(movies: np.ndarray, weights: list[float]) -> int:

def rated_preprocessed_to_np(rows: Sequence[Row[tuple]]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Args:
    `rows`: (`rating`, `id`, `feature_1`, ..., `feature_n`), where `id` is an `int` < 700,000,
    and `rating` and `feature_x` are floats

    Returns:
    `(
    [[feature_1_1, ..., feature_1_n], ..., [feature_m_1, ..., feature_m_n]],
    [id_1, ..., id_m],
    [rating_1, ..., rating_m]
    )`
    """

    m = len(rows)
    assert m != 0

    id_col = 0
    rating_col = 1
    features_start_col = 2
    assert len(rows[0]) > features_start_col

    movie_features = np.empty((m,), dtype=np.ndarray)
    ids = np.empty((m,), dtype=np.int32)
    ratings = np.empty((m,))

    for i, row in enumerate(rows):
        movie_features[i] = np.array(row[features_start_col:], dtype=np.float64)
        ids[i] = row[id_col]
        ratings[i] = row[rating_col]

    return (movie_features, ids, ratings)


def unwatched_preprocessed_movies(con: Connection, user_table: Table) -> Iterable[Row[tuple]]:
    """
    Args:
    `con`: sqlalchemy engine `Connection`
    `user_table`: a sqlalchemy `Table` created using `create_temp_user_table`

    Returns:
    `(id, feature_1, ..., feature_n)` where `id` is an `int` < 700,000, 
    and `feature_x` are `float`s, for each movie from `preprocessed_movie` not watched 
    (i.e liked or rated) by the user
    """
    cur = con.execute(
            select(PreprocessedMovie)
            .outerjoin_from(
                PreprocessedMovie, 
                user_table, 
                and_(
                    user_table.c.original_title == PreprocessedMovie.original_title,
                    user_table.c.release_year == PreprocessedMovie.release_year
                    )
                )
            # This holds for movies that could not be matched
            .where(user_table.c.original_title == None)
            # `PreprocessedMovie.id` is sufficient for matching with `movie`, so these aren't necessary
            .options(
                defer(PreprocessedMovie.original_title), 
                defer(PreprocessedMovie.release_year)
                )
            )
    for row in cur:
        yield row
    cur.close()

# def select_recommendations():

def select_representative(username: str) -> None:
    # using Connection over Session to immediately unpack values
    with engine.connect() as con:
        with create_temp_user_table(engine, con, username, test) as user_table:
            print(rated_preprocessed_movies(con, user_table))

if __name__ == "__main__":
    engine = get_engine(echo=True)
    for i in range(10):
        select_representative(f'username')
    # init_db()
else:
    engine = get_engine(echo=True)

