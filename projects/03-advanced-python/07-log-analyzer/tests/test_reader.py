"""Unit tests for the streaming file reader."""

import sys
from inspect import isgenerator
from pathlib import Path
import tempfile
import unittest

project_root = Path(__file__).resolve().parent.parent
src_dir = project_root / "src"
for path_str in (str(project_root), str(src_dir)):
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from log_analyzer.reader import read_log_lines, read_log_raw


class TestReader(unittest.TestCase):
    """Test cases for the generator-based file reader."""

    def setUp(self) -> None:
        self.fixtures_dir = Path(__file__).parent / "fixtures"
        self.sample_log = self.fixtures_dir / "sample.log"
        self.empty_log = self.fixtures_dir / "empty.log"

    def test_returns_generator(self) -> None:
        """Verify that reader returns a generator object without consuming file immediately."""
        gen = read_log_lines(self.sample_log)
        self.assertTrue(isgenerator(gen))
        # Ensure raw reader also returns a generator
        raw_gen = read_log_raw(self.sample_log)
        self.assertTrue(isgenerator(raw_gen))

    def test_reads_sample_file_line_by_line(self) -> None:
        """Verify line-by-line reading with correct 1-based line numbering."""
        lines = list(read_log_lines(self.sample_log))
        self.assertEqual(len(lines), 26)
        first_num, first_line = lines[0]
        self.assertEqual(first_num, 1)
        self.assertTrue(first_line.startswith("2026-11-23 08:00:00 INFO"))

        last_num, last_line = lines[-1]
        self.assertEqual(last_num, 26)
        self.assertEqual(last_line, "2026-11-23 11:30:00 INFO Service shutdown complete")

    def test_empty_file_yields_nothing(self) -> None:
        """Verify empty log file completes immediately yielding zero lines."""
        lines = list(read_log_lines(self.empty_log))
        self.assertEqual(lines, [])

    def test_missing_file_raises_filenotfound(self) -> None:
        """Verify attempting to read a non-existent file raises FileNotFoundError upon invocation."""
        missing = self.fixtures_dir / "does_not_exist.log"
        gen = read_log_lines(missing)
        with self.assertRaises(FileNotFoundError):
            next(gen)

    def test_directory_path_raises_isadirectoryerror(self) -> None:
        """Verify attempting to read a directory raises IsADirectoryError."""
        gen = read_log_lines(self.fixtures_dir)
        with self.assertRaises(IsADirectoryError):
            next(gen)

    def test_handles_encoding_issues_gracefully(self) -> None:
        """Verify reader uses error replacement strategy for non-UTF8 bytes."""
        with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
            # Write invalid UTF-8 bytes (e.g. 0xFF, 0xFE in isolation)
            tmp.write(b"2026-11-23 10:00:00 INFO Valid line\n")
            tmp.write(b"2026-11-23 10:00:01 INFO Corrupt byte \xff\xfe here\n")
            tmp_path = Path(tmp.name)

        try:
            results = list(read_log_lines(tmp_path))
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0][0], 1)
            self.assertEqual(results[1][0], 2)
            # Unicode replacement character \ufffd should appear instead of crashing
            self.assertIn("\ufffd", results[1][1])
        finally:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
