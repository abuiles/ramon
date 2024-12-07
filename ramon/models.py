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
    todo: Path = THIS_DIR / 'tasks.json'
    done: Path = THIS_DIR / 'done.json'

    def read_tasks(self) -> List[Task]:
        with open(self.todo, "r") as f:
            return json.load(f)

    def write_tasks(self, tasks: List[Task]) -> None:
        with open(self.todo, "w", encoding='utf-8') as f:
                json.dump([task.model_dump() for task in tasks], f, ensure_ascii=False, indent=4)

    # this could be refactor into a single func and then we can read done or todos based on an arg
    def read_done(self) -> List[Task]:
        with open(self.done, "r") as f:
            return json.load(f)

    def write_done(self, tasks: List[Task]) -> None:
        with open(self.done, "w", encoding='utf-8') as f:
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
