from app.utils.relative_path_from_file import relative_path_from_file

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os


def compute_similarity_score():
  cleaned_data_dir = relative_path_from_file(__file__, "../../data")
  games = pd.read_csv(f'{cleaned_data_dir}/games_cleaned.csv')

  path = relative_path_from_file(__file__, "../..")

  if os.path.exists(f"{path}/app/db/similarity_matrix"):
    if len(os.listdir(f"{path}/app/db/similarity_matrix")) == len(games):
      print("similarities already computed")
      return # similarities already exist
  else:
    print("creating folder to save similarities")
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

  # similarity_scores = cosine_similarity(tfidf_matrix).astype(np.float32)

  path = relative_path_from_file(__file__, "../..")
  # np.save(f"{path}/app/db/similarity_matrix", similarity_scores)

  for i, row in enumerate(tfidf_matrix):
    similarities = cosine_similarity(row, tfidf_matrix).astype(np.float32)
    np.save(f"{path}/app/db/similarity_matrix/similarity_row_{i}", similarities)

  # for i, row in enumerate(similarity_scores):
  #   np.save(f"{path}/app/db/similarity_matrix/similarity_row_{i}", row)

