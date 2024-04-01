FROM rust as volta-build
WORKDIR /src
RUN git clone https://github.com/volta-cli/volta.git /src
RUN cargo build
RUN ls /src/target/debug

# Pull base image for Python 3.11
FROM python:3.11

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

# Copy over Volta binaries
RUN mkdir -p /root/.volta/bin
COPY --from=volta-build /src/target/debug/volta /root/.volta/bin
COPY --from=volta-build /src/target/debug/volta-migrate /root/.volta/bin
COPY --from=volta-build /src/target/debug/volta-shim /root/.volta/bin

# shell stuff for volta
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV ~/.bashrc
ENV VOLTA_HOME /root/.volta
ENV PATH $VOLTA_HOME/bin:$PATH

RUN ln -s /root/.volta/bin/volta-shim /root/.volta/bin/node 
RUN ln -s /root/.volta/bin/volta-shim /root/.volta/bin/npm 
RUN ln -s /root/.volta/bin/volta-shim /root/.volta/bin/npx
RUN ln -s /root/.volta/bin/volta-shim /root/.volta/bin/pnpm 
RUN ln -s /root/.volta/bin/volta-shim /root/.volta/bin/yarn

# Copy project
COPY . /app/

# triggers node installation
RUN node -v && npm -v

RUN npm install

ENV TAILWIND_CSS_PATH='../../static/css/dist/styles.css'
RUN poetry run python3 manage.py tailwind install
RUN poetry run python3 manage.py tailwind build
RUN poetry run python3 manage.py collectstatic --no-input

CMD poetry run python3 manage.py runserver 0.0.0.0:8000
