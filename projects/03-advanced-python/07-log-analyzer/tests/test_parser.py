"""Unit tests for regular expression log parsing."""

from datetime import datetime
from pathlib import Path
import sys
import unittest

project_root = Path(__file__).resolve().parent.parent
src_dir = project_root / "src"
for path_str in (str(project_root), str(src_dir)):
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from log_analyzer.models import LogEntry
from log_analyzer.parser import parse_line


class TestParser(unittest.TestCase):
    """Test suite validating regex parsing and date validation."""

    def test_parse_valid_debug_entry(self) -> None:
        """Verify parsing a valid DEBUG entry."""
        line = "2026-11-23 10:01:08 DEBUG Cache lookup completed"
        entry = parse_line(line, line_number=1)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.timestamp, datetime(2026, 11, 23, 10, 1, 8))
        self.assertEqual(entry.level, "DEBUG")
        self.assertEqual(entry.message, "Cache lookup completed")
        self.assertEqual(entry.line_number, 1)

    def test_parse_valid_info_entry(self) -> None:
        """Verify parsing a valid INFO entry."""
        line = "2026-11-23 10:01:01 INFO Server started"
        entry = parse_line(line)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.timestamp, datetime(2026, 11, 23, 10, 1, 1))
        self.assertEqual(entry.level, "INFO")
        self.assertEqual(entry.message, "Server started")

    def test_parse_valid_warning_entry(self) -> None:
        """Verify parsing a valid WARNING entry."""
        line = "2026-11-23 10:01:06 WARNING Response took 4.2 seconds"
        entry = parse_line(line)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.timestamp, datetime(2026, 11, 23, 10, 1, 6))
        self.assertEqual(entry.level, "WARNING")
        self.assertEqual(entry.message, "Response took 4.2 seconds")

    def test_parse_valid_error_entry(self) -> None:
        """Verify parsing a valid ERROR entry."""
        line = "2026-11-23 10:01:03 ERROR Database connection failed"
        entry = parse_line(line)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.timestamp, datetime(2026, 11, 23, 10, 1, 3))
        self.assertEqual(entry.level, "ERROR")
        self.assertEqual(entry.message, "Database connection failed")

    def test_parse_valid_critical_entry(self) -> None:
        """Verify parsing a valid CRITICAL entry."""
        line = "2026-11-23 10:01:07 CRITICAL Database unavailable"
        entry = parse_line(line)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.timestamp, datetime(2026, 11, 23, 10, 1, 7))
        self.assertEqual(entry.level, "CRITICAL")
        self.assertEqual(entry.message, "Database unavailable")

    def test_invalid_calendar_timestamp_returns_none(self) -> None:
        """Verify impossible calendar values (month 99, minute 99) return None."""
        line = "2026-11-23 10:99:99 ERROR Invalid time"
        self.assertIsNone(parse_line(line))

        line2 = "2026-02-30 10:00:00 INFO February 30th does not exist"
        self.assertIsNone(parse_line(line2))

    def test_invalid_level_returns_none(self) -> None:
        """Verify unsupported levels (TRACE, VERBOSE, lowercase info) return None."""
        self.assertIsNone(parse_line("2026-11-23 10:00:00 TRACE Entering func"))
        self.assertIsNone(parse_line("2026-11-23 10:00:00 info Lowercase level"))
        self.assertIsNone(parse_line("2026-11-23 10:00:00 CUSTOM Custom level"))

    def test_malformed_lines_return_none(self) -> None:
        """Verify arbitrary text, missing components, or inverted syntax return None."""
        self.assertIsNone(parse_line("NOT A LOG LINE"))
        self.assertIsNone(parse_line("2026-11-23-10:00:00 INFO Missing space delimiter"))
        self.assertIsNone(parse_line("10:00:00 2026-11-23 INFO Swapped date and time"))
        self.assertIsNone(parse_line(""))
        self.assertIsNone(parse_line("    "))

    def test_empty_message_allowed(self) -> None:
        """Verify an entry with valid timestamp and level but empty message is parsed."""
        line = "2026-11-23 10:00:00 INFO"
        entry = parse_line(line)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.level, "INFO")
        self.assertEqual(entry.message, "")

        line_with_spaces = "2026-11-23 10:00:00 INFO    "
        entry_spaces = parse_line(line_with_spaces)
        self.assertIsNotNone(entry_spaces)
        self.assertEqual(entry_spaces.message, "")

    def test_extra_spaces_tolerated(self) -> None:
        """Verify parser tolerates multiple spaces between tokens."""
        line = "2026-11-23   10:00:00    WARNING    Memory threshold reached"
        entry = parse_line(line)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.level, "WARNING")
        self.assertEqual(entry.message, "Memory threshold reached")


if __name__ == "__main__":
    unittest.main()
