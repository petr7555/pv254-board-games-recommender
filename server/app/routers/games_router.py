from fastapi import APIRouter

from app.types.shared_types import PagedRequest, GamesResponse
from app.utils.get_games_by_name import get_games_by_name
from app.utils.get_paged_games import get_paged_games

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


class GamesSearchRequest(PagedRequest):
    searchTerm: str


@router.post("/")
def get_games_by_name_route(request: GamesSearchRequest) -> GamesResponse:
    search_term = request.searchTerm
    offset = request.offset
    limit = request.limit

    all_matching_games = get_games_by_name(search_term)
    return get_paged_games(all_matching_games, offset, limit)
