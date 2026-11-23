# Project 06: CLI Task Manager

**Level:** Intermediate
**Estimated Time:** 12–16 hours

---

## Overview

Build a full-featured CLI task manager using object-oriented Python. Tasks have priorities, due dates, and statuses. All data persists to a JSON file between sessions.

---

## Objectives

- Apply OOP with classes and dataclasses.
- Use enums for categorical values.
- Implement sorting and filtering.
- Persist data with JSON serialisation.

---

## Python Concepts Practised

- OOP: classes, methods, `__repr__`, `__str__`
- `dataclasses.dataclass`
- `enum.Enum`
- Type hints
- `datetime.date`
- Sorting with `key`
- Filtering with comprehensions
- JSON serialisation/deserialisation

---

## Functional Requirements

1. Create a task with: title, description, priority (LOW/MEDIUM/HIGH), due date, status.
2. Update any field of a task.
3. Delete a task.
4. Mark a task as DONE.
5. List all tasks.
6. Filter by status (TODO, IN_PROGRESS, DONE).
7. Filter by priority.
8. Sort by due date or priority.
9. Search tasks by title keyword.
10. Persist to `data/tasks.json`.

---

## Non-Functional Requirements

- Use a `Task` dataclass or class.
- Use `Priority` and `Status` enums.
- JSON serialisation must handle `date` objects.

---

## Edge Cases

- Task with no due date.
- Filtering with no results.
- Sorting tasks where some have no due date.
- Updating a non-existent task.
- Invalid priority or status value.

---

## Acceptance Criteria

- [ ] All CRUD operations work.
- [ ] Filters return correct subsets.
- [ ] Sorting produces the correct order.
- [ ] Persistence works across sessions.
- [ ] Enums prevent invalid status and priority values.

---

## Suggested Implementation Steps

1. Define `Priority` and `Status` enums.
2. Define the `Task` dataclass.
3. Write JSON serialisation/deserialisation for `Task`.
4. Implement the `TaskManager` class with CRUD methods.
5. Implement filtering and sorting methods.
6. Build the CLI menu.
7. Write tests.

---

## Testing Requirements

- Test task creation with all fields.
- Test filtering by status and priority.
- Test sorting by due date.
- Test serialisation and deserialisation round-trip.
- Test updating and deleting tasks.

---

## Constraints

- Standard library only.
- Use `uuid` for unique IDs.

---

## Completion Checklist

- [ ] All functional requirements implemented.
- [ ] Tests written and passing.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- Recurring tasks.
- Tags.
- Task dependencies.
- Due-date notifications.
