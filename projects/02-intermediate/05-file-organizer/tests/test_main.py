"""Tests for File Organizer.

Use tmp_path fixture — never test against real user directories.
"""

from pathlib import Path

import pytest

# from src.main import get_category, handle_duplicate, scan_files


class TestGetCategory:
    def test_image_extension(self) -> None:
        pytest.skip("Implement this test.")

    def test_document_extension(self) -> None:
        pytest.skip("Implement this test.")

    def test_unknown_extension(self) -> None:
        pytest.skip("Implement this test.")

    def test_no_extension(self) -> None:
        pytest.skip("Implement this test.")


class TestDryRun:
    def test_dry_run_does_not_move_files(self, tmp_path: Path) -> None:
        pytest.skip("Implement this test.")


class TestDuplicateHandling:
    def test_renames_duplicate(self, tmp_path: Path) -> None:
        pytest.skip("Implement this test.")
