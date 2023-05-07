# Board games recommender server

The server is deployed at [https://pv254-board-games-recommender-server.onrender.com](https://pv254-board-games-recommender-server.onrender.com).

## How to run:

- Download [data](https://www.kaggle.com/datasets/threnjen/board-games-database-from-boardgamegeek) and unzip it to `data` folder.
- Run `playground/jakub_kraus/preprocessing.ipynb`. This will create `data/cleaned/` folder with preprocessed data.
- Install dependencies: `poetry install`.
- Run server: `uvicorn app.main:app --reload`.

## Useful Poetry commands:

- Install all dependencies: `poetry install`.
- Add new package at the latest version: `poetry add <package>`, e.g. `poetry add numpy`.
- Add package only for development: `poetry add <package> --group dev`, e.g. `poetry add jupyter --group dev`.
- Regenerate `poetry.lock` file: `poetry lock --no-update`.
- Remove package: `poetry remove <package>`, e.g. `poetry remove numpy`.

## Lint autoformat
- `poetry run black --config black.py.toml .`

## Lint check
- `poetry run black --config black.py.toml . --check`
