#!/usr/bin/env python3
"""Synthetic log generator for log-analyzer benchmarking and testing.

Generates deterministic log datasets of configurable size without buffering
the full dataset in memory. Supports realistic timestamps, repeating errors,
configurable log level distributions, and injection of malformed lines.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path
import random
import sys
from typing import Generator

# Templates for synthetic log messages
INFO_MESSAGES = [
    "Server started listening on port 8080",
    "Request received: GET /api/v1/health",
    "Request received: POST /api/v1/users",
    "Request received: GET /api/v1/orders",
    "Request received: GET /api/v1/metrics",
    "User authentication succeeded for session_id={session_id}",
    "Payment processed successfully for order_id={order_id}",
    "Background job completed: cleanup_temp_tables",
    "Cache refreshed: {count} keys loaded in {latency}ms",
    "Service graceful shutdown initiated",
]

DEBUG_MESSAGES = [
    "Connection pool status: active={active}, idle={idle}",
    "Query execution plan cached for hash={query_hash}",
    "Redis key TTL evaluated for user:{user_id}",
    "Thread worker-{worker_id} acquired lock",
    "Serializing response payload: {bytes_count} bytes",
    "TLS handshake completed in {latency}ms with cipher TLS_AES_256_GCM_SHA384",
]

WARNING_MESSAGES = [
    "Slow HTTP request: {latency}ms for path /api/v1/reports",
    "High memory usage detected: {percent}% memory threshold exceeded",
    "Connection pool exhaustion risk: active connections at {percent}%",
    "Deprecated API endpoint invoked: /api/v0/authenticate",
    "Disk utilization above threshold on partition /data: {percent}%",
    "Rate limit warning: client {ip} reached 80% of quota",
]

ERROR_MESSAGES = [
    "Database connection failed: connection refused on port 5432",
    "Authentication failed for user: invalid credentials",
    "Disk quota exceeded for volume /var/log",
    "Upstream microservice timeout after {latency}ms: service=inventory",
    "Failed to parse incoming payload: JSONDecodeError at char {pos}",
    "Network socket reset by peer during file transfer",
]

CRITICAL_MESSAGES = [
    "Primary database cluster is unreachable",
    "Data corruption detected in segment storage node 3",
    "Unrecoverable deadlock encountered in transaction manager",
    "Security intrusion alert: anomalous privilege escalation attempted",
    "Core memory allocation failure in native worker thread",
]

MALFORMED_PATTERNS = [
    "THIS_IS_CORRUPT_GARBAGE_NO_STRUCTURE_HERE",
    "2026-99-99 12:00:00 INFO Invalid date numbers in entry",
    "2026-01-01 25:61:99 ERROR Hour and minute out of bounds",
    "2026-01-01-12:00:00 INFO Missing space delimiter between date and time",
    "2026-01-01 12:00:00 UNKNOWN_LEVEL Message with unsupported level",
    "12:00:00 2026-01-01 WARNING Date and time fields transposed",
    "[2026-01-01 12:00:00] [INFO] Square brackets format not supported",
    "--- System reboot message ---",
]


def generate_log_stream(
    count: int,
    seed: int = 42,
    malformed_percent: float = 2.0,
    start_time: datetime | None = None,
) -> Generator[str, None, None]:
    """Yield log lines one at a time using a deterministic pseudo-random stream.

    Args:
        count: Total number of log lines to generate.
        seed: Deterministic random seed for reproducibility.
        malformed_percent: Percentage (0.0 to 100.0) of malformed lines to inject.
        start_time: Initial timestamp for the log sequence.

    Yields:
        Formatted log string lines without trailing newline.
    """
    rng = random.Random(seed)
    current_time = start_time or datetime(2026, 1, 1, 8, 0, 0)

    # Weighted distribution of levels: INFO 50%, DEBUG 25%, WARNING 12%, ERROR 10%, CRITICAL 3%
    level_weights = [
        ("INFO", 0.50, INFO_MESSAGES),
        ("DEBUG", 0.25, DEBUG_MESSAGES),
        ("WARNING", 0.12, WARNING_MESSAGES),
        ("ERROR", 0.10, ERROR_MESSAGES),
        ("CRITICAL", 0.03, CRITICAL_MESSAGES),
    ]
    levels, weights, message_pools = zip(*[
        (item[0], item[1], item[2]) for item in level_weights
    ], strict=True)

    malformed_ratio = max(0.0, min(100.0, malformed_percent)) / 100.0

    for i in range(count):
        # Deterministically advance timestamp by 0 to 5 seconds
        step_seconds = rng.randint(0, 5)
        current_time += timedelta(seconds=step_seconds)

        # Decide whether to inject a malformed line
        if malformed_ratio > 0.0 and rng.random() < malformed_ratio:
            malformed_line = rng.choice(MALFORMED_PATTERNS)
            yield malformed_line
            continue

        # Choose log level according to weights
        selected_level = rng.choices(levels, weights=weights, k=1)[0]
        level_index = levels.index(selected_level)
        templates = message_pools[level_index]

        # Template formatting with bounded deterministic parameters to ensure repetition
        template = rng.choice(templates)
        message = template.format(
            session_id=rng.randint(1000, 1020),
            order_id=rng.randint(5000, 5020),
            count=rng.choice([10, 50, 100, 250]),
            latency=rng.choice([12, 45, 120, 450, 3200, 5000]),
            active=rng.randint(5, 50),
            idle=rng.randint(1, 20),
            query_hash=f"{rng.randint(1000, 1010):04x}",
            user_id=rng.randint(1, 15),
            worker_id=rng.randint(1, 4),
            bytes_count=rng.choice([128, 512, 1024, 4096]),
            percent=rng.choice([80, 85, 90, 95, 99]),
            ip=f"192.168.1.{rng.randint(10, 25)}",
            pos=rng.choice([12, 45, 89]),
        )

        time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        yield f"{time_str} {selected_level} {message}"


def generate_logs_to_file(
    output_path: Path | None,
    count: int,
    seed: int = 42,
    malformed_percent: float = 2.0,
) -> None:
    """Stream generated logs into a file or standard output."""
    stream = generate_log_stream(
        count=count, seed=seed, malformed_percent=malformed_percent
    )

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as out:
            for line in stream:
                out.write(line + "\n")
    else:
        for line in stream:
            sys.stdout.write(line + "\n")


def build_parser() -> argparse.ArgumentParser:
    """Construct CLI argument parser for synthetic log generation."""
    parser = argparse.ArgumentParser(
        description="Deterministic synthetic log generator for log-analyzer benchmarking."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1000,
        help="Number of log entries to generate (default: 1000).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Destination path for generated log file (default: stdout).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible log generation (default: 42).",
    )
    parser.add_argument(
        "--malformed-percent",
        type=float,
        default=2.0,
        help="Percentage of malformed entries to inject (default: 2.0).",
    )
    return parser


def main() -> None:
    """CLI entry point for log generation tool."""
    parser = build_parser()
    args = parser.parse_args()

    if args.count < 0:
        parser.error("--count must be non-negative")
    if not (0.0 <= args.malformed_percent <= 100.0):
        parser.error("--malformed-percent must be between 0.0 and 100.0")

    try:
        generate_logs_to_file(
            output_path=args.output,
            count=args.count,
            seed=args.seed,
            malformed_percent=args.malformed_percent,
        )
        if args.output:
            print(
                f"Generated {args.count:,} entries into {args.output} (seed={args.seed})",
                file=sys.stderr,
            )
    except Exception as exc:
        print(f"Error generating logs: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
