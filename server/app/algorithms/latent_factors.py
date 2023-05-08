import numpy as np
import pandas as pd
from numpy import linalg

from app.types.shared_types import Game, GameRatingSimple


def predict_ratings(user_factors: np.ndarray, items_factors: pd.DataFrame) -> pd.Series:
    return user_factors @ items_factors.T


def get_x_y(ratings: list[GameRatingSimple], items_factors: pd.DataFrame) -> tuple[np.ndarray, list[int]]:
    game_ids = [rating.gameId for rating in ratings]
    coefficients = items_factors.loc[game_ids, :].values
    ratings_values = [rating.value for rating in ratings]
    return coefficients, ratings_values


def get_user_factors_least_squares(ratings: list[GameRatingSimple], items_factors: pd.DataFrame) -> np.ndarray:
    x, y = get_x_y(ratings, items_factors)
    return linalg.lstsq(x, y, rcond=None)[0]


def get_latent_factors_recommendations(games: dict[str, Game], ratings: list[GameRatingSimple],
                                       items_factors: pd.DataFrame) -> list[Game]:
    user_factors = get_user_factors_least_squares(ratings, items_factors)

    predicted_ratings = predict_ratings(user_factors, items_factors)
    sorted_games_ids = predicted_ratings.sort_values(ascending=False).index.tolist()
    recommended_games = [games[str(game_id)] for game_id in sorted_games_ids]
    return recommended_games
