# Development Workflow

## For Each Project

### 1. Read

Open `projects/<level>/<project>/README.md` and read it completely.

Understand:
- What the project does.
- What concepts are being practised.
- What the acceptance criteria are.
- What edge cases must be handled.

### 2. Plan

Before writing code:
- Identify the key functions or classes needed.
- Sketch the data flow.
- Note which Python concepts to apply.

Do not write code until you have a mental model of the structure.

### 3. Implement

```bash
# Start a new branch
git checkout -b project/NN-project-name

# Work in the src/ directory
# Start with main.py
```

Build incrementally:
1. Implement the simplest case first.
2. Add error handling.
3. Add edge case handling.
4. Refactor for clarity.

### 4. Test

```bash
uv run pytest projects/<level>/<project>/tests/ -v
```

Write tests as you go, not only at the end.

### 5. Lint and Format

```bash
uv run ruff check projects/<level>/<project>/
uv run ruff format projects/<level>/<project>/
```

Fix all issues before marking as complete.

### 6. Review

Commit, then request a code review.

```bash
git add .
git commit -m "feat: complete <project-name>"
```

### 7. Update Progress

Update `progress/progress.md` with:
- Completion date.
- Score (after review).
- Skills learned.
- Notes.

---

## Daily Practice

- One session minimum per work day.
- Aim for a 90-minute focused block.
- Document blockers in your notes.
- Commit progress at the end of each session.
