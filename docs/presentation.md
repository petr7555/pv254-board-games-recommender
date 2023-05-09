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

[//]: # (description of the used data, some basic descriptive statistics of the data)

---

# Data preprocessing

- removed duplicate ratings
- removed users with less than 10 ratings
- removed games with less than 10 ratings

---

# Data analysis

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

- Description of the used recommender techniques, relation to standard techniques discussed during lectures (focus on
  the description of the overall pipeline, not on details of individual steps, particularly when using standard
  techniques like TF-IDF or cosine similarity)
- Specific examples of recommendations, e.g., in the form of screenshots of the developed application
- Results of the evaluation
- Experience report (problems, mistakes, useful tools, ...)

---

# Latent factors

- Description of the used recommender techniques, relation to standard techniques discussed during lectures (focus on
  the description of the overall pipeline, not on details of individual steps, particularly when using standard
  techniques like TF-IDF or cosine similarity)
- Specific examples of recommendations, e.g., in the form of screenshots of the developed application
- Results of the evaluation
- Experience report (problems, mistakes, useful tools, ...)

---

# Memory based CF

- Description of the used recommender techniques, relation to standard techniques discussed during lectures (focus on
  the description of the overall pipeline, not on details of individual steps, particularly when using standard
  techniques like TF-IDF or cosine similarity)
- Specific examples of recommendations, e.g., in the form of screenshots of the developed application
- Results of the evaluation
- Experience report (problems, mistakes, useful tools, ...)

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
