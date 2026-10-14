FROM docker.io/library/node:22.23.2-trixie-slim@sha256:c5849ff9c9ebcd66615412f0b548ca5b8ecaef84003dc9ac2e077ebe46aaa3f6 AS assets
WORKDIR /app
COPY . .
RUN cd theme/static_src && npm ci && npm run build

FROM docker.io/library/python:3.11-slim@sha256:e88e9763f943ec1834f992a4b51e0f24500486803e8bc534e5767af9ea65f6ce AS builder
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true
RUN apt-get update \
    && apt-get install --yes --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip install --no-cache-dir poetry==1.8.3
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root --no-interaction --no-ansi

FROM docker.io/library/python:3.11-slim@sha256:e88e9763f943ec1834f992a4b51e0f24500486803e8bc534e5767af9ea65f6ce AS base
ENV DJANGO_READ_DOT_ENV_FILE=False \
    PATH=/app/.venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update \
    && apt-get install --yes --no-install-recommends libgomp1 libpq5 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .
COPY --from=assets /app/theme/static/css/dist theme/static/css/dist

FROM base AS test
RUN export DJANGO_SECRET_KEY=test-only-7f3a9c1e5b8d2f6a4c9e1b7d3f5a8c2e6b9d4f1a7c3e8b5d \
    && python manage.py check --deploy --tag security --fail-level WARNING \
    && python manage.py makemigrations --check --dry-run \
    && python manage.py test config.tests

FROM base AS runtime
ARG SOURCE_SHA=""
ENV APPLICATION_REVISION=$SOURCE_SHA \
    SOURCE_SHA=$SOURCE_SHA
RUN DJANGO_SECRET_KEY=build python manage.py collectstatic --no-input \
    && addgroup --gid 10001 app \
    && adduser --disabled-password --gecos "" --uid 10001 --gid 10001 app
USER 10001:10001
EXPOSE 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "--access-log", "-", "config.asgi:application"]
