#!/bin/bash

set -euf -o pipefail

exec uvicorn --factory --no-access-log task_queue_service.asgi:build_app --host 0.0.0.0 --port 8010 --reload
