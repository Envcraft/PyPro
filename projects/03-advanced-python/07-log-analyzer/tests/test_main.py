"""Integration and unit tests for Log Analyzer main functions."""

from datetime import datetime
from pathlib import Path
import sys
import unittest

project_root = Path(__file__).resolve().parent.parent
src_dir = project_root / "src"
for path_str in (str(project_root), str(src_dir)):
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from log_analyzer.analyzer import count_by_level, get_errors
from log_analyzer.models import LogEntry
from log_analyzer.parser import parse_line

SAMPLE_LOG_LINE = "2024-01-15 10:23:45 ERROR Database connection failed"
MALFORMED_LINE = "this is not a valid log line"


class TestParseLine(unittest.TestCase):
    """Test parse_line behavior with sample lines."""

    def test_parses_valid_line(self) -> None:
        entry = parse_line(SAMPLE_LOG_LINE)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.level, "ERROR")
        self.assertEqual(entry.message, "Database connection failed")

    def test_returns_none_for_malformed_line(self) -> None:
        entry = parse_line(MALFORMED_LINE)
        self.assertIsNone(entry)

    def test_extracts_timestamp(self) -> None:
        entry = parse_line(SAMPLE_LOG_LINE)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.timestamp, datetime(2024, 1, 15, 10, 23, 45))

    def test_extracts_log_level(self) -> None:
        entry = parse_line(SAMPLE_LOG_LINE)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.level, "ERROR")


class TestCountByLevel(unittest.TestCase):
    """Test counting log entries by level."""

    def test_counts_each_level(self) -> None:
        entries = [
            LogEntry(datetime(2026, 1, 1, 10, 0), "INFO", "Started"),
            LogEntry(datetime(2026, 1, 1, 10, 1), "INFO", "Ready"),
            LogEntry(datetime(2026, 1, 1, 10, 2), "ERROR", "Failed"),
            LogEntry(datetime(2026, 1, 1, 10, 3), "DEBUG", "Traced"),
        ]
        counts = count_by_level(entries)
        self.assertEqual(counts["INFO"], 2)
        self.assertEqual(counts["ERROR"], 1)
        self.assertEqual(counts["DEBUG"], 1)
        self.assertEqual(counts["CRITICAL"], 0)


class TestGetErrors(unittest.TestCase):
    """Test extracting error and critical log entries."""

    def test_returns_only_error_and_critical(self) -> None:
        entries = [
            LogEntry(datetime(2026, 1, 1, 10, 0), "INFO", "Started"),
            LogEntry(datetime(2026, 1, 1, 10, 1), "ERROR", "Error 1"),
            LogEntry(datetime(2026, 1, 1, 10, 2), "WARNING", "Warning 1"),
            LogEntry(datetime(2026, 1, 1, 10, 3), "CRITICAL", "Critical 1"),
            LogEntry(datetime(2026, 1, 1, 10, 4), "DEBUG", "Debug 1"),
        ]
        errors = list(get_errors(entries))
        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[0].level, "ERROR")
        self.assertEqual(errors[1].level, "CRITICAL")


if __name__ == "__main__":
    unittest.main()
