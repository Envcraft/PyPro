# PyPro — Python Projects

**Build. Test. Master.**

PyPro is a structured, project-based Python skill development environment. It is an engineering practice repository—not a tutorial collection. You learn by implementing, testing, debugging, refactoring, and reviewing real projects.

---

## Philosophy

- Implementation over consumption.
- Testing is non-negotiable.
- Debugging is a skill to develop.
- Refactoring follows working code.
- Code review is part of completion.

---

## Skill Progression

| Level | Focus | Projects |
|-------|-------|----------|
| 1 — Fundamentals | Variables, functions, control flow, exceptions | 01–03 |
| 2 — Intermediate | OOP, file I/O, JSON, CLI tools | 04–06 |
| 3 — Advanced Python | Regex, async, HTTP, generators | 07–09 |
| 4 — Backend Engineering | SQL, concurrency, REST APIs, Docker | 10–12 |

---

## Roadmap

```
01 CLI Calculator       → 02 Number Guessing Game  → 03 Expense Tracker
04 Contact Manager      → 05 File Organizer         → 06 CLI Task Manager
07 Log Analyzer         → 08 REST API Client        → 09 Web Scraper
10 Inventory System     → 11 Concurrent Processor   → 12 Production REST API
```

---

## Tooling

| Tool | Purpose |
|------|---------|
| Python 3.13+ | Language runtime |
| uv | Dependency and environment management |
| pytest | Automated testing |
| Ruff | Linting and formatting |
| pyproject.toml | Project configuration |

### Setup

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dev dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Check code quality
uv run ruff check .

# Format code
uv run ruff format .
```

---

## Repository Structure

```
PyPro/
├── projects/
│   ├── 01-fundamentals/        # Projects 01–03
│   ├── 02-intermediate/        # Projects 04–06
│   ├── 03-advanced-python/     # Projects 07–09
│   └── 04-backend-engineering/ # Projects 10–12
├── docs/                       # Guides and standards
├── challenges/                 # Weekly challenges
├── notes/                      # Personal revision notes
├── resources/                  # Reference material
└── progress/                   # Progress tracking
```

---

## How to Get Started

1. Clone or initialise this repository.
2. Run `uv sync --extra dev` to set up the environment.
3. Read `docs/workflow.md` for the development workflow.
4. Read `docs/coding-standards.md` for code quality expectations.
5. Open `progress/progress.md` to see your current state.
6. Start with `projects/01-fundamentals/01-cli-calculator/README.md`.
7. Implement. Test. Refactor. Commit.

---

## Learning Rules

- Do not follow tutorials during implementation.
- Do not copy complete solutions.
- Use documentation for reference.
- Attempt debugging independently before seeking help.
- Write tests before refactoring.
- Commit at meaningful milestones.
- Request a code review when a project is complete.

See `CONTRIBUTING.md` for the full guidelines.

---

## Evaluation

Each project is evaluated out of 100 across:

- Functionality (20)
- Code structure (15)
- Python concepts (15)
- Error handling (10)
- Edge cases (10)
- Automated testing (15)
- Readability (10)
- Git usage (5)

See `docs/evaluation-rubric.md` for scoring interpretation.

---

## Progress

Track your status in `progress/progress.md`.
