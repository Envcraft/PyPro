# Project 10: Inventory Management System

**Level:** Backend Engineering
**Estimated Time:** 24–32 hours

---

## Overview

Build a CLI inventory management system backed by SQLite. Products have categories and suppliers. All stock movements are recorded in a history table. Low-stock alerts are generated automatically.

---

## Objectives

- Design and implement a relational database schema.
- Use SQL transactions for data integrity.
- Implement a repository pattern.
- Enforce business rules at the data layer.

---

## Python Concepts Practised

- `sqlite3` module
- SQL: DDL and DML
- Database transactions (`commit`, `rollback`)
- Repository pattern
- Business logic separation
- Type hints
- OOP

---

## Functional Requirements

1. Product management: add, update, delete, search.
2. Category management: create, list.
3. Supplier management: add, update, list.
4. Stock-in: record incoming stock with quantity, unit cost, supplier, date.
5. Stock-out: record stock removal with quantity and reason.
6. Inventory history: view all movements for a product.
7. Low-stock alerts: list products below their reorder threshold.
8. Search and filter: by name, category, supplier.
9. Reject stock-out operations that would result in negative inventory.

---

## Database Schema

Design at minimum:
- `products` table: id, name, sku, description, category_id, unit_price, quantity, reorder_threshold.
- `categories` table: id, name.
- `suppliers` table: id, name, contact_email, phone.
- `stock_movements` table: id, product_id, movement_type, quantity, unit_cost, supplier_id, notes, created_at.

---

## Edge Cases

- Stock-out exceeding available quantity.
- Deleting a product with stock history.
- Duplicate SKU.
- Product with no supplier.
- Category with no products.
- Low-stock threshold of zero.

---

## Acceptance Criteria

- [ ] Products can be created, updated, deleted, and searched.
- [ ] Stock-in and stock-out update product quantity correctly.
- [ ] Stock-out below zero is rejected.
- [ ] Stock movements are recorded in history.
- [ ] Low-stock alert lists the correct products.
- [ ] All writes use transactions.

---

## Suggested Implementation Steps

1. Design and create the database schema.
2. Implement the `ProductRepository`.
3. Implement the `SupplierRepository`.
4. Implement the `StockMovementRepository`.
5. Implement business logic (stock-in, stock-out, alerts).
6. Build the CLI interface.
7. Write tests using an in-memory SQLite database.

---

## Testing Requirements

Use an in-memory SQLite database (`:memory:`) for all tests.

- Test product CRUD.
- Test that stock-out below zero raises an error.
- Test that stock history is recorded correctly.
- Test low-stock alert logic.
- Test transaction rollback on failure.

---

## Constraints

- Standard library only (`sqlite3`).
- No ORM.
- Raw SQL required.

---

## Completion Checklist

- [ ] All functional requirements implemented.
- [ ] Transactions used for all writes.
- [ ] Tests use in-memory database.
- [ ] Tests written and passing.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- Reporting: inventory value by category.
- CSV import of initial product data.
- Audit log for all schema changes.
