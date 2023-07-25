from typing import Protocol
from uuid import UUID

from task_queue_service.task import TaskStatus


class AbstractPollTasksUseCase(Protocol):
    async def __call__(self) -> None:
        """Polling tasks and update"""


class AbstractAddTaskUseCase(Protocol):
    async def __call__(self, task_title: str) -> UUID:
        """Create task and send into queue."""


class AbstractGetTaskStatusUseCase(Protocol):
    async def __call__(self, task_id: UUID) -> TaskStatus:
        """Get task status."""
