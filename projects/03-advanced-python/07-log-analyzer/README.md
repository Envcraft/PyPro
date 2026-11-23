# Project 07: Log Analyzer

**Level:** Advanced Python
**Estimated Time:** 16–20 hours

---

## Overview

Build a log file analyser that reads large log files using generators, parses log entries with regular expressions, and produces statistical summaries. Supports JSON and CSV export.

---

## Objectives

- Use regular expressions to parse structured text.
- Use generators for memory-efficient file processing.
- Aggregate data with `collections.Counter`.
- Export results to JSON and CSV.

---

## Python Concepts Practised

- Regular expressions (`re` module)
- Generators (`yield`)
- `collections.Counter`
- `collections.defaultdict`
- File streaming (do not load entire file into memory)
- `csv` module
- `json` module
- `datetime` parsing

---

## Functional Requirements

1. Read log files line by line using a generator.
2. Parse log entries: timestamp, log level, message.
3. Count entries by log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
4. Extract all ERROR and CRITICAL entries.
5. Search entries by keyword.
6. Identify the most frequent error messages (top N).
7. Generate a summary: total lines, counts by level, time range.
8. Export summary to JSON.
9. Export entries to CSV.

---

## Non-Functional Requirements

- Must process large files without loading them entirely into memory.
- Parsing must use regular expressions.
- Use generators for the line-reading pipeline.

---

## Supported Log Format

```
2024-01-15 10:23:45 ERROR Database connection failed: timeout after 30s
2024-01-15 10:23:46 INFO Retrying connection (attempt 1 of 3)
2024-01-15 10:24:12 WARNING Memory usage at 85%
```

---

## Edge Cases

- Malformed log lines (do not crash).
- Empty log file.
- Log file not found.
- Lines with no recognisable level.
- Very large files.

---

## Acceptance Criteria

- [ ] Log lines parsed correctly with regex.
- [ ] Level counts are accurate.
- [ ] Generator used for file reading (no `readlines()`).
- [ ] Malformed lines are skipped with a count reported.
- [ ] JSON export contains the full summary.
- [ ] CSV export contains all parsed entries.

---

## Suggested Implementation Steps

1. Write the regex pattern for log line parsing.
2. Write the generator for reading and parsing lines.
3. Write the aggregation functions.
4. Write the summary generator.
5. Write the JSON export.
6. Write the CSV export.
7. Build the CLI.
8. Write tests using sample log files.

---

## Testing Requirements

- Test regex parsing against known log line formats.
- Test level counting accuracy.
- Test that malformed lines are skipped.
- Test that the generator reads line by line.
- Test JSON and CSV export format.

Create `tests/sample.log` with known content for deterministic testing.

---

## Constraints

- Standard library only.
- Must use generators.
- Must use `re` for parsing.

---

## Completion Checklist

- [ ] All functional requirements implemented.
- [ ] Generator used for file processing.
- [ ] Tests written and passing.
- [ ] Linting passes.
- [ ] Progress updated.

---

## Stretch Goals

- Support multiple log formats.
- Real-time log tailing (`tail -f` behaviour).
- Anomaly detection (spike in errors within a time window).
