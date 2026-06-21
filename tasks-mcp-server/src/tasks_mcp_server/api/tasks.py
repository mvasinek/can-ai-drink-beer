from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session

from tasks_mcp_server.database import get_db
from tasks_mcp_server.models import TaskStatus
from tasks_mcp_server.schemas import TaskCreate, TaskRead, TaskUpdate
from tasks_mcp_server.services import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def get_task_service(session: Session = Depends(get_db)) -> TaskService:
    return TaskService(session)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    status: TaskStatus | None = Query(default=None),
    service: TaskService = Depends(get_task_service),
) -> list[TaskRead]:
    return service.list_tasks(status=status)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskRead:
    return service.create_task(task_create)


@router.get("/next/open", response_model=TaskRead)
def get_next_open_task(
    service: TaskService = Depends(get_task_service),
) -> TaskRead:
    task = service.get_next_open_task()
    if task is None:
        raise HTTPException(status_code=404, detail="No open task found")
    return task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskRead:
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskRead:
    task = service.update_task(task_id, task_update)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> Response:
    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{task_id}/done", response_model=TaskRead)
def mark_task_done(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskRead:
    task = service.mark_task_done(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
