"""Tests for CLI Task Manager."""

import pytest

# from src.main import TaskManager, Priority, Status, Task


class TestTaskCreation:
    def test_creates_task_with_required_fields(self) -> None:
        pytest.skip("Implement this test.")

    def test_task_has_unique_id(self) -> None:
        pytest.skip("Implement this test.")

    def test_default_status_is_todo(self) -> None:
        pytest.skip("Implement this test.")


class TestFiltering:
    def test_filter_by_status(self) -> None:
        pytest.skip("Implement this test.")

    def test_filter_by_priority(self) -> None:
        pytest.skip("Implement this test.")


class TestSorting:
    def test_sort_by_due_date(self) -> None:
        pytest.skip("Implement this test.")


class TestPersistence:
    def test_serialisation_round_trip(self, tmp_path) -> None:
        pytest.skip("Implement this test.")
