import os
import sys
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD

if os.getcwd().endswith("helpers"):
    from paths import Path
    from init_dataset import read_csvs_to_df, write_df_to_csvs 
    from preprocess_features import preprocess_movie_dataset
else:
    from helpers.paths import Path
    from helpers.init_dataset import read_csvs_to_df, write_df_to_csvs 
    from helpers.preprocess_features import preprocess_movie_dataset


def reduce_features(df: pd.DataFrame, model_path: str, n_components: int | None) -> pd.DataFrame:
    print("Performing feature reduction...")
    saved_cols = ["original_title", "release_year"]
    saved_col_values = df[saved_cols].values
    df.drop(columns=saved_cols, inplace=True)

    plot_results = False
    if n_components is None:
        n_components = len(df)
        plot_results = True

    warnings.filterwarnings("ignore")
    feature_reducer = TruncatedSVD(n_components)
    reduced_data = feature_reducer.fit_transform(df)

    if plot_results:
        plot_explained_variance_ratios(feature_reducer)

    columns = [f"c_{i+1}" for i in range(n_components)]
    create_db_model(model_path, columns)
    df = pd.DataFrame(reduced_data, columns=columns)
    df[saved_cols] = saved_col_values
    return df

def create_db_model(model_path: str, columns: list[str]) -> None:
    with open(model_path, "w") as file:
        output = (
                "from sqlalchemy import ForeignKey\n"
                "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column\n"
                "\n"
                "class Base(DeclarativeBase):\n"
                "\tpass\n"
                "\n"
                "class PreprocessedMovie(Base):\n"
                "\t__tablename__ = \"preprocessed_movie\"\n"
                "\n"
                "\tid = mapped_column(ForeignKey(\"movie.id\"), primary_key=True, autoincrement=True)\n"
                "\toriginal_title: Mapped[str]\n"
                "\trelease_year: Mapped[int]\n"
                )
        for col in columns:
            output += f"\t{col}: Mapped[float]\n"
        output += "\n"
        file.write(output)


# def generate_db_table(model_path: str, columns: list[str]) -> None:
#     with open(model_path, "w") as file:
#         output = (
#                 "from sqlalchemy import Table, Column, ForeignKey, String, Integer, Float\n"
#                 "from sqlalchemy.orm import DeclarativeBase\n"
#                 "\n"
#                 "class Base(DeclarativeBase):\n"
#                 "\tpass\n"
#                 "\n"
#                 "preprocessed_movie_table = Table(\n"
#                 "\t\t\"preprocessed_movie\",\n"
#                 "\t\tBase.metadata,\n"
#                 "\t\tColumn(\"id\", ForeignKey(\"movie.id\"), primary_key=True, autoincrement=\"ignore_fk\"),\n"
#                 "\t\tColumn(\"original_title\", String),\n"
#                 "\t\tColumn(\"release_year\", Integer),\n"
#                 )
#         for col in columns:
#             output += f"\t\tColumn(\"{col}\", Float),\n"
#         output += (
#                 "\t\t)\n"
#                 "\n"
#                 )
#         file.write(output)


def plot_explained_variance_ratios(fit_transformed_feature_reducer: TruncatedSVD) -> None:
    print("Plotting results...")
    explained_variance_ratios = fit_transformed_feature_reducer.explained_variance_ratio_
    total = 0
    cumumlative_explained_variance_ratios = []
    for ratio in explained_variance_ratios:
        cumumlative_explained_variance_ratios.append(total)
        total += ratio
    num_components = [i + 1 for i in range(len(cumumlative_explained_variance_ratios))]
    plt.scatter(num_components, cumumlative_explained_variance_ratios)
    plt.ylabel("cumulative explained variance ratios")
    plt.xlabel("n components")
    plt.show()


def main():
    if "preprocess" in sys.argv:
        df = read_csvs_to_df(Path.MOVIES_FOLDER)
        df = preprocess_movie_dataset(df)
    else:
        df = read_csvs_to_df(Path.PREPROCESSED_MOVIES_FOLDER)

    if "save" in sys.argv:
        write_df_to_csvs(df, 7500, Path.PREPROCESSED_MOVIES_FOLDER)

    if "plot" in sys.argv:
        n_components = None
    else:
        n_components = 90
    df = reduce_features(df, Path.PREPROCESSED_MOVIE_MODEL, n_components) 
    write_df_to_csvs(df, 7500, Path.REDUCED_PREPROCESSED_MOVIES_FOLDER)
    

if __name__ == "__main__":
    main()
 
