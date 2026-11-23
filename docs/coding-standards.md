# Coding Standards

## Python Version

Python 3.13+ is required. Use modern Python features where appropriate.

---

## Code Style

All code must pass `ruff check` and `ruff format` without errors.

```bash
uv run ruff check .
uv run ruff format .
```

---

## Type Hints

Use type hints for all function signatures.

```python
# Correct
def add(a: float, b: float) -> float:
    return a + b

# Incorrect
def add(a, b):
    return a + b
```

---

## Functions

- One function, one responsibility.
- Keep functions short. If a function exceeds 20 lines, consider refactoring.
- Avoid side effects where possible.
- Prefer explicit return values over modifying global state.

---

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Variables | snake_case | `total_price` |
| Functions | snake_case | `calculate_total()` |
| Classes | PascalCase | `ExpenseTracker` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| Modules | snake_case | `expense_tracker.py` |

---

## Error Handling

- Catch specific exceptions, not bare `except:`.
- Provide useful error messages.
- Do not silently swallow exceptions.

```python
# Correct
try:
    result = int(user_input)
except ValueError:
    print("Please enter a valid integer.")

# Incorrect
try:
    result = int(user_input)
except:
    pass
```

---

## Imports

- Standard library first.
- Third-party second.
- Local imports last.
- Separate groups with a blank line.

```python
import json
import os
from pathlib import Path

import httpx

from .models import Task
```

---

## Comments

Write comments only when the reason is non-obvious. Code should be self-documenting through clear naming.

---

## Testing

- Write tests in the `tests/` directory of each project.
- Test normal cases, failure cases, and edge cases.
- Test file naming: `test_<module>.py`.
- Use descriptive test function names: `test_division_by_zero_raises_error`.

---

## Git Commits

- Commit at meaningful milestones.
- Use the commit format defined in `CONTRIBUTING.md`.
- Do not commit commented-out code.
- Do not commit debug print statements.
