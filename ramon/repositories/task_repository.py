
from typing import List
from abc import ABC, abstractmethod
from ramon.models import Task

class TaskRepository(ABC):
    @abstractmethod
    def get_tasks(self) -> List[Task]:
        pass

    @abstractmethod
    def add_task(self, task: Task) -> None:
        pass

    @abstractmethod
    def get_completed_tasks(self) -> List[Task]:
        pass

    @abstractmethod
    def add_completed_task(self, task: Task) -> None:
        pass