import json
from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum
from pathlib import Path
from typing import List
import os

class StatusEnum(str, Enum):
        to_do = "to_do"
        in_progress = "in_progress"
        completed = "completed"
        blocked = "blocked"
        on_hold = "on_hold"
        canceled = "canceled"

class Task(BaseModel):
    id: str
    task: str
    owner: str
    priority: str
    description: str
    due_date: str
    completed_at: str
    metadata: str
    status: StatusEnum = StatusEnum.to_do


DB_DIR = Path(os.getenv('DB_DIR'))

@dataclass
class Database:
    tasks_file: Path = DB_DIR / 'tasks.json'

    def read_tasks(self) -> List[Task]:
        with open(self.tasks_file, "r") as f:
            tasks_data = json.load(f)
            return [Task(**task) for task in tasks_data]

    def write_tasks(self, tasks: List[Task]) -> None:
        existing_tasks = {task.id: task for task in self.read_tasks()}
        for task in tasks:
            existing_tasks[task.id] = task
        with open(self.tasks_file, "w", encoding='utf-8') as f:
            json.dump([task.model_dump() for task in existing_tasks.values()], f, ensure_ascii=False, indent=4)


        
