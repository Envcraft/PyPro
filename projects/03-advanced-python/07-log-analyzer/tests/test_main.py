"""Tests for Log Analyzer."""

from pathlib import Path

import pytest

# from src.main import parse_line, count_by_level, get_errors

SAMPLE_LOG_LINE = "2024-01-15 10:23:45 ERROR Database connection failed"
MALFORMED_LINE = "this is not a valid log line"


class TestParseLine:
    def test_parses_valid_line(self) -> None:
        pytest.skip("Implement this test.")

    def test_returns_none_for_malformed_line(self) -> None:
        pytest.skip("Implement this test.")

    def test_extracts_timestamp(self) -> None:
        pytest.skip("Implement this test.")

    def test_extracts_log_level(self) -> None:
        pytest.skip("Implement this test.")


class TestCountByLevel:
    def test_counts_each_level(self) -> None:
        pytest.skip("Implement this test.")


class TestGetErrors:
    def test_returns_only_error_and_critical(self) -> None:
        pytest.skip("Implement this test.")
