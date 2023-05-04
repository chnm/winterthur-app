# Development Instructions

## Setup and installation

Initial setup and installation:

- Install and activate Python 3.11.0. It's recommended to use [pyenv](https://github.com/pyenv/pyenv) for this.
- Install required python dependencies:

```bash
% poetry install
```

- Use [Volta](https://volta.sh/) for Node version management
- Install required Javascript dependencies:

```bash
% npm install
```

- Set secrets to a local `.env` file:

```bash
% echo DEBUG=True >> .env
% echo DJANGO_SECRET_KEY=$(poetry run python -c "import secrets; print(secrets.token_urlsafe())") >> .env
```

- Then, update your settings.py file.

```python
# Add the following lines
import environ
from dotenv import load_dotenv

load_dotenv()

env = environ.FileAwareEnv(
    DEBUG=(bool, False)
)

# [...]

# Update this existing value
DEBUG = env('DEBUG')

# Update this existing value
SECRET_KEY = env('DJANGO_SECRET_KEY')
```

- Create a new database and update your database settings accordingly
- Run database migrations:

```bash
make migrate
```

### Install pre-commmit hooks

The project uses [pre-commit](https://pre-commit.com/) to install and
manage commit hooks to ensure consistently formatted code. To install,
run:

```bash
% pre-commit install
```

Current hooks include Black for Python formatting, isort for
standardized imports, djhtml for consistent indentation in templates,
and prettier for Javascript, CSS, and related files.

## Unit Tests

Python tests are written with [py.test](http://doc.pytest.org/) and
should be run with `pytest`.
