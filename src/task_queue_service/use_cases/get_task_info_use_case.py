from uuid import UUID

from task_queue_service.repositories.interface import AbstractTaskRepository
from task_queue_service.task import TaskStatus
from task_queue_service.use_cases.interface import AbstractGetTaskStatusUseCase


class GetTaskStatusUseCaseImpl(AbstractGetTaskStatusUseCase):
    def __init__(
        self,
        task_repository: AbstractTaskRepository,
    ) -> None:
        self._task_repository = task_repository

    async def __call__(self, task_id: UUID) -> TaskStatus:
        task = await self._task_repository.get_by_id(task_id)
        return task.status
