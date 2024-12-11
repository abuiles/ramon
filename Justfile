# Run tests
@default: test

# Install dependencies
@init:
  uv sync

# Run pytest with supplied options
@test *options:
  uv run pytest {{options}}
