from app.types.shared_types import Game, GameRatingSimple, GamesResponse, PagedRequest
from app.utils.relative_path_from_file import relative_path_from_file

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PersonalizedRecommendationsRequest(PagedRequest):
    ratings: list[GameRatingSimple]


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

  similarities = np.zeros(num_games)

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