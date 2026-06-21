from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from tasks_mcp_server.app import app
from tasks_mcp_server.database import (
    create_db_and_tables,
    get_db,
    get_session,
    reset_engine,
)

IN_MEMORY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(autouse=True)
def _reset_engine() -> Generator[None, None, None]:
    reset_engine()
    yield
    reset_engine()
    app.dependency_overrides.clear()


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    monkeypatch.setenv("TASKS_MCP_DATABASE_URL", IN_MEMORY_DATABASE_URL)
    reset_engine()
    create_db_and_tables(database_url=IN_MEMORY_DATABASE_URL)

    def override_get_db() -> Generator:
        with get_session(database_url=IN_MEMORY_DATABASE_URL) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task(client: TestClient) -> None:
    response = client.post(
        "/api/tasks",
        json={"title": "Example task", "description": "Created through REST API"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Example task"
    assert data["description"] == "Created through REST API"
    assert data["status"] == "open"
    assert data["id"] is not None


def test_list_tasks(client: TestClient) -> None:
    client.post("/api/tasks", json={"title": "First"})
    client.post("/api/tasks", json={"title": "Second"})

    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Second"
    assert tasks[1]["title"] == "First"


def test_filter_tasks_by_status(client: TestClient) -> None:
    open_task = client.post("/api/tasks", json={"title": "Open task"}).json()
    done_task = client.post("/api/tasks", json={"title": "Done task"}).json()
    client.post(f"/api/tasks/{done_task['id']}/done")

    response = client.get("/api/tasks", params={"status": "open"})
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == open_task["id"]


def test_get_existing_task(client: TestClient) -> None:
    created = client.post("/api/tasks", json={"title": "Lookup me"}).json()
    response = client.get(f"/api/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Lookup me"


def test_get_missing_task_returns_404(client: TestClient) -> None:
    response = client.get("/api/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task(client: TestClient) -> None:
    created = client.post("/api/tasks", json={"title": "Original"}).json()
    response = client.patch(
        f"/api/tasks/{created['id']}",
        json={"title": "Updated title", "status": "in_progress"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["status"] == "in_progress"


def test_update_missing_task_returns_404(client: TestClient) -> None:
    response = client.patch("/api/tasks/999", json={"title": "Missing"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task(client: TestClient) -> None:
    created = client.post("/api/tasks", json={"title": "Delete me"}).json()
    response = client.delete(f"/api/tasks/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/api/tasks/{created['id']}").status_code == 404


def test_delete_missing_task_returns_404(client: TestClient) -> None:
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_mark_task_done(client: TestClient) -> None:
    created = client.post("/api/tasks", json={"title": "Finish me"}).json()
    response = client.post(f"/api/tasks/{created['id']}/done")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    assert data["completed_at"] is not None


def test_mark_missing_task_done_returns_404(client: TestClient) -> None:
    response = client.post("/api/tasks/999/done")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_get_next_open_task(client: TestClient) -> None:
    first = client.post("/api/tasks", json={"title": "First open"}).json()
    client.post("/api/tasks", json={"title": "Second open"})
    client.patch(f"/api/tasks/{first['id']}", json={"status": "in_progress"})

    response = client.get("/api/tasks/next/open")
    assert response.status_code == 200
    assert response.json()["title"] == "Second open"


def test_get_next_open_task_returns_404_when_none(client: TestClient) -> None:
    response = client.get("/api/tasks/next/open")
    assert response.status_code == 404
    assert response.json() == {"detail": "No open task found"}
