# Run tests
@default: test

# Install dependencies
@init:
  uv sync

@lint-fix:
  uv run ruff check --fix

@lint *options:
  uv run ruff check {{options}}

@chat:
  uv run python -m ramon

@archive:
  uv run python -m ramon archive-completed-tasks

@summary *options:
  uv run python -m ramon summary {{options}}

# Run pytest with supplied options
@test *options:
  uv run pytest {{options}}
