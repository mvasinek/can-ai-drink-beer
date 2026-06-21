from tasks_mcp_server.mcp_api_client import TasksApiClient


def task_to_dict(task: dict, *, concise: bool = False) -> dict:
    data = {
        "id": task["id"],
        "title": task["title"],
        "description": task.get("description"),
        "status": task["status"],
    }
    if not concise:
        data.update(
            {
                "created_at": task.get("created_at"),
                "updated_at": task.get("updated_at"),
                "completed_at": task.get("completed_at"),
            }
        )
    return data


def _is_api_error(result: dict) -> bool:
    return result.get("success") is False and "message" in result


def get_next_task(client: TasksApiClient) -> dict:
    result = client.get_next_open_task()
    if _is_api_error(result):
        return result
    if "message" in result:
        return result
    return task_to_dict(result, concise=True)


def mark_task_done(client: TasksApiClient, task_id: int) -> dict:
    result = client.mark_task_done(task_id)
    if _is_api_error(result):
        return result
    if "message" in result and result.get("success") is False:
        return result
    return {"success": True, "task_id": result["id"], "status": result["status"]}


def get_task(client: TasksApiClient, task_id: int) -> dict:
    result = client.get_task(task_id)
    if _is_api_error(result):
        return result
    if "message" in result:
        return result
    return task_to_dict(result)


def list_open_tasks(client: TasksApiClient) -> dict:
    result = client.list_open_tasks()
    if isinstance(result, dict) and _is_api_error(result):
        return result
    tasks = result
    return {
        "tasks": [task_to_dict(task, concise=True) for task in tasks],
        "count": len(tasks),
    }


def get_open_tasks_resource(client: TasksApiClient) -> dict:
    return list_open_tasks(client)
