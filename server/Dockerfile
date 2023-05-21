ARG PYTHON_VERSION=3.9
FROM python:$PYTHON_VERSION

LABEL name="python-$PYTHON_VERSION"
LABEL version="$PYTHON_VERSION"
LABEL maintainer="Petr Janik <485122@mail.muni.cz>"

ARG POETRY_VERSION=1.2.2

# Install Poetry system-wide using pip
RUN pip install --upgrade pip && \
    pip install poetry==${POETRY_VERSION} 

WORKDIR /app

COPY pyproject.toml poetry.lock ./

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN poetry install --only main --no-root --no-cache --no-interaction

COPY app ./app

# Generate files which are too large to be stored in git
COPY data/cleaned/games.csv data/cleaned/games.csv
COPY data/cleaned/mechanics.csv data/cleaned/mechanics.csv
COPY data/cleaned/subcategories.csv data/cleaned/subcategories.csv
COPY data/cleaned/themes.csv data/cleaned/themes.csv
RUN poetry run create-similarity-matrix

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
