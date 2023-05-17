FROM --platform=x86_64 python:3.11 as py-build-stage

ENV PYTHONUNBUFFERED 1

WORKDIR /src
COPY pyproject.toml .
COPY poetry.lock .

#ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN python -m venv /venv

ENV PATH="/venv/bin:$PATH"
ENV VIRTUAL_ENV="/venv"

# install poetry
RUN pip3 install poetry

RUN poetry install --no-root --no-dev

FROM --platform=x86_64 python:3.11 as npm-build-stage

# copy python artifacts from previous stage
COPY --from=py-build-stage /venv /venv
ENV PATH="/venv/bin:$PATH"
ENV VIRTUAL_ENV="/venv"

# shell stuff for volta
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV ~/.bashrc
ENV VOLTA_HOME /root/.volta
ENV PATH $VOLTA_HOME/bin:$PATH

# install volta
RUN curl https://get.volta.sh | bash

WORKDIR /src
COPY . .

# triggers volta to install node/npm
RUN node -v && npm -v

RUN npm install

#ENV TAILWIND_CSS_PATH='../../static/css/dist/styles.css'
RUN poetry run python3 manage.py tailwind install
RUN poetry run python3 manage.py tailwind build
RUN poetry run python3 manage.py collectstatic --no-input


FROM --platform=x86_64 python:3.11

RUN adduser --disabled-password django
USER django

WORKDIR /app
COPY . .
COPY --from=py-build-stage /venv /venv
COPY --from=npm-build-stage /src/staticfiles /app/staticfiles

ENV PATH="/venv/bin:$PATH"
ENV VIRTUAL_ENV="/venv"

CMD poetry run uwsgi --http :8000 --static-map /static=/app/stati    cfiles --chdir /app --module config.wsgi
