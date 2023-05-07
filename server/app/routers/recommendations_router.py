import random

from fastapi import APIRouter

from app.algorithms.latent_factors import get_latent_factors_recommendations
from app.algorithms.tfidf import get_tfidf_recommendations
from app.types.shared_types import PagedRequest, GamesResponse, GameRatingSimple
from app.utils.get_paged_games import get_paged_games
from app.utils.load_factors import load_factors
from app.utils.load_games_from_json import load_games_list_from_json, load_games_dict_from_json
from app.utils.relative_path_from_file import relative_path_from_file

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)

games_ordered_by_rank = load_games_list_from_json(
    relative_path_from_file(__file__, "../db/gamesOrderedByRank.json")
)
games_ordered_by_name = load_games_list_from_json(
    relative_path_from_file(__file__, "../db/gamesOrderedByName.json")
)
games_ordered_by_number_of_ratings = load_games_list_from_json(
    relative_path_from_file(__file__, "../db/gamesOrderedByNumberOfRatings.json")
)
games_by_id = load_games_dict_from_json(relative_path_from_file(__file__, "../db/gamesById.json"))

items_factors = load_factors(relative_path_from_file(__file__, "../db/item_factors.pkl"))


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


@router.post("/tfidf")
def get_recommendations_tfidf(request: PersonalizedRecommendationsRequest) -> GamesResponse:
    ratings = request.ratings
    offset = request.offset
    limit = request.limit

    games_ordered_by_cosine_similarity = get_tfidf_recommendations(games_by_id, ratings)
    return get_paged_games(games_ordered_by_cosine_similarity, offset, limit)


@router.post("/latent-factors")
def latent_factors_recommendations(request: PersonalizedRecommendationsRequest) -> GamesResponse:
    ratings = request.ratings
    offset = request.offset
    limit = request.limit

    recommended_games = get_latent_factors_recommendations(games_by_id, ratings, items_factors)
    return get_paged_games(recommended_games, offset, limit)
