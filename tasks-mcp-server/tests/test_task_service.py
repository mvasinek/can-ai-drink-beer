import time

import pytest

from tasks_mcp_server.database import create_db_and_tables, get_session, reset_engine
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


def test_create_task(service: TaskService):
    task = service.create_task(TaskCreate(title="Buy milk", description="2%"))

    assert task.id is not None
    assert task.title == "Buy milk"
    assert task.description == "2%"
    assert task.status == TaskStatus.OPEN
    assert task.completed_at is None


def test_list_tasks(service: TaskService):
    service.create_task(TaskCreate(title="First"))
    time.sleep(0.01)
    service.create_task(TaskCreate(title="Second"))

    tasks = service.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Second"
    assert tasks[1].title == "First"


def test_update_task(service: TaskService):
    created = service.create_task(TaskCreate(title="Original"))
    updated = service.update_task(
        created.id,
        TaskUpdate(title="Updated", status=TaskStatus.IN_PROGRESS),
    )

    assert updated is not None
    assert updated.title == "Updated"
    assert updated.status == TaskStatus.IN_PROGRESS


def test_get_next_open_task(service: TaskService):
    first = service.create_task(TaskCreate(title="First open"))
    time.sleep(0.01)
    service.create_task(TaskCreate(title="Second open"))
    service.update_task(first.id, TaskUpdate(status=TaskStatus.IN_PROGRESS))

    next_task = service.get_next_open_task()
    assert next_task is not None
    assert next_task.title == "Second open"


def test_mark_task_done(service: TaskService):
    created = service.create_task(TaskCreate(title="Finish me"))
    done = service.mark_task_done(created.id)

    assert done is not None
    assert done.status == TaskStatus.DONE
    assert done.completed_at is not None
    assert done.updated_at is not None


def test_delete_task(service: TaskService):
    created = service.create_task(TaskCreate(title="Temporary"))
    deleted = service.delete_task(created.id)

    assert deleted is True
    assert service.get_task(created.id) is None
