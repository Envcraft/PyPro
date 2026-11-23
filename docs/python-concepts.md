# Python Concepts Reference

A quick-reference index of concepts covered across PyPro projects.

---

## Level 1 — Fundamentals

### Variables and Data Types
- `int`, `float`, `str`, `bool`
- Type conversion: `int()`, `float()`, `str()`
- Variable naming conventions

### Operators
- Arithmetic: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `and`, `or`, `not`

### Control Flow
- `if`, `elif`, `else`
- `while` loops
- `for` loops
- `break`, `continue`

### Functions
- `def` keyword
- Parameters and arguments
- Return values
- Default parameters

### Exception Handling
- `try`, `except`, `finally`
- Common exceptions: `ValueError`, `ZeroDivisionError`, `FileNotFoundError`
- Raising exceptions: `raise`

### Standard Library (Level 1)
- `random`: `random.randint()`
- `math`: basic mathematical functions

---

## Level 2 — Intermediate Python

### Collections
- `list`: indexing, slicing, methods
- `dict`: keys, values, items, methods
- `set`: uniqueness, set operations
- List comprehensions, dict comprehensions

### File I/O
- `open()`, context managers (`with`)
- Reading: `read()`, `readline()`, `readlines()`
- Writing: `write()`, `writelines()`
- Modes: `r`, `w`, `a`, `rb`, `wb`

### JSON
- `json.load()`, `json.loads()`
- `json.dump()`, `json.dumps()`

### pathlib
- `Path()`, `.exists()`, `.is_file()`, `.is_dir()`
- `.glob()`, `.rglob()`
- `.mkdir()`, `.rename()`, `.unlink()`

### OOP
- Classes, `__init__`, `self`
- Instance methods, class methods, static methods
- Inheritance
- `dataclasses.dataclass`
- `enum.Enum`

### Type Hints
- Basic: `int`, `str`, `list[str]`, `dict[str, int]`
- Optional: `str | None`
- `from typing import ...`

---

## Level 3 — Advanced Python

### Regular Expressions
- `re.match()`, `re.search()`, `re.findall()`
- Groups, quantifiers, anchors
- Compiled patterns: `re.compile()`

### Generators
- `yield` keyword
- Generator expressions
- Memory-efficient iteration

### Collections Module
- `Counter`, `defaultdict`, `OrderedDict`, `deque`

### HTTP and APIs
- `httpx` for HTTP requests
- Request/response cycle
- Status codes
- Headers, query parameters
- JSON serialisation

### HTML Parsing
- `html.parser` or `BeautifulSoup`
- DOM traversal
- Data extraction

---

## Level 4 — Backend Engineering

### SQLite
- `sqlite3` module
- DDL: `CREATE TABLE`, `ALTER TABLE`
- DML: `INSERT`, `UPDATE`, `DELETE`, `SELECT`
- Transactions: `commit()`, `rollback()`
- Parameterised queries

### Concurrency
- `asyncio`, `async`, `await`
- `asyncio.gather()`
- `threading.Thread`
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.ProcessPoolExecutor`

### Web Frameworks
- FastAPI: routes, request models, response models
- Pydantic for validation
- JWT authentication
- Dependency injection

### Testing (Advanced)
- `pytest` fixtures
- `pytest-asyncio` for async tests
- Mocking with `unittest.mock`
- API testing with `httpx.AsyncClient`
