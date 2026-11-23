# Contributing to PyPro

## Purpose

This document defines the rules and expectations for working through PyPro projects.

---

## Learning Rules

### What you must do

- Implement each project independently.
- Read the project README completely before starting.
- Write your own implementation from scratch.
- Test normal cases, failure cases, and edge cases.
- Refactor after achieving a working version.
- Commit at meaningful milestones with clear commit messages.
- Request a code review after completing each project.

### What you must not do

- Do not follow step-by-step tutorials during implementation.
- Do not copy complete solutions from any source.
- Do not use AI to write your implementation.

### What is allowed

- Reading official Python documentation.
- Searching for specific error messages.
- Looking up how a specific module or function works.
- Asking for concept explanations.
- Asking for debugging help after attempting to resolve the issue independently.

---

## Role of AI

AI assistance is permitted in the following roles only:

| Role | Permitted |
|------|-----------|
| Code reviewer | Yes |
| Debugging assistant | Yes — after independent attempts |
| Concept explainer | Yes |
| Architecture advisor | Yes |
| Implementation author | No |

---

## Git Workflow

```bash
# Start a project
git checkout -b project/01-cli-calculator

# Commit at milestones
git add .
git commit -m "feat: add basic arithmetic operations"

# When complete
git commit -m "feat: complete cli-calculator with full test coverage"
```

Commit message format:

```
type: short description

feat:     new feature or capability
fix:      bug fix
test:     adding or updating tests
refactor: restructuring without behaviour change
docs:     documentation only
chore:    tooling, config, maintenance
```

---

## Code Quality Standards

- Run `uv run ruff check .` before committing.
- Run `uv run ruff format .` before committing.
- Run `uv run pytest` and ensure all tests pass.
- Use type hints for function signatures.
- Keep functions focused on a single responsibility.

See `docs/coding-standards.md` for detailed guidance.

---

## Project Completion Checklist

Before marking a project complete:

- [ ] All functional requirements implemented.
- [ ] All acceptance criteria met.
- [ ] Tests written and passing.
- [ ] Edge cases handled.
- [ ] Code formatted and linted.
- [ ] Progress updated in `progress/progress.md`.
- [ ] Code review requested.
