import json
from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum
from pathlib import Path
from typing import List
from typing import Any, Protocol

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

THIS_DIR = Path(__file__).parent

@dataclass
class Database:
    tasks_file: Path = THIS_DIR / 'tasks.json'

    def read_tasks(self) -> List[Task]:
        with open(self.tasks_file, "r") as f:
            tasks_data = json.load(f)
            return [Task(**task) for task in tasks_data]

    def write_tasks(self, tasks: List[Task]) -> None:
        with open(self.tasks_file, "w", encoding='utf-8') as f:
            json.dump([task.model_dump() for task in tasks], f, ensure_ascii=False, indent=4)


@dataclass
class JiraClient:
    def create_ticket(self, project_key: str, task: Task) -> str:
        print("Creating ticket", project_key, task.model_dump())
        return "AFF-1234"


@dataclass
class Deps:
        tasks_db: Database
        jira_client: Any = None
