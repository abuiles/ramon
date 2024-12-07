import click
from click_default_group import DefaultGroup
import asyncio
from ramon import (
    agent,
    Database,
    JiraClient,
    Deps,
    Message,
)    

@click.group(cls=DefaultGroup, default='chat', default_if_no_args=True)
def cli():
    pass

@cli.command()
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
