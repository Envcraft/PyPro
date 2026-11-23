# Project 03: Expense Tracker

**Level:** Fundamentals
**Estimated Time:** 6–8 hours

---

## Overview

Build a CLI expense tracker that lets a user record, categorise, view, and analyse expenses during a session. Data is held in memory (no persistence required at this level).

---

## Objectives

- Work with lists and dictionaries.
- Use comprehensions for data aggregation.
- Write functions that transform collections.
- Handle empty states and missing data.

---

## Python Concepts Practised

- Lists
- Dictionaries
- Functions
- List comprehensions
- Dictionary comprehensions
- Data aggregation (`sum`, `max`, `filter`)
- Input validation

---

## Functional Requirements

1. Add an expense with: amount, category, description, date.
2. List all expenses in a formatted table.
3. Delete an expense by ID.
4. Calculate the total of all expenses.
5. Calculate the total per category.
6. Find the largest expense.
7. Filter expenses by category.
8. Display a simple summary report.

---

## Non-Functional Requirements

- Expenses should be stored as dictionaries or dataclasses in a list.
- Functions must accept and return data rather than print directly where practical.
- Type hints required.

---

## Edge Cases

- Negative amounts.
- Zero-amount expenses.
- Deleting a non-existent ID.
- Filtering by a category with no expenses.
- Operations on an empty expense list.
- Invalid date format.

---

## Acceptance Criteria

- [ ] Expenses can be added with all required fields.
- [ ] Invalid amounts are rejected.
- [ ] All expenses display correctly.
- [ ] Total calculation is correct.
- [ ] Category totals are correct.
- [ ] Largest expense is correctly identified.
- [ ] Delete removes the correct expense.
- [ ] Edge cases produce clear error messages, not crashes.

---

## Suggested Implementation Steps

1. Define the data structure for an expense.
2. Implement `add_expense`.
3. Implement `list_expenses`.
4. Implement `delete_expense`.
5. Implement `get_total`.
6. Implement `get_category_totals`.
7. Implement `get_largest_expense`.
8. Implement `filter_by_category`.
9. Build the CLI menu loop.
10. Write tests.

---

## Testing Requirements

- Test `get_total` with multiple expenses.
- Test `get_total` with an empty list.
- Test `get_category_totals` with mixed categories.
- Test `get_largest_expense`.
- Test `filter_by_category`.
- Test `delete_expense` with valid and invalid IDs.

---

## Constraints

- No persistence (data lives in memory for this project).
- Standard library only.
- Use `datetime.date.today()` for default date.

---

## Completion Checklist

- [ ] All functional requirements implemented.
- [ ] Tests written and passing.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- Persist expenses to a JSON file.
- Budget limits per category with alerts.
- Monthly filtering.
- Export to CSV.
