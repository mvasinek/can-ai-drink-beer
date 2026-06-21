from unittest.mock import MagicMock

import pytest

from tasks_mcp_server.mcp_api_client import TasksApiClient
from tasks_mcp_server.mcp_tools import (
    get_next_task,
    get_task,
    list_open_tasks,
    mark_task_done,
)

SAMPLE_TASK = {
    "id": 1,
    "title": "First",
    "description": "Oldest",
    "status": "open",
    "created_at": "2026-01-01T12:00:00+00:00",
    "updated_at": "2026-01-01T12:00:00+00:00",
    "completed_at": None,
}


@pytest.fixture
def client() -> MagicMock:
    return MagicMock(spec=TasksApiClient)


def test_get_next_task_returns_concise_task(client: MagicMock) -> None:
    client.get_next_open_task.return_value = SAMPLE_TASK

    result = get_next_task(client)

    assert result == {
        "id": 1,
        "title": "First",
        "description": "Oldest",
        "status": "open",
    }


def test_get_next_task_returns_message_when_none(client: MagicMock) -> None:
    client.get_next_open_task.return_value = {"message": "No open task found"}

    result = get_next_task(client)

    assert result == {"message": "No open task found"}


def test_mark_task_done_success(client: MagicMock) -> None:
    client.mark_task_done.return_value = {**SAMPLE_TASK, "status": "done"}

    result = mark_task_done(client, 1)

    assert result == {"success": True, "task_id": 1, "status": "done"}


def test_mark_task_done_not_found(client: MagicMock) -> None:
    client.mark_task_done.return_value = {
        "success": False,
        "message": "Task not found",
    }

    result = mark_task_done(client, 999)

    assert result == {"success": False, "message": "Task not found"}


def test_get_task_returns_full_task(client: MagicMock) -> None:
    client.get_task.return_value = SAMPLE_TASK

    result = get_task(client, 1)

    assert result["id"] == 1
    assert result["title"] == "First"
    assert "created_at" in result


def test_get_task_not_found(client: MagicMock) -> None:
    client.get_task.return_value = {"message": "Task not found"}

    result = get_task(client, 999)

    assert result == {"message": "Task not found"}


def test_list_open_tasks(client: MagicMock) -> None:
    client.list_open_tasks.return_value = [SAMPLE_TASK]

    result = list_open_tasks(client)

    assert result["count"] == 1
    assert result["tasks"][0]["title"] == "First"
