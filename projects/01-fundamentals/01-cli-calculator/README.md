# Project 01: CLI Calculator

**Level:** Fundamentals
**Estimated Time:** 4–6 hours

---

## Overview

Build a command-line calculator that accepts user input, performs arithmetic operations, and handles invalid input gracefully. The application runs in a continuous loop until the user exits.

---

## Objectives

- Implement arithmetic operations using functions.
- Validate user input before processing.
- Handle exceptions without crashing.
- Build a continuous interactive loop with an exit mechanism.

---

## Python Concepts Practised

- Variables and data types
- Arithmetic operators
- Functions
- Conditional statements
- While loops
- Exception handling (`ValueError`, `ZeroDivisionError`)
- Input validation

---

## Functional Requirements

1. Support the following operations:
   - Addition (`+`)
   - Subtraction (`-`)
   - Multiplication (`*`)
   - Division (`/`)
   - Modulus (`%`)
   - Exponentiation (`**`)
2. Accept two numbers and an operator from the user.
3. Display the result.
4. Continue accepting input after each calculation.
5. Exit cleanly when the user types `quit` or `exit`.
6. Handle invalid numbers with a clear message.
7. Handle division by zero with a clear message.

---

## Non-Functional Requirements

- Functions must have type hints.
- No global mutable state.
- Input validation must be separate from calculation logic.

---

## Input and Output

**Input:**
```
Enter first number (or 'quit' to exit): 10
Enter operator (+, -, *, /, %, **): /
Enter second number: 3
```

**Output:**
```
Result: 10 / 3 = 3.3333333333333335
```

---

## Edge Cases

- Non-numeric input for numbers.
- Unsupported operator.
- Division by zero.
- Empty input.
- Very large numbers.

---

## Acceptance Criteria

- [ ] All six operations produce correct results.
- [ ] Invalid number input displays an error and re-prompts.
- [ ] Division by zero displays a specific error message.
- [ ] Unsupported operator displays an error message.
- [ ] Application continues after any error.
- [ ] Application exits cleanly on `quit`.
- [ ] At least 10 unit tests pass.

---

## Suggested Implementation Steps

1. Write a function for each arithmetic operation.
2. Write an input validation function for numbers.
3. Write an operator validation function.
4. Write the main loop.
5. Connect all parts.
6. Test manually.
7. Write automated tests.
8. Refactor.

---

## Testing Requirements

Write tests in `tests/test_main.py` covering:

- Each arithmetic operation with valid input.
- Division by zero.
- Invalid operator handling.
- Correct return types.

Do not test `input()` calls directly — structure your code so that calculation logic is testable independently.

---

## Constraints

- Use only the Python standard library.
- No third-party packages.

---

## Completion Checklist

- [ ] All functional requirements implemented.
- [ ] All acceptance criteria met.
- [ ] Tests written and passing.
- [ ] `ruff check` passes.
- [ ] `ruff format` applied.
- [ ] Progress updated.

---

## Stretch Goals

- Support chaining operations (use the previous result as the first operand).
- Display a calculation history.
- Support parentheses.
