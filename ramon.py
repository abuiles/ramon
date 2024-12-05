import click
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
from nanoid import generate
from pydantic_ai.messages import (
    Message
)
import datetime

logfire.configure(send_to_logfire='if-token-present')

THIS_DIR = Path(__file__).parent

SYSTEM_PROMPT = (THIS_DIR / 'prompt.txt').read_text()

class Task(BaseModel):
    id: str
    task: str
    owner: str
    priority: str
    description: str
    due_date: str
    completed_at: str # this is only done for completed tasks not for todo
    metadata: str

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

gpt4o = "openai:gpt-4o-mini"
agent = Agent(
    gpt4o,
    deps_type=Deps,
)

@agent.system_prompt
async def system_prompt() -> str:
    return SYSTEM_PROMPT

@agent.tool
async def create_jira_ticket(ctx: RunContext[Deps], project_key: str, task: Task) -> str:
    """Create a new Jira ticket.

    Args:
        ctx: The context.
        task: The task to create a ticket for.
    """
    return ctx.deps.jira_client.create_ticket(project_key, task)

@agent.tool
async def get_tasks(ctx: RunContext[Deps]) -> list[Task]:
    """Get all tasks from the database.

    Args:
        ctx: The context.
    """
    return ctx.deps.tasks_db.read_tasks()

@agent.tool
async def add_new_task(ctx: RunContext[Deps], tasks: list[Task]) -> None:
    """Write a new tasks to the database. This needs all the list of task not only the new one

    Args:
        ctx: The context.p
        tasks: The list of tasks to write.
    """
    ctx.deps.tasks_db.write_tasks(tasks)
@agent.tool
async def get_completed_tasks(ctx: RunContext[Deps]) -> list[Task]:
    """Get all completed tasks from the database.

    Args:
        ctx: The context.
    """
    return ctx.deps.tasks_db.read_done()

@agent.tool
async def add_new_completed_task(ctx: RunContext[Deps], tasks: list[Task]) -> None:
    """Write a new completed tasks to the database. This needs all the list of done task not only the new one. Make sure that whenever a new task is added to the list of completed, it has a new attribute called completed_at with the current date and time in ISO format.

    Args:
        ctx: The context.p
        tasks: The list of completed tasks to write.
    """
    ctx.deps.tasks_db.write_done(tasks)

@agent.tool
async def current_date_time(ctx: RunContext[Deps]) -> str:
    """Get the current date and time in ISO format.

    Args:
        ctx: The context.
    """
    return datetime.datetime.now().isoformat()



@agent.tool
def generate_task_id(ctx: RunContext[Deps]) -> str:
    """Generate a new task id.
    """
    return generate()


@click.command()
@click.argument('prompt', required=False, default='What do I need to work on?')
def chat(prompt: str):
    """Start a new chat with ramon."""
    click.echo("Type 'exit' or 'quit' to exit")
    database = Database()
    jira = JiraClient()
    deps = Deps(database, jira)
    message_history: list[Message] = []
    while True:
        prompt = click.prompt("", prompt_suffix="> ")
        if prompt.strip() in ("exit", "quit"):
            break
        if prompt.strip():
            result = agent.run_sync(prompt, deps=deps, message_history=message_history)
            print(result.data)
            message_history.extend(result.new_messages())

if __name__ == '__main__':
    asyncio.run(asyncio.sleep(1))
    chat()
