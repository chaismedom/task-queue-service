from uuid import UUID

from task_queue_service.services.task_timer import AbstractTaskTimerService
from task_queue_service.task import Task
from task_queue_service.uow import AbstractUnitOfWork
from task_queue_service.use_cases.interface import AbstractAddTaskUseCase


class AddTaskUseCaseImpl(AbstractAddTaskUseCase):
    def __init__(
        self,
        task_timer: AbstractTaskTimerService,
        uow: AbstractUnitOfWork,
    ) -> None:
        self._task_timer = task_timer
        self._uow = uow

    async def __call__(self, task_title: str) -> UUID:
        task = Task(
            title=task_title,
            waiting_time=self._task_timer(),
        )
        async with self._uow:
            await self._uow.task_repository.add(task)
            await self._uow.commit()

        return task.id_
