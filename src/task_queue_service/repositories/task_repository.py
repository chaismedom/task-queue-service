from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from task_queue_service.db.tables import TaskTable
from task_queue_service.repositories.interface import (
    AbstractTaskRepository,
    TaskNotFoundError,
)
from task_queue_service.task import Task, TaskStatus


class TaskRepository(AbstractTaskRepository):
    def __init__(self, db_session: AsyncSession) -> None:
        self.session = db_session

    async def get_by_id(self, task_id: UUID) -> Task:
        result = await self.session.execute(
            select(TaskTable).where(TaskTable.id == task_id)
        )
        task_row = result.scalar_one_or_none()
        if not task_row:
            raise TaskNotFoundError

        return self._map_into_domain(task_row)

    async def add(self, task: Task) -> None:
        task_row = TaskTable(
            id=task.id_,
            title=task.title,
            waiting_time=task.waiting_time,
            status=task.status.value,
        )
        self.session.add(task_row)
        await self.session.flush()

    async def persist(self, task: Task) -> None:
        result = await self.session.execute(
            update(TaskTable)
            .values(
                title=task.title,
                waiting_time=task.waiting_time,
                status=task.status.value,
            )
            .where(TaskTable.id == task.id_)
            .returning(TaskTable.id)
        )
        is_in_db = result.scalar_one_or_none()
        if is_in_db is None:
            raise TaskNotFoundError

        await self.session.flush()

    async def list_expired(self) -> list[Task]:
        result = await self.session.execute(
            select(TaskTable).where(TaskTable.waiting_time < datetime.now())
        )
        expired_tasks_rows = result.scalars().all()
        return [self._map_into_domain(row) for row in expired_tasks_rows]

    def _map_into_domain(self, row: TaskTable) -> Task:
        return Task(
            id_=row.id,
            title=row.title,
            waiting_time=row.waiting_time,
            status=TaskStatus(row.status),
        )
