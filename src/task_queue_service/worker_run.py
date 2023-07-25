import asyncio

from task_queue_service.container import bootstrap


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
