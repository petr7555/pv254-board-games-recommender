import pandas as pd

from app.types.shared_types import Game
from app.utils.relative_path_from_file import relative_path_from_file


def get_games_by_name(search_term: str) -> list[Game]:
    games = pd.read_json(relative_path_from_file(__file__, "../db/gamesOrderedByName.json"))
    filtered_games = games[games["name"].str.contains(search_term, case=False)]
    return filtered_games.to_dict("records")
