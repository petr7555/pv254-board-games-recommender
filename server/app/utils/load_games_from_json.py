import json

from app.types.shared_types import Game


def load_games_from_json(file_path: str) -> list[Game]:
    with open(file_path) as f:
        return json.load(f)
