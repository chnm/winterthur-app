Development Instructions
========================

Setup and installation
-----------------------

Initial setup and installation:

- Install and activate Python 3.11.0. It's recommended to use `pyenv <https://github.com/pyenv/pyenv>`_ for this.

- Install required python dependencies::

.. code-block:: bash

    poetry install

- Use `Volta <https://volta.sh/>`_ for Node version management

- Install required Javascript dependencies::

.. code-block:: bash

    npm install

- Set secrets to a local `.env` file::

.. code-block:: bash

    % echo DEBUG=True >> .env
    % echo DJANGO_SECRET_KEY=$(poetry run python -c "import secrets; print(secrets.token_urlsafe())") >> .env

- Then, update your settings.py file.

.. code-block:: python

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

- Create a new database and update your database settings accordingly

- Run database migrations::

.. code-block:: bash

    make migrate

Install pre-commmit hooks
~~~~~~~~~~~~~~~~~~~~~~~~~

The project uses `pre-commit <https://pre-commit.com/>`_ to install and manage commit hooks to ensure consistently formatted code. To install, run::

.. code-block:: bash
    
    pre-commit install

Current hooks include Black for Python formatting, isort for standardized imports, djhtml for consistent indentation in templates, and prettier for Javascript, CSS, and related files.

Unit Tests
----------

Python tests are written with `py.test <http://doc.pytest.org/>`_
and should be run with ``pytest``.
