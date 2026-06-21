from datetime import UTC, datetime

from sqlmodel import Session, select

from tasks_mcp_server.models import Task, TaskStatus
from tasks_mcp_server.schemas import TaskCreate, TaskUpdate


def create_task(session: Session, task_create: TaskCreate) -> Task:
    now = datetime.now(UTC)
    task = Task(
        title=task_create.title,
        description=task_create.description,
        status=TaskStatus.OPEN,
        created_at=now,
        updated_at=now,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)


def list_tasks(session: Session, *, status: TaskStatus | None = None) -> list[Task]:
    statement = select(Task)
    if status is not None:
        statement = statement.where(Task.status == status)
    statement = statement.order_by(Task.created_at.desc())
    return list(session.exec(statement).all())


def update_task(session: Session, task_id: int, task_update: TaskUpdate) -> Task | None:
    task = session.get(Task, task_id)
    if task is None:
        return None

    update_data = task_update.model_dump(exclude_unset=True)
    now = datetime.now(UTC)

    if "status" in update_data:
        new_status = update_data["status"]
        if new_status == TaskStatus.DONE and task.status != TaskStatus.DONE:
            task.completed_at = now
        elif new_status != TaskStatus.DONE and task.status == TaskStatus.DONE:
            task.completed_at = None

    for key, value in update_data.items():
        setattr(task, key, value)
    task.updated_at = now

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)
    if task is None:
        return False
    session.delete(task)
    session.commit()
    return True


def get_next_open_task(session: Session) -> Task | None:
    statement = (
        select(Task)
        .where(Task.status == TaskStatus.OPEN)
        .order_by(Task.created_at.asc())
    )
    return session.exec(statement).first()


def mark_task_done(session: Session, task_id: int) -> Task | None:
    task = session.get(Task, task_id)
    if task is None:
        return None

    now = datetime.now(UTC)
    task.status = TaskStatus.DONE
    task.completed_at = now
    task.updated_at = now

    session.add(task)
    session.commit()
    session.refresh(task)
    return task
