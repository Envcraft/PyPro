"""Export engines for serializing log summaries and entries.

Provides streaming CSV export and formatted UTF-8 JSON summary generation
with directory auto-creation and input overwrite protection.
"""

from __future__ import annotations

from collections.abc import Iterable
import csv
from datetime import datetime
import json
from pathlib import Path
from typing import Any

from log_analyzer.models import LogEntry, LogSummary


def _json_serializer(obj: Any) -> Any:
    """Fallback JSON serializer handling datetime objects."""
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def export_json(
    summary: LogSummary | dict[str, Any],
    output_path: str | Path,
    input_path: str | Path | None = None,
    indent: int = 2,
) -> Path:
    """Export an analysis summary to a UTF-8 JSON file.

    Args:
        summary: LogSummary instance or dictionary containing summary metrics.
        output_path: Target filesystem path for the JSON file.
        input_path: Optional source log file path to safeguard against accidental overwrite.
        indent: Indentation spaces for pretty-printed output (default: 2).

    Returns:
        Resolved Path to the written JSON file.

    Raises:
        ValueError: If output_path resolves to the same location as input_path.
    """
    out_file = Path(output_path).resolve()

    if input_path is not None:
        in_file = Path(input_path).resolve()
        if out_file == in_file:
            raise ValueError(
                f"Output path cannot overwrite input log file: {out_file}"
            )

    out_file.parent.mkdir(parents=True, exist_ok=True)

    data = summary.to_dict() if isinstance(summary, LogSummary) else summary

    with out_file.open("w", encoding="utf-8") as file_handle:
        json.dump(
            data,
            file_handle,
            indent=indent,
            ensure_ascii=False,
            default=_json_serializer,
        )
        file_handle.write("\n")

    return out_file


def export_csv(
    entries: Iterable[LogEntry],
    output_path: str | Path,
    input_path: str | Path | None = None,
) -> int:
    """Stream parsed LogEntry objects into a CSV file with standard headers.

    Uses O(1) memory by writing entries as they arrive from an iterator or generator.

    Args:
        entries: Stream or iterable of LogEntry objects.
        output_path: Destination path for the CSV file.
        input_path: Optional input path to safeguard against accidental overwrite.

    Returns:
        Total count of entries successfully written to the CSV file.

    Raises:
        ValueError: If output_path resolves to the same location as input_path.
    """
    out_file = Path(output_path).resolve()

    if input_path is not None:
        in_file = Path(input_path).resolve()
        if out_file == in_file:
            raise ValueError(
                f"Output path cannot overwrite input log file: {out_file}"
            )

    out_file.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["timestamp", "level", "message"]
    count = 0

    with out_file.open("w", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        writer.writeheader()

        for entry in entries:
            writer.writerow(entry.to_csv_row())
            count += 1

    return count
