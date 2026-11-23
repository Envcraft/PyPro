"""Statistical analysis and aggregation engine for log data.

Provides incremental, streaming aggregation using collections.Counter and
collections.defaultdict, calculating summary statistics with minimal memory overhead.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable
from datetime import datetime
from typing import Generator

from log_analyzer.models import LogEntry, LogSummary
from log_analyzer.parser import parse_line


class LogAnalyzer:
    """Incremental accumulator for streaming log statistics."""

    def __init__(self, file_path: str = "") -> None:
        self.file_path: str = file_path
        self.total_lines: int = 0
        self.parsed_entries: int = 0
        self.malformed_entries: int = 0
        self.level_counts: Counter[str] = Counter()
        self.error_counts: Counter[str] = Counter()
        self.critical_counts: Counter[str] = Counter()
        # Group message frequencies per log level using defaultdict
        self.messages_by_level: defaultdict[str, Counter[str]] = defaultdict(Counter)
        self.earliest_timestamp: datetime | None = None
        self.latest_timestamp: datetime | None = None

    def process_line(
        self,
        line: str,
        line_number: int | None = None,
    ) -> LogEntry | None:
        """Process a raw line incrementally, updating internal counters.

        Args:
            line: Raw unparsed log line string.
            line_number: Optional 1-based source line index.

        Returns:
            LogEntry if valid; None if malformed.
        """
        self.total_lines += 1
        entry = parse_line(line, line_number=line_number)
        if entry is not None:
            self.process_entry(entry)
        else:
            self.malformed_entries += 1
        return entry

    def process_entry(self, entry: LogEntry) -> None:
        """Incorporate a parsed LogEntry into running statistical counters.

        Args:
            entry: Structured log entry.
        """
        self.parsed_entries += 1
        self.level_counts[entry.level] += 1
        self.messages_by_level[entry.level][entry.message] += 1

        if entry.level == "ERROR":
            self.error_counts[entry.message] += 1
        elif entry.level == "CRITICAL":
            self.critical_counts[entry.message] += 1

        if self.earliest_timestamp is None or entry.timestamp < self.earliest_timestamp:
            self.earliest_timestamp = entry.timestamp
        if self.latest_timestamp is None or entry.timestamp > self.latest_timestamp:
            self.latest_timestamp = entry.timestamp

    def get_top_errors(self, n: int = 10) -> list[tuple[str, int]]:
        """Return the top N most frequent ERROR messages."""
        return self.error_counts.most_common(n)

    def get_summary(self, top_n: int = 10) -> LogSummary:
        """Produce an immutable snapshot of aggregate metrics."""
        return LogSummary(
            file_path=self.file_path,
            total_lines=self.total_lines,
            parsed_entries=self.parsed_entries,
            malformed_entries=self.malformed_entries,
            level_counts=dict(self.level_counts),
            top_errors=self.get_top_errors(top_n),
            earliest_timestamp=self.earliest_timestamp,
            latest_timestamp=self.latest_timestamp,
        )


def filter_entries(
    entries: Iterable[LogEntry],
    level: str | None = None,
    keyword: str | None = None,
    case_sensitive: bool = False,
) -> Generator[LogEntry, None, None]:
    """Yield log entries matching level and/or keyword criteria lazily.

    Args:
        entries: Stream or collection of LogEntry objects.
        level: Optional log level filter (case-insensitive, matched against uppercase).
        keyword: Optional substring filter for message body.
        case_sensitive: Whether keyword filtering is case-sensitive (default: False).

    Yields:
        LogEntry items that satisfy all active filter criteria.
    """
    target_level = level.upper() if level else None
    search_keyword = (
        keyword if (case_sensitive or keyword is None) else keyword.lower()
    )

    for entry in entries:
        if target_level is not None and entry.level != target_level:
            continue
        if search_keyword is not None:
            msg = entry.message if case_sensitive else entry.message.lower()
            if search_keyword not in msg:
                continue
        yield entry


def count_by_level(entries: Iterable[LogEntry]) -> Counter[str]:
    """Count entries grouped by log level."""
    return Counter(entry.level for entry in entries)


def get_errors(entries: Iterable[LogEntry]) -> Generator[LogEntry, None, None]:
    """Yield entries where level is ERROR or CRITICAL."""
    for entry in entries:
        if entry.level in ("ERROR", "CRITICAL"):
            yield entry


def search_entries(
    entries: Iterable[LogEntry],
    keyword: str,
    case_sensitive: bool = False,
) -> Generator[LogEntry, None, None]:
    """Yield entries matching keyword search in message."""
    kw = keyword if case_sensitive else keyword.lower()
    for entry in entries:
        msg = entry.message if case_sensitive else entry.message.lower()
        if kw in msg:
            yield entry


def top_errors(entries: Iterable[LogEntry], n: int = 10) -> list[tuple[str, int]]:
    """Return top N most frequent error messages from an iterable of entries."""
    error_counter: Counter[str] = Counter(
        entry.message for entry in entries if entry.level == "ERROR"
    )
    return error_counter.most_common(n)


def analyze_stream(
    stream: Iterable[tuple[int, str]] | Iterable[str],
    file_path: str = "",
    top_n: int = 10,
) -> tuple[LogSummary, LogAnalyzer]:
    """Process an iterable stream of lines incrementally into a LogSummary.

    Args:
        stream: Iterable yielding either line strings or (line_number, line) tuples.
        file_path: Identifier for the source file.
        top_n: Number of top error messages to include in summary.

    Returns:
        Tuple containing the generated LogSummary and the populated LogAnalyzer.
    """
    analyzer = LogAnalyzer(file_path=file_path)
    for item in stream:
        if isinstance(item, tuple):
            line_num, line_str = item
            analyzer.process_line(line_str, line_number=line_num)
        else:
            analyzer.process_line(item)
    return analyzer.get_summary(top_n=top_n), analyzer
