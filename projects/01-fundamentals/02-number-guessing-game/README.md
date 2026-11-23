# Project 02: Number Guessing Game

**Level:** Fundamentals
**Estimated Time:** 4–6 hours

---

## Overview

Build an interactive number guessing game. The application generates a random number and gives the user hints (higher/lower) until they guess correctly. Supports difficulty levels and replay.

---

## Objectives

- Use loops and conditional logic.
- Use the `random` module.
- Validate user input.
- Track state across a game session.

---

## Python Concepts Practised

- `while` loops
- Conditional statements
- `random` module
- Input validation
- Functions
- State tracking with variables

---

## Functional Requirements

1. Generate a random integer between 1 and 100.
2. Accept integer guesses from the user.
3. Display "Too high" or "Too low" hints.
4. Display "Correct!" and the number of attempts when guessed.
5. Support three difficulty levels:
   - Easy: unlimited guesses.
   - Medium: 10 guesses maximum.
   - Hard: 5 guesses maximum.
6. Offer replay at the end of each game.
7. Display statistics at the end: total games, wins, average attempts.

---

## Non-Functional Requirements

- Input validation must prevent non-integer input from crashing the game.
- Functions must have type hints.

---

## Edge Cases

- Non-integer input for guess.
- Input outside the valid range.
- Exceeding the maximum allowed guesses.
- Replaying multiple times.

---

## Acceptance Criteria

- [ ] Random number is generated within the correct range.
- [ ] Higher/lower hints are correct.
- [ ] Attempt counter increments correctly.
- [ ] Maximum guess limit is enforced for Medium and Hard.
- [ ] Replay works correctly.
- [ ] Stats are accurate across multiple games.
- [ ] Invalid input does not crash the game.

---

## Suggested Implementation Steps

1. Write a function to get difficulty settings.
2. Write a function to run a single game.
3. Write an input validation function.
4. Write a replay loop.
5. Write a stats tracker.
6. Write automated tests.

---

## Testing Requirements

- Test that hints are correct (too high, too low).
- Test that the win condition is correctly detected.
- Test that the guess limit is enforced.
- Test input validation.

---

## Constraints

- Use only `random` from the standard library.
- No third-party packages.

---

## Completion Checklist

- [ ] All functional requirements implemented.
- [ ] Tests written and passing.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- Leaderboard stored to a file.
- Allow the user to set a custom range.
- Two-player mode (one player sets the number, one guesses).
