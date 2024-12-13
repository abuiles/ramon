from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pathlib import Path
from nanoid import generate
import datetime
from .models import Task, Database, summarize_tasks
import ramon.plugins.jira as jira_client
import os

@dataclass
class JiraClient:
    def create_ticket(self, project_key: str, task: Task) -> tuple[bool, str]:
        return jira_client.create_issue_in_jira(project_key, task)

    def get_task_status(self, task_key: str) -> str:
        return jira_client.get_task_status_in_jira(task_key)

    def get_task_assignee(self, task_key: str) -> str:
        return jira_client.get_task_assignee_in_jira(task_key)

    def open_jira_issue(self, task_key: str) -> None:
        return jira_client.open_jira_issue(task_key)

    def load_comments_for_jira_issue(self, task_key: str) -> list[str]:
        return jira_client.load_comments_for_jira_issue(task_key)

    def add_comment_to_jira_issue(self, task_key: str, comment: str) -> None:
        return jira_client.add_comment_to_jira_issue(task_key, comment)


THIS_DIR = Path(__file__).parent
SYSTEM_PROMPT = (THIS_DIR / 'prompt.txt').read_text()

@dataclass
class Deps:
        tasks_db: Database
        jira_client: JiraClient

gpt4omini = "openai:gpt-4o-mini"
agent = Agent(
    gpt4omini,
    deps_type=Deps,
)

@agent.system_prompt
async def system_prompt(ctx: RunContext[Deps]) -> str:
    tasks_summary = summarize_tasks(ctx.deps.tasks_db.read_tasks())
    return f"{SYSTEM_PROMPT}\n\n{os.getenv('PROMPT_EXTENSION')}\ncurrent tasks:\n{tasks_summary} "

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
def open_jira_issue_in_browser(ctx: RunContext[Deps], task_key: str) -> None:
    """Open a Jira issue in the default web browser.

    Args:
        ctx: The context.
        task_key: The key of the task to open.
    """
    ctx.deps.jira_client.open_jira_issue(task_key)

@agent.tool
def load_all_comments_for_jira_issue(ctx: RunContext[Deps], task_key: str) -> list[str]:
    """Load all comments from a Jira issue.

    Args:
        ctx: The context.
        task_key: The key of the task to load comments from.
    """
    return ctx.deps.jira_client.load_comments_for_jira_issue(task_key)

@agent.tool
def add_comment_to_jira_issue(ctx: RunContext[Deps], task_key: str, comment: str) -> None:
    """Add a comment to a Jira issue.

    Args:
        ctx: The context.
        task_key: The key of the task to add a comment to.
        comment: The comment to add.
    """
    return ctx.deps.jira_client.add_comment_to_jira_issue(task_key, comment)

@agent.tool
def archive_task(ctx: RunContext[Deps], task_id: str) -> None:
    """Archive a task.

    Args:
        ctx: The context.
        task_id: The id of the task to archive.
    """
    ctx.deps.tasks_db.archive_task(task_id)

@agent.tool
async def get_task_by_id(ctx: RunContext[Deps], task_id: str) -> Task:
    """Get a task by its id.

    Args:
        ctx: The context.
        task_id: The id of the task to get.
    """
    tasks = ctx.deps.tasks_db.read_tasks()
    return next((task for task in tasks if task.id == task_id), None)

@agent.tool
async def get_tasks(ctx: RunContext[Deps], status: list[str] = None, db: str = "tasks") -> list[Task]:
    """Get all tasks from the database. By default we should load 'to_do' tasks.
    Only load 'in_progress', 'blocked', 'on_hold', canceled and completed tasks if explicitly asked.

    Args:
        ctx: The context.
        status: The status of the tasks to get. It can be a list of statuses. Valid statuses are: {', '.join(Task.Status.values())}
        db: The database to read the tasks from. It can be 'tasks' or 'archived_tasks'.
    """
    print("filtering by status", status)
    tasks = ctx.deps.tasks_db.read_tasks(db)
    if status:
        tasks = [task for task in tasks if task.status in status]

    status_counts = {}
    for task in tasks:
        status = task.status
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1
    for status, count in status_counts.items():
        print(f"Tasks with status '{status}': {count}")

    return [task.model_dump() for task in tasks]

@agent.tool
async def update_or_create_task(ctx: RunContext[Deps], tasks: list[Task], db = "tasks") -> None:
    """Write or update tasks to the database.

    Args:
        ctx: The context.
        tasks: The list of tasks to write or update.
        db: The database to write the tasks to. It can be 'tasks' or 'archived_tasks'.
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
