from app.types.shared_types import Game, GamesResponse


def get_paged_games(games: list[Game], offset: int, limit: int) -> GamesResponse:
    return {
        "games": games[offset:offset + limit],
        "totalNumberOfGames": len(games),
    }
