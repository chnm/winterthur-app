#!/bin/bash

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

init() {
  # Ensure that we're in a virtualenv.
  python -c 'import sys; sys.prefix != sys.base_prefix' 2>/dev/null || (
    echo 'Please activate your virtualenv before running this script.' &&
    exit 1
  )
}

# Test that Poetry is installed 
if ! command -v poetry &> /dev/null
then
    echo "Poetry could not be found"
    echo "Please install poetry before running this script"
    echo "https://python-poetry.org/docs/#installation"
    exit
fi

# Install project dependencies.
install() {
  echo 'Installing dependencies with Poetry...\n'

  poetry install

}

init "$1"
install
