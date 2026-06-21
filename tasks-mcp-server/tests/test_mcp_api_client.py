from unittest.mock import MagicMock, patch

import httpx
import pytest

from tasks_mcp_server.mcp_api_client import TasksApiClient

BASE_URL = "http://127.0.0.1:8000"
SAMPLE_TASK = {
    "id": 1,
    "title": "Create hello_mcp.txt",
    "description": "Demo task",
    "status": "open",
    "created_at": "2026-01-01T12:00:00+00:00",
    "updated_at": "2026-01-01T12:00:00+00:00",
    "completed_at": None,
}


@pytest.fixture
def client() -> TasksApiClient:
    return TasksApiClient(base_url=BASE_URL)


def _mock_response(status_code: int, json_data):
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = json_data
    return response


@patch("tasks_mcp_server.mcp_api_client.httpx.Client")
def test_get_next_open_task_success(mock_client_cls, client: TasksApiClient) -> None:
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.request.return_value = _mock_response(200, SAMPLE_TASK)
    mock_client_cls.return_value = mock_client

    result = client.get_next_open_task()

    assert result == SAMPLE_TASK
    mock_client.request.assert_called_once_with("GET", "/api/tasks/next/open")


@patch("tasks_mcp_server.mcp_api_client.httpx.Client")
def test_get_next_open_task_not_found(mock_client_cls, client: TasksApiClient) -> None:
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.request.return_value = _mock_response(
        404,
        {"detail": "No open task found"},
    )
    mock_client_cls.return_value = mock_client

    result = client.get_next_open_task()

    assert result == {"message": "No open task found"}


@patch("tasks_mcp_server.mcp_api_client.httpx.Client")
def test_get_task_success(mock_client_cls, client: TasksApiClient) -> None:
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.request.return_value = _mock_response(200, SAMPLE_TASK)
    mock_client_cls.return_value = mock_client

    result = client.get_task(1)

    assert result == SAMPLE_TASK


@patch("tasks_mcp_server.mcp_api_client.httpx.Client")
def test_get_task_not_found(mock_client_cls, client: TasksApiClient) -> None:
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.request.return_value = _mock_response(404, {"detail": "Task not found"})
    mock_client_cls.return_value = mock_client

    result = client.get_task(999)

    assert result == {"message": "Task not found"}


@patch("tasks_mcp_server.mcp_api_client.httpx.Client")
def test_list_open_tasks_success(mock_client_cls, client: TasksApiClient) -> None:
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.request.return_value = _mock_response(200, [SAMPLE_TASK])
    mock_client_cls.return_value = mock_client

    result = client.list_open_tasks()

    assert result == [SAMPLE_TASK]
    mock_client.request.assert_called_once_with(
        "GET",
        "/api/tasks",
        params={"status": "open"},
    )


@patch("tasks_mcp_server.mcp_api_client.httpx.Client")
def test_mark_task_done_success(mock_client_cls, client: TasksApiClient) -> None:
    done_task = {
        **SAMPLE_TASK,
        "status": "done",
        "completed_at": "2026-01-02T12:00:00+00:00",
    }
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.request.return_value = _mock_response(200, done_task)
    mock_client_cls.return_value = mock_client

    result = client.mark_task_done(1)

    assert result == done_task
    mock_client.request.assert_called_once_with("POST", "/api/tasks/1/done")


@patch("tasks_mcp_server.mcp_api_client.httpx.Client")
def test_mark_task_done_not_found(mock_client_cls, client: TasksApiClient) -> None:
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.request.return_value = _mock_response(404, {"detail": "Task not found"})
    mock_client_cls.return_value = mock_client

    result = client.mark_task_done(999)

    assert result == {"success": False, "message": "Task not found"}


@patch("tasks_mcp_server.mcp_api_client.httpx.Client")
def test_api_unavailable(mock_client_cls, client: TasksApiClient) -> None:
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.request.side_effect = httpx.ConnectError("connection refused")
    mock_client_cls.return_value = mock_client

    result = client.get_next_open_task()

    assert result == {
        "success": False,
        "message": "Unable to contact Tasks REST API.",
    }
