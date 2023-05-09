---
theme: uncover
paginate: true
---

<style scoped>
section {
  background: #ff6f00;
}
h1 {
  color: #ffc107;
}
</style>

![width:200px](assets/android-chrome-512x512.png)

# Board games recommender

Matěj Bukáček, Petr Janík, Jakub Kraus, Michal Salášek, 2023

---
<style>
section {
  background: #ffc107;
}
</style>

[//]: # (Part 1)

# Goal & Motivation

- Develop a recommender system for board games
	- users who like to play board games and want to try new ones
- Possible monetization:
	- e-shop
	- referral links to e-shops

---

# Data

- from [kaggle](https://www.kaggle.com/datasets/threnjen/board-games-database-from-boardgamegeek)
- `games`, `mechanics`, `subcategories`, `themes`
- `user_ratings`
	- `BGGId` - BoardGameGeek game ID
	- `Rating` - Raw rating given by user
	- `Username` - User giving rating

---

## Data preprocessing

- removed duplicate ratings
- removed users with less than 10 ratings
- removed games with less than 10 ratings

---

## Data analysis

- **18 340 284** user ratings
- **224 557** users, **21 919** games, **157** mechanics, **217**&nbsp;themes, **10** subcategories
- density of user ratings matrix: **0.37%**
- ratings per user:
	- average: **81.67**
	- median: **39**
	- maximum: **6478**
- average rating: **7.10** (range **[0, 10]**)

---

![bg contain](../images/number_of_ratings_per_rating_value_histogram.png)

---

![bg contain](../images/number_of_users_per_number_of_ratings_histogram.png)

---

![bg contain](../images/average_rating_of_games_by_subcategory_bar_plot.png)

---

![bg contain](../images/number_of_ratings_by_subcategory_bar_plot.png)

---

[//]: # (Part 2)

# TF-IDF

- most of relevant data are binary flags + some numerical values and Description
- pipeline:
	- convert binary flags and numerical values to text
	- concatenate with description
	- compute TF-IDF matrix
	- compute cosine similarities
	- choose rows with rated games
	- sort games based on similarity score

---

## Problems

- during development:
	- converting everything to text (so that library function could be used)
	- mapping index in matrix to index in database
- finished product:
	- reimplementations

---

## Evaluation

- no exact metric, just by feedback
- mostly positive feedback, but problems when game has too many reimplementations
  (those are very similar, so they get high score)
- examples of recommendations at the end

---

# Latent factors

- **idea**:
	- we are trying to model "taste" of users and "features" of items
	- matrices of user / item latent factors
- **approach**: minimize squared errors (+ regularization)
- **method**: stochastic / mini-batch gradient descent

---

![width:300px](assets/latent_factors/latent_factors_predicted_rating.png)
![width:800px](assets/latent_factors/latent_factors_squared_errors.png)

---

![bg contain](assets/latent_factors/latent_factors_2d_example.png)

---

## Pipeline I

- split dataset into **train**, **validation** and **test** set
	- **idea**: all games should be present in all three datasets

---

![bg contain](assets/latent_factors/latent_factors_data_split_train.png)

---

![bg contain](assets/latent_factors/latent_factors_data_split_validation.png)

---

## Pipeline II

- use training set (user ratings) to **train** the model
	- adjust matrices of user / item factors using **gradient descent**
- use validation set to prevent overfitting
	- compute **RMSE**
	- apply early stopping if necessary
- use test set to **evaluate** the trained model (RMSE)

---

## Initial results I

- **stochastic** gradient descent too **slow**
	- necessary to reduce data
- adopt **mini-batch** gradient descent
	- allows to train on full data with more epochs / hyper-parameter tuning

---

## Initial results II

- predictions not quite "reasonable" (no obvious pattern)
	- 2 latent factors → 2D plane (similar to PCA) → **find features** in similar / "opposite" clusters
	- compare RMSE of latent factors model with **baselines**

---

![bg contain](assets/latent_factors/2d_factors_plot.png)

---

## RMSE comparison

- global mean: 1.530
- user mean: 1.376
- item mean: 1.316
- global mean + item/user bias: 1.230
- latent factors: 1.19
- latent factors with global effects: 1.19

---

## New user

- approximate **user factors** from ratings
- item factors matrix is constant
- least squares
- simple approach (systems of equations)
- examples of recommendations at the end

---

## Experience report

- necessary to implement gradient descent myself
- necessary to make mini-batch
- additional effort to confirm algorithms are implemented correctly
- computing recommendations for new user initially unclear

---

# Memory based CF

- **pipeline:**
	- ratings matrix (users × games) - get users that rated the same games as me
	- unrated game - keep users who rated it
	- find k most similar users to me
	- get mean rating

---

## Qualitative evaluation

- only on local device (not integrated into the app)
- low amount of feedback - testing in Postman
- not very intuitive, much novelty and unexpected recommendations
- stick to category - RPGs recommend RPGs

---

![bg contain](assets/ibnncf/01.png)

---

![bg contain](assets/ibnncf/02.png)

---

![bg contain](assets/ibnncf/03.png)

---

![bg contain](assets/ibnncf/04.png)

---

## Encountered problems

- performance - not usable in real-time, not deployed
- implementation - several new technologies (also programming on Windows)
- memory - creation of ratings matrix on local device

---

[//]: # (Part 3)

# User interface

---

![bg contain](assets/screenshots/01.png)

---

![bg contain](assets/screenshots/02.png)

---
<style scoped>
section {
  background: #ff6f00;
}
</style>

![bg contain](assets/screenshots/03.png)

---

![bg contain](assets/screenshots/04.png)

---

![bg contain](assets/screenshots/05.png)

---

![bg contain](assets/screenshots/06.png)

---

![bg contain](assets/screenshots/07.png)

---

![bg contain](assets/screenshots/08.png)

---

# Thank you

![width:300px](assets/qr-code.svg)
Try it out: https://pv254-board-games-recommender.vercel.app/
Code: https://github.com/petr7555/pv254-board-games-recommender
