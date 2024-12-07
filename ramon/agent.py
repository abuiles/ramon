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
from .models import Task, Database, JiraClient, Deps

logfire.configure(send_to_logfire='if-token-present')

THIS_DIR = Path(__file__).parent
SYSTEM_PROMPT = (THIS_DIR / 'prompt.txt').read_text()

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
    """Get all tasks from the database."""
    tasks = ctx.deps.tasks_db.read_tasks()
    return [task.model_dump() for task in tasks]

@agent.tool
async def update_or_create_task(ctx: RunContext[Deps], tasks: list[Task]) -> None:
    """Write or update tasks to the database.

    Args:
        ctx: The context.p
        tasks: The list of tasks to write or update.
    """
    ctx.deps.tasks_db.write_tasks(tasks)

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
