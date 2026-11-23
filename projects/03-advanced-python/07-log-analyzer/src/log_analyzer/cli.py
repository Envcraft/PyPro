"""Command-line interface for log analysis.

Orchestrates the streaming pipeline, argument parsing, report formatting,
and export dispatch while ensuring robust error handling without unhandled tracebacks.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys
from typing import Sequence

from log_analyzer.analyzer import LogAnalyzer
from log_analyzer.exporter import export_json
from log_analyzer.models import VALID_LEVELS, LogEntry, LogSummary
from log_analyzer.parser import parse_line
from log_analyzer.reader import read_log_lines


def build_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="log-analyzer",
        description="Fast, streaming, memory-efficient log analysis tool.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available commands",
    )

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a log file and generate summary reports.",
    )
    analyze_parser.add_argument(
        "file",
        type=Path,
        help="Path to the log file to analyze.",
    )
    analyze_parser.add_argument(
        "--json-output",
        type=Path,
        default=None,
        metavar="PATH",
        help="Path to export the statistical summary as JSON.",
    )
    analyze_parser.add_argument(
        "--csv-output",
        type=Path,
        default=None,
        metavar="PATH",
        help="Path to export parsed log entries as CSV.",
    )
    analyze_parser.add_argument(
        "--top",
        type=int,
        default=10,
        metavar="N",
        help="Number of most frequent error messages to display (default: 10).",
    )
    analyze_parser.add_argument(
        "--level",
        type=str,
        default=None,
        metavar="LEVEL",
        help=f"Filter entries by log level ({', '.join(sorted(VALID_LEVELS))}).",
    )
    analyze_parser.add_argument(
        "--keyword",
        type=str,
        default=None,
        metavar="TEXT",
        help="Filter log entries containing case-insensitive keyword in message.",
    )

    return parser


def format_summary_report(
    summary: LogSummary,
    level_filter: str | None = None,
    keyword_filter: str | None = None,
    matched_filter_count: int | None = None,
) -> str:
    """Format analysis metrics into a clean human-readable terminal report."""
    border = "=" * 68
    divider = "-" * 68
    lines: list[str] = [
        border,
        "                    LOG ANALYSIS SUMMARY REPORT                     ",
        border,
        f"File Path:          {summary.file_path}",
        f"Total Lines:        {summary.total_lines:,}",
        f"Parsed Entries:     {summary.parsed_entries:,}",
        f"Malformed Entries:  {summary.malformed_entries:,}",
        divider,
        "Log Level Distribution:",
        f"  DEBUG:            {summary.debug_count:,}",
        f"  INFO:             {summary.info_count:,}",
        f"  WARNING:          {summary.warning_count:,}",
        f"  ERROR:            {summary.error_count:,}",
        f"  CRITICAL:         {summary.critical_count:,}",
        divider,
        "Time Range:",
        f"  Earliest:         {summary.earliest_timestamp or 'N/A'}",
        f"  Latest:           {summary.latest_timestamp or 'N/A'}",
        divider,
        f"Top {len(summary.top_errors)} Error Messages (Total Errors: {summary.total_errors:,}, Critical: {summary.total_critical:,}):",
    ]

    if summary.top_errors:
        for idx, (msg, count) in enumerate(summary.top_errors, start=1):
            lines.append(f"  {idx}. [{count}x] {msg}")
    else:
        lines.append("  (No error messages recorded)")

    if level_filter or keyword_filter:
        lines.append(divider)
        lines.append("Active Filter Results:")
        if level_filter:
            lines.append(f"  Level Filter:     {level_filter}")
        if keyword_filter:
            lines.append(f"  Keyword Filter:   {keyword_filter}")
        if matched_filter_count is not None:
            lines.append(f"  Matching Entries: {matched_filter_count:,}")

    if summary.malformed_entries > 0:
        lines.append(divider)
        lines.append(
            f"Note: {summary.malformed_entries:,} malformed line(s) were safely skipped."
        )

    lines.append(border)
    return "\n".join(lines)


def run_pipeline(
    file_path: Path,
    top_n: int = 10,
    level: str | None = None,
    keyword: str | None = None,
    json_output: Path | None = None,
    csv_output: Path | None = None,
) -> tuple[LogSummary, int]:
    """Execute the streaming analysis pipeline in a single O(1) memory pass.

    Args:
        file_path: Source log file path.
        top_n: Number of top error messages.
        level: Optional log level filter.
        keyword: Optional keyword substring filter.
        json_output: Destination path for summary JSON export.
        csv_output: Destination path for entries CSV export.

    Returns:
        Tuple of (LogSummary, matching_filter_entries_count).
    """
    resolved_path = file_path.resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if resolved_path.is_dir():
        raise IsADirectoryError(f"Expected a log file, but found a directory: {file_path}")

    target_level = level.upper() if level else None
    search_keyword = keyword.lower() if keyword else None

    # Check for output overwrite collisions
    if json_output and json_output.resolve() == resolved_path:
        raise ValueError("JSON output path cannot overwrite input log file.")
    if csv_output and csv_output.resolve() == resolved_path:
        raise ValueError("CSV output path cannot overwrite input log file.")

    analyzer = LogAnalyzer(file_path=str(file_path))
    matching_entries_count = 0

    # If CSV export is requested, initialize writer for streaming output
    csv_file_handle = None
    csv_writer = None
    if csv_output is not None:
        csv_output.resolve().parent.mkdir(parents=True, exist_ok=True)
        csv_file_handle = csv_output.open("w", newline="", encoding="utf-8")
        csv_writer = csv.DictWriter(
            csv_file_handle, fieldnames=["timestamp", "level", "message"]
        )
        csv_writer.writeheader()

    try:
        for line_num, raw_line in read_log_lines(resolved_path):
            entry = analyzer.process_line(raw_line, line_number=line_num)
            if entry is None:
                continue

            # Check filter criteria
            matches = True
            if target_level is not None and entry.level != target_level:
                matches = False
            if matches and search_keyword is not None and search_keyword not in entry.message.lower():
                matches = False

            if matches:
                matching_entries_count += 1
                if csv_writer is not None:
                    csv_writer.writerow(entry.to_csv_row())

    finally:
        if csv_file_handle is not None:
            csv_file_handle.close()

    summary = analyzer.get_summary(top_n=top_n)

    # Export JSON if requested
    if json_output is not None:
        export_json(summary, json_output, input_path=resolved_path)

    return summary, matching_entries_count


def main(argv: Sequence[str] | None = None) -> int:
    """CLI application entrypoint."""
    args_list = list(sys.argv[1:] if argv is None else argv)

    # Support invocation without explicit "analyze" subcommand if file is passed directly
    if args_list and args_list[0] not in ("analyze", "-h", "--help"):
        args_list.insert(0, "analyze")

    parser = build_parser()
    args = parser.parse_args(args_list)

    if not args.command:
        parser.print_help(sys.stderr)
        return 2

    # Validate level argument if provided
    if args.level and args.level.upper() not in VALID_LEVELS:
        print(
            f"Error: Invalid log level '{args.level}'. Supported levels: {', '.join(sorted(VALID_LEVELS))}",
            file=sys.stderr,
        )
        return 2

    if args.top < 0:
        print("Error: --top must be a non-negative integer.", file=sys.stderr)
        return 2

    try:
        summary, match_count = run_pipeline(
            file_path=args.file,
            top_n=args.top,
            level=args.level,
            keyword=args.keyword,
            json_output=args.json_output,
            csv_output=args.csv_output,
        )

        report = format_summary_report(
            summary=summary,
            level_filter=args.level.upper() if args.level else None,
            keyword_filter=args.keyword,
            matched_filter_count=match_count if (args.level or args.keyword) else None,
        )
        print(report)

        if args.json_output:
            print(f"[JSON Export] Summary exported to: {args.json_output}")
        if args.csv_output:
            print(f"[CSV Export]  {match_count:,} entries exported to: {args.csv_output}")

        return 0

    except (FileNotFoundError, IsADirectoryError, ValueError, PermissionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
