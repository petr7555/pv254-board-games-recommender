from fastapi import APIRouter

from app.types.shared_types import GamesResponse

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)


@router.post("/top-rated")
def get_recommendations() -> GamesResponse:
    # TODO
    return {
        "games": [],
        "totalNumberOfGames": 0,
    }

@router.post("/most-rated")
def get_recommendations() -> GamesResponse:
    # TODO
    return {
        "games": [],
        "totalNumberOfGames": 0,
    }

@router.post("/random")
def get_recommendations() -> GamesResponse:
    # TODO
    return {
        "games": [],
        "totalNumberOfGames": 0,
    }
