FROM python:3.8-slim-buster
MAINTAINER Zech Zimmerman "hi@zech.codes"

WORKDIR /usr/src/app
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.in-project true

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

USER 1000:1000

COPY auth .
CMD ["poetry", "run", "hypercorn", "--bind", "0.0.0.0:8080", "--workers", "8", "auth.app:app"]
