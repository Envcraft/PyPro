"""CLI Task Manager."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "tasks.json"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @classmethod
    def _priority_order(cls) -> dict[str, int]:
        return {cls.LOW.value: 0, cls.MEDIUM.value: 1, cls.HIGH.value: 2}

    def order(self) -> int:
        return self._priority_order()[self.value]


class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass
class Task:
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    due_date: date | None = None
    status: Status = Status.TODO
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __str__(self) -> str:
        due = self.due_date.isoformat() if self.due_date else "none"
        return (
            f"[{self.id[:8]}] {self.title} | {self.priority.value.upper()} | "
            f"{self.status.value} | due: {due}"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Task:
        return cls(
            id=d["id"],
            title=d["title"],
            description=d.get("description", ""),
            priority=Priority(d["priority"]),
            due_date=date.fromisoformat(d["due_date"]) if d.get("due_date") else None,
            status=Status(d["status"]),
        )


class TaskManager:
    def __init__(self, data_file: Path = DATA_FILE) -> None:
        self.data_file = data_file
        self.tasks: list[Task] = []
        self._load()

    def _load(self) -> None:
        if self.data_file.exists():
            with open(self.data_file) as f:
                self.tasks = [Task.from_dict(d) for d in json.load(f)]

    def _save(self) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        due_date: date | None = None,
    ) -> Task:
        task = Task(title=title, description=description, priority=priority, due_date=due_date)
        self.tasks.append(task)
        self._save()
        return task

    def get_task(self, task_id: str) -> Task | None:
        for task in self.tasks:
            if task.id.startswith(task_id):
                return task
        return None

    def update_task(self, task_id: str, **fields) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        for key, value in fields.items():
            if hasattr(task, key):
                setattr(task, key, value)
        self._save()
        return True

    def delete_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        self._save()
        return True

    def mark_done(self, task_id: str) -> bool:
        return self.update_task(task_id, status=Status.DONE)

    def filter_by_status(self, status: Status) -> list[Task]:
        return [t for t in self.tasks if t.status == status]

    def filter_by_priority(self, priority: Priority) -> list[Task]:
        return [t for t in self.tasks if t.priority == priority]

    def sort_by_due_date(self) -> list[Task]:
        return sorted(self.tasks, key=lambda t: (t.due_date is None, t.due_date or date.max))

    def sort_by_priority(self) -> list[Task]:
        return sorted(self.tasks, key=lambda t: t.priority.order(), reverse=True)

    def search(self, keyword: str) -> list[Task]:
        kw = keyword.lower()
        return [t for t in self.tasks if kw in t.title.lower() or kw in t.description.lower()]


# ── CLI helpers ────────────────────────────────────────────────────────────────

def _parse_date(s: str) -> date | None:
    s = s.strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        print("  Invalid date format. Use YYYY-MM-DD.")
        return None


def _choose_enum(prompt: str, enum_cls, default):
    values = [e.value for e in enum_cls]
    s = input(f"{prompt} ({'/'.join(values)}) [{default.value}]: ").strip().lower()
    if not s:
        return default
    try:
        return enum_cls(s)
    except ValueError:
        print(f"  Invalid value. Using {default.value}.")
        return default


def _print_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("  No tasks found.")
        return
    for t in tasks:
        print(f"  {t}")


def _cmd_add(mgr: TaskManager) -> None:
    title = input("Title: ").strip()
    if not title:
        print("  Title cannot be empty.")
        return
    description = input("Description (optional): ").strip()
    priority = _choose_enum("Priority", Priority, Priority.MEDIUM)
    due_str = input("Due date YYYY-MM-DD (optional): ")
    due_date = _parse_date(due_str)
    task = mgr.add_task(title, description, priority, due_date)
    print(f"  Created: {task}")


def _cmd_list(mgr: TaskManager) -> None:
    _print_tasks(mgr.tasks)


def _cmd_filter(mgr: TaskManager) -> None:
    print("  Filter by: (1) status  (2) priority")
    choice = input("Choice: ").strip()
    if choice == "1":
        status = _choose_enum("Status", Status, Status.TODO)
        _print_tasks(mgr.filter_by_status(status))
    elif choice == "2":
        priority = _choose_enum("Priority", Priority, Priority.MEDIUM)
        _print_tasks(mgr.filter_by_priority(priority))
    else:
        print("  Unknown choice.")


def _cmd_sort(mgr: TaskManager) -> None:
    print("  Sort by: (1) due date  (2) priority")
    choice = input("Choice: ").strip()
    if choice == "1":
        _print_tasks(mgr.sort_by_due_date())
    elif choice == "2":
        _print_tasks(mgr.sort_by_priority())
    else:
        print("  Unknown choice.")


def _cmd_search(mgr: TaskManager) -> None:
    kw = input("Keyword: ").strip()
    if not kw:
        return
    _print_tasks(mgr.search(kw))


def _cmd_update(mgr: TaskManager) -> None:
    task_id = input("Task ID prefix: ").strip()
    task = mgr.get_task(task_id)
    if task is None:
        print("  Task not found.")
        return
    print(f"  Updating: {task}")
    print("  Leave blank to keep current value.")
    fields: dict = {}

    title = input(f"Title [{task.title}]: ").strip()
    if title:
        fields["title"] = title

    desc = input(f"Description [{task.description}]: ").strip()
    if desc:
        fields["description"] = desc

    prio_str = input(f"Priority [{task.priority.value}]: ").strip().lower()
    if prio_str:
        try:
            fields["priority"] = Priority(prio_str)
        except ValueError:
            print("  Invalid priority, keeping current.")

    due_str = input(f"Due date [{task.due_date}]: ").strip()
    if due_str:
        d = _parse_date(due_str)
        if d:
            fields["due_date"] = d

    status_str = input(f"Status [{task.status.value}]: ").strip().lower()
    if status_str:
        try:
            fields["status"] = Status(status_str)
        except ValueError:
            print("  Invalid status, keeping current.")

    if fields:
        mgr.update_task(task_id, **fields)
        print("  Updated.")
    else:
        print("  Nothing changed.")


def _cmd_done(mgr: TaskManager) -> None:
    task_id = input("Task ID prefix: ").strip()
    if mgr.mark_done(task_id):
        print("  Marked as done.")
    else:
        print("  Task not found.")


def _cmd_delete(mgr: TaskManager) -> None:
    task_id = input("Task ID prefix: ").strip()
    if mgr.delete_task(task_id):
        print("  Deleted.")
    else:
        print("  Task not found.")


MENU = """
╔══════════════════════════════╗
║       CLI Task Manager       ║
╠══════════════════════════════╣
║  1  Add task                 ║
║  2  List all tasks           ║
║  3  Filter tasks             ║
║  4  Sort tasks               ║
║  5  Search tasks             ║
║  6  Update task              ║
║  7  Mark task as done        ║
║  8  Delete task              ║
║  q  Quit                     ║
╚══════════════════════════════╝
"""

COMMANDS = {
    "1": _cmd_add,
    "2": _cmd_list,
    "3": _cmd_filter,
    "4": _cmd_sort,
    "5": _cmd_search,
    "6": _cmd_update,
    "7": _cmd_done,
    "8": _cmd_delete,
}


def main() -> None:
    mgr = TaskManager()
    print(MENU)
    while True:
        choice = input("Choice: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        cmd = COMMANDS.get(choice)
        if cmd:
            cmd(mgr)
        else:
            print("  Invalid choice.")
        print()


if __name__ == "__main__":
    main()
