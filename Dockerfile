FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY ./decks_tool /app/decks_tool
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-dev

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["poetry", "run", "streamlit", "run", "decks_tool/decks_tool.py", "--server.port=8501", "--server.address=0.0.0.0"]