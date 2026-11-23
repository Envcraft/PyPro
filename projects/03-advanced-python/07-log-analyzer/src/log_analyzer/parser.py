"""Log parsing engine using regular expressions.

Extracts timestamp, log level, and message while safely validating structure
and handling malformed entries without breaking streaming pipelines.
"""

from __future__ import annotations

from datetime import datetime
import re

from log_analyzer.models import VALID_LEVELS, LogEntry

# Regex pattern matching: YYYY-MM-DD HH:MM:SS LEVEL MESSAGE
# Tolerates multiple spaces between tokens, empty messages, and captures named groups.
LOG_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>[A-Za-z]+)(?:\s+(?P<message>.*))?$"
)


def parse_line(line: str, line_number: int | None = None) -> LogEntry | None:
    """Parse a single raw log line into a structured LogEntry.

    Args:
        line: Raw log line string.
        line_number: Optional 1-based source line number.

    Returns:
        LogEntry if line is structurally valid and contains a supported log level
        and valid timestamp; None if the line is malformed.
    """
    stripped_line = line.strip()
    if not stripped_line:
        return None

    match = LOG_PATTERN.match(stripped_line)
    if match is None:
        return None

    date_part = match.group("date")
    time_part = match.group("time")
    level_raw = match.group("level")
    raw_message = match.group("message")

    # Validate log level strictly against supported levels
    if level_raw not in VALID_LEVELS:
        return None

    # Parse and validate the datetime strictly (handles invalid calendar days/times)
    timestamp_str = f"{date_part} {time_part}"
    try:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

    message = raw_message if raw_message is not None else ""

    return LogEntry(
        timestamp=timestamp,
        level=level_raw,
        message=message,
        line_number=line_number,
    )
