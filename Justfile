# Run tests and linters
@default: test

# Install dependencies and test dependencies
@init:
  uv sync

# Run pytest with supplied options
@test *options:
  uv run pytest {{options}}
