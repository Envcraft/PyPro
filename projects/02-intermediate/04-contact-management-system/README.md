# Project 04: Contact Management System

**Level:** Intermediate
**Estimated Time:** 8–12 hours

---

## Overview

Build a CLI contact management system with full CRUD operations and JSON-based persistence. Contacts persist between sessions.

---

## Objectives

- Implement CRUD operations against a file-backed data store.
- Validate input before storage.
- Prevent duplicate records.
- Serialise and deserialise data with JSON.

---

## Python Concepts Practised

- CRUD patterns
- JSON (`json` module)
- File I/O with context managers
- Input validation
- Functions
- Error handling
- `pathlib.Path`

---

## Functional Requirements

1. Create a contact: name, phone, email, optional notes.
2. Read contacts: list all, search by name or phone.
3. Update a contact by ID.
4. Delete a contact by ID.
5. Prevent duplicate phone numbers and emails.
6. Persist contacts to `data/contacts.json`.
7. Load contacts on startup.

---

## Non-Functional Requirements

- Validation logic must be separate from persistence logic.
- Use type hints throughout.
- Handle file-not-found gracefully on first run.

---

## Edge Cases

- Duplicate phone number.
- Duplicate email.
- Updating a non-existent contact.
- Deleting a non-existent contact.
- Malformed JSON file.
- Empty search results.
- Special characters in names.

---

## Acceptance Criteria

- [ ] All CRUD operations work correctly.
- [ ] Duplicates are rejected with a clear message.
- [ ] Data persists between sessions.
- [ ] Invalid input is rejected with a clear message.
- [ ] Search returns correct results.

---

## Suggested Implementation Steps

1. Define the contact schema.
2. Implement `load_contacts` and `save_contacts`.
3. Implement `create_contact` with validation.
4. Implement `search_contacts`.
5. Implement `update_contact`.
6. Implement `delete_contact`.
7. Build the CLI menu.
8. Write tests.

---

## Testing Requirements

- Test creation with valid data.
- Test duplicate detection.
- Test search with matching and non-matching terms.
- Test update and delete.
- Test loading from a valid and invalid JSON file.

---

## Constraints

- Standard library only.
- JSON file must be human-readable with indentation.

---

## Completion Checklist

- [ ] All functional requirements implemented.
- [ ] Tests written and passing.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- Export contacts to CSV.
- Import contacts from CSV.
- Group contacts by first letter.
