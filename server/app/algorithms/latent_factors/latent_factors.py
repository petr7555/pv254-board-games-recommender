import numpy as np
import pandas as pd
from numpy import linalg


def rating_prediction(user_factors, item_factors):
    return np.dot(user_factors, item_factors.T)


def predict_ratings(user_factors, items_factors):
    predicted_ratings = []

    for _, item_factors in items_factors.iterrows():
        predicted_ratings.append(rating_prediction(user_factors, item_factors))

    return pd.DataFrame({"predicted_rating": predicted_ratings}, index=items_factors.index)


def get_latent_factors_recommendations(ratings, items_factors, user_id=None):
    k_latent_factors = get_k_latent_factors(items_factors)

    # since we currently only support new users' predictions, we can avoid loading users factors for no reason
    user_factors = []
    if user_id is not None:  # and user_id in users_factors.index:
        # user_factors = users_factors.loc[user_id]
        pass
    else:
        user_factors = get_new_user_factors(ratings, k_latent_factors, items_factors)

    predicted_ratings = predict_ratings(user_factors, items_factors)
    return predicted_ratings.sort_values("predicted_rating", ascending=False).index.array


# split array (ratings) into groups with "k" items + loop to start to include all elements if necessary
def split(arr, k):
    n = len(arr)
    chunks = len(arr) // k
    res = [arr[i * k : (i + 1) * k] for i in range(chunks)]
    remainder = n % k
    if remainder != 0:
        new_chunk = arr[-remainder:] + arr[: k - remainder]
        res.append(new_chunk)
    return res


# https://en.wikipedia.org/wiki/Overdetermined_system#Approximate_solutions
# > QR factorization not used, only least squares
def get_new_user_factors(ratings, k, items_factors):
    try:
        factors = get_user_factors_LSTSQ(ratings, items_factors)
        return factors
    except linalg.LinAlgError:
        return get_user_factors_EQAVG(ratings, k, items_factors)


# average of solutions from systems of linear equations
def get_user_factors_EQAVG(ratings, k, items_factors):
    results = []

    # in case user ratings contain a game that is not present in the items_factors matrix
    # (shouldn't happen, but just in case there is a discrepancy between games, or user/FE sends a game with invalid id)
    filtered_ratings = list(filter(lambda x: x.gameId in items_factors.index, ratings))

    for group in split(filtered_ratings, k):
        coeffs, values = get_X_y(group, items_factors)

        # solve a system of linear equations for "k" ratings to get "k" user factors:
        # > single equation: user_factors * item_factors^T = rating,
        #   solve for user_factors (u1, u2, u3) with given item_factors and rating
        # > if somehow coeffs matrix was to be singular, i.e. doesn't have one solution, skip
        if linalg.det(coeffs) != 0:
            equation_system_result = linalg.solve(coeffs, values)
            results.append(equation_system_result)

    # average over all solutions to get an approximation of the user factors,
    # since we can only use "k_latent_factors" ratings to solve for user factors
    return np.average(results, axis=0)


def get_k_latent_factors(factors_matrix):
    return len(factors_matrix.columns)


def get_user_factors_LSTSQ(ratings, items_factors):
    x, y = get_X_y(ratings, items_factors)
    return linalg.lstsq(x, y, rcond=None)[0]


def get_X_y(ratings, items_factors):
    coeffs = []
    values = []
    for rating in ratings:
        item_factors = items_factors.loc[rating.gameId, :].values
        coeffs.append(item_factors)
        values.append(rating.value)
    return [coeffs, values]
