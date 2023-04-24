import numpy as np
import pandas as pd

from app.utils.load_latent_factors_matrices import load_user_factors, load_item_factors


# TODO: create constants file 
k_latent_factors = 3
n_epochs = 20
learning_rate = 0.05 # 0.005
_lambda = 0.2 # 0.02


def rating_prediction(user_factors, item_factors):
    return np.dot(user_factors, item_factors.T)


def predict_ratings(user_factors, items_factors):    
    predicted_ratings = []

    for _, item_factors in items_factors.iterrows():
        predicted_ratings.append(rating_prediction(user_factors, item_factors))
    
    return pd.DataFrame({'predicted_rating': predicted_ratings}, index=items_factors.index)


def get_k_recommendations(k, ratings, user_id=None):

    # would be better to store id in local storage? (but since we don't update matrix, it doesn't matter?)
    if user_id is None:
        user_id = "pv254_random_user"
        # user_id = "Stirlingmoomoo"  # for k=5 should respond with IDs: [137841, 293671, 66218, 13440, 2103]

    users_factors = load_user_factors()
    items_factors = load_item_factors()

    print(f'Q length: {len(items_factors)}')

    if user_id not in users_factors.index:
        users_factors.loc[user_id, :] = 3 * np.random.rand(1, k_latent_factors)
        update_latent_factors(users_factors, items_factors, user_id, ratings) 

    user_factors = users_factors.loc[user_id]
    predicted_ratings = predict_ratings(user_factors, items_factors)
    return predicted_ratings.sort_values('predicted_rating', ascending = False).head(k).index.array


def update_latent_factors(P, Q, user_id, ratings):
    for epoch in range(n_epochs):
        for user_rating in ratings:

            item_id = user_rating.gameId
            
            if item_id not in Q.index:
                Q.loc[item_id, :] = 3 * np.random.rand(1, k_latent_factors)

            user_factors = P.loc[user_id, :].values
            item_factors = Q.loc[item_id, :].values

            actual_rating = user_rating.value
            predicted_rating = rating_prediction(user_factors, item_factors)
            error = actual_rating - predicted_rating
            
            # extract into 'update' method / try adjusting the update method
            P_gradient = learning_rate * (error * item_factors - _lambda * user_factors)
            Q_gradient = learning_rate * (error * user_factors - _lambda * item_factors)

            P.loc[user_id, :] += P_gradient
            Q.loc[item_id, :] += Q_gradient
            