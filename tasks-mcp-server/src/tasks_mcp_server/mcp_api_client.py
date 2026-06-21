from typing import Any

import httpx

from tasks_mcp_server.config import get_api_base_url

API_UNAVAILABLE = {
    "success": False,
    "message": "Unable to contact Tasks REST API.",
}


class TasksApiClient:
    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 5.0,
    ) -> None:
        self.base_url = (base_url or get_api_base_url()).rstrip("/")
        self.timeout = timeout

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> tuple[int | None, dict[str, Any] | list[Any] | None]:
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                response = client.request(method, path, **kwargs)
        except httpx.HTTPError:
            return None, None

        if response.status_code == 204:
            return response.status_code, None

        try:
            payload = response.json()
        except ValueError:
            return response.status_code, None

        return response.status_code, payload

    def get_next_open_task(self) -> dict[str, Any]:
        status_code, data = self._request("GET", "/api/tasks/next/open")
        if status_code is None:
            return API_UNAVAILABLE.copy()
        if status_code == 404:
            return {"message": "No open task found"}
        if status_code != 200 or not isinstance(data, dict):
            return API_UNAVAILABLE.copy()
        return data

    def get_task(self, task_id: int) -> dict[str, Any]:
        status_code, data = self._request("GET", f"/api/tasks/{task_id}")
        if status_code is None:
            return API_UNAVAILABLE.copy()
        if status_code == 404:
            return {"message": "Task not found"}
        if status_code != 200 or not isinstance(data, dict):
            return API_UNAVAILABLE.copy()
        return data

    def list_open_tasks(self) -> dict[str, Any] | list[dict[str, Any]]:
        status_code, data = self._request(
            "GET",
            "/api/tasks",
            params={"status": "open"},
        )
        if status_code is None:
            return API_UNAVAILABLE.copy()
        if status_code != 200 or not isinstance(data, list):
            return API_UNAVAILABLE.copy()
        return data

    def mark_task_done(self, task_id: int) -> dict[str, Any]:
        status_code, data = self._request("POST", f"/api/tasks/{task_id}/done")
        if status_code is None:
            return API_UNAVAILABLE.copy()
        if status_code == 404:
            return {"success": False, "message": "Task not found"}
        if status_code != 200 or not isinstance(data, dict):
            return API_UNAVAILABLE.copy()
        return data
