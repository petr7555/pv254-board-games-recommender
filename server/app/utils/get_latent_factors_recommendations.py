import numpy as np
import pandas as pd
from numpy import linalg

from app.utils.load_latent_factors_matrices import load_user_factors, load_item_factors


def rating_prediction(user_factors, item_factors):
    return np.dot(user_factors, item_factors.T)


def predict_ratings(user_factors, items_factors):    
    predicted_ratings = []

    for _, item_factors in items_factors.iterrows():
        predicted_ratings.append(rating_prediction(user_factors, item_factors))
    
    return pd.DataFrame({'predicted_rating': predicted_ratings}, index=items_factors.index)


def get_LF_recommendations(ratings, user_id=None):

    # would be better to store id in local storage? (but since we don't update matrix, it doesn't matter?)
    if user_id is None:
        user_id = "pv254_random_user"
        # user_id = "Stirlingmoomoo"  # for k=5 should respond with IDs: [137841, 293671, 66218, 13440, 2103]

    users_factors = load_user_factors()
    items_factors = load_item_factors()
    
    k_latent_factors = get_k_latent_factors(users_factors)

    is_new_user = user_id not in users_factors.index
    user_factors = get_new_user_factors(ratings, k_latent_factors, items_factors) if is_new_user else users_factors.loc[user_id]

    predicted_ratings = predict_ratings(user_factors, items_factors)
    return predicted_ratings.sort_values('predicted_rating', ascending = False).index.array


# split array (ratings) into groups with "k" items + loop to start to include all elements if necessary
def split(arr, k):
    n = len(arr)
    chunks = len(arr) // k
    res = [arr[i*k : (i+1)*k] for i in range(chunks)]
    remainder = n % k
    if remainder != 0:
        new_chunk = arr[-remainder:] + arr[:k-remainder]
        res.append(new_chunk)
    return res


def get_new_user_factors(ratings, k, items_factors):
    results = []

    # in case user ratings contain a game that is not present in the items_factors matrix
    # (shouldn't happen, but just in case there is a discrepancy between games, or user/FE sends a game with invalid id)
    filtered_ratings = list(filter(lambda x: x.gameId in items_factors.index, ratings))

    for group in split(filtered_ratings, k):
        coeffs = []
        values = []
        for rating in group:
            item_factors = items_factors.loc[rating.gameId, :].values
            coeffs.append(item_factors)
            values.append(rating.value)

        # solve a system of linear equations for "k" ratings to get "k" user factors:
        # > single equation: user_factors * item_factors^T = rating,
        #   solve for user_factors (u1, u2, u3) with given item_factors and rating
        # > if somehow coeffs matrix was to be singular, i.e. doesn't have one solution, skip
        if linalg.det(coeffs) != 0:
            equation_system_result = linalg.solve(np.array(coeffs), np.array(values))
            results.append(equation_system_result)

    # average over all solutions to get an approximation of the user factors,
    # since we can only use "k_latent_factors" ratings to solve for user factors
    return np.average(results, axis=0)


def get_k_latent_factors(factors_matrix):
    return len(factors_matrix.columns)