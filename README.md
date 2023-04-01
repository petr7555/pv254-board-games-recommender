# 🎲 Board games recommender system

## Team

- Matěj Bukáček
- Petr Janík
- Jakub Kraus
- Michal Salášek

## Consultation 1 - April 4th 10:00

- problem formulation, clarification of the purpose, for whom, why
	- recommendation board games to users who like to play board games and want to try new ones
- usage
	- website visitor rates 10 games and gets paged recommendations sorted from the most relevant
	- we are considering showing the recommendation reasons as well (e.g. "recommended to you because you rated \[other
	  game\] 9/10"), but we are not sure if it is possible
- hypothetical business model
	- referral links / eshop
- specific aspects of the domain
	- TODO
- specific data with some basic analysis (value distributions etc.)
	- [dataset](https://www.kaggle.com/datasets/threnjen/board-games-database-from-boardgamegeek?select=user_ratings.csv):
		- relevant columns:
			- games
				- ImagePath - Image http:// path
			- user_ratings
				- BGGId - BoardGameGeek game ID
				- Rating - Raw rating given by user
				- Username - User giving rating
	- analysis:
		- 21925 different games, 217 themes, 10 categories (only 10 033 games (45.8%) belong to some category)
		- average rating per category
			- ![barplot](images/average_rating_by_subcategory_barplot.png)
		- number of ratings per category
			- ![barplot](images/number_of_ratings_by_subcategory_barplot.png)
		- values of ratings:
			- ![histogram](images/ratings_values_histogram.png)
			- average rating = 7.13
			- 18 909 528 user ratings of distinct games
		- number of ratings per user
			- ![histogram](images/ratings_per_user_histogram.png)
			- average number of ratings per user = 46.05 (median = 12)
			- maximum number of ratings by user = 6493
			- 411 374 distinct users rated at least 1 game
			- 19.3% of users (79 296) rated only 1 game
		- density of ratings matrix = 0.0021
	- data cleaning/preprocessing:
		- multiple ratings of the same game by some users - duplicates removed, only latest rating kept (ratings don't have timestamps, so we assumed file user_ratings.csv is ordered chronologically and kept the last occurence of Username-BGGId pair in the file) -> 32 687 rows removed, 0.017%
- specific proposal for algorithms that you want to implement
	- memory based CF (Pearson correlation coefficient)
	- model based CF (gradient descent)
- implementation of some naive baseline
	- most rated games
	- top-rated games
	- random games
- basic idea of evaluation approach
	- technical:
		- data will be split into 80% and 20%
			- at the very end, once we choose the best model, we will use the 20% of data for final evaluation
			- 80% will be used for training
				- it will be split into 80% and 20% using 5-fold cross-validation
					- for models that require validation set (to stop the training) this 80 % will be split again into
					  80%
					  and 20%
		- used metric will be RMSE
	- by real users’ happiness:
		- we will give our system to real users and collect their feedback
	- by archetype users:
		- we will create several archetypes of users and evaluate our system on them (by seeing if the recommendations
		  are what we would expect)

## Consultation 2 - April 25th 10:00

- functional demo of several recommendation algorithms (at least some basic version)
- preliminary subjective evaluation (does it seem to do something meaningful?)
- specific examples of "interesting" recommendations (both good and poor)
- detailed plan for evaluation
- specific problems encountered, questions
