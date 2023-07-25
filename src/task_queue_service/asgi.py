from fastapi import FastAPI

from task_queue_service.container import bootstrap


def build_app() -> FastAPI:
    container = bootstrap()
    return container.fastapi_app()
