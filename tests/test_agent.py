from datetime import timezone
import pytest
from dirty_equals import IsNow
import json

from pydantic_ai import models
from pydantic_ai.models.test import TestModel
from pydantic_ai.messages import (
    SystemPrompt,
    UserPrompt,
    ModelStructuredResponse,
    ToolCall,
    ArgsDict,
    ToolReturn,
    ModelTextResponse,
)



from ramon.models import Database, StatusEnum
from ramon.agent import agent, SYSTEM_PROMPT, JiraClient, Deps

pytestmark = pytest.mark.anyio
models.ALLOW_MODEL_REQUESTS = False


@pytest.fixture
def temp_tasks_file(tmp_path):
    tasks_file = tmp_path / "tasks.json"
    sample_tasks = [
        {
            "id": "task-1",
            "task": "Existing task",
            "owner": "test-user",
            "priority": "medium",
            "description": "Existing description",
            "due_date": "2024-03-21",
            "completed_at": "",
            "metadata": "",
            "status": "to_do"
        }
    ]
    tasks_file.write_text(json.dumps(sample_tasks))
    return tasks_file

@pytest.fixture
def deps(temp_tasks_file):
    return Deps(
        tasks_db=Database(tasks_file=temp_tasks_file),
        jira_client=JiraClient()
    )

async def test_get_tasks(deps):
    with agent.override(model=TestModel(call_tools=['get_tasks'])):
        await agent.run(
            "Show me all tasks",
            deps=deps
        )

        assert agent.last_run_messages == [
            SystemPrompt(content=SYSTEM_PROMPT, role="system"),
            UserPrompt(
                content="Show me all tasks",
                timestamp=IsNow(tz=timezone.utc),
            ),
            ModelStructuredResponse(
                calls=[ToolCall(tool_name="get_tasks", args=ArgsDict(args_dict={}))],
                timestamp=IsNow(tz=timezone.utc),
            ),
            ToolReturn(
                tool_name="get_tasks",
                content=[
                    {
                        "id": "task-1",
                        "task": "Existing task",
                        "owner": "test-user",
                        "priority": "medium",
                        "description": "Existing description",
                        "due_date": "2024-03-21",
                        "completed_at": "",
                        "metadata": "",
                        "status": StatusEnum.to_do,
                    }
                ],
                timestamp=IsNow(tz=timezone.utc),
            ),
            ModelTextResponse(
                content='{"get_tasks":[{"id":"task-1","task":"Existing task","owner":"test-user","priority":"medium","description":"Existing description","due_date":"2024-03-21","completed_at":"","metadata":"","status":"to_do"}]}',
                timestamp=IsNow(tz=timezone.utc),
            ),
        ]
