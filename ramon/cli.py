import click
from click_default_group import DefaultGroup
from ramon import (
    agent,
    Database,
    JiraClient,
    Deps,
    Message,
    summarize_tasks
)

import logfire
logfire.configure(send_to_logfire='if-token-present')

@click.group(cls=DefaultGroup, default='chat', default_if_no_args=True)
def cli():
    pass

@cli.command()
@click.argument('prompt', required=False, default='What do I need to work on?')
def chat(prompt: str) -> None: 
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


@cli.command()
def archive_completed_tasks() -> None:
    """Archive all completed tasks."""
    database = Database()
    tasks = database.read_tasks()
    completed_tasks = [task for task in tasks if task.status == "completed"]    
    for task in completed_tasks:
        database.archive_task(task.id)
    click.echo(f"Archived {len(completed_tasks)} completed tasks.")

@cli.command()
@click.option('--smart', is_flag=True, help='Show a smart summary of the tasks.')
def summary(smart: bool) -> None:
    """Show a summary of the tasks."""
    database = Database()
    tasks = database.read_tasks()
    print(summarize_tasks(tasks, smart))
