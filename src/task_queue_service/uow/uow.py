from typing import Any, Self

from sqlalchemy.ext.asyncio import AsyncSession

from task_queue_service.repositories.task_repository import TaskRepository
from task_queue_service.uow.interface import AbstractUnitOfWork
from task_queue_service.utils import AsyncSessionFactory


class UnitOfWork(AbstractUnitOfWork):
    task_repository: TaskRepository

    def __init__(self, session_factory: AsyncSessionFactory) -> None:
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.is_committed = False

    def init_repositories(self, session: AsyncSession) -> None:
        self.task_repository = TaskRepository(session)

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        self.init_repositories(self.session)

        return await super().__aenter__()

    async def __aexit__(self, *exc_info: Any) -> None:
        await super().__aexit__(*exc_info)

        assert self.session is not None
        await self.session.close()

        self.session = None
        self.is_committed = False

    async def commit(self) -> None:
        assert self.session is not None
        await self.session.commit()
        self._committed = True

    async def rollback(self) -> None:
        assert self.session is not None
        await self.session.rollback()
