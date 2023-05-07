import json
from typing import Any

from app.types.shared_types import Game


def load_games_from_json(file_path: str) -> Any:
    with open(file_path) as f:
        return json.load(f)


def load_games_list_from_json(file_path: str) -> list[Game]:
    return load_games_from_json(file_path)


def load_games_dict_from_json(file_path: str) -> dict[str, Game]:
    return load_games_from_json(file_path)
