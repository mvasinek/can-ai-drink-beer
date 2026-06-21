from fastapi.testclient import TestClient

from tasks_mcp_server.app import app


def test_index_page_returns_200() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Tasks MCP Server" in response.text
