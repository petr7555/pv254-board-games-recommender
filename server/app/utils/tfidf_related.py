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

  games.set_index("BGGId", inplace=True)

  games = games.drop(columns=['NumOwned', 'NumWant', 'NumWish', 'NumWeightVotes', 'StdDev', 'BayesAvgRating', 'GoodPlayers', 'ImagePath', 'NumUserRatings', 'NumComments', 'NumAlternates', 'NumExpansions', 'NumImplementations', 'IsReimplementation', 'NumImplementations', 'Family'])
  games = games.drop(games.select_dtypes(include=['float']).columns, axis=1)
  games = games[games.columns.drop(list(games.filter(regex='Rank')))]
  # Drop all columns containing floats

  string_dict = {}
  for idx, row in games.loc[:, ~games.columns.isin(['BGGId'])].iterrows():
    string_dict[idx] = str(row["Description"]).lower()
    temp = ['_'.join(column_name.split()) + '_' + str(value) for column_name, value in row.items() if value != 0 and column_name!="Description"]
    string = ' ' + ' '.join(temp) + ' '
    string_dict[idx] += string

  for table in [mechanics, subcategories, themes]:
    table.set_index("BGGId", inplace=True)
    for idx, row in table.loc[:, ~table.columns.isin(['BGGId'])].iterrows():
        # Create a list of column names where the corresponding value is 1
        columns_with_ones = ['_'.join(column_name.split()) for column_name, value in row.items() if value == 1]
        
        # Combine the column names into a string, with the format "Column1, Column3"
        string = ' '.join(columns_with_ones) + ' '
        
        # Add the string to the list
        string_dict[idx] += str(string)

  df_conc = pd.merge(games, mechanics, on='BGGId')
  df_conc = pd.merge(df_conc, subcategories, on='BGGId')
  df_conc = pd.merge(df_conc, themes, on='BGGId')

  df_conc.sort_values(by='BGGId')
  # df = df_conc.drop(columns=['BGGId', 'Name', 'GoodPlayers', 'ImagePath', 'NumUserRatings', 'NumComments', 'NumAlternates', 'NumExpansions', 'NumImplementations', 'IsReimplementation', 'NumImplementations', 'Family'])

  # remove possible multiple whitespaces
  for idx in string_dict.keys():
     string_dict[idx] = ' '.join(string_dict[idx].split())

  games = pd.read_csv(f'{cleaned_data_dir}/games_cleaned.csv')
  return games, string_dict


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


def tfidf(string_dict):
   # just to be safe sort it by id
   strings = [value for (id, value) in sorted(string_dict.items(), key=lambda x: x[0])]
   return TfidfVectorizer().fit_transform(strings) 


def get_most_similar(games, similarity_scores, item_ratings: list[GameRatingSimple]):
  # similarity_scores = cosine_similarity(tfidf_matrix)

  games = games.set_index('BGGId')

  game_ids = [rating.gameId for rating in item_ratings]
  ratings = [rating.value for rating in item_ratings]

  sortedthing = sorted(games.index)
  tuples = [(value, sortedthing.index(value)) for value in games.index]
  dicti = {t[0]: t[1] for t in tuples}
  dicti2 = {t[1]: t[0] for t in tuples}

  sorted_items = []

  rated_games = set(game_ids)

  similarities = np.zeros(similarity_scores.shape[1])
  for idx, gid in enumerate(game_ids):
    similarities = np.maximum(similarities, similarity_scores[dicti[gid]] * 0.2 * (ratings[idx] - 5))

  # sort the similarity scores in descending order
  # returns 1000 to make it a bit faster
  most_similar_indices = np.argsort(-similarities)[:len(item_ratings) + 1000]

  # indices and similarity scores of the top k most similar items
  # print(f"Top {k} most similar items to item {id}:")
  for i in most_similar_indices:
    if dicti2[i] in rated_games:
       continue
    # print(f"Item {i+1}: similarity score = {similarity_scores_r[i]}")
    sorted_items.append(dicti2[i])

  # response: GamesResponse = {'games': [], 'totalNumberOfGames': 0}
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
    # response['games'].append(game)
    # response['totalNumberOfGames'] += 1

  return sorted_games


if __name__ == "__main__":
  games, string_dict = get_data()
  # print(string_dict[1])
  tfidf_matrix = tfidf(string_dict)
  print(tfidf_matrix.shape)
  similarity_scores = cosine_similarity(tfidf_matrix)
  get_most_similar(games, similarity_scores, item_rating=None)

  games = games.set_index('BGGId')
  # print(df_conc.index) 2905-1
  # print(games.columns[:29])
  """
  print(df_conc.loc[7644+1])
  
  print(df_conc.loc[3458])
  print(df_conc.loc[3458+1])
  print(df_conc.loc[25]['Name'])
  """


  # get_most_similar(df_conc, tfidf_matrix, item_rating=None)