from uuid import UUID

from task_queue_service.task import TaskStatus
from task_queue_service.uow import AbstractUnitOfWork
from task_queue_service.use_cases.interface import AbstractGetTaskStatusUseCase


class GetTaskStatusUseCaseImpl(AbstractGetTaskStatusUseCase):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ) -> None:
        self._uow = uow

    async def __call__(self, task_id: UUID) -> TaskStatus:
        async with self._uow:
            task = await self._uow.task_repository.get_by_id(task_id)

        return task.status
