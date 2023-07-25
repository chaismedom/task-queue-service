from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dependency_injector.containers import Container
from fastapi import FastAPI, Request, Response
from starlette.types import Lifespan

from task_queue_service.handlers import router as task_router
from task_queue_service.repositories.interface import TaskNotFoundError


async def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> Response:
    return Response(status_code=404)


def lifespan(
    container: Container,
) -> Lifespan:  # type: ignore[type-arg]
    @asynccontextmanager
    async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
        result = container.init_resources()
        if result:
            await result
        try:
            yield
        finally:
            result = container.shutdown_resources()
            if result:
                await result

    return _lifespan


def fastapi_app(container: Container) -> FastAPI:
    app = FastAPI(
        title="Task queue service",
        lifespan=lifespan(container),
    )
    app.include_router(task_router)
    app.exception_handler(TaskNotFoundError)(task_not_found_handler)

    return app
