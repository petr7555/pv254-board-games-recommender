import os
from app.types.shared_types import Game, GameRatingSimple, GamesResponse, PagedRequest
from app.utils.relative_path_from_file import relative_path_from_file

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PersonalizedRecommendationsRequest(PagedRequest):
    ratings: list[GameRatingSimple]

def compute_similarity_score():
  cleaned_data_dir = relative_path_from_file(__file__, "../../data")
  games = pd.read_csv(f'{cleaned_data_dir}/games_cleaned.csv')

  path = relative_path_from_file(__file__, "../..")

  if os.path.exists(f"{path}/app/db/similarity_matrix"):
    if len(os.listdir(f"{path}/app/db/similarity_matrix")) == len(games):
      print("similarities already computed")
      return # similarities already exist
  else:
    print("created folder to save similarities")
    os.mkdir(f"{path}/app/db/similarity_matrix")

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

  # games = pd.read_csv(f'{cleaned_data_dir}/games_cleaned.csv')

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
  # np.save(f"{path}/app/db/similarity_matrix", similarity_scores)

  print("computing similarities")
  # for i, row in enumerate(tfidf_matrix): # very slow
  #   similarities = cosine_similarity(row, tfidf_matrix).astype(np.float32)
  #   np.save(f"{path}/app/db/similarity_matrix/similarity_row_{i}", similarities)

  similarity_scores = cosine_similarity(tfidf_matrix).astype(np.float32)
  for i, row in enumerate(similarity_scores):
    np.save(f"{path}/app/db/similarity_matrix/similarity_row_{i}", row)
  print("finished")



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


def get_most_similar_alt(games, num_games, item_ratings: list[GameRatingSimple]):
  # similarity_scores = cosine_similarity(tfidf_matrix)

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

  similarities = np.zeros(num_games) - 1000

  for idx, gid in enumerate(game_ids):
    sim = np.load(f'{cleaned_data_dir}/similarity_row_{dicti[gid]}.npy')
    similarities = np.maximum(similarities, sim * 0.2 * (ratings[idx] - 5))

  # sort the similarity scores in descending order
  # returns 1000 to make it a bit faster
  most_similar_indices = np.argsort(-similarities)[:len(item_ratings) + 1000]

  # indices and similarity scores of the top k most similar items
  # print(f"Top {k} most similar items to item {id}:")
  for i in most_similar_indices:
    if dicti2[i] in rated_games:
       # pass
       continue
    # print(f"Item {dicti2[i]}: similarity score = {similarities[i]}")
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
