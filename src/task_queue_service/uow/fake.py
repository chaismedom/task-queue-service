from task_queue_service.repositories.fake import FakeTaskRepository
from task_queue_service.uow.interface import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def __init__(
        self,
        fake_task_repository: FakeTaskRepository,
    ) -> None:
        self._fake_task_repository = fake_task_repository
        self.is_committed = False

    async def commit(self) -> None:
        self.is_committed = True

    async def rollback(self) -> None:
        """noop"""
