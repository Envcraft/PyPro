# Project 07 — Log Analyzer
## Fast, Streaming, Memory-Efficient Production-Grade Log Analysis

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-standard%20library-brightgreen.svg)](https://docs.python.org/3/library/)
[![Tests](https://img.shields.io/badge/tests-48%20passed-success.svg)]()

---

## 1. Project Overview

**Log Analyzer** is a high-performance command-line utility built entirely with Python's standard library. It processes large log files line by line using lazy generator pipelines, extracts structured metadata with regular expressions, computes incremental statistical metrics via `collections.Counter` and `collections.defaultdict`, and exports analysis reports to formatted JSON and streaming CSV.

Designed under production software engineering principles, the application never loads complete datasets into memory, maintaining an $O(1)$ memory footprint while parsing and summarizing logs containing millions of lines.

---

## 2. Problem Statement

Modern backend applications, cloud environments, and container platforms generate gigabytes or terabytes of structured textual logs daily. Analyzing these files presents critical challenges:
- **Out of Memory (OOM) Failures:** Traditional approaches using `file.readlines()` or loading complete dataframes (e.g., via pandas) attempt to allocate memory proportional to the file size ($O(N)$), crashing when log files exceed available physical RAM.
- **Corrupted Lines and Non-Uniformities:** Real-world logs often contain truncated lines, network-scrambled payloads, or unsupported log levels. A fragile parser that crashes halts the entire ingestion pipeline.
- **Dependency Overhead:** In resource-constrained deployment runners, secure enclaves, or air-gapped environments, installing heavy third-party parsing dependencies or data analysis frameworks is often prohibited or undesirable.

**Log Analyzer solves this** by leveraging Python's streaming primitives (`yield`, file iterators, `Counter`) to process files of arbitrary size safely, predictably, and with zero third-party dependencies.

---

## 3. Features

- **Streaming Line Ingestion:** Reads log files line-by-line using Python generator iterators without buffering lines in RAM.
- **Robust Regex Parsing:** Validates log entries against a strict format while safely isolating malformed lines without pipeline interruption.
- **Calendar & Time Validation:** Converts timestamp strings to Python `datetime` instances, validating genuine calendar dates (rejecting out-of-range months, days, minutes, or seconds).
- **Incremental Statistical Aggregation:** Continuously updates log level frequencies, message groupings, time boundaries, and recurring error counts.
- **Top-N Error Identification:** Detects and ranks recurring error messages using optimized heap/counter algorithms.
- **Dynamic Filtering:** Supports filtering entries by log level and case-insensitive keyword searches on the fly.
- **Streaming CSV Export:** Writes parsed entries directly to CSV using `csv.DictWriter` concurrently with analysis.
- **Formatted JSON Export:** Serializes complete aggregate metrics and ISO 8601 timestamps to human-readable UTF-8 JSON.
- **Input Overwrite Protection:** Safeguards input files against accidental overwriting by JSON/CSV output destinations.
- **Zero Third-Party Dependencies:** 100% Python standard library (`pathlib`, `re`, `collections`, `datetime`, `csv`, `json`, `argparse`, `unittest`).

---

## 4. Supported Log Format

The analyzer parses structured text records following standard syslog and service conventions:

```text
YYYY-MM-DD HH:MM:SS LEVEL MESSAGE
```

### Supported Log Levels
- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

### Examples

```log
2026-11-23 08:00:00 INFO Service initialized on port 8080
2026-11-23 08:00:05 DEBUG Configuration loaded successfully: 42 keys
2026-11-23 08:02:16 WARNING High memory usage detected: 85%
2026-11-23 08:02:20 ERROR Database connection failed: connection refused on port 5432
2026-11-23 08:06:00 CRITICAL Primary database cluster is unreachable
```

Malformed entries (e.g., missing levels, invalid timestamps, arbitrary text) are skipped safely, and their count is recorded in the statistical summary.

---

## 5. Project Structure

```text
07-log-analyzer/
│
├── main.py                          # Top-level CLI application entrypoint
├── pyproject.toml                   # Project metadata and packaging configuration
├── .gitignore                       # Git exclusions (preserves fixtures and .gitkeep)
├── README.md                        # Complete project documentation
│
├── src/
│   ├── main.py                      # Module entrypoint delegating to cli.py
│   └── log_analyzer/
│       ├── __init__.py              # Package descriptor and versioning
│       ├── models.py                # LogEntry and LogSummary dataclasses
│       ├── reader.py                # Generator-based line streamer (FR-01)
│       ├── parser.py                # Regex extraction and validation engine (FR-02)
│       ├── analyzer.py              # Incremental Counter and defaultdict analytics (FR-03, FR-04, FR-05)
│       ├── exporter.py              # UTF-8 JSON and streaming CSV export (FR-06, FR-07)
│       └── cli.py                   # Argparse CLI interface and formatting (FR-08)
│
├── tests/
│   ├── __init__.py                  # Test package initialization with sys.path resolution
│   ├── fixtures/
│   │   ├── sample.log               # Deterministic multi-level dataset with known edge cases
│   │   ├── empty.log                # 0-byte log file fixture
│   │   └── malformed.log            # Purely invalid entries fixture
│   ├── test_reader.py               # Unit tests for reader generator behavior
│   ├── test_parser.py               # Unit tests for regex and datetime validation
│   ├── test_analyzer.py             # Unit tests for statistical counters, top errors, and filters
│   ├── test_exporter.py             # Unit tests for JSON and CSV exporters
│   ├── test_cli.py                  # Unit tests for command line parsing and exit codes
│   └── test_main.py                 # Integration tests for core entrypoints
│
├── tools/
│   └── generate_large_logs.py       # Deterministic synthetic log generator (benchmark tool)
│
├── output/
│   └── .gitkeep                     # Placeholder directory for generated exports
│
└── docs/
    └── LEARNING_NOTES.md            # In-depth architectural & conceptual guide
```

---

## 6. Python Concepts Practiced

| Python Concept | Standard Library Module | Practical Application in Project |
| :--- | :--- | :--- |
| **Generators & Yield** | Built-in (`yield`) | Lazy file streaming without memory buffering ($O(1)$ memory) |
| **Regular Expressions** | `re` | Compiling token-matching patterns to extract date, level, message |
| **Multisets / Counting** | `collections.Counter` | Tracking log level frequencies and top-N recurring errors |
| **Grouping Structures** | `collections.defaultdict` | Categorizing error messages per log level without KeyError |
| **Temporal Data** | `datetime.datetime` | Validating true calendar dates and calculating time intervals |
| **Tabular Serialization** | `csv` (`csv.DictWriter`) | Streaming parsed records directly to disk with standard escaping |
| **Structured Output** | `json` | Serializing analysis summaries with custom ISO date serialization |
| **Path Manipulation** | `pathlib.Path` | Robust cross-platform path resolution, checks, and parent directory creation |
| **CLI Argument Parsing** | `argparse` | POSIX-compliant flags, type coercion, and user-friendly error messages |
| **Immutable Models** | `dataclasses` (`slots=True`) | High-speed, memory-efficient structured representations |
| **Unit Testing** | `unittest` | Deterministic unit tests with mocking, fixture isolation, and edge-case validation |

---

## 7. Installation & Setup

### Prerequisites
- Python 3.12 or newer (Tested on Python 3.14.5).
- No external packages or package managers required.

### Setup Instructions
1. Navigate to the project root directory:
   ```bash
   cd projects/03-advanced-python/07-log-analyzer
   ```
2. Verify Python version:
   ```bash
   python --version
   ```

---

## 8. Usage

Run the analyzer via the `main.py` entrypoint:

```bash
# Basic analysis with summary printed to stdout
python main.py analyze tests/fixtures/sample.log

# Direct invocation (analyze is default command)
python main.py tests/fixtures/sample.log
```

### Example Terminal Output

```text
====================================================================
                    LOG ANALYSIS SUMMARY REPORT                     
====================================================================
File Path:          tests/fixtures/sample.log
Total Lines:        26
Parsed Entries:     21
Malformed Entries:  5
--------------------------------------------------------------------
Log Level Distribution:
  DEBUG:            3
  INFO:             7
  WARNING:          3
  ERROR:            6
  CRITICAL:         2
--------------------------------------------------------------------
Time Range:
  Earliest:         2026-11-23 08:00:00
  Latest:           2026-11-23 11:30:00
--------------------------------------------------------------------
Top 3 Error Messages (Total Errors: 6, Critical: 2):
  1. [3x] Database connection failed: connection refused on port 5432
  2. [2x] Authentication failed for user admin
  3. [1x] Disk quota exceeded for volume /var/log
--------------------------------------------------------------------
Note: 5 malformed line(s) were safely skipped.
====================================================================
```

---

## 9. CLI Options

```text
usage: log-analyzer analyze [-h] [--json-output PATH] [--csv-output PATH]
                           [--top N] [--level LEVEL] [--keyword TEXT]
                           file

positional arguments:
  file                Path to the log file to analyze.

options:
  -h, --help          show this help message and exit
  --json-output PATH  Path to export the statistical summary as JSON.
  --csv-output PATH   Path to export parsed log entries as CSV.
  --top N             Number of most frequent error messages to display (default: 10).
  --level LEVEL       Filter entries by log level (CRITICAL, DEBUG, ERROR, INFO, WARNING).
  --keyword TEXT      Filter log entries containing case-insensitive keyword in message.
```

### Common CLI Command Examples

```bash
# Export summary metrics to JSON
python main.py analyze tests/fixtures/sample.log --json-output output/summary.json

# Export all parsed entries to CSV
python main.py analyze tests/fixtures/sample.log --csv-output output/entries.csv

# Extract top 5 recurring errors
python main.py analyze tests/fixtures/sample.log --top 5

# Filter for ERROR logs containing the keyword "database" and export matches to CSV
python main.py analyze tests/fixtures/sample.log --level ERROR --keyword database --csv-output output/db_errors.csv
```

---

## 10. JSON Export Example

When `--json-output output/summary.json` is specified:

```json
{
  "file_path": "tests/fixtures/sample.log",
  "total_lines": 26,
  "parsed_entries": 21,
  "malformed_entries": 5,
  "level_counts": {
    "DEBUG": 3,
    "INFO": 7,
    "WARNING": 3,
    "ERROR": 6,
    "CRITICAL": 2
  },
  "total_errors": 6,
  "total_critical": 2,
  "earliest_timestamp": "2026-11-23 08:00:00",
  "latest_timestamp": "2026-11-23 11:30:00",
  "top_errors": [
    {
      "message": "Database connection failed: connection refused on port 5432",
      "count": 3
    },
    {
      "message": "Authentication failed for user admin",
      "count": 2
    },
    {
      "message": "Disk quota exceeded for volume /var/log",
      "count": 1
    }
  ]
}
```

---

## 11. CSV Export Example

When `--csv-output output/entries.csv` is specified:

```csv
timestamp,level,message
2026-11-23 08:00:00,INFO,Service initialized on port 8080
2026-11-23 08:00:05,DEBUG,Configuration loaded successfully: 42 keys
2026-11-23 08:01:10,INFO,Incoming request GET /api/v1/health from 192.168.1.10
2026-11-23 08:02:16,WARNING,High memory usage detected: 85%
2026-11-23 08:02:20,ERROR,Database connection failed: connection refused on port 5432
2026-11-23 08:06:00,CRITICAL,Primary database cluster is unreachable
```

---

## 12. Test Execution

The project includes an extensive unit test suite written with Python's standard `unittest` framework.

### Running All Unit Tests

From the project root:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Running Individual Test Modules

```bash
# Test file reader
python -m unittest tests/test_reader.py

# Test regex parser
python -m unittest tests/test_parser.py

# Test statistical analyzer
python -m unittest tests/test_analyzer.py

# Test JSON/CSV exporters
python -m unittest tests/test_exporter.py

# Test command line interface
python -m unittest tests/test_cli.py
```

### Current Test Suite Status
```text
Ran 48 tests in 0.060s
OK
```

---

## 13. Synthetic Dataset Generation

To benchmark performance without committing large files to version control, use the provided synthetic log generator in `tools/generate_large_logs.py`:

```bash
# Generate 100,000 synthetic log lines (deterministic with seed 42)
python tools/generate_large_logs.py --count 100000 --output tests/fixtures/large.log --seed 42

# Generate with 5% malformed lines
python tools/generate_large_logs.py --count 50000 --malformed-percent 5.0 --output tests/fixtures/corrupted.log

# Stream directly to pipeline via stdout/pipe (zero intermediate disk storage)
python tools/generate_large_logs.py --count 10000 | python main.py -
```

### Generator Capabilities
- **Deterministic:** Produces identical output streams given the same `--seed`.
- **Realistic Data:** Models weighted distributions (50% INFO, 25% DEBUG, 12% WARNING, 10% ERROR, 3% CRITICAL).
- **Repetitive Error Templates:** Generates realistic repeating errors for accurate top-N ranking tests.
- **Incremental Streaming:** Streams lines directly to disk or stdout without allocating entries in memory.

---

## 14. Memory-Efficiency Design

The application implements an end-to-end streaming architecture:

```text
[ Disk File: 10 GB ]
        │
        ▼ (O(1) line buffer)
[ reader.py: read_log_lines() ] ── yields (line_number, raw_line)
        │
        ▼
[ parser.py: parse_line() ] ───── yields LogEntry (or None if malformed)
        │
        ├──► [ analyzer.py: process_entry() ] ── incremental Counter updates (O(1))
        │
        └──► [ exporter.py: export_csv() ]   ── streaming csv.writer row output (O(1))
```

### Key Architectural Choices:
1. **Never use `readlines()` or `read()`:** Python's standard file iteration (`for line in file:`) utilizes an internal 8KB buffer, loading lines as needed and discarding them upon next iteration.
2. **Generators (`yield`):** Each pipeline component acts as a lazy producer-consumer, pulling single items on demand.
3. **Incremental Statistics:** Earliest and latest timestamps are tracked with simple min/max comparisons (`entry.timestamp < self.earliest_timestamp`), never requiring an in-memory list of dates.
4. **Single-Pass Execution:** When both analysis and CSV export are requested, the file is read exactly once; parsed records update counters and are written to the CSV file simultaneously.

---

## 15. Limitations

- **Unique Error Message Memory Proportionality:** While level counts, timestamps, and line counts consume strict $O(1)$ memory, aggregating unique error messages in `collections.Counter` requires memory proportional to the number of *distinct* error strings ($O(U)$ where $U$ is unique messages). In pathological scenarios where every error message is completely unique (e.g., embedding unique UUIDs or timestamps inside the error text), the Counter dictionary grows linearly with $U$.
- **Single Log Format:** The current regex engine parses the standard `YYYY-MM-DD HH:MM:SS LEVEL MESSAGE` format. Structured JSON logs or alternative timestamp formats (e.g., Apache/Nginx format) require pattern adaptation.
- **Single-Threaded Processing:** Streaming runs on a single CPU core. While parsing 100,000 lines executes in ~3 seconds, extremely large multi-gigabyte files could benefit from parallel chunk streaming.

---

## 16. Future Improvements

Documented as planned extensions for future iterations:
- **Multiple Log Formats:** Configurable regex templates and automated format auto-detection (Syslog RFC 5424, Nginx access logs, Django default logs).
- **JSON Lines (`.jsonl`) Parser:** Streaming JSON line ingestion without regex.
- **Real-Time Log Tailing:** Streaming live file additions using `tail -f` polling loops with non-blocking generator yields.
- **Time-Windowed Anomaly Detection:** Tracking error frequency spikes across rolling 5-minute sliding windows.
- **Multi-File Batch Analysis:** Analyzing log directories using concurrent file worker threads.
