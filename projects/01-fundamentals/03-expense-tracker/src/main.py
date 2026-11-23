"""Expense Tracker — implement your solution here."""

from datetime import date


def add_expense(
    expenses: list,
    amount: float,
    category: str,
    description: str,
    expense_date: str,
) -> dict:
    expense_id = max((e["id"] for e in expenses), default=0) + 1
    expense = {
        "id": expense_id,
        "amount": amount,
        "category": category,
        "description": description,
        "date": expense_date,
    }
    expenses.append(expense)
    return expense


def delete_expense(expenses: list, expense_id: int) -> bool:
    for i, e in enumerate(expenses):
        if e["id"] == expense_id:
            expenses.pop(i)
            return True
    return False


def get_total(expenses: list) -> float:
    return sum(e["amount"] for e in expenses)


def get_category_totals(expenses: list) -> dict[str, float]:
    totals: dict[str, float] = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return totals


def get_largest_expense(expenses: list) -> dict | None:
    return max(expenses, key=lambda e: e["amount"]) if expenses else None


def filter_by_category(expenses: list, category: str) -> list:
    return [e for e in expenses if e["category"].lower() == category.lower()]


def _prompt_amount() -> float | None:
    try:
        return float(input("Amount: $").strip())
    except ValueError:
        print("Error: Enter a valid number.")
        return None


def _print_expense(e: dict) -> None:
    print(f"  [{e['id']}] {e['date']}  [{e['category']}]  {e['description']}: ${e['amount']:.2f}")


def _show_menu() -> None:
    print("\nExpense Tracker")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Totals by category")
    print("4. Grand total")
    print("5. Largest expense")
    print("6. Filter by category")
    print("7. Delete expense")
    print("8. Quit")


def main() -> None:
    expenses: list = []

    while True:
        _show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            desc = input("Description: ").strip()
            cat = input("Category (e.g. Food, Travel, Bills): ").strip()
            amount = _prompt_amount()
            if amount is None:
                continue
            expense_date = input(f"Date (YYYY-MM-DD) [Enter for today]: ").strip()
            if not expense_date:
                expense_date = date.today().isoformat()
            e = add_expense(expenses, amount, cat, desc, expense_date)
            print(f"Added: [{e['id']}] {e['description']} ({e['category']}) — ${e['amount']:.2f}")

        elif choice == "2":
            if not expenses:
                print("No expenses recorded yet.")
            else:
                print("\n--- All Expenses ---")
                for e in expenses:
                    _print_expense(e)

        elif choice == "3":
            totals = get_category_totals(expenses)
            if not totals:
                print("No expenses recorded yet.")
            else:
                print("\n--- Totals by Category ---")
                for cat, total in sorted(totals.items()):
                    print(f"  {cat}: ${total:.2f}")

        elif choice == "4":
            print(f"\nGrand Total: ${get_total(expenses):.2f}")

        elif choice == "5":
            largest = get_largest_expense(expenses)
            if largest:
                print("\n--- Largest Expense ---")
                _print_expense(largest)
            else:
                print("No expenses recorded yet.")

        elif choice == "6":
            cat = input("Category to filter: ").strip()
            results = filter_by_category(expenses, cat)
            if results:
                print(f"\n--- Expenses in '{cat}' ---")
                for e in results:
                    _print_expense(e)
                print(f"  Subtotal: ${sum(e['amount'] for e in results):.2f}")
            else:
                print(f"No expenses found in category '{cat}'.")

        elif choice == "7":
            try:
                expense_id = int(input("Enter expense ID to delete: ").strip())
            except ValueError:
                print("Error: Enter a valid ID number.")
                continue
            if delete_expense(expenses, expense_id):
                print(f"Expense {expense_id} deleted.")
            else:
                print(f"No expense found with ID {expense_id}.")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1–8.")


if __name__ == "__main__":
    main()
