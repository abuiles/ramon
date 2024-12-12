import json
from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum
from pathlib import Path
from typing import List
import os
from datetime import datetime
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

    
def summarize_tasks(tasks: List[Task] , smart: bool = False) -> str:
    def get_immediate_priorities(tasks):
        today = datetime.now().date()
        return [task for task in tasks if task.status == 'to_do' and datetime.strptime(task.due_date, '%Y-%m-%d').date() > today]

    def get_contextual_relevance(tasks):
        return [task for task in tasks if task.status == 'in_progress']
    
    summary = ""
    if smart:
        immediate_priorities = get_immediate_priorities(tasks)
        contextual_relevance = get_contextual_relevance(tasks)

        summary += "Immediate Priorities:\n"
        for task in immediate_priorities:
            due_date = datetime.strptime(task.due_date, '%Y-%m-%d').strftime('%b %d, %Y')
            summary += f"- {task.task}, due {due_date}\n"

        summary += "\nRecurring Reminders:\nNone currently scheduled.\n"

        summary += "\nContextual Relevance:\n"
        for task in contextual_relevance:
            summary += f"- {task.task}, ongoing task.\n"
    else:
        for task in tasks:
            summary += f"- {task.task} (ID: {task.id}, Owner: {task.owner}), due {task.due_date}\n"

    return summary


DB_DIR = Path(os.getenv('DB_DIR'))

@dataclass
class Database:
    tasks_file: Path = DB_DIR / 'tasks.json'
    archived_tasks_file: Path = DB_DIR / 'archived_tasks.json' 

    def create_files(self) -> None:
        if not self.tasks_file.exists():
            with open(self.tasks_file, "w", encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        if not self.archived_tasks_file.exists():
            with open(self.archived_tasks_file, "w", encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def read_tasks(self) -> List[Task]:
        self.create_files() 
        with open(self.tasks_file, "r") as f:
            tasks_data = json.load(f)
            return [Task(**task) for task in tasks_data]

    def write_tasks(self, tasks: List[Task]) -> None:
        existing_tasks = {task.id: task for task in self.read_tasks()}
        for task in tasks:
            existing_tasks[task.id] = task
        with open(self.tasks_file, "w", encoding='utf-8') as f:
            json.dump([task.model_dump() for task in existing_tasks.values()], f, ensure_ascii=False, indent=4)

    def archive_task(self, task_id: str) -> None:
        self.create_files()
        existing_tasks = {task.id: task for task in self.read_tasks()}
        if task_id in existing_tasks:
            task_to_archive = existing_tasks.pop(task_id)
            with open(self.tasks_file, "w", encoding='utf-8') as f:
                json.dump([task.model_dump() for task in existing_tasks.values()], f, ensure_ascii=False, indent=4)
            with open(self.archived_tasks_file, "r", encoding='utf-8') as f:
                archived_tasks = json.load(f)
            archived_tasks.append(task_to_archive.model_dump())
            with open(self.archived_tasks_file, "w", encoding='utf-8') as f:
                json.dump(archived_tasks, f, ensure_ascii=False, indent=4)
