FROM python:3.12-slim

ENV PORT 8080

WORKDIR /app

RUN pip install poetry

COPY ./decks_tool /app
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-dev

EXPOSE $PORT

HEALTHCHECK CMD curl --fail http://localhost:$PORT/_stcore/health

ENTRYPOINT poetry run streamlit run decks_tool.py --server.port=$PORT --server.address=0.0.0.0