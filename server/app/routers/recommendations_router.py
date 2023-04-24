import random

from fastapi import APIRouter

from app.types.shared_types import PagedRequest, GamesResponse, GameRatingSimple, Game
from app.utils.get_paged_games import get_paged_games
from app.utils.load_games_from_json import load_games_from_json
from app.utils.relative_path_from_file import relative_path_from_file
from app.utils.get_latent_factors_recommendations import get_LF_recommendations

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)

games_ordered_by_rank = load_games_from_json(relative_path_from_file(__file__, "../db/gamesOrderedByRank.json"))
games_ordered_by_name = load_games_from_json(relative_path_from_file(__file__, "../db/gamesOrderedByName.json"))
games_ordered_by_number_of_ratings = load_games_from_json(
    relative_path_from_file(__file__, "../db/gamesOrderedByNumberOfRatings.json"))


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

    shuffled_games = random.sample(games_ordered_by_name, len(games_ordered_by_name))
    return get_paged_games(shuffled_games, offset, limit)


@router.post("/latent-factors")
def latent_factors_recommendations(request: PersonalizedRecommendationsRequest) -> GamesResponse:
    ratings = request.ratings
    offset = request.offset
    limit = request.limit

    games_dict = { game['id'] : game for game in games_ordered_by_name }

    recommended_games_ids = get_LF_recommendations(ratings)
    recommended_games_sorted = [games_dict[game_id] for game_id in recommended_games_ids]

    return get_paged_games(recommended_games_sorted, offset, limit)