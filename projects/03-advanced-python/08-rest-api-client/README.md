# Project 08: REST API Client

**Level:** Advanced Python
**Estimated Time:** 16–24 hours

---

## Overview

Build a reusable REST API client library with support for GET and POST requests, authentication, retry logic, and logging. Test it against a public API.

---

## Objectives

- Use `httpx` for HTTP requests.
- Implement retry logic with exponential backoff.
- Handle authentication headers.
- Log requests and responses.
- Handle HTTP errors correctly.

---

## Python Concepts Practised

- HTTP protocol fundamentals
- `httpx` library
- JSON serialisation
- Exception handling hierarchy
- Retry strategies
- Logging
- Type hints
- Context managers

---

## Functional Requirements

1. Send GET requests with optional query parameters.
2. Send POST requests with a JSON body.
3. Add authentication headers (Bearer token and Basic auth).
4. Set timeouts.
5. Retry on network errors and 5xx responses with exponential backoff.
6. Raise on 4xx responses.
7. Log all requests and responses at DEBUG level.
8. Log errors at ERROR level.
9. Return parsed JSON responses.

---

## Non-Functional Requirements

- The client must be usable as a class or context manager.
- Retry logic must be configurable (max retries, backoff factor).
- Logging must not expose authentication headers.

---

## Edge Cases

- Timeout.
- 404 response.
- 500 response (should retry).
- 401 response (should not retry).
- Invalid JSON in response.
- Network unavailable.

---

## Acceptance Criteria

- [ ] GET and POST work correctly.
- [ ] Auth headers are sent correctly.
- [ ] Retry fires on 5xx and network errors.
- [ ] 4xx errors raise an exception immediately without retrying.
- [ ] Timeout raises a clear error.
- [ ] Logging captures requests without exposing credentials.

---

## Suggested Implementation Steps

1. Install `httpx`: `uv add httpx`.
2. Write the base client class.
3. Implement GET.
4. Implement POST.
5. Add authentication.
6. Add timeout configuration.
7. Add retry logic.
8. Add logging.
9. Write tests (mock HTTP responses).
10. Test against a real public API.

---

## Testing Requirements

Use `httpx`'s built-in test transport or `respx` to mock HTTP responses.

- Test successful GET.
- Test successful POST.
- Test retry on 500.
- Test no retry on 400.
- Test timeout handling.
- Test auth header presence.

---

## Constraints

- Use `httpx` for HTTP.
- No other third-party packages unless `respx` for testing.

---

## Completion Checklist

- [ ] All functional requirements implemented.
- [ ] Tests written and passing.
- [ ] Credentials not logged.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- Async version using `httpx.AsyncClient`.
- Rate limiting.
- Response caching.
- OpenAPI spec generation.
