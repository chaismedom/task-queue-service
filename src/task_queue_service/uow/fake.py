from task_queue_service.repositories.fake import FakeTaskRepository
from task_queue_service.uow.interface import AbstractUnitOfWork


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        task_repository: FakeTaskRepository,
    ) -> None:
        self.task_repository = task_repository
        self.is_committed = False

    async def commit(self) -> None:
        self.is_committed = True

    async def rollback(self) -> None:
        """noop"""
