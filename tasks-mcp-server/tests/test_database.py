import pytest
from sqlmodel import Session

from tasks_mcp_server.database import (
    create_db_and_tables,
    get_engine,
    get_session,
    reset_engine,
)
from tasks_mcp_server.models import Task, TaskStatus

IN_MEMORY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(autouse=True)
def _reset_engine():
    reset_engine()
    yield
    reset_engine()


@pytest.fixture
def database_url() -> str:
    return IN_MEMORY_DATABASE_URL


@pytest.fixture
def session(database_url: str):
    create_db_and_tables(database_url=database_url)
    with get_session(database_url=database_url) as db_session:
        yield db_session


def test_create_db_and_tables(database_url: str):
    create_db_and_tables(database_url=database_url)
    engine = get_engine(database_url=database_url)
    assert engine is not None


def test_get_session(database_url: str):
    create_db_and_tables(database_url=database_url)
    with get_session(database_url=database_url) as db_session:
        assert isinstance(db_session, Session)


def test_insert_and_read_task(session: Session):
    task = Task(title="Test task", status=TaskStatus.OPEN)
    session.add(task)
    session.commit()
    session.refresh(task)

    loaded = session.get(Task, task.id)
    assert loaded is not None
    assert loaded.title == "Test task"
    assert loaded.status == TaskStatus.OPEN
