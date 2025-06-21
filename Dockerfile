ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

# Python
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Poetry
ENV POETRY_HOME='/usr/local' \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=2.1.1 \
    PATH="$PATH:$POETRY_HOME/bin"


RUN apt-get update && apt-get install -y curl unixodbc libodbc2 && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY . /app

RUN poetry install

EXPOSE 8080

ENTRYPOINT ["poetry", "run", "gunicorn", "rest_fastapi.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080"]
