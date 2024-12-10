import pytest
from unittest.mock import Mock, patch
from ramon.plugins.jira import create_issue_in_jira, get_jira_instance
from ramon.models import Task, StatusEnum

@pytest.fixture
def mock_jira():
    with patch('ramon.plugins.jira.JIRA') as mock_jira:
        # Create a mock issue with a key attribute
        mock_issue = Mock()
        mock_issue.key = "TEST-123"
        
        # Configure the mock JIRA instance
        mock_jira_instance = mock_jira.return_value
        mock_jira_instance.create_issue.return_value = mock_issue
        
        yield mock_jira_instance

@pytest.fixture
def sample_task():
    return Task(
        id="task-1",
        task="Test JIRA Integration",
        owner="test-user",
        priority="High",
        description="This is a test description",
        due_date="2024-03-20",
        completed_at="",
        metadata="",
        status=StatusEnum.to_do
    )

@pytest.fixture
def mock_env_vars():
    with patch.dict('os.environ', {
        'JIRA_SERVER': 'https://your-domain.atlassian.net',
        'JIRA_EMAIL': 'test@example.com',
        'JIRA_TOKEN': 'dummy-token'
    }):
        yield

def test_get_jira_instance(mock_env_vars):
    with patch('ramon.plugins.jira.JIRA') as mock_jira:
        get_jira_instance()
        
        mock_jira.assert_called_once_with(
            server='https://your-domain.atlassian.net',
            basic_auth=('test@example.com', 'dummy-token')
        )

def test_create_issue_success(mock_jira, sample_task, mock_env_vars):
    success, issue_key = create_issue_in_jira("TEST", sample_task)
    
    assert success is True
    assert issue_key == "TEST-123"
    
    # Verify JIRA create_issue was called with correct parameters
    mock_jira.create_issue.assert_called_once_with(
        project="TEST",
        summary=sample_task.task,
        description=sample_task.description,
        issuetype={'name': 'Task'},
        priority={'name': sample_task.priority}
    )

def test_create_issue_missing_fields(mock_jira, mock_env_vars):
    task = Task(
        id="task-2",
        task="",  # Empty summary
        owner="test-user",
        priority="High",
        description="",  # Empty description
        due_date="2024-03-20",
        completed_at="",
        metadata="",
        status=StatusEnum.to_do
    )
    
    success, issue_key = create_issue_in_jira("TEST", task)
    
    assert success is False
    assert issue_key == ""
    # Verify create_issue was not called
    mock_jira.create_issue.assert_not_called()

def test_create_issue_jira_error(mock_jira, sample_task, mock_env_vars):
    # Configure mock to raise an exception
    mock_jira.create_issue.side_effect = Exception("JIRA API Error")
    
    success, issue_key = create_issue_in_jira("TEST", sample_task)
    
    assert success is False
    assert issue_key == ""

def test_create_issue_missing_project_key(mock_jira, sample_task, mock_env_vars):
    success, issue_key = create_issue_in_jira("", sample_task)
    
    assert success is False
    assert issue_key == ""
    mock_jira.create_issue.assert_not_called()

def test_create_issue_priority_handling(mock_jira, sample_task, mock_env_vars):
    # Test with no priority
    sample_task.priority = None
    success, issue_key = create_issue_in_jira("TEST", sample_task)
    
    assert success is True
    assert issue_key == "TEST-123"
    
    # Verify default priority was used
    mock_jira.create_issue.assert_called_once_with(
        project="TEST",
        summary=sample_task.task,
        description=sample_task.description,
        issuetype={'name': 'Task'},
        priority={'name': 'Medium'}  # Default priority
    ) 