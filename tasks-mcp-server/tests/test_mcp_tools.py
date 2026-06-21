import pytest

from tasks_mcp_server.database import create_db_and_tables, get_session, reset_engine
from tasks_mcp_server.mcp_tools import (
    get_next_task,
    get_task,
    list_open_tasks,
    mark_task_done,
)
from tasks_mcp_server.models import TaskStatus
from tasks_mcp_server.schemas import TaskCreate, TaskUpdate
from tasks_mcp_server.services import TaskService

IN_MEMORY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(autouse=True)
def _reset_engine():
    reset_engine()
    yield
    reset_engine()


@pytest.fixture
def service() -> TaskService:
    create_db_and_tables(database_url=IN_MEMORY_DATABASE_URL)
    with get_session(database_url=IN_MEMORY_DATABASE_URL) as session:
        yield TaskService(session)


def test_get_next_task_returns_oldest_open(service: TaskService) -> None:
    oldest = service.create_task(TaskCreate(title="First", description="Oldest"))
    service.create_task(TaskCreate(title="Second", description="Later"))

    result = get_next_task(service)

    assert result["id"] == oldest.id
    assert result["title"] == "First"
    assert result["status"] == "open"


def test_get_next_task_returns_message_when_none(service: TaskService) -> None:
    result = get_next_task(service)
    assert result == {"message": "No open task found"}


def test_mark_task_done_success(service: TaskService) -> None:
    created = service.create_task(TaskCreate(title="Finish me"))

    result = mark_task_done(service, created.id)

    assert result == {"success": True, "task_id": created.id, "status": "done"}


def test_mark_task_done_not_found(service: TaskService) -> None:
    result = mark_task_done(service, 999)
    assert result == {"success": False, "message": "Task not found"}


def test_get_task_returns_full_task(service: TaskService) -> None:
    created = service.create_task(
        TaskCreate(title="Lookup", description="Full details"),
    )

    result = get_task(service, created.id)

    assert result["id"] == created.id
    assert result["title"] == "Lookup"
    assert result["description"] == "Full details"
    assert result["status"] == "open"
    assert "created_at" in result
    assert "updated_at" in result


def test_get_task_not_found(service: TaskService) -> None:
    result = get_task(service, 999)
    assert result == {"message": "Task not found"}


def test_list_open_tasks(service: TaskService) -> None:
    open_task = service.create_task(TaskCreate(title="Open task"))
    done_task = service.create_task(TaskCreate(title="Done task"))
    service.mark_task_done(done_task.id)
    service.update_task(
        open_task.id,
        TaskUpdate(status=TaskStatus.IN_PROGRESS),
    )
    service.create_task(TaskCreate(title="Another open"))

    result = list_open_tasks(service)

    assert result["count"] == 1
    assert len(result["tasks"]) == 1
    assert result["tasks"][0]["title"] == "Another open"
