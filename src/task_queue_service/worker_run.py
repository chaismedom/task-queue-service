import asyncio

from task_queue_service.container import bootstrap

# XXX: There're better ways to implement workers using external services
# like celery with schedulers
# (and for sure that will be the case if the service will be in prod)
# But I just want to keep it simple and do not
# add additional dependencies to the project


async def main() -> None:
    container = bootstrap()
    container.init_resources()
    worker_loop = container.worker_loop()
    print("worker started.")
    try:
        await worker_loop.run()
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        pass
    finally:
        print("worker closed.")
        container.shutdown_resources()


if __name__ == "__main__":
    asyncio.run(main())
