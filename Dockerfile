FROM python:3.12-slim

ENV PORT=8080
ENV HOME=/root

WORKDIR /app

RUN pip install poetry

COPY ./decks_tool /app
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-dev

ENTRYPOINT ["sh", "-c", "poetry run streamlit run Main.py --server.port=${PORT} --server.address=0.0.0.0"]