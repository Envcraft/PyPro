# Evaluation Rubric

Each project is scored out of 100.

---

## Scoring Categories

| Category | Weight | Description |
|----------|-------:|-------------|
| Functionality | 20 | All requirements implemented and working correctly |
| Code structure | 15 | Logical organisation, separation of concerns, appropriate modularity |
| Python concepts | 15 | Correct and idiomatic use of the target concepts for this project |
| Error handling | 10 | Specific exceptions caught, useful messages, no silent failures |
| Edge cases | 10 | Boundary conditions handled: empty input, zero, None, missing files |
| Automated testing | 15 | Tests written, covering normal, failure, and edge cases |
| Readability | 10 | Clear naming, minimal comments, clean formatting |
| Git usage | 5 | Meaningful commits at milestones, clear messages |
| **Total** | **100** | |

---

## Score Interpretation

| Score | Level |
|-------|-------|
| 0–49 | Fundamental gaps — revisit core concepts |
| 50–64 | Beginner — partial implementation or significant issues |
| 65–74 | Developing intermediate — works but needs improvement |
| 75–84 | Intermediate — solid implementation, minor issues |
| 85–94 | Strong intermediate — well-implemented, clean code |
| 95–100 | Excellent — exceptional execution for the project scope |

Scores are relative to the complexity of each project. A score of 80 on Project 12 represents stronger work than 80 on Project 01.

---

## Review Process

1. Complete the project.
2. Ensure all checklist items in the project README are met.
3. Run tests: `uv run pytest projects/<project>/tests/`.
4. Run linter: `uv run ruff check projects/<project>/`.
5. Update `progress/progress.md`.
6. Request a code review.
7. Address feedback.
8. Mark as completed when review is passed.
