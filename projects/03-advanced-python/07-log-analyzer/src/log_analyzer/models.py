"""Data models for log analyzer.

Provides typed, immutable data structures representing parsed log entries
and consolidated statistical analysis summaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

VALID_LEVELS: frozenset[str] = frozenset(
    {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
)


@dataclass(frozen=True, slots=True)
class LogEntry:
    """Represents a single parsed, structured log entry."""

    timestamp: datetime
    level: str
    message: str
    line_number: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert entry to a dictionary representation."""
        return {
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "level": self.level,
            "message": self.message,
            "line_number": self.line_number,
        }

    def to_csv_row(self) -> dict[str, str]:
        """Format entry for CSV serialization matching standard columns."""
        return {
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "level": self.level,
            "message": self.message,
        }


@dataclass
class LogSummary:
    """Statistical summary of processed log data."""

    file_path: str = ""
    total_lines: int = 0
    parsed_entries: int = 0
    malformed_entries: int = 0
    level_counts: dict[str, int] = field(default_factory=dict)
    top_errors: list[tuple[str, int]] = field(default_factory=list)
    earliest_timestamp: datetime | None = None
    latest_timestamp: datetime | None = None

    @property
    def debug_count(self) -> int:
        """Count of DEBUG log entries."""
        return self.level_counts.get("DEBUG", 0)

    @property
    def info_count(self) -> int:
        """Count of INFO log entries."""
        return self.level_counts.get("INFO", 0)

    @property
    def warning_count(self) -> int:
        """Count of WARNING log entries."""
        return self.level_counts.get("WARNING", 0)

    @property
    def error_count(self) -> int:
        """Count of ERROR log entries."""
        return self.level_counts.get("ERROR", 0)

    @property
    def critical_count(self) -> int:
        """Count of CRITICAL log entries."""
        return self.level_counts.get("CRITICAL", 0)

    @property
    def total_errors(self) -> int:
        """Total number of ERROR entries."""
        return self.error_count

    @property
    def total_critical(self) -> int:
        """Total number of CRITICAL entries."""
        return self.critical_count

    def to_dict(self) -> dict[str, Any]:
        """Convert summary into a JSON-serializable dictionary."""
        return {
            "file_path": self.file_path,
            "total_lines": self.total_lines,
            "parsed_entries": self.parsed_entries,
            "malformed_entries": self.malformed_entries,
            "level_counts": {
                "DEBUG": self.debug_count,
                "INFO": self.info_count,
                "WARNING": self.warning_count,
                "ERROR": self.error_count,
                "CRITICAL": self.critical_count,
            },
            "total_errors": self.total_errors,
            "total_critical": self.total_critical,
            "earliest_timestamp": (
                self.earliest_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                if self.earliest_timestamp
                else None
            ),
            "latest_timestamp": (
                self.latest_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                if self.latest_timestamp
                else None
            ),
            "top_errors": [
                {"message": msg, "count": count} for msg, count in self.top_errors
            ],
        }
