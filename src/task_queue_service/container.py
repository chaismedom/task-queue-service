from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import (
    Callable,
    Configuration,
    Factory,
    Provider,
    Self,
    Singleton,
)
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from task_queue_service.app import fastapi_app
from task_queue_service.services.task_queue import (
    AbstractTaskQueueService,
    TaskQueueService,
)
from task_queue_service.services.task_timer import (
    AbstractTaskTimerService,
    RandomTaskTimerService,
)
from task_queue_service.settings import Settings
from task_queue_service.uow import AbstractUnitOfWork, UnitOfWork
from task_queue_service.use_cases import (
    AbstractAddTaskUseCase,
    AbstractGetTaskStatusUseCase,
    AbstractPollTasksUseCase,
    AddTaskUseCaseImpl,
    GetTaskStatusUseCaseImpl,
    PollTasksUseCaseImpl,
)
from task_queue_service.utils import AsyncSessionFactory, pg_dsn_factory
from task_queue_service.worker import AbstractPollWorkerLoop, PollWorkerLoop


class MainContainer(DeclarativeContainer):
    __self__ = Self()
    settings: Configuration = Configuration()
    wiring_config = WiringConfiguration(
        modules=[".handlers"],
    )

    # db
    pg_dsn: Factory[str] = Factory(
        pg_dsn_factory,
        user=settings.postgres_user,
        password=settings.postgres_password,
        host=settings.postgres_host,
        port=settings.postgres_port,
        db=settings.postgres_db,
    )
    sa_engine: Singleton[AsyncEngine] = Singleton(create_async_engine, pg_dsn)
    sa_session_factory: Singleton[AsyncSessionFactory] = Singleton(
        async_sessionmaker,
        bind=sa_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    uow: Provider[AbstractUnitOfWork] = Factory(
        UnitOfWork,
        session_factory=sa_session_factory,
    )

    # services
    task_timer: Provider[AbstractTaskTimerService] = Factory(
        RandomTaskTimerService,
        low_time_limit=settings.add_time_low_limit,
        high_time_limit=settings.add_time_high_limit,
    )
    task_queue: Provider[AbstractTaskQueueService] = Factory(
        TaskQueueService,
        uow=uow,
    )

    # use cases
    add_task_use_case: Provider[AbstractAddTaskUseCase] = Factory(
        AddTaskUseCaseImpl,
        task_timer=task_timer,
        uow=uow,
    )
    get_task_status_use_case: Provider[AbstractGetTaskStatusUseCase] = Factory(
        GetTaskStatusUseCaseImpl,
        uow=uow,
    )
    poll_tasks_use_case: Provider[AbstractPollTasksUseCase] = Factory(
        PollTasksUseCaseImpl,
        task_queue=task_queue,
    )

    worker_loop: Provider[AbstractPollWorkerLoop] = Factory(
        PollWorkerLoop,
        poll_timeout=settings.poll_timeout,
        use_case=poll_tasks_use_case,
    )
    fastapi_app: Provider[FastAPI] = Callable(
        fastapi_app,
        container=__self__,
    )


def bootstrap(init_resources: bool = False) -> MainContainer:
    container = MainContainer()
    settings = Settings()

    container.settings.from_dict(settings.model_dump())

    if init_resources:
        container.init_resources()

    return container
