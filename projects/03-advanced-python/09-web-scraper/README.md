# Project 09: Web Scraper

**Level:** Advanced Python
**Estimated Time:** 16–24 hours

---

## Overview

Build a web scraper that fetches web pages, parses HTML to extract structured data, deduplicates results, and persists them to CSV or SQLite. The scraper must respect rate limits and handle errors gracefully.

---

## Objectives

- Fetch and parse HTML.
- Extract structured data from DOM elements.
- Avoid duplicate records.
- Persist to CSV or SQLite.
- Implement rate limiting.

---

## Python Concepts Practised

- HTTP with `httpx`
- HTML parsing with `html.parser` or a third-party library
- Data extraction
- Deduplication
- CSV (`csv` module)
- SQLite (`sqlite3` module)
- Rate limiting (`time.sleep`)
- Error handling
- Logging

---

## Functional Requirements

1. Accept a list of URLs to scrape.
2. Fetch each URL with error handling.
3. Parse HTML to extract specified fields.
4. Deduplicate records by a unique field.
5. Persist results to CSV.
6. Optionally persist to SQLite.
7. Log each request: URL, status, fields extracted.
8. Log errors without stopping the entire run.
9. Respect a configurable delay between requests.

---

## Legal and Ethical Requirements

- Scrape only public, freely available web pages.
- Respect `robots.txt` where present.
- Use a reasonable delay (minimum 1 second between requests).
- Do not scrape pages that explicitly prohibit it.

---

## Edge Cases

- URL that returns 404.
- URL that times out.
- Page with missing expected fields.
- Duplicate URLs in the input list.
- HTML with inconsistent structure.
- Network failure mid-run.

---

## Acceptance Criteria

- [ ] At least one real site is scraped and results saved.
- [ ] Errors do not stop the entire scrape.
- [ ] Duplicates are detected and skipped.
- [ ] All results are written to CSV.
- [ ] Rate limiting delay is applied between requests.
- [ ] All operations are logged.

---

## Suggested Implementation Steps

1. Write the fetch function.
2. Write the HTML parser for the target site.
3. Write the deduplication check.
4. Write CSV export.
5. Write SQLite persistence.
6. Add rate limiting.
7. Add logging.
8. Write tests using mock HTML content.

---

## Testing Requirements

- Test HTML parsing with known HTML strings.
- Test deduplication logic.
- Test that failed requests are logged and skipped.
- Test CSV output format.

---

## Constraints

- Use only `httpx` and standard library.
- If using HTML parsing beyond `html.parser`, justify the dependency.

---

## Completion Checklist

- [ ] All functional requirements implemented.
- [ ] Rate limiting applied.
- [ ] Tests written and passing.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- Scrape multiple pages with pagination.
- Async scraping with `asyncio` and `httpx.AsyncClient`.
- Proxy support.
