import json
from typing import List
from dataclasses import dataclass
from typing import Any, Protocol
from pydantic_ai import Agent, RunContext
from pathlib import Path
from nanoid import generate
from pydantic_ai.messages import Message
import datetime
from .models import Task, Database
from .plugins.jira import create_issue_in_jira, get_task_status_in_jira, get_task_assignee_in_jira

@dataclass
class JiraClient:
    def create_ticket(self, project_key: str, task: Task) -> tuple[bool, str]:
        return create_issue_in_jira(project_key, task)

    def get_task_status(self, task_key: str) -> str:
        return get_task_status_in_jira(task_key)
    
    def get_task_assignee(self, task_key: str) -> str:
        return get_task_assignee_in_jira(task_key)


THIS_DIR = Path(__file__).parent
SYSTEM_PROMPT = (THIS_DIR / 'prompt.txt').read_text()

@dataclass
class Deps:
        tasks_db: Database
        jira_client: JiraClient

gpt4o = "openai:gpt-4o"
agent = Agent(
    gpt4o,
    deps_type=Deps,
)

@agent.system_prompt
async def system_prompt() -> str:
    return SYSTEM_PROMPT

@agent.tool
def get_jira_task_assignee(ctx: RunContext[Deps], task_key: str) -> str:
    """Get the assignee of a task in Jira.

    Args:
        ctx: The context.
        task_key: The key of the task to get the assignee of.

    Returns:
        The assignee of the task.
    """
    return ctx.deps.jira_client.get_task_assignee(task_key) 

@agent.tool
def get_jira_task_status(ctx: RunContext[Deps], task_key: str) -> str:   
    """Get the status of a task in Jira.

    Args:
        ctx: The context.
        task_key: The key of the task to get the status of.

    Returns:
        The status of the task.
    """
    return ctx.deps.jira_client.get_task_status(task_key)

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
        ctx: The context.
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
