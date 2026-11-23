"""Contact Management System — implement your solution here."""

import json
import uuid
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "contacts.json"


def load_contacts(filepath: Path) -> list[dict]:
    if not filepath.exists():
        return []
    with filepath.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_contacts(contacts: list[dict], filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)


def _email_taken(contacts: list[dict], email: str, exclude_id: str = "") -> bool:
    return any(
        c["email"].lower() == email.lower()
        for c in contacts
        if c["id"] != exclude_id
    )


def create_contact(
    contacts: list[dict],
    name: str,
    phone: str,
    email: str,
    notes: str = "",
) -> dict:
    if _email_taken(contacts, email):
        raise ValueError(f"Email '{email}' is already used by another contact.")
    contact = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "phone": phone,
        "email": email,
        "notes": notes,
    }
    contacts.append(contact)
    return contact


def search_contacts(contacts: list[dict], query: str) -> list[dict]:
    q = query.lower()
    return [
        c for c in contacts
        if q in c["name"].lower()
        or q in c["phone"]
        or q in c["email"].lower()
        or q in c["notes"].lower()
    ]


def update_contact(contacts: list[dict], contact_id: str, **fields) -> bool:
    allowed = {"name", "phone", "email", "notes"}
    if "email" in fields and _email_taken(contacts, fields["email"], exclude_id=contact_id):
        raise ValueError(f"Email '{fields['email']}' is already used by another contact.")
    for c in contacts:
        if c["id"] == contact_id:
            for key, value in fields.items():
                if key in allowed:
                    c[key] = value
            return True
    return False


def delete_contact(contacts: list[dict], contact_id: str) -> bool:
    for i, c in enumerate(contacts):
        if c["id"] == contact_id:
            contacts.pop(i)
            return True
    return False


def _print_contact(c: dict) -> None:
    print(f"  ID: {c['id']}")
    print(f"  Name:  {c['name']}")
    print(f"  Phone: {c['phone']}")
    print(f"  Email: {c['email']}")
    if c["notes"]:
        print(f"  Notes: {c['notes']}")
    print()


def _show_menu() -> None:
    print("\nContact Management System")
    print("1. Add contact")
    print("2. List all contacts")
    print("3. Search contacts")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. Quit")


def main() -> None:
    contacts = load_contacts(DATA_FILE)
    print(f"Loaded {len(contacts)} contact(s) from storage.")

    while True:
        _show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            phone = input("Phone: ").strip()
            email = input("Email: ").strip()
            notes = input("Notes (optional): ").strip()
            try:
                c = create_contact(contacts, name, phone, email, notes)
            except ValueError as e:
                print(f"Error: {e}")
                continue
            save_contacts(contacts, DATA_FILE)
            print(f"Contact added with ID: {c['id']}")

        elif choice == "2":
            if not contacts:
                print("No contacts saved yet.")
            else:
                print(f"\n--- {len(contacts)} Contact(s) ---")
                for c in sorted(contacts, key=lambda x: x["name"].lower()):
                    _print_contact(c)

        elif choice == "3":
            query = input("Search (name / phone / email / notes): ").strip()
            results = search_contacts(contacts, query)
            if results:
                print(f"\n--- {len(results)} result(s) for '{query}' ---")
                for c in results:
                    _print_contact(c)
            else:
                print(f"No contacts found for '{query}'.")

        elif choice == "4":
            contact_id = input("Enter contact ID to update: ").strip()
            existing = next((c for c in contacts if c["id"] == contact_id), None)
            if not existing:
                print(f"No contact found with ID '{contact_id}'.")
                continue
            print("Leave blank to keep current value.")
            fields = {}
            for field in ("name", "phone", "email", "notes"):
                val = input(f"{field.capitalize()} [{existing[field]}]: ").strip()
                if val:
                    fields[field] = val
            if fields:
                try:
                    update_contact(contacts, contact_id, **fields)
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
                save_contacts(contacts, DATA_FILE)
                print("Contact updated.")
            else:
                print("No changes made.")

        elif choice == "5":
            contact_id = input("Enter contact ID to delete: ").strip()
            if delete_contact(contacts, contact_id):
                save_contacts(contacts, DATA_FILE)
                print(f"Contact {contact_id} deleted.")
            else:
                print(f"No contact found with ID '{contact_id}'.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1–6.")


if __name__ == "__main__":
    main()
