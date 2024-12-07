# Run tests and linters
@default: test

# Install dependencies and test dependencies
@init:
  pipenv run pip install -e '.[test]'

# Run pytest with supplied options
@test *options:
  pipenv run pytest {{options}}
