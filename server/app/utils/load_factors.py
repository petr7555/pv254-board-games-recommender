import pandas as pd


def load_factors(file_path: str) -> pd.DataFrame:
    return pd.read_pickle(file_path)
