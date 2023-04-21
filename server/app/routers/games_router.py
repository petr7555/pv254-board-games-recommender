from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.types.shared_types import PagedRequest, GamesResponse
from app.utils.get_games_by_name import get_games_by_name

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


class GamesSearchRequest(BaseModel):
    searchTerm: str
    offset: int
    limit: int


@router.post("/")
def get_games_by_name_route(request: GamesSearchRequest) -> GamesResponse:
    search_term = request.searchTerm
    offset = request.offset
    limit = request.limit

    # TODO refactor
    all_matching_games = get_games_by_name(search_term)
    paged_games = all_matching_games[offset:offset + limit]

    return {
        "games": paged_games,
        "totalNumberOfGames": len(all_matching_games),
    }
