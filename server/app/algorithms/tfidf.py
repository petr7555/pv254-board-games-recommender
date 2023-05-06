import os

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.types.shared_types import Game, GameRatingSimple
from app.utils.relative_path_from_file import relative_path_from_file


def compute_similarity_score():
    cleaned_data_dir = relative_path_from_file(__file__, "../../data")
    games = pd.read_csv(f'{cleaned_data_dir}/games_cleaned.csv')

    path = relative_path_from_file(__file__, "../..")

    if os.path.exists(f"{path}/app/db/similarity_matrix"):
        if len(os.listdir(f"{path}/app/db/similarity_matrix")) == len(games):
            print("similarities already computed")
            return  # similarities already exist
    else:
        print("created folder to save similarities")
        os.mkdir(f"{path}/app/db/similarity_matrix")

    mechanics = pd.read_csv(f'{cleaned_data_dir}/mechanics_cleaned.csv')
    subcategories = pd.read_csv(f'{cleaned_data_dir}/subcategories_cleaned.csv')
    themes = pd.read_csv(f'{cleaned_data_dir}/themes_cleaned.csv')

    games.set_index("BGGId", inplace=True)

    games = games.drop(
        columns=['NumOwned', 'NumWant', 'NumWish', 'NumWeightVotes', 'StdDev', 'BayesAvgRating', 'GoodPlayers',
                 'ImagePath', 'NumUserRatings', 'NumComments', 'NumAlternates', 'NumExpansions', 'NumImplementations',
                 'IsReimplementation', 'NumImplementations', 'Family'])
    games = games.drop(games.select_dtypes(include=['float']).columns, axis=1)
    games = games[games.columns.drop(list(games.filter(regex='Rank')))]
    # Drop all columns containing floats

    string_dict = {}
    for idx, row in games.loc[:, ~games.columns.isin(['BGGId'])].iterrows():
        string_dict[idx] = str(row["Description"]).lower()
        temp = ['_'.join(column_name.split()) + '_' + str(value) for column_name, value in row.items() if
                value != 0 and column_name != "Description"]

        # Combine the column names into a string, place thm into string twice to increase weight when compared to Description
        string = ' ' + ' '.join(temp) + ' ' + ' '.join(temp) + ' '
        string_dict[idx] += string

    for table in [mechanics, subcategories, themes]:
        table.set_index("BGGId", inplace=True)
        for idx, row in table.loc[:, ~table.columns.isin(['BGGId'])].iterrows():
            # Create a list of column names where the corresponding value is 1
            columns_with_ones = ['_'.join(column_name.split()) for column_name, value in row.items() if value == 1]

            # Combine the column names into a string, place thm into string twice to increase weight when compared to Description
            string = ' '.join(columns_with_ones) + ' ' + ' '.join(columns_with_ones) + ' '

            # Add the string to the list
            string_dict[idx] += str(string)

    # remove possible multiple whitespaces
    for idx in string_dict.keys():
        string_dict[idx] = ' '.join(string_dict[idx].split())

    del mechanics
    del subcategories
    del themes
    del games

    strings = [value for (id, value) in sorted(string_dict.items(), key=lambda x: x[0])]
    tfidf_matrix = TfidfVectorizer().fit_transform(strings)

    # nedostatek RAM mi zabijel program
    del strings
    del string_dict

    path = relative_path_from_file(__file__, "../..")

    similarity_scores = cosine_similarity(tfidf_matrix).astype(np.float32)
    for i, row in enumerate(similarity_scores):
        np.save(f"{path}/app/db/similarity_matrix/similarity_row_{i}", row)


def get_tfidf_recommendations(games, item_ratings: list[GameRatingSimple]):
    games = games.set_index('BGGId')

    game_ids = [rating.gameId for rating in item_ratings]
    ratings = [rating.value for rating in item_ratings]

    sortedthing = sorted(games.index)
    tuples = [(value, sortedthing.index(value)) for value in games.index]
    dicti = {t[0]: t[1] for t in tuples}  # BGGId: idx
    dicti2 = {t[1]: t[0] for t in tuples}  # idx: BGGId

    sorted_items = []

    rated_games = set(game_ids)

    cleaned_data_dir = relative_path_from_file(__file__, "../db/similarity_matrix")

    similarities = np.zeros(len(games)) - 1000

    for idx, gid in enumerate(game_ids):
        sim = np.load(f'{cleaned_data_dir}/similarity_row_{dicti[gid]}.npy')
        similarities = np.maximum(similarities, sim * 0.2 * (ratings[idx] - 5))

    # sort the similarity scores in descending order
    # returns 1000 to make it a bit faster
    most_similar_indices = np.argsort(-similarities)[:len(item_ratings) + 1000]

    # indices and similarity scores of the top k most similar items
    for i in most_similar_indices:
        if dicti2[i] in rated_games:
            # pass
            continue
        sorted_items.append(dicti2[i])

    sorted_games = []
    for i in range(len(sorted_items)):
        game: Game = {
            'id': sorted_items[i],
            'name': games.loc[sorted_items[i]]['Name'],
            'yearPublished': games.loc[sorted_items[i]]['YearPublished'],
            'difficulty': games.loc[sorted_items[i]]['GameWeight'],
            'avgRating': games.loc[sorted_items[i]]['AvgRating'],
            'minPlayers': games.loc[sorted_items[i]]['MinPlayers'],
            'maxPlayers': games.loc[sorted_items[i]]['MaxPlayers'],
            'playtime': games.loc[sorted_items[i]]['MfgPlaytime'],
            'minAge': games.loc[sorted_items[i]]['MfgAgeRec'],
            'image': games.loc[sorted_items[i]]['ImagePath'],
        }
        sorted_games.append(game)

    return sorted_games
