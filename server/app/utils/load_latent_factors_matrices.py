import pandas as pd

from app.utils.relative_path_from_file import relative_path_from_file


def load_latent_factors(filename, ext=".pkl"):
    filepath = relative_path_from_file(__file__, f"../db/{filename}{ext}")
    return pd.read_pickle(filepath)


def load_user_factors():
    return load_latent_factors("user_factors")


def load_item_factors():
    return load_latent_factors("item_factors")
