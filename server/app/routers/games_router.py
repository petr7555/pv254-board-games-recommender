from fastapi import APIRouter

from app.types.shared_types import PagedRequest, GamesResponse
from app.utils.get_paged_games import get_paged_games
from app.utils.load_games_from_json import load_games_list_from_json
from app.utils.relative_path_from_file import relative_path_from_file

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


class GamesSearchRequest(PagedRequest):
    searchTerm: str


games = load_games_list_from_json(
    relative_path_from_file(__file__, "../db/gamesOrderedByName.json")
)


@router.post("/")
def get_games_by_name_route(request: GamesSearchRequest) -> GamesResponse:
    search_term = request.searchTerm
    offset = request.offset
    limit = request.limit

    filtered_games = [game for game in games if search_term.lower() in game["name"].lower()]

    return get_paged_games(filtered_games, offset, limit)
