"""Streaming log file reader.

Reads log files line by line using Python generators to maintain O(1)
memory consumption regardless of file size.
"""

from __future__ import annotations

from pathlib import Path
from typing import Generator


def read_log_lines(
    file_path: str | Path,
    encoding: str = "utf-8",
    errors: str = "replace",
) -> Generator[tuple[int, str], None, None]:
    """Yield line numbers and stripped lines one by one from a log file.

    Args:
        file_path: Path to the log file to read.
        encoding: File character encoding (default: utf-8).
        errors: Encoding error handling strategy (default: replace).

    Yields:
        Tuples of (line_number, line_text) where line_number is 1-based and
        trailing line terminators (\r, \n) are stripped.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IsADirectoryError: If the specified path points to a directory.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    if path.is_dir():
        raise IsADirectoryError(f"Expected a log file, but found a directory: {path}")

    with path.open("r", encoding=encoding, errors=errors) as file_handle:
        for line_number, raw_line in enumerate(file_handle, start=1):
            yield line_number, raw_line.rstrip("\r\n")


def read_log_raw(
    file_path: str | Path,
    encoding: str = "utf-8",
    errors: str = "replace",
) -> Generator[str, None, None]:
    """Yield raw line strings one by one from a log file.

    Args:
        file_path: Path to the log file to read.
        encoding: File character encoding (default: utf-8).
        errors: Encoding error handling strategy (default: replace).

    Yields:
        Line string stripped of trailing newline characters.
    """
    for _, line in read_log_lines(file_path, encoding=encoding, errors=errors):
        yield line
