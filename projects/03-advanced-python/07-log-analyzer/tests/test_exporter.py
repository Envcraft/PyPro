"""Unit tests for JSON and CSV exporters."""

import csv
from datetime import datetime
import json
from pathlib import Path
import sys
import tempfile
import unittest

project_root = Path(__file__).resolve().parent.parent
src_dir = project_root / "src"
for path_str in (str(project_root), str(src_dir)):
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from log_analyzer.exporter import export_csv, export_json
from log_analyzer.models import LogEntry, LogSummary


class TestExporter(unittest.TestCase):
    """Test suite for export_json and export_csv."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_export_json_valid_summary(self) -> None:
        """Verify JSON export creates valid UTF-8 JSON with all expected fields."""
        summary = LogSummary(
            file_path="sample.log",
            total_lines=10,
            parsed_entries=8,
            malformed_entries=2,
            level_counts={"INFO": 5, "ERROR": 3},
            top_errors=[("DB timeout", 3)],
            earliest_timestamp=datetime(2026, 11, 23, 8, 0, 0),
            latest_timestamp=datetime(2026, 11, 23, 8, 30, 0),
        )

        out_path = self.test_dir / "nested" / "summary.json"
        result_path = export_json(summary, out_path)

        self.assertTrue(result_path.exists())
        with result_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["file_path"], "sample.log")
        self.assertEqual(data["total_lines"], 10)
        self.assertEqual(data["parsed_entries"], 8)
        self.assertEqual(data["malformed_entries"], 2)
        self.assertEqual(data["level_counts"]["INFO"], 5)
        self.assertEqual(data["level_counts"]["ERROR"], 3)
        self.assertEqual(data["total_errors"], 3)
        self.assertEqual(data["earliest_timestamp"], "2026-11-23 08:00:00")
        self.assertEqual(data["latest_timestamp"], "2026-11-23 08:30:00")
        self.assertEqual(len(data["top_errors"]), 1)
        self.assertEqual(data["top_errors"][0]["message"], "DB timeout")

    def test_export_json_empty_summary(self) -> None:
        """Verify JSON export works cleanly on an empty summary."""
        summary = LogSummary()
        out_path = self.test_dir / "empty_summary.json"
        export_json(summary, out_path)

        with out_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["total_lines"], 0)
        self.assertIsNone(data["earliest_timestamp"])
        self.assertIsNone(data["latest_timestamp"])
        self.assertEqual(data["top_errors"], [])

    def test_export_csv_streaming(self) -> None:
        """Verify CSV export writes headers and formats rows properly."""
        entries = [
            LogEntry(datetime(2026, 1, 1, 10, 0, 0), "INFO", "Server started"),
            LogEntry(datetime(2026, 1, 1, 10, 1, 0), "ERROR", 'Comma, "quotes", and\nnewlines'),
            LogEntry(datetime(2026, 1, 1, 10, 2, 0), "WARNING", "High memory"),
        ]

        out_path = self.test_dir / "entries.csv"
        written_count = export_csv(iter(entries), out_path)

        self.assertEqual(written_count, 3)
        self.assertTrue(out_path.exists())

        with out_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.assertEqual(rows[0], ["timestamp", "level", "message"])
        self.assertEqual(rows[1], ["2026-01-01 10:00:00", "INFO", "Server started"])
        self.assertEqual(rows[2], ["2026-01-01 10:01:00", "ERROR", 'Comma, "quotes", and\nnewlines'])
        self.assertEqual(rows[3], ["2026-01-01 10:02:00", "WARNING", "High memory"])

    def test_export_csv_empty_iterable(self) -> None:
        """Verify CSV export on empty iterable writes header and 0 rows."""
        out_path = self.test_dir / "empty.csv"
        written = export_csv([], out_path)
        self.assertEqual(written, 0)

        with out_path.open("r", newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ["timestamp", "level", "message"])

    def test_prevents_overwriting_input_file(self) -> None:
        """Verify export functions raise ValueError if output path matches input path."""
        target_file = self.test_dir / "data.log"
        target_file.touch()

        with self.assertRaises(ValueError):
            export_json(LogSummary(), target_file, input_path=target_file)

        with self.assertRaises(ValueError):
            export_csv([], target_file, input_path=target_file)


if __name__ == "__main__":
    unittest.main()
