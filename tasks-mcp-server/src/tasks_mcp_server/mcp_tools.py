from tasks_mcp_server.models import TaskStatus
from tasks_mcp_server.schemas import TaskRead
from tasks_mcp_server.services import TaskService


def task_to_dict(task: TaskRead, *, concise: bool = False) -> dict:
    data = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
    }
    if not concise:
        data.update(
            {
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "completed_at": (
                    task.completed_at.isoformat() if task.completed_at else None
                ),
            }
        )
    return data


def get_next_task(service: TaskService) -> dict:
    task = service.get_next_open_task()
    if task is None:
        return {"message": "No open task found"}
    return task_to_dict(task, concise=True)


def mark_task_done(service: TaskService, task_id: int) -> dict:
    task = service.mark_task_done(task_id)
    if task is None:
        return {"success": False, "message": "Task not found"}
    return {"success": True, "task_id": task.id, "status": task.status.value}


def get_task(service: TaskService, task_id: int) -> dict:
    task = service.get_task(task_id)
    if task is None:
        return {"message": "Task not found"}
    return task_to_dict(task)


def list_open_tasks(service: TaskService) -> dict:
    tasks = service.list_tasks(status=TaskStatus.OPEN)
    return {
        "tasks": [task_to_dict(task, concise=True) for task in tasks],
        "count": len(tasks),
    }


def get_open_tasks_resource(service: TaskService) -> dict:
    return list_open_tasks(service)
