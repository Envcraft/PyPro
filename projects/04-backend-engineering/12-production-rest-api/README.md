# Project 12: Production REST API

**Level:** Backend Engineering
**Estimated Time:** 32–40 hours

---

## Overview

Build a production-quality REST API for a task management application using FastAPI. Includes user registration, JWT authentication, full CRUD for tasks, pagination, filtering, sorting, automated tests, logging, and Docker support.

---

## Objectives

- Design a REST API following REST conventions.
- Implement JWT-based authentication.
- Use FastAPI with Pydantic for validation.
- Write automated API tests.
- Package the application in Docker.

---

## Python Concepts Practised

- FastAPI
- Pydantic v2
- JWT authentication
- SQLite or PostgreSQL
- Dependency injection
- Middleware
- Automated testing with `pytest` and `httpx.AsyncClient`
- Docker
- Logging

---

## Functional Requirements

### Authentication
1. `POST /auth/register` — register a user (email, password).
2. `POST /auth/login` — authenticate and return a JWT.
3. `POST /auth/refresh` — refresh an expired token.

### Tasks
4. `GET /tasks` — list tasks (paginated, filterable, sortable).
5. `POST /tasks` — create a task.
6. `GET /tasks/{id}` — get a task by ID.
7. `PATCH /tasks/{id}` — partial update.
8. `DELETE /tasks/{id}` — delete a task.

### Business Rules
- Users can only access their own tasks.
- Passwords must be hashed.
- Tokens must expire.
- Requests without a valid token return 401.

### Non-Functional
- Pagination: `?page=1&page_size=20`.
- Filtering: `?status=todo&priority=high`.
- Sorting: `?sort_by=due_date&order=asc`.
- Validation errors return 422 with field details.
- All errors return structured JSON.
- API documentation available at `/docs`.

---

## Edge Cases

- Registration with existing email.
- Login with wrong password.
- Accessing another user's task.
- Pagination with no results.
- Invalid filter values.
- Expired token.

---

## Acceptance Criteria

- [ ] All endpoints return correct status codes.
- [ ] JWT authentication works end-to-end.
- [ ] Tasks are scoped to the authenticated user.
- [ ] Pagination returns correct page and total count.
- [ ] Filters reduce the result set correctly.
- [ ] All endpoints have automated tests.
- [ ] Application runs in Docker.

---

## Suggested Implementation Steps

1. Set up FastAPI project structure.
2. Configure database (SQLite or PostgreSQL).
3. Implement user model and registration.
4. Implement JWT authentication.
5. Implement task model and CRUD endpoints.
6. Add pagination, filtering, and sorting.
7. Write automated tests.
8. Add structured logging.
9. Create `Dockerfile` and `docker-compose.yml`.
10. Test the Docker build.

---

## Required Dependencies

```bash
uv add fastapi uvicorn pydantic python-jose passlib
uv add --dev httpx pytest-asyncio
```

---

## Testing Requirements

Use `httpx.AsyncClient` with FastAPI's `app` directly.

- Test registration with valid and duplicate emails.
- Test login with correct and incorrect passwords.
- Test all CRUD endpoints with authentication.
- Test that cross-user access is rejected.
- Test pagination.

---

## Completion Checklist

- [ ] All endpoints implemented.
- [ ] JWT authentication working.
- [ ] Tests written and passing.
- [ ] Docker build succeeds.
- [ ] API docs accessible at `/docs`.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- Rate limiting per user.
- Email verification.
- Webhook notifications on task completion.
- OpenAPI spec export.
