import random
from app.utils.tfidf_related import tfidf, get_data, get_most_similar
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from fastapi import APIRouter

from app.types.shared_types import PagedRequest, GamesResponse, GameRatingSimple
from app.utils.get_paged_games import get_paged_games
from app.utils.load_games_from_json import load_games_from_json
from app.utils.relative_path_from_file import relative_path_from_file


router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)

games_ordered_by_rank = load_games_from_json(relative_path_from_file(__file__, "../db/gamesOrderedByRank.json"))
games_ordered_by_name = load_games_from_json(relative_path_from_file(__file__, "../db/gamesOrderedByName.json"))
games_ordered_by_number_of_ratings = load_games_from_json(
    relative_path_from_file(__file__, "../db/gamesOrderedByNumberOfRatings.json"))


cleaned_data_dir = relative_path_from_file(__file__, "../../data")
games = pd.read_csv(f'{cleaned_data_dir}/games_cleaned.csv')
similarity_scores = np.load("app/db/similarity_matrix.npy")


@router.post("/top-rated")
def get_recommendations_top_rated(request: PagedRequest) -> GamesResponse:
    offset = request.offset
    limit = request.limit

    return get_paged_games(games_ordered_by_rank, offset, limit)


@router.post("/most-rated")
def get_recommendations_most_rated(request: PagedRequest) -> GamesResponse:
    offset = request.offset
    limit = request.limit

    return get_paged_games(games_ordered_by_number_of_ratings, offset, limit)


@router.post("/random")
def get_recommendations_random(request: PagedRequest) -> GamesResponse:
    offset = request.offset
    limit = request.limit

    shuffled_games = random.sample(games_ordered_by_name, len(games_ordered_by_name))
    return get_paged_games(shuffled_games, offset, limit)


class PersonalizedRecommendationsRequest(PagedRequest):
    ratings: list[GameRatingSimple]

# TODO
@router.post("/personalized")
def personalized_recommendations(request: PersonalizedRecommendationsRequest) -> GamesResponse:
    ratings = request.ratings
    offset = request.offset
    limit = request.limit
    print(limit)
    # games, string_dict = get_data()

    # tfidf_matrix = tfidf(string_dict)
    # similarity_scores = cosine_similarity(tfidf_matrix)
    shuffled_games = get_most_similar(games, similarity_scores, ratings)
    return get_paged_games(shuffled_games, offset, limit)

# TODO
"""
@router.post("/personalized")
def personalized_recommendations(request: PersonalizedRecommendationsRequest) -> GamesResponse:
    ratings = request.ratings
    offset = request.offset
    limit = request.limit

    shuffled_games = random.sample(games_ordered_by_name, len(games_ordered_by_name))
    return get_paged_games(shuffled_games, offset, limit)
"""