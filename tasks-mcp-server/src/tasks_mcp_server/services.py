from sqlmodel import Session

from tasks_mcp_server import repositories
from tasks_mcp_server.schemas import TaskCreate, TaskRead, TaskUpdate


class TaskService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_task(self, task_create: TaskCreate) -> TaskRead:
        task = repositories.create_task(self._session, task_create)
        return TaskRead.model_validate(task)

    def get_task(self, task_id: int) -> TaskRead | None:
        task = repositories.get_task(self._session, task_id)
        if task is None:
            return None
        return TaskRead.model_validate(task)

    def list_tasks(self) -> list[TaskRead]:
        tasks = repositories.list_tasks(self._session)
        return [TaskRead.model_validate(task) for task in tasks]

    def update_task(self, task_id: int, task_update: TaskUpdate) -> TaskRead | None:
        task = repositories.update_task(self._session, task_id, task_update)
        if task is None:
            return None
        return TaskRead.model_validate(task)

    def delete_task(self, task_id: int) -> bool:
        return repositories.delete_task(self._session, task_id)

    def get_next_open_task(self) -> TaskRead | None:
        task = repositories.get_next_open_task(self._session)
        if task is None:
            return None
        return TaskRead.model_validate(task)

    def mark_task_done(self, task_id: int) -> TaskRead | None:
        task = repositories.mark_task_done(self._session, task_id)
        if task is None:
            return None
        return TaskRead.model_validate(task)
