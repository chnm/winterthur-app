# Pull base image for Python 3.11
FROM --platform=x86_64 python:3.11

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies with Poetry
COPY poetry.lock pyproject.toml /app/
RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# shell stuff for volta
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV ~/.bashrc
ENV VOLTA_HOME /root/.volta
ENV PATH $VOLTA_HOME/bin:$PATH

# install volta
RUN curl https://get.volta.sh | bash

# Copy project
COPY . /app/

RUN node -v && npm -v

RUN npm install

#ENV TAILWIND_CSS_PATH='../../static/css/dist/styles.css'
RUN poetry run python3 manage.py tailwind install
RUN poetry run python3 manage.py tailwind build
RUN poetry run python3 manage.py collectstatic --no-input

CMD poetry run python3 manage.py runserver 0.0.0.0:8000
