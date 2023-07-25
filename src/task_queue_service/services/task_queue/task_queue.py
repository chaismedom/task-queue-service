from task_queue_service.services.task_queue import AbstractTaskQueueService
from task_queue_service.uow import AbstractUnitOfWork


class TaskQueueService(AbstractTaskQueueService):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def poll(self) -> None:
        async with self._uow:
            tasks = await self._uow.task_repository.list_expired()
            for task in tasks:
                task.mark_done()
                await self._uow.task_repository.persist(task)

            await self._uow.commit()
