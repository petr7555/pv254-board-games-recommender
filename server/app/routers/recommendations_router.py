import json
import random

from fastapi import APIRouter

from app.types.shared_types import PagedRequest, GamesResponse, GameRatingSimple
from app.utils.get_paged_games import get_paged_games
from app.utils.relative_path_from_file import relative_path_from_file

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)


@router.post("/top-rated")
def get_recommendations_top_rated(request: PagedRequest) -> GamesResponse:
    offset = request.offset
    limit = request.limit

    with open(relative_path_from_file(__file__, "../db/gamesOrderedByRank.json")) as f:
        games = json.load(f)
        return get_paged_games(games, offset, limit)


@router.post("/most-rated")
def get_recommendations_most_rated(request: PagedRequest) -> GamesResponse:
    offset = request.offset
    limit = request.limit

    with open(relative_path_from_file(__file__, "../db/gamesOrderedByNumberOfRatings.json")) as f:
        games = json.load(f)
        return get_paged_games(games, offset, limit)


@router.post("/random")
def get_recommendations_random(request: PagedRequest) -> GamesResponse:
    offset = request.offset
    limit = request.limit

    with open(relative_path_from_file(__file__, "../db/gamesOrderedByName.json")) as f:
        games = json.load(f)
        shuffled_games = random.sample(games, len(games))
        return get_paged_games(shuffled_games, offset, limit)


class PersonalizedRecommendationsRequest(PagedRequest):
    ratings: list[GameRatingSimple]


# TODO
@router.post("/personalized")
def personalized_recommendations(request: PersonalizedRecommendationsRequest) -> GamesResponse:
    ratings = request.ratings
    offset = request.offset
    limit = request.limit

    with open(relative_path_from_file(__file__, "../db/gamesOrderedByName.json")) as f:
        games = json.load(f)
        shuffled_games = random.sample(games, len(games))
        return get_paged_games(shuffled_games, offset, limit)
