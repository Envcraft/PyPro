"""Unit tests for the CLI module and execution flows."""

import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

project_root = Path(__file__).resolve().parent.parent
src_dir = project_root / "src"
for path_str in (str(project_root), str(src_dir)):
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from log_analyzer.cli import main, run_pipeline


class TestCLI(unittest.TestCase):
    """Test suite for CLI arguments, exit codes, and output formatting."""

    def setUp(self) -> None:
        self.fixtures_dir = Path(__file__).parent / "fixtures"
        self.sample_log = self.fixtures_dir / "sample.log"
        self.empty_log = self.fixtures_dir / "empty.log"
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_cli_basic_analyze_command(self) -> None:
        """Verify python main.py analyze sample.log exits 0 and prints report."""
        stdout_capture = io.StringIO()
        with patch("sys.stdout", stdout_capture):
            exit_code = main(["analyze", str(self.sample_log)])

        self.assertEqual(exit_code, 0)
        output = stdout_capture.getvalue()
        self.assertIn("LOG ANALYSIS SUMMARY REPORT", output)
        self.assertIn("Total Lines:        26", output)
        self.assertIn("Parsed Entries:     21", output)
        self.assertIn("Malformed Entries:  5", output)
        self.assertIn("Database connection failed", output)

    def test_cli_direct_invocation_without_subcommand(self) -> None:
        """Verify python main.py sample.log defaults to analyze."""
        stdout_capture = io.StringIO()
        with patch("sys.stdout", stdout_capture):
            exit_code = main([str(self.sample_log)])

        self.assertEqual(exit_code, 0)
        self.assertIn("Total Lines:        26", stdout_capture.getvalue())

    def test_cli_json_export_option(self) -> None:
        """Verify --json-output writes valid JSON summary."""
        json_file = self.output_dir / "summary.json"
        with patch("sys.stdout", io.StringIO()):
            exit_code = main(["analyze", str(self.sample_log), "--json-output", str(json_file)])
        self.assertEqual(exit_code, 0)
        self.assertTrue(json_file.exists())
        self.assertGreater(json_file.stat().st_size, 0)

    def test_cli_csv_export_option(self) -> None:
        """Verify --csv-output writes entries CSV."""
        csv_file = self.output_dir / "entries.csv"
        with patch("sys.stdout", io.StringIO()):
            exit_code = main(["analyze", str(self.sample_log), "--csv-output", str(csv_file)])
        self.assertEqual(exit_code, 0)
        self.assertTrue(csv_file.exists())
        self.assertGreater(csv_file.stat().st_size, 0)

    def test_cli_level_and_keyword_filtering(self) -> None:
        """Verify --level and --keyword filter correctly and export matched entries."""
        csv_file = self.output_dir / "filtered.csv"
        stdout_capture = io.StringIO()
        with patch("sys.stdout", stdout_capture):
            exit_code = main([
                "analyze",
                str(self.sample_log),
                "--level", "ERROR",
                "--keyword", "database",
                "--csv-output", str(csv_file),
            ])

        self.assertEqual(exit_code, 0)
        output = stdout_capture.getvalue()
        self.assertIn("Level Filter:     ERROR", output)
        self.assertIn("Keyword Filter:   database", output)
        self.assertIn("Matching Entries: 3", output)
        self.assertIn("3 entries exported to:", output)
        self.assertTrue(csv_file.exists())

    def test_cli_missing_input_file_returns_code_1(self) -> None:
        """Verify non-existent input file prints error and returns exit code 1."""
        stderr_capture = io.StringIO()
        with patch("sys.stderr", stderr_capture):
            exit_code = main(["analyze", "non_existent_file.log"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Error: File not found", stderr_capture.getvalue())

    def test_cli_invalid_level_argument_returns_code_2(self) -> None:
        """Verify invalid log level argument returns exit code 2."""
        stderr_capture = io.StringIO()
        with patch("sys.stderr", stderr_capture):
            exit_code = main(["analyze", str(self.sample_log), "--level", "INVALID_LEVEL"])

        self.assertEqual(exit_code, 2)
        self.assertIn("Invalid log level", stderr_capture.getvalue())

    def test_cli_negative_top_argument_returns_code_2(self) -> None:
        """Verify negative --top value returns exit code 2."""
        stderr_capture = io.StringIO()
        with patch("sys.stderr", stderr_capture):
            exit_code = main(["analyze", str(self.sample_log), "--top", "-5"])

        self.assertEqual(exit_code, 2)
        self.assertIn("--top must be a non-negative integer", stderr_capture.getvalue())

    def test_cli_empty_file_handling(self) -> None:
        """Verify analyzing an empty file runs cleanly with 0 counts."""
        stdout_capture = io.StringIO()
        with patch("sys.stdout", stdout_capture):
            exit_code = main(["analyze", str(self.empty_log)])

        self.assertEqual(exit_code, 0)
        output = stdout_capture.getvalue()
        self.assertIn("Total Lines:        0", output)
        self.assertIn("Parsed Entries:     0", output)

    def test_cli_prevents_overwriting_input_file(self) -> None:
        """Verify specifying the input file as output path returns exit code 1."""
        stderr_capture = io.StringIO()
        with patch("sys.stderr", stderr_capture):
            exit_code = main([
                "analyze",
                str(self.sample_log),
                "--json-output",
                str(self.sample_log),
            ])

        self.assertEqual(exit_code, 1)
        self.assertIn("cannot overwrite input log file", stderr_capture.getvalue())


if __name__ == "__main__":
    unittest.main()
