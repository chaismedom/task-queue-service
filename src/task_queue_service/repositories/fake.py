from uuid import UUID

from task_queue_service.repositories.interface import (
    AbstractTaskRepository,
    TaskNotFoundError,
)
from task_queue_service.task import Task


class FakeTaskRepository(AbstractTaskRepository):
    def __init__(self, db: list[Task] | None = None) -> None:
        self.db: list[Task] = db or []

    async def add(self, task: Task) -> None:
        self.db.append(task)

    async def persist(self, task: Task) -> None:
        previous_task_in_db = (db_task for db_task in self.db if db_task.id_ == task.id_)
        try:
            previous_task = next(previous_task_in_db)
        except StopIteration:
            raise TaskNotFoundError

        self.db.remove(previous_task)
        self.db.append(task)

    async def get_by_id(self, task_id: UUID) -> Task:
        task_in_db = (db_task for db_task in self.db if db_task.id_ == task_id)

        try:
            return next(task_in_db)
        except StopIteration:
            raise TaskNotFoundError

    async def list_expired(self) -> list[Task]:
        return [task for task in self.db if task.is_expired()]
