import math
import os
import time

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from app.utils.relative_path_from_file import relative_path_from_file

data_dir = relative_path_from_file(__file__, "../../../data/cleaned")
user_ratings_path = os.path.join(data_dir, "user_ratings.csv")
users_factors_output_path = relative_path_from_file(__file__, "../../db/users_factors.pkl")
items_factors_output_path = relative_path_from_file(__file__, "../../db/items_factors.pkl")


def rmse(p: pd.DataFrame, q: pd.DataFrame, user_ratings: pd.DataFrame) -> float:
    user_ids: pd.Series = user_ratings["Username"]
    item_ids: pd.Series = user_ratings["BGGId"]

    users_factors: np.ndarray = p.loc[user_ids].values
    items_factors: np.ndarray = q.loc[item_ids].values

    actual_ratings: np.ndarray = user_ratings["Rating"].values
    predicted_ratings: np.ndarray = np.einsum("ij, ij->i", users_factors, items_factors)

    error: float = mean_squared_error(actual_ratings, predicted_ratings, squared=False)
    return error


def train_val_test_split(
    df: pd.DataFrame, stratify_col_name: str
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ratios = [0.8, 0.1, 0.1]
    assert sum(ratios) == 1

    train, val_test = train_test_split(
        df,
        train_size=ratios[0],
        test_size=ratios[1] + ratios[2],
        stratify=df[[stratify_col_name]],
        random_state=0,
    )

    val_size = ratios[1] / (ratios[1] + ratios[2])
    val, test = train_test_split(
        val_test,
        train_size=val_size,
        test_size=1 - val_size,
        stratify=val_test[[stratify_col_name]],
        random_state=0,
    )

    return train, val, test


def initialize_matrix(
    unique_elements: np.ndarray, col_prefix: str, k_latent_factors: int, upper_range: int
) -> pd.DataFrame:
    np.random.seed(0)

    matrix_data = upper_range * np.random.rand(len(unique_elements), k_latent_factors)
    matrix = pd.DataFrame(
        data=matrix_data,
        index=unique_elements,
        columns=[f"{col_prefix}_{i + 1}" for i in range(k_latent_factors)],
    )
    return matrix


def split_into_batches(df: pd.DataFrame, batch_size: int) -> list[pd.DataFrame]:
    batches = []
    num_batches = math.ceil(len(df) / batch_size)
    for i in range(num_batches):
        batches.append(df.iloc[i * batch_size : (i + 1) * batch_size])
    return batches


def should_stop(validation_errors: list[float], epoch_improvement_threshold: float) -> bool:
    if len(validation_errors) < 2:
        return False

    improvement_value = validation_errors[-2] - validation_errors[-1]
    error_increased = improvement_value < 0
    return error_increased or improvement_value < epoch_improvement_threshold


def fit(
    x_train: pd.DataFrame,
    x_val: pd.DataFrame,
    unique_users: np.ndarray,
    unique_items: np.ndarray,
    *,
    k_latent_factors: int,
    max_epochs: int,
    learning_rate: float,
    reg: float,
    batch_size: int,
    epoch_improvement_threshold: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    p = initialize_matrix(unique_users, "user_feature", k_latent_factors, upper_range=3)
    q = initialize_matrix(unique_items, "item_feature", k_latent_factors, upper_range=3)

    validation_errors = []

    print("Splitting into batches...")
    batch_split_start_time = time.time()
    batches = split_into_batches(x_train, batch_size)
    print(f"Splitting took {time.time() - batch_split_start_time:.1f} seconds")

    for epoch in range(max_epochs):
        print(f"{10 * '='} [ Epoch #{epoch + 1} ] {10 * '='}")
        epoch_start_time = time.time()

        for batch_number, batch in enumerate(batches):
            if len(batches) // 5 > 0 and batch_number % (len(batches) // 5) == 0:
                print(f"Batch #{batch_number + 1}")

            user_ids: pd.Series = batch["Username"]
            item_ids: pd.Series = batch["BGGId"]

            users_factors: np.ndarray = p.loc[user_ids].values
            items_factors: np.ndarray = q.loc[item_ids].values

            actual_ratings: np.ndarray = batch["Rating"].values
            predicted_ratings: np.ndarray = np.einsum("ij, ij->i", users_factors, items_factors)
            error: np.ndarray = actual_ratings - predicted_ratings

            p_err: np.ndarray = items_factors * error[:, None]
            q_err: np.ndarray = users_factors * error[:, None]

            p_gradient: np.ndarray = learning_rate * (p_err - reg * users_factors)
            q_gradient: np.ndarray = learning_rate * (q_err - reg * items_factors)

            p.loc[user_ids] += p_gradient
            q.loc[item_ids] += q_gradient

        train_rmse = rmse(p, q, x_train)
        val_rmse = rmse(p, q, x_val)

        validation_errors.append(val_rmse)

        print(f"\nTrain error: {train_rmse}")
        print(f"Validation error: {val_rmse}")

        should_early_stop = should_stop(validation_errors, epoch_improvement_threshold)

        print(f"\nEpoch took {time.time() - epoch_start_time} seconds")

        if should_early_stop:
            print(f"Early stopping after {epoch + 1} epochs")
            break

    return p, q


def create_items_factors() -> None:
    print("Loading data...")
    start_time = time.time()
    user_ratings = pd.read_csv(user_ratings_path)
    print(f"Data loaded in {time.time() - start_time:.1f} seconds")

    print("Splitting data into train, validation and test sets...")
    start_time = time.time()
    x_train, x_val, x_test = train_val_test_split(user_ratings, "BGGId")
    print(f"Data split in {time.time() - start_time:.1f} seconds")

    unique_users = user_ratings["Username"].unique()
    unique_games = user_ratings["BGGId"].unique()

    print("Computing latent factors...")
    start_time = time.time()
    p, q = fit(
        x_train,
        x_val,
        unique_users,
        unique_games,
        k_latent_factors=3,
        max_epochs=30,
        learning_rate=0.005,
        reg=0.02,
        batch_size=64,
        epoch_improvement_threshold=0.005,
    )
    print(f"Latent factors computed in {time.time() - start_time:.1f} seconds")
    print(f"Test error: {rmse(p, q, x_test)}")

    print("Saving latent factors...")
    p.to_pickle(users_factors_output_path)
    q.to_pickle(items_factors_output_path)
    print(f"Latent factors saved in {items_factors_output_path} and {users_factors_output_path}")


# Run this to generate items factors matrix
if __name__ == "__main__":
    create_items_factors()
