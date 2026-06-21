import json
from collections.abc import Callable
from typing import Any

from mcp.server.fastmcp import FastMCP

from tasks_mcp_server.mcp_api_client import TasksApiClient
from tasks_mcp_server.mcp_tools import (
    get_next_task as get_next_task_result,
)
from tasks_mcp_server.mcp_tools import (
    get_open_tasks_resource,
)
from tasks_mcp_server.mcp_tools import (
    get_task as get_task_result,
)
from tasks_mcp_server.mcp_tools import (
    list_open_tasks as list_open_tasks_result,
)
from tasks_mcp_server.mcp_tools import (
    mark_task_done as mark_task_done_result,
)

IMPLEMENT_NEXT_TASK_PROMPT = """Use the Tasks MCP Server tools to complete work:

1. Call get_next_task to retrieve the next open task.
2. Implement the requested change in the project.
3. Call mark_task_done with the task ID when the work is finished.

If no open task exists, report that no work is pending."""

mcp = FastMCP(
    "Tasks MCP Server",
    instructions=(
        "Task management tools for a local demo project. "
        "Tools call the Tasks REST API. Start the web app before using them."
    ),
)

_api_client = TasksApiClient()


def _run_with_client(action: Callable[[TasksApiClient], Any]) -> Any:
    return action(_api_client)


@mcp.tool()
def get_next_task() -> dict:
    """Return the oldest task with status open."""
    return _run_with_client(get_next_task_result)


@mcp.tool()
def mark_task_done(task_id: int) -> dict:
    """Mark a task as done and set its completion timestamp."""
    return _run_with_client(
        lambda client: mark_task_done_result(client, task_id),
    )


@mcp.tool()
def get_task(task_id: int) -> dict:
    """Return complete information for a task by ID."""
    return _run_with_client(lambda client: get_task_result(client, task_id))


@mcp.tool()
def list_open_tasks() -> dict:
    """List all tasks with status open."""
    return _run_with_client(list_open_tasks_result)


@mcp.resource("tasks://open")
def open_tasks_resource() -> str:
    """Expose all open tasks as a JSON resource."""
    result = _run_with_client(get_open_tasks_resource)
    return json.dumps(result, indent=2)


@mcp.prompt()
def implement_next_task() -> str:
    """Guide an agent through retrieving, implementing, and completing a task."""
    return IMPLEMENT_NEXT_TASK_PROMPT


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
