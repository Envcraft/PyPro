"""Tests for CLI Task Manager."""

import json
from datetime import date
from pathlib import Path

import pytest

from src.main import Priority, Status, Task, TaskManager


@pytest.fixture
def mgr(tmp_path: Path) -> TaskManager:
    return TaskManager(data_file=tmp_path / "tasks.json")


class TestTaskCreation:
    def test_creates_task_with_required_fields(self, mgr: TaskManager) -> None:
        task = mgr.add_task("Buy milk")
        assert task.title == "Buy milk"
        assert task.status == Status.TODO

    def test_task_has_unique_id(self, mgr: TaskManager) -> None:
        t1 = mgr.add_task("Task A")
        t2 = mgr.add_task("Task B")
        assert t1.id != t2.id

    def test_default_status_is_todo(self, mgr: TaskManager) -> None:
        task = mgr.add_task("Review PR")
        assert task.status == Status.TODO

    def test_creates_task_with_all_fields(self, mgr: TaskManager) -> None:
        task = mgr.add_task(
            "Write report",
            description="Quarterly summary",
            priority=Priority.HIGH,
            due_date=date(2025, 12, 31),
        )
        assert task.description == "Quarterly summary"
        assert task.priority == Priority.HIGH
        assert task.due_date == date(2025, 12, 31)


class TestFiltering:
    def test_filter_by_status(self, mgr: TaskManager) -> None:
        mgr.add_task("Alpha")
        t2 = mgr.add_task("Beta")
        mgr.mark_done(t2.id)
        done = mgr.filter_by_status(Status.DONE)
        assert len(done) == 1
        assert done[0].title == "Beta"

    def test_filter_by_priority(self, mgr: TaskManager) -> None:
        mgr.add_task("Low task", priority=Priority.LOW)
        mgr.add_task("High task", priority=Priority.HIGH)
        highs = mgr.filter_by_priority(Priority.HIGH)
        assert len(highs) == 1
        assert highs[0].title == "High task"

    def test_filter_returns_empty_when_no_match(self, mgr: TaskManager) -> None:
        mgr.add_task("Task")
        assert mgr.filter_by_status(Status.DONE) == []


class TestSorting:
    def test_sort_by_due_date(self, mgr: TaskManager) -> None:
        mgr.add_task("Later", due_date=date(2025, 6, 1))
        mgr.add_task("Earlier", due_date=date(2025, 1, 1))
        mgr.add_task("No date")
        sorted_tasks = mgr.sort_by_due_date()
        assert sorted_tasks[0].title == "Earlier"
        assert sorted_tasks[1].title == "Later"
        assert sorted_tasks[2].title == "No date"

    def test_sort_by_priority(self, mgr: TaskManager) -> None:
        mgr.add_task("Low", priority=Priority.LOW)
        mgr.add_task("High", priority=Priority.HIGH)
        mgr.add_task("Med", priority=Priority.MEDIUM)
        sorted_tasks = mgr.sort_by_priority()
        assert sorted_tasks[0].priority == Priority.HIGH
        assert sorted_tasks[-1].priority == Priority.LOW


class TestPersistence:
    def test_serialisation_round_trip(self, tmp_path: Path) -> None:
        path = tmp_path / "tasks.json"
        mgr1 = TaskManager(data_file=path)
        mgr1.add_task("Persist me", priority=Priority.HIGH, due_date=date(2025, 3, 15))
        mgr2 = TaskManager(data_file=path)
        assert len(mgr2.tasks) == 1
        assert mgr2.tasks[0].title == "Persist me"
        assert mgr2.tasks[0].priority == Priority.HIGH
        assert mgr2.tasks[0].due_date == date(2025, 3, 15)

    def test_saves_and_loads_multiple_tasks(self, tmp_path: Path) -> None:
        path = tmp_path / "tasks.json"
        mgr1 = TaskManager(data_file=path)
        mgr1.add_task("A")
        mgr1.add_task("B")
        mgr2 = TaskManager(data_file=path)
        assert len(mgr2.tasks) == 2


class TestUpdateAndDelete:
    def test_update_task_title(self, mgr: TaskManager) -> None:
        task = mgr.add_task("Old title")
        assert mgr.update_task(task.id, title="New title")
        assert mgr.get_task(task.id).title == "New title"

    def test_update_nonexistent_task_returns_false(self, mgr: TaskManager) -> None:
        assert not mgr.update_task("nonexistent-id", title="x")

    def test_delete_task(self, mgr: TaskManager) -> None:
        task = mgr.add_task("To delete")
        assert mgr.delete_task(task.id)
        assert mgr.get_task(task.id) is None

    def test_delete_nonexistent_task_returns_false(self, mgr: TaskManager) -> None:
        assert not mgr.delete_task("nonexistent-id")

    def test_mark_done(self, mgr: TaskManager) -> None:
        task = mgr.add_task("Finish me")
        mgr.mark_done(task.id)
        assert mgr.get_task(task.id).status == Status.DONE


class TestSearch:
    def test_search_by_keyword_in_title(self, mgr: TaskManager) -> None:
        mgr.add_task("Buy groceries")
        mgr.add_task("Call doctor")
        results = mgr.search("buy")
        assert len(results) == 1
        assert results[0].title == "Buy groceries"

    def test_search_by_keyword_in_description(self, mgr: TaskManager) -> None:
        mgr.add_task("Task", description="important meeting notes")
        results = mgr.search("meeting")
        assert len(results) == 1

    def test_search_case_insensitive(self, mgr: TaskManager) -> None:
        mgr.add_task("URGENT task")
        assert len(mgr.search("urgent")) == 1

    def test_search_no_results(self, mgr: TaskManager) -> None:
        mgr.add_task("Something else")
        assert mgr.search("xyz") == []
