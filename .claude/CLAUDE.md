# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync --extra dev

# Run all tests
uv run pytest

# Run tests for a single project
uv run pytest projects/02-intermediate/06-cli-task-manager/

# Run a single test file
uv run pytest projects/02-intermediate/06-cli-task-manager/tests/test_main.py

# Run a single test by name
uv run pytest -k "test_filter_by_status"

# Lint
uv run ruff check .

# Format
uv run ruff format .
```

## Architecture

This is a skill-progression repository. Each project is a self-contained Python package under `projects/<tier>/<project-number>-<name>/` with the layout:

```
src/main.py          # all implementation lives here — one file per project
tests/test_main.py   # pytest tests; import from src.main
data/                # JSON persistence files (created at runtime, gitignored)
README.md            # spec: requirements, edge cases, acceptance criteria
```

`pyproject.toml` at the root configures pytest (`testpaths = ["projects"]`) and Ruff (`target-version = "py313"`). There is no package installation step — pytest finds `src/` via the rootdir config.

Projects are numbered 01–12 across four tiers:

| Tier | Projects | Focus |
|------|----------|-------|
| 01-fundamentals | 01–03 | functions, control flow, exceptions |
| 02-intermediate | 04–06 | OOP, file I/O, JSON, CLI tools |
| 03-advanced-python | 07–09 | regex, async, HTTP, generators |
| 04-backend-engineering | 10–12 | SQL, concurrency, REST APIs, Docker |

Each project's README is the authoritative spec. Read it before implementing.

## Git Commits

Do not reference Claude, AI, or any AI tool in commit messages or PR descriptions.
