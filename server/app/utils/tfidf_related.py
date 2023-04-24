from app.types.shared_types import Game, GameRatingSimple, GamesResponse, PagedRequest
from app.utils.relative_path_from_file import relative_path_from_file

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class PersonalizedRecommendationsRequest(PagedRequest):
    ratings: list[GameRatingSimple]


def get_data():
  # prepare data (can add or remove some columns)
  cleaned_data_dir = relative_path_from_file(__file__, "../../data")

  games = pd.read_csv(f'{cleaned_data_dir}/games_cleaned.csv')
  mechanics = pd.read_csv(f'{cleaned_data_dir}/mechanics_cleaned.csv')
  subcategories = pd.read_csv(f'{cleaned_data_dir}/subcategories_cleaned.csv')
  themes = pd.read_csv(f'{cleaned_data_dir}/themes_cleaned.csv')
  # print(games.dtypes)

  df_conc = pd.merge(games, mechanics, on='BGGId')
  df_conc = pd.merge(df_conc, subcategories, on='BGGId')
  df_conc = pd.merge(df_conc, themes, on='BGGId')

  df_conc.sort_values(by='BGGId')
  df = df_conc.drop(columns=['BGGId', 'Description', 'Name', 'GoodPlayers', 'ImagePath', 'NumUserRatings', 'NumComments', 'NumAlternates', 'NumExpansions', 'NumImplementations', 'IsReimplementation', 'NumImplementations', 'Family'])

  df = df[df.columns.drop(list(df.filter(regex='Rank')))]
  return df, df_conc


def compute_tfidf_matrix(df):
    """
    in 'df' should be dataframe with chosen columns, returns matrix which will be used for computing cosine similarity
    """
    # define a dictionary that maps each data type to a preprocessing function
    preprocess_fn = {
        'float64': lambda x: MinMaxScaler().fit_transform(x.fillna(0).values.reshape(-1,1)),
        'int64': lambda x:   MinMaxScaler().fit_transform(x.fillna(0).values.reshape(-1,1)),  # dataset has binary flags saved as ints, so i would not be able to distinguish them from values like number of players
        'object': lambda x:  TfidfVectorizer().fit_transform(x.fillna(''))
    }

    tfidf_matrix_list = []
    # preprocess data using the corresponding preprocessing function
    for name, col in df.select_dtypes(include=['float', 'int', 'object']).items():
        data = preprocess_fn[str(col.dtypes)](col)
        if data.ndim != 2:
            raise ValueError("Data is not a 2D array")
        if type(data) != np.ndarray:
            print(type(data))
        tfidf_matrix_list.append(pd.Series(data.flatten()))

    # combine the dataframes
    # temp = pd.concat(tfidf_matrix_list, axis=1)
    temp = np.stack(tfidf_matrix_list, axis=-1)
    tfidf_matrix = pd.DataFrame(temp)

    return tfidf_matrix

   
def get_most_similar(df_conc, tfidf_matrix, item_rating: PersonalizedRecommendationsRequest):
  similarity_scores = cosine_similarity(tfidf_matrix)

  df_conc = df_conc.set_index('BGGId')

  game_ids = [rating.gameId for rating in item_rating.ratings]
  ratings = [rating.value for rating in item_rating.ratings]

  sortedthing = sorted(df_conc.index)
  tuples = [(value, sortedthing.index(value)) for value in df_conc.index]
  dicti = {t[0]: t[1] for t in tuples}
  dicti2 = {t[1]: t[0] for t in tuples}

  response: GamesResponse = {'games': [], 'totalNumberOfGames': 0}

  for idx, gid in enumerate(game_ids):

    similarity_scores_r = similarity_scores[dicti[gid]] * 0.1 * ratings[idx] # extract the 1D array of similarity scores and weight it based on user's rating

    # sort the similarity scores in descending order and get the indices of the top k most similar items
    k = 5 # for example, get the top 5 most similar items

    most_similar_indices = np.argsort(-similarity_scores_r)[:k]

    top_items = []
    # indices and similarity scores of the top k most similar items
    # print(f"Top {k} most similar items to item {id}:")
    for i in most_similar_indices:
        # print(f"Item {i+1}: similarity score = {similarity_scores_r[i]}")
        top_items.append(dicti2[i])

    for i in range(len(top_items)):
      game: Game = {
        'id': top_items[i],
        'name': df_conc.loc[top_items[i]]['Name'],
        'yearPublished': df_conc.loc[top_items[i]]['YearPublished'],
        'difficulty': df_conc.loc[top_items[i]]['GameWeight'],
        'avgRating': df_conc.loc[top_items[i]]['AvgRating'],
        'minPlayers': df_conc.loc[top_items[i]]['MinPlayers'],
        'maxPlayers': df_conc.loc[top_items[i]]['MaxPlayers'],
        'playtime': df_conc.loc[top_items[i]]['MfgPlaytime'],
        'minAge': df_conc.loc[top_items[i]]['MfgAgeRec'],
        'image': df_conc.loc[top_items[i]]['ImagePath'],
      }
      response['games'].append(game)
      
      # Increment the total number of games in the GamesResponse
      response['totalNumberOfGames'] += 1

  ## todo drop duplicates, drop rated games
  return response

if __name__ == "__main__":
  df, df_conc = get_data()
  tfidf_matrix = compute_tfidf_matrix(df)
  df_conc = df_conc.set_index('BGGId')
  # print(df_conc.index) 2905-1
  print(df_conc.loc[7644+1])
  
  print(df_conc.loc[3458])
  print(df_conc.loc[3458+1])
  print(df_conc.loc[25]['Name'])
  # get_most_similar(df_conc, tfidf_matrix, item_rating=None)