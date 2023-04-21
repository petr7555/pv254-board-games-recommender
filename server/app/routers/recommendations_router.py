import json

from fastapi import APIRouter
from pydantic import BaseModel

from app.types.shared_types import PagedRequest, GamesResponse, GameRatingSimple
from app.utils.relative_path_from_file import relative_path_from_file

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)


# TODO
@router.post("/top-rated")
def get_recommendations_top_rated(request: PagedRequest) -> GamesResponse:
    offset = request.offset
    limit = request.limit

    with open(relative_path_from_file(__file__, "../db/bestGamesByRank.json")) as f:
        games = json.load(f)
        paged_games = games[offset:offset + limit]

        return {
            "games": paged_games,
            "totalNumberOfGames": len(games),
        }


@router.post("/most-rated")
def get_recommendations_most_rated(request: PagedRequest) -> GamesResponse:
    # TODO
    offset = request.offset
    limit = request.limit

    with open(relative_path_from_file(__file__, "../db/bestGamesByRank.json")) as f:
        games = json.load(f)
        paged_games = games[offset:offset + limit]

        return {
            "games": paged_games,
            "totalNumberOfGames": len(games),
        }


@router.post("/random")
def get_recommendations_random(request: PagedRequest) -> GamesResponse:
    # TODO
    offset = request.offset
    limit = request.limit

    with open(relative_path_from_file(__file__, "../db/bestGamesByRank.json")) as f:
        games = json.load(f)
        paged_games = games[offset:offset + limit]

        return {
            "games": paged_games,
            "totalNumberOfGames": len(games),
        }


class PersonalizedRecommendationsRequest(PagedRequest):
    ratings: list[GameRatingSimple]


@router.post("/personalized")
def personalized_recommendations(request: PersonalizedRecommendationsRequest) -> GamesResponse:
    # TODO
    ratings = request.ratings
    offset = request.offset
    limit = request.limit

    with open(relative_path_from_file(__file__, "../db/bestGamesByRank.json")) as f:
        games = json.load(f)
        paged_games = games[offset:offset + limit]

        return {
            "games": paged_games,
            "totalNumberOfGames": len(games),
        }
