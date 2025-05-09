FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl gcc \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY ./pyproject.toml ./poetry.lock* /app/

WORKDIR /app

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]