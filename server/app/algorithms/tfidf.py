import json
import os

import numpy as np

from app.types.shared_types import Game, GameRatingSimple
from app.utils.relative_path_from_file import relative_path_from_file

db_dir = relative_path_from_file(__file__, "../db")
similarity_matrix_path = os.path.join(db_dir, "similarity_matrix.npy")
map_from_bgg_id_to_index_path = os.path.join(db_dir, "map_from_bgg_id_to_index.json")


def get_tfidf_recommendations(
    games: dict[str, Game], ratings: list[GameRatingSimple]
) -> list[Game]:
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
    ids_without_rated_games = [
        bgg_id for bgg_id in unique_bgg_ids_of_similar_games if bgg_id not in rated_ids
    ]

    sorted_games = [games[str(bgg_id)] for bgg_id in ids_without_rated_games]
    return sorted_games
