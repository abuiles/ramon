# Run tests
@default: test

# Install dependencies
@init:
  uv sync

@chat:
  uv run python -m ramon

# Run pytest with supplied options
@test *options:
  uv run pytest {{options}}
