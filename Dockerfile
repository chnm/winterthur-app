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
RUN cd theme/static_src && npm install

#RUN npm install --save-dev cross-env
#RUN npm install --save-dev rimraf
#RUN npm install --save-dev @tailwindcss/aspect-ratio
#RUN npm install --save-dev @tailwindcss/line-clamp
#RUN npm install --save-dev @tailwindcss/typography
#RUN npm install --save-dev @tailwindcss/forms
#RUN npm install --save-dev tailwindcss
#RUN npm install --save-dev postcss-simple-vars

# build: poetry run python3 manage.py tailwindcss build
#ENV TAILWIND_CSS_PATH='../../static/css/dist/styles.css'
RUN npm run build


FROM --platform=x86_64 python:3.11

#RUN apt-get update 
#RUN apt-get install -y curl

RUN adduser --disabled-password django
USER django

WORKDIR /app
COPY . .
COPY --from=py-build-stage /venv /venv
COPY --from=npm-build-stage /src/static/css /app/static/css

ENV PATH="/venv/bin:$PATH"
ENV VIRTUAL_ENV="/venv"

CMD poetry run uwsgi --http :8000 --chdir /app --module config.wsgi
