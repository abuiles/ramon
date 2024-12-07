# Run tests and linters
@default: test

# Install dependencies and test dependencies
@init:
  poetry install

# Run pytest with supplied options
@test *options:
  poetry run pytest {{options}}
