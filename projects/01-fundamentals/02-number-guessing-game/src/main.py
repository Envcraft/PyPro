"""Number Guessing Game — implement your solution here."""

import random

DIFFICULTIES = {
    "easy":   ("Easy",   None),   # unlimited attempts
    "medium": ("Medium", 10),
    "hard":   ("Hard",   5),
}


def get_difficulty() -> tuple[str, int | None]:
    print("Choose difficulty:  easy / medium (10 attempts) / hard (5 attempts)")
    while True:
        choice = input("Difficulty: ").strip().lower()
        if choice in DIFFICULTIES:
            label, max_attempts = DIFFICULTIES[choice]
            return label, max_attempts
        print("Please type easy, medium, or hard.")


def check_guess(guess: int, target: int) -> str:
    if guess < target:
        return "Too low! Try higher."
    if guess > target:
        return "Too high! Try lower."
    return "correct"


def get_guess(attempt: int, max_attempts: int | None) -> int | None:
    limit_info = f" ({max_attempts - attempt + 1} left)" if max_attempts else ""
    while True:
        raw = input(f"Your guess{limit_info}: ").strip()
        if raw.lower() in ("quit", "exit"):
            return None
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.")


def play_game(target: int, max_attempts: int | None) -> int | None:
    """Return the number of attempts on a win, or None on a loss/quit."""
    attempt = 1
    while max_attempts is None or attempt <= max_attempts:
        guess = get_guess(attempt, max_attempts)
        if guess is None:
            print("Game quit.")
            return None

        result = check_guess(guess, target)
        attempt += 1

        if result == "correct":
            print(f"Correct! You guessed it in {attempt - 1} attempt(s).")
            return attempt - 1

        print(result)

    print(f"Out of attempts! The number was {target}.")
    return None


def main() -> None:
    print("Welcome to Guess the Number!\n")
    games_played = wins = total_attempts = 0
    best = None

    while True:
        label, max_attempts = get_difficulty()
        target = random.randint(1, 100)
        limit_str = f"{max_attempts} attempts" if max_attempts else "unlimited attempts"
        print(f"\n[{label}] I'm thinking of a number between 1 and 100 — {limit_str}.\n")

        games_played += 1
        result = play_game(target, max_attempts)

        if result is not None:
            wins += 1
            total_attempts += result
            best = result if best is None else min(best, result)

        print(f"\n--- Stats: {wins}/{games_played} wins", end="")
        if wins:
            print(f" | avg {total_attempts / wins:.1f} attempts | best {best}", end="")
        print(" ---\n")

        again = input("Play again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
