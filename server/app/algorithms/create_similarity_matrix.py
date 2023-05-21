import json
import os
import time

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.relative_path_from_file import relative_path_from_file

data_dir = relative_path_from_file(__file__, "../../data/cleaned")
db_dir = relative_path_from_file(__file__, "../db")
similarity_matrix_path = os.path.join(db_dir, "similarity_matrix.npy")
map_from_bgg_id_to_index_path = os.path.join(db_dir, "map_from_bgg_id_to_index.json")

games_df = pd.read_csv(os.path.join(data_dir, "games.csv"))
mechanics_df = pd.read_csv(os.path.join(data_dir, "mechanics.csv"))
subcategories_df = pd.read_csv(os.path.join(data_dir, "subcategories.csv"))
themes_df = pd.read_csv(os.path.join(data_dir, "themes.csv"))


def get_column_name(column: str) -> str:
    return column.replace("/", "_").replace(" ", "_")


def get_textual_columns_representation(row: pd.Series, textual_columns: list[str]) -> str:
    return " ".join([row[column] for column in textual_columns])


def get_value_columns_representation(row: pd.Series, value_columns: list[str], weight: int) -> str:
    return " ".join(
        [f"{get_column_name(column)}_{row[column]} " * weight for column in value_columns]
    )


def get_binary_columns_representation(
    row: pd.Series, categorical_columns: list[str], weight: int
) -> str:
    return " ".join(
        [
            f"{get_column_name(column)}_1 " * weight
            for column in categorical_columns
            if row[column] == 1
        ]
    )


def create_similarity_matrix(
    games: pd.DataFrame, mechanics: pd.DataFrame, subcategories: pd.DataFrame, themes: pd.DataFrame
) -> None:
    games["Description"] = games["Description"].fillna("")

    mechanics_columns = mechanics.columns[1:].tolist()
    subcategories_columns = subcategories.columns[1:].tolist()
    themes_columns = themes.columns[1:].tolist()

    merged_tables = (
        games.merge(mechanics, on="BGGId", how="left")
        .merge(subcategories, on="BGGId", how="left")
        .merge(themes, on="BGGId", how="left")
    )
    map_from_bgg_id_to_index = {
        bgg_id: index for index, bgg_id in enumerate(merged_tables["BGGId"])
    }
    merged_tables = merged_tables.set_index("BGGId")

    textual_columns = ["Name", "Description"]
    value_columns = [
        "YearPublished",
        "MinPlayers",
        "MaxPlayers",
        "BestPlayers",
        "MfgPlaytime",
        "ComMinPlaytime",
        "ComMaxPlaytime",
        "MfgAgeRec",
        "Kickstarted",
    ]
    binary_columns = (
        [
            "Cat:Thematic",
            "Cat:Strategy",
            "Cat:War",
            "Cat:Family",
            "Cat:CGS",
            "Cat:Abstract",
            "Cat:Party",
            "Cat:Childrens",
        ]
        + mechanics_columns
        + subcategories_columns
        + themes_columns
    )

    print("Computing string representation of games...")
    start_time = time.time()
    string_games = merged_tables.apply(
        lambda row: get_textual_columns_representation(row, textual_columns)
        + get_value_columns_representation(row, value_columns, weight=2)
        + get_binary_columns_representation(row, binary_columns, weight=2),
        axis=1,
    ).tolist()
    print(f"String representation of games computed in {time.time() - start_time:.1f} seconds")

    print("Computing tfidf matrix...")
    start_time = time.time()
    vectorizer = TfidfVectorizer(dtype=np.float32)
    tfidf_matrix = vectorizer.fit_transform(string_games)
    print(f"Tfidf matrix computed in {time.time() - start_time:.1f} seconds")

    print("Computing similarity matrix...")
    start_time = time.time()
    similarity_matrix = cosine_similarity(tfidf_matrix)
    print(f"Similarity matrix computed in {time.time() - start_time:.1f} seconds")

    print("Saving similarity matrix...")
    start_time = time.time()
    np.save(similarity_matrix_path, similarity_matrix)
    print(f"Similarity matrix saved in {time.time() - start_time:.1f} seconds")

    print("Saving map from BGGId to index...")
    with open(map_from_bgg_id_to_index_path, "w") as f:
        json.dump(map_from_bgg_id_to_index, f)
    print(f"Map from BGGId to index saved.")


def run() -> None:
    create_similarity_matrix(games_df, mechanics_df, subcategories_df, themes_df)


# Run this to generate similarity matrix
if __name__ == "__main__":
    run()
