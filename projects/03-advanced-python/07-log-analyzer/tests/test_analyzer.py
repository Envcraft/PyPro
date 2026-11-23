"""Unit tests for the log analyzer aggregation engine."""

from collections import Counter
from datetime import datetime
from pathlib import Path
import sys
import unittest

project_root = Path(__file__).resolve().parent.parent
src_dir = project_root / "src"
for path_str in (str(project_root), str(src_dir)):
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from log_analyzer.analyzer import (
    LogAnalyzer,
    analyze_stream,
    count_by_level,
    filter_entries,
    get_errors,
    search_entries,
    top_errors,
)
from log_analyzer.models import LogEntry
from log_analyzer.reader import read_log_lines


class TestAnalyzer(unittest.TestCase):
    """Test suite for LogAnalyzer and filtering functions."""

    def setUp(self) -> None:
        self.fixtures_dir = Path(__file__).parent / "fixtures"
        self.sample_log = self.fixtures_dir / "sample.log"
        self.empty_log = self.fixtures_dir / "empty.log"
        self.malformed_log = self.fixtures_dir / "malformed.log"

    def test_sample_file_line_counts(self) -> None:
        """Verify accurate total, valid, and malformed line counts for sample.log."""
        summary, analyzer = analyze_stream(
            read_log_lines(self.sample_log),
            file_path=str(self.sample_log),
            top_n=10,
        )
        self.assertEqual(summary.total_lines, 26)
        self.assertEqual(summary.parsed_entries, 21)
        self.assertEqual(summary.malformed_entries, 5)

    def test_sample_file_level_counts(self) -> None:
        """Verify exact level counts matching the sample fixture."""
        summary, _ = analyze_stream(read_log_lines(self.sample_log))
        self.assertEqual(summary.debug_count, 3)
        self.assertEqual(summary.info_count, 7)
        self.assertEqual(summary.warning_count, 3)
        self.assertEqual(summary.error_count, 6)
        self.assertEqual(summary.critical_count, 2)
        self.assertEqual(summary.total_errors, 6)
        self.assertEqual(summary.total_critical, 2)

    def test_sample_file_top_errors(self) -> None:
        """Verify frequency ordering and counts of recurring errors."""
        summary, _ = analyze_stream(read_log_lines(self.sample_log), top_n=2)
        # Should return top 2 errors
        self.assertEqual(len(summary.top_errors), 2)
        top1_msg, top1_count = summary.top_errors[0]
        self.assertEqual(
            top1_msg, "Database connection failed: connection refused on port 5432"
        )
        self.assertEqual(top1_count, 3)

        top2_msg, top2_count = summary.top_errors[1]
        self.assertEqual(top2_msg, "Authentication failed for user admin")
        self.assertEqual(top2_count, 2)

    def test_sample_file_time_range(self) -> None:
        """Verify earliest and latest timestamp computation."""
        summary, _ = analyze_stream(read_log_lines(self.sample_log))
        self.assertEqual(summary.earliest_timestamp, datetime(2026, 11, 23, 8, 0, 0))
        self.assertEqual(summary.latest_timestamp, datetime(2026, 11, 23, 11, 30, 0))

    def test_empty_file_analysis(self) -> None:
        """Verify behavior on an empty log file."""
        summary, _ = analyze_stream(
            read_log_lines(self.empty_log), file_path=str(self.empty_log)
        )
        self.assertEqual(summary.total_lines, 0)
        self.assertEqual(summary.parsed_entries, 0)
        self.assertEqual(summary.malformed_entries, 0)
        self.assertEqual(summary.debug_count, 0)
        self.assertEqual(summary.info_count, 0)
        self.assertEqual(summary.warning_count, 0)
        self.assertEqual(summary.error_count, 0)
        self.assertEqual(summary.critical_count, 0)
        self.assertIsNone(summary.earliest_timestamp)
        self.assertIsNone(summary.latest_timestamp)
        self.assertEqual(summary.top_errors, [])

    def test_malformed_only_file(self) -> None:
        """Verify behavior on a file containing only malformed lines."""
        summary, _ = analyze_stream(
            read_log_lines(self.malformed_log), file_path=str(self.malformed_log)
        )
        self.assertEqual(summary.total_lines, 7)
        self.assertEqual(summary.parsed_entries, 0)
        self.assertEqual(summary.malformed_entries, 7)
        self.assertIsNone(summary.earliest_timestamp)
        self.assertIsNone(summary.latest_timestamp)
        self.assertEqual(summary.top_errors, [])

    def test_messages_grouped_by_level_defaultdict(self) -> None:
        """Verify defaultdict groups message frequencies accurately per level."""
        _, analyzer = analyze_stream(read_log_lines(self.sample_log))
        # Ensure messages_by_level is populated for each level
        self.assertIn("INFO", analyzer.messages_by_level)
        self.assertIn("ERROR", analyzer.messages_by_level)
        self.assertEqual(
            analyzer.messages_by_level["WARNING"]["High memory usage detected: 85%"], 2
        )

    def test_filter_by_level(self) -> None:
        """Verify filter_entries isolates target level."""
        entries = [
            LogEntry(datetime(2026, 1, 1, 10, 0), "INFO", "Message 1"),
            LogEntry(datetime(2026, 1, 1, 10, 1), "ERROR", "Message 2"),
            LogEntry(datetime(2026, 1, 1, 10, 2), "WARNING", "Message 3"),
            LogEntry(datetime(2026, 1, 1, 10, 3), "ERROR", "Message 4"),
        ]
        errors = list(filter_entries(entries, level="ERROR"))
        self.assertEqual(len(errors), 2)
        self.assertTrue(all(e.level == "ERROR" for e in errors))

    def test_filter_by_keyword(self) -> None:
        """Verify case-insensitive keyword filtering."""
        entries = [
            LogEntry(datetime(2026, 1, 1, 10, 0), "INFO", "Database cache warm"),
            LogEntry(datetime(2026, 1, 1, 10, 1), "ERROR", "DATABASE connection timeout"),
            LogEntry(datetime(2026, 1, 1, 10, 2), "WARNING", "Network latency high"),
        ]
        matches = list(filter_entries(entries, keyword="database"))
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].level, "INFO")
        self.assertEqual(matches[1].level, "ERROR")

        # Test case-sensitive
        cs_matches = list(filter_entries(entries, keyword="DATABASE", case_sensitive=True))
        self.assertEqual(len(cs_matches), 1)
        self.assertEqual(cs_matches[0].level, "ERROR")

    def test_filter_by_both_level_and_keyword(self) -> None:
        """Verify combining level and keyword filters."""
        entries = [
            LogEntry(datetime(2026, 1, 1, 10, 0), "INFO", "Database cache warm"),
            LogEntry(datetime(2026, 1, 1, 10, 1), "ERROR", "Database connection timeout"),
            LogEntry(datetime(2026, 1, 1, 10, 2), "ERROR", "Disk full"),
        ]
        matches = list(filter_entries(entries, level="ERROR", keyword="database"))
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].message, "Database connection timeout")

    def test_standalone_functions(self) -> None:
        """Verify count_by_level, get_errors, search_entries, and top_errors functions."""
        entries = [
            LogEntry(datetime(2026, 1, 1, 10, 0), "INFO", "Login user 1"),
            LogEntry(datetime(2026, 1, 1, 10, 1), "ERROR", "Disk full"),
            LogEntry(datetime(2026, 1, 1, 10, 2), "CRITICAL", "System panic"),
            LogEntry(datetime(2026, 1, 1, 10, 3), "ERROR", "Disk full"),
        ]
        counts = count_by_level(entries)
        self.assertEqual(counts["INFO"], 1)
        self.assertEqual(counts["ERROR"], 2)
        self.assertEqual(counts["CRITICAL"], 1)

        err_list = list(get_errors(entries))
        self.assertEqual(len(err_list), 3)

        searched = list(search_entries(entries, "disk"))
        self.assertEqual(len(searched), 2)

        top = top_errors(entries, n=1)
        self.assertEqual(top, [("Disk full", 2)])


if __name__ == "__main__":
    unittest.main()
