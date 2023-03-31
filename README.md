# Denig Manuscript Project

This repository contains code for the Denig manuscript project, a partnership [between RRCHNM and the Winterthur Museum](https://rrchnm.org/news/rrchnm-partners-with-winterthur-museum-to-present-pennsylvania-illuminated-manuscript/).

Python 3.11.0 / Django 4.1 / Postgresql

## Development

The project uses [Poetry](https://python-poetry.org/docs/basic-usage/) for dependency and package management. To create your Django environment, navigate to the root (cloned) directory and do the following:

```sh
% cd winterthur-app
% poetry install
```

We also use [pre-commit](https://pre-commit.com) with `black` and `djhtml` to keep things nicely formatted.

```
% poetry run pre-commit install
% poetry run pre-commit autoupdate
```

Running `manage.py` will require prepending poetry to the commands, like so:

```sh
poetry run python manage.py migrate
poetry run python manage.py tailwind build
poetry run python manage.py runserver
```

A Makefile exists to make life a little more convenient. The common commands are:

- `make preview`: preview the site locally; this runs `poetry run python manage.py runserver`. You can also use `npm run serve`.
- `make tailwind`: compile the CSS; this runs `poetry run python manage.py tailwind start` and will reload the browser anytime updates happen.
- `make mm`: performs Django's `makemigration`
- `make migrate`: performs Django's `migrate`

## Setting up configuration in environment

For security, we store configurations in a local `.env` file. To get a local environment file to work with `django-environ`, we install `python-dotenv`:

```sh
% poetry add python-dotenv
```

Then add relevant files to an `.env` file:

```
% echo DEBUG=True >> .env
% echo DJANGO_SECRET_KEY=$(poetry run python -c "import secrets; print(secrets.token_urlsafe())") >> .env
```

Update `config/settings.py` to read the `.env` file.

```python
import environ
from dotenv import load_dotenv

load_dotenv()

env = environ.FileAwareEnv(
    DEBUG=(bool, False)
)

[...]

# Update this existing value
DEBUG = env('DEBUG')

# Update this existing value
SECRET_KEY = env('DJANGO_SECRET_KEY')
```

When it comes time to connect to Postgres, we also store the [Postgres connection string](https://django-environ.readthedocs.io/en/latest/types.html) in `.env`.
