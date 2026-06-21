import pytest
from sqlmodel import select

import load_sample_tasks
from tasks_mcp_server.database import get_session, reset_engine
from tasks_mcp_server.models import Task

IN_MEMORY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(autouse=True)
def _reset_engine(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("TASKS_MCP_DATABASE_URL", IN_MEMORY_DATABASE_URL)
    reset_engine()
    yield
    reset_engine()


def test_load_sample_tasks_creates_records(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TASKS_MCP_DATABASE_URL", IN_MEMORY_DATABASE_URL)

    reset_engine()
    created_count = load_sample_tasks.load_sample_tasks(
        load_sample_tasks.DEFAULT_SAMPLE_FILE
    )

    assert created_count == 3

    with get_session(database_url=IN_MEMORY_DATABASE_URL) as session:
        tasks = list(session.exec(select(Task)).all())
        assert len(tasks) == 3
        titles = {task.title for task in tasks}
        assert "Create hello_mcp.txt" in titles
