from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get("/top_rated/{page}")
def top_rated(page: int):
    """
    returns PAGE_SIZE items sorted by average rating (page indexing starts with 0)
    """
    # change later to keep sorted dataframe in memory (global constant?) instead of loading it each time
    DATA_PATH = "../../data/user_ratings_cleaned.csv"
    user_ratings = pd.read_csv(DATA_PATH)

    avg_ratings = user_ratings.groupby("BGGId")["Rating"].mean().reset_index()

    # later just import as global constant
    PAGE_SIZE = 10  # number of items per page
    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE

    # Sort the dataframe by rating and return the relevant page of data
    sorted_ratings = avg_ratings.sort_values("Rating", ascending=False)

    top_items = sorted_ratings.iloc[start_index:end_index][["BGGId"]].to_dict("records")
    return top_items


@app.get("/random_items/{page}")
def random_items(page: int):
    """
    returns PAGE_SIZE random items (page indexing starts with 0)
    """
    # change later to keep dataframe in memory (global constant?) instead of loading it each time
    DATA_PATH = "../../data/games_cleaned.csv"
    games = pd.read_csv(DATA_PATH)

    PAGE_SIZE = 10  # number of items per page

    # Get a random sample of rows from the dataframe
    sample = games[["BGGId"]].sample(n=PAGE_SIZE).to_dict("records")

    return sample


@app.get("/most_rated/{page}")
def most_rated(page: int):
    """
    returns PAGE_SIZE items sorted by number of rating (page indexing starts with 0)
    """
    # change later to keep dataframe in memory (global constant?) instead of loading it each time
    DATA_PATH = "../../data/user_ratings_cleaned.csv"
    user_ratings = pd.read_csv(DATA_PATH)
    avg_ratings = user_ratings.groupby("BGGId")["Rating"].count().reset_index()

    # later just import as global constant
    PAGE_SIZE = 10  # number of items per page
    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE

    # Sort the dataframe by rating and return the relevant page of data
    sorted_ratings = avg_ratings.sort_values("Rating", ascending=False)

    top_items = sorted_ratings.iloc[start_index:end_index][["BGGId"]].to_dict("records")
    return top_items
