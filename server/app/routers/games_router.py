from fastapi import APIRouter

from app.types.shared_types import PagedRequest, GamesResponse

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


class GamesSearchRequest(PagedRequest):
    searchTerm: str


@router.post("/")
def get_games_by_name(request: GamesSearchRequest) -> GamesResponse:
    # TODO
    return {
        "games": [],
        "totalNumberOfGames": 0,
    }
