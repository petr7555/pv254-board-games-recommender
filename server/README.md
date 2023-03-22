## How to run:

- install dependencies: `poetry install`
- run server: `uvicorn app.main:app --reload`

## Useful Poetry commands:

- install all dependencies: `poetry install`
- add new package at the latest version: `poetry add <package>`, e.g. `poetry add numpy`
- add package only for development: `poetry add <package> --group dev`, e.g. `poetry add jupyter --group dev`
- regenerate `poetry.lock` file: `poetry lock --no-update`
- remove package: `poetry remove <package>`, e.g. `poetry remove numpy`
