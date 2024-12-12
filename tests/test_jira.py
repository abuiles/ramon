import pytest
from unittest.mock import Mock, patch
from ramon.plugins.jira import (
    get_jira_instance,
    get_task_status_in_jira,
    get_task_assignee_in_jira,
    add_comment_to_jira_issue,
    load_comments_for_jira_issue,
    open_jira_issue,
    get_jira_issue_url,
)

@pytest.fixture
def mock_env_vars():
    with patch.dict('os.environ', {
        'JIRA_SERVER': 'https://test.atlassian.net',
        'JIRA_EMAIL': 'test@example.com',
        'JIRA_TOKEN': 'test-token'
    }):
        yield

@pytest.fixture
def mock_jira():
    with patch('ramon.plugins.jira.JIRA') as mock:
        yield mock

def test_get_jira_instance(mock_env_vars, mock_jira):
    get_jira_instance()
    mock_jira.assert_called_once_with(
        server='https://test.atlassian.net',
        basic_auth=('test@example.com', 'test-token')
    )

def test_get_task_status_in_jira(mock_env_vars, mock_jira):
    # Setup mock issue
    mock_issue = Mock()
    mock_issue.fields.status.name = 'In Progress'
    mock_jira.return_value.issue.return_value = mock_issue

    status = get_task_status_in_jira('TEST-123')
    assert status == 'In Progress'
    mock_jira.return_value.issue.assert_called_once_with('TEST-123')

def test_get_task_assignee_in_jira_with_assignee(mock_env_vars, mock_jira):
    # Setup mock issue with assignee
    mock_issue = Mock()
    mock_issue.fields.assignee.displayName = 'John Doe'
    mock_jira.return_value.issue.return_value = mock_issue

    assignee = get_task_assignee_in_jira('TEST-123')
    assert assignee == 'John Doe'
    mock_jira.return_value.issue.assert_called_once_with('TEST-123')

def test_get_task_assignee_in_jira_unassigned(mock_env_vars, mock_jira):
    # Setup mock issue without assignee
    mock_issue = Mock()
    mock_issue.fields.assignee = None
    mock_jira.return_value.issue.return_value = mock_issue

    assignee = get_task_assignee_in_jira('TEST-123')
    assert assignee == 'Unassigned'
    mock_jira.return_value.issue.assert_called_once_with('TEST-123')

def test_add_comment_to_jira_issue(mock_env_vars, mock_jira):
    add_comment_to_jira_issue('TEST-123', 'Test comment')
    mock_jira.return_value.add_comment.assert_called_once_with('TEST-123', 'Test comment')

def test_load_comments_for_jira_issue(mock_env_vars, mock_jira):
    # Setup mock comments
    mock_comment1 = Mock()
    mock_comment1.author.displayName = 'John Doe'
    mock_comment1.body = 'First comment'
    
    mock_comment2 = Mock()
    mock_comment2.author.displayName = 'Jane Smith'
    mock_comment2.body = 'Second comment'

    mock_issue = Mock()
    mock_issue.fields.comment.comments = [mock_comment1, mock_comment2]
    mock_jira.return_value.issue.return_value = mock_issue

    comments = load_comments_for_jira_issue('TEST-123')
    assert len(comments) == 2
    assert comments[0] == 'from: John Doe, message: First comment'
    assert comments[1] == 'from: Jane Smith, message: Second comment'
    mock_jira.return_value.issue.assert_called_once_with('TEST-123')

@patch('webbrowser.open')
def test_open_jira_issue(mock_webbrowser, mock_env_vars):
    open_jira_issue('TEST-123')
    mock_webbrowser.assert_called_once_with('https://test.atlassian.net/browse/TEST-123')

def test_get_jira_issue_url(mock_env_vars):
    url = get_jira_issue_url('TEST-123')
    assert url == 'https://test.atlassian.net/browse/TEST-123'