# Board games recommender server

The server is deployed at [https://pv254-board-games-recommender-server.onrender.com](https://pv254-board-games-recommender-server.onrender.com).

## How to run:

- download [data](https://www.kaggle.com/datasets/threnjen/board-games-database-from-boardgamegeek) and unzip it to `data` folder
- install dependencies: `poetry install`
- run server: `uvicorn app.main:app --reload`

## Useful Poetry commands:

- install all dependencies: `poetry install`
- add new package at the latest version: `poetry add <package>`, e.g. `poetry add numpy`
- add package only for development: `poetry add <package> --group dev`, e.g. `poetry add jupyter --group dev`
- regenerate `poetry.lock` file: `poetry lock --no-update`
- remove package: `poetry remove <package>`, e.g. `poetry remove numpy`

## Lint autoformat
- `poetry run black --config black.py.toml .`

## Lint check
- `poetry run black --config black.py.toml . --check`
