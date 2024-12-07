
import json
from pathlib import Path
from typing import List
from .models import Task
from .task_repository import TaskRepository

class FileTaskRepository(TaskRepository):
    def __init__(self, todo_path: Path, done_path: Path):
        self.todo_path = todo_path
        self.done_path = done_path

    def get_tasks(self) -> List[Task]:
        with open(self.todo_path, "r") as f:
            return json.load(f)

    def add_task(self, task: Task) -> None:
        tasks = self.get_tasks()
        tasks.append(task)
        with open(self.todo_path, "w", encoding='utf-8') as f:
            json.dump([task.model_dump() for task in tasks], f, ensure_ascii=False, indent=4)

    def get_completed_tasks(self) -> List[Task]:
        with open(self.done_path, "r") as f:
            return json.load(f)

    def add_completed_task(self, task: Task) -> None:
        tasks = self.get_completed_tasks()
        tasks.append(task)
        with open(self.done_path, "w", encoding='utf-8') as f:
            json.dump([task.model_dump() for task in tasks], f, ensure_ascii=False, indent=4)