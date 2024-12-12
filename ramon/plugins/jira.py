from jira import JIRA
import os
from ramon.models import Task
import webbrowser

def get_jira_instance() -> JIRA:
    server = os.getenv('JIRA_SERVER')
    email = os.getenv('JIRA_EMAIL')
    api_token = os.getenv('JIRA_TOKEN')
    return JIRA(server=server, basic_auth=(email, api_token))



def get_task_status_in_jira(task_key: str) -> str:
    jira = get_jira_instance()
    issue = jira.issue(task_key)
    return issue.fields.status.name

def create_issue_in_jira(project_key: str, task: Task) -> tuple[bool, str]:
    """
    Creates an issue in JIRA based on the provided task and project key.

    Args:
        project_key (str): The key of the JIRA project where the issue will be created.
        task (Task): The task object containing details for the JIRA issue.

    Returns:
        tuple (bool, str): A tuple containing a boolean indicating success or failure, 
                           and a string with the issue key if successful, or an empty string if not.
    """
    jira = get_jira_instance()

    summary = task.task
    description = task.description
    issue_type = 'Task'
    priority = task.priority if task.priority else 'Medium'

    if not project_key or not summary or not description:
        print(f"Skipping task due to missing fields: {task}")
        return (False, "")

    # Debug print all arguments
    print("Creating JIRA issue with arguments:")
    print(f"  project: {project_key}")
    print(f"  summary: {summary}")
    print(f"  description: {description}")
    print(f"  issuetype: {{'name': {issue_type}}}")
    print(f"  priority: {{'name': {priority}}}")

    try:
        new_issue = jira.create_issue(
            project=project_key,
            summary=summary,
            description=description,
            issuetype={'name': issue_type},
            priority={'name': priority}
        )
        print(f"Issue created: {new_issue.key}")
        return (True, new_issue.key)
    except Exception as e:
        print(f"Failed to create issue: {task}. Error: {e}")
        return (False, "")

def get_task_assignee_in_jira(task_key: str) -> str:
    """
    Gets the assignee name for a JIRA task.
    
    Args:
        task_key (str): The JIRA issue key (e.g., 'PROJ-123')
    
    Returns:
        str: The assignee's display name or 'Unassigned' if no assignee
    """
    jira = get_jira_instance()
    issue = jira.issue(task_key)
    assignee = issue.fields.assignee
    return assignee.displayName if assignee else 'Unassigned'

def add_comment_to_jira_issue(task_key: str, comment: str) -> None:
    """
    Adds a comment to a JIRA issue.
    
    Args:
        task_key: The JIRA issue key (e.g., 'PROJ-123')
        comment: The comment to add to the JIRA issue   

    Returns:
        None    
    """
    jira = get_jira_instance()
    jira.add_comment(task_key, comment)

def load_comments_for_jira_issue(task_key: str) -> list[str]:
    """
    Loads all comments for a JIRA issue.
    
    Args:
        task_key: The JIRA issue key (e.g., 'PROJ-123')

    Returns:
        list[str]: A list of comments from the JIRA issue.
    """
    jira = get_jira_instance()
    issue = jira.issue(task_key)
    return [f"from: {comment.author.displayName}, message: {comment.body}" for comment in issue.fields.comment.comments]
    
def open_jira_issue(task_key: str) -> None:
    """
    Opens the JIRA issue in the default web browser.
    
    Args:
        task_key: The JIRA issue key (e.g., 'PROJ-123')
    """
    webbrowser.open(get_jira_issue_url(task_key))
    

def get_jira_issue_url(task_key: str) -> str:
    return f"{os.getenv('JIRA_SERVER')}/browse/{task_key}"
