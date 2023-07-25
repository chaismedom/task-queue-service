from typing import Protocol
from uuid import UUID

from task_queue_service.task import Task


class TaskNotFoundError(Exception):
    pass


class AbstractTaskRepository(Protocol):
    async def add(self, task: Task) -> None:
        """Add task to repository."""

    async def persist(self, task: Task) -> None:
        """Save task to repository.

        raises TaskNotFoundError: if task not found.
        """

    async def get_by_id(self, task_id: UUID) -> Task:
        """Get task by id.

        raises TaskNotFoundError: if task not found.
        """

    async def list_expired(self) -> list[Task]:
        """Get list of expired tasks."""

    async def commit(self) -> None:
        """Persist changes."""
        # It's better to move logic into UoW in case application will grow
        # But currently we only have one domain object
        # so it's quite easy to control sessions through the only repository.
