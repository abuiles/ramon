import json
from typing import List

from dataclasses import dataclass
from typing import Any, Protocol
from pydantic_ai import Agent, ModelRetry, RunContext
from devtools import debug
import asyncio
import sys
import logfire
from pathlib import Path
from pydantic import BaseModel

logfire.configure()

THIS_DIR = Path(__file__).parent

SYSTEM_PROMPT = (THIS_DIR / 'prompt.txt').read_text()

class Task(BaseModel):
    task: str
    owner: str
    priority: str
    description: str
    due_date: str
    metadata: str

@dataclass
class Database:
    file: Path = THIS_DIR / 'tasks.json'
    
    def read_tasks(self) -> List[Task]:
        with open(self.file, "r") as f:
            return json.load(f)

    def write_tasks(self, tasks: List[Task]) -> None:
        with open(self.file, "w") as f:
            json.dump([task.dict() for task in tasks], f, indent=4)

@dataclass
class Deps:
    tasks_db: Database

gpt4o = "openai:gpt-4o-mini"
agent = Agent(
    gpt4o,
    deps_type=Deps,
)

@agent.system_prompt
async def system_prompt() -> str:
    return SYSTEM_PROMPT

@agent.tool
async def get_tasks(ctx: RunContext[Deps]) -> list[Task]:
    """Get all tasks from the database.

    Args:
        ctx: The context.
    """
    return ctx.deps.tasks_db.read_tasks()

@agent.tool
async def write_tasks(ctx: RunContext[Deps], tasks: str) -> None:
    """Write tasks to the database.

    Args:
        ctx: The context.
        tasks: The list of tasks to write.
    """
    # tasks_data = [task.__dict__ for task in tasks]
    ctx.deps.tasks_db.write_tasks(tasks)



async def main():
    if len(sys.argv) == 1:
        prompt = 'What do I need to work on?'
    else:
        prompt = sys.argv[1]

    database = Database()
    deps = Deps(database)
    result = await agent.run(prompt, deps=deps)
    debug(result.data)

if __name__ == '__main__':
    asyncio.run(main())