import json
import os
import time

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.types.shared_types import Game, GameRatingSimple
from app.utils.relative_path_from_file import relative_path_from_file

data_dir = relative_path_from_file(__file__, "../../data/cleaned")
db_dir = relative_path_from_file(__file__, "../db")
similarity_matrix_path = os.path.join(db_dir, "similarity_matrix.npy")
map_from_bgg_id_to_index_path = os.path.join(db_dir, "map_from_bgg_id_to_index.json")


def get_column_name(column: str) -> str:
    return column.replace("/", "_").replace(" ", "_")


def get_textual_columns_representation(row: pd.Series, textual_columns: list[str]) -> str:
    return " ".join([row[column] for column in textual_columns])


def get_value_columns_representation(row: pd.Series, value_columns: list[str], weight: int) -> str:
    return " ".join(
        [f"{get_column_name(column)}_{row[column]} " * weight for column in value_columns]
    )


def get_binary_columns_representation(row: pd.Series, categorical_columns: list[str], weight: int) -> str:
    return " ".join(
        [
            f"{get_column_name(column)}_1 " * weight
            for column in categorical_columns
            if row[column] == 1
        ]
    )


def create_similarity_matrix() -> None:
    games = pd.read_csv(os.path.join(data_dir, "games.csv"))
    games["Description"] = games["Description"].fillna("")

    mechanics = pd.read_csv(os.path.join(data_dir, "mechanics.csv"))
    mechanics_columns = mechanics.columns[1:].tolist()
    subcategories = pd.read_csv(os.path.join(data_dir, "subcategories.csv"))
    subcategories_columns = subcategories.columns[1:].tolist()
    themes = pd.read_csv(os.path.join(data_dir, "themes.csv"))
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


def get_tfidf_recommendations(games: dict[str, Game], ratings: list[GameRatingSimple]) -> list[Game]:
    similarity_matrix = np.load(similarity_matrix_path, mmap_mode="r")

    with open(map_from_bgg_id_to_index_path, "r") as f:
        map_from_bgg_id_to_index = {int(bgg_id): index for bgg_id, index in json.load(f).items()}
    map_from_index_to_bgg_id = {index: bgg_id for bgg_id, index in map_from_bgg_id_to_index.items()}

    rated_ids = [rating.gameId for rating in ratings]
    indices_of_games_rated_by_user = [map_from_bgg_id_to_index[bgg_id] for bgg_id in rated_ids]

    ratings_values = np.array([rating.value for rating in ratings]).reshape(-1, 1)

    similarities = similarity_matrix[indices_of_games_rated_by_user]
    weighted_similarities = similarities * 0.2 * (ratings_values - 5)

    similarities_flattened = weighted_similarities.flatten()
    sorted_indices_of_similarities_from_most_similar = np.argsort(similarities_flattened)[::-1]

    num_games = len(games)
    bgg_ids_of_similar_games = [
        map_from_index_to_bgg_id[index % num_games]
        for index in sorted_indices_of_similarities_from_most_similar
    ]
    unique_bgg_ids_of_similar_games = list(dict.fromkeys(bgg_ids_of_similar_games))
    ids_without_rated_games = [bgg_id for bgg_id in unique_bgg_ids_of_similar_games if bgg_id not in rated_ids]

    sorted_games = [games[str(bgg_id)] for bgg_id in ids_without_rated_games]
    return sorted_games


# Run this to generate similarity matrix
# create_similarity_matrix()
