FROM python:3.11-slim-bullseye as base

ARG HOMEDIR=/home/user
ARG WORKDIR=/usr/src/app
ARG VIRTUAL_ENV=/usr/src/env
ARG USERNAME=app
ARG UID=1313
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN useradd -m -d "$HOMEDIR" -N -G users -u "$UID" "$USERNAME"
RUN mkdir "$WORKDIR" && chown "$USERNAME:users" "$WORKDIR"
WORKDIR $WORKDIR

FROM base as venv

ENV PIP_CACHE_DIR=/var/cache/pip
ENV POETRY_CACHE_DIR=/var/cache/poetry
ENV POETRY_VIRTUALENVS_CREATE=0

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends

RUN --mount=type=cache,id=pip,target=$PIP_CACHE_DIR,sharing=locked \
    pip install poetry==1.5.1

RUN python -m venv /usr/src/env

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./pyproject.toml ./poetry.lock ./
RUN --mount=type=cache,id=poetry,target=$POETRY_CACHE_DIR,sharing=locked \
    poetry install --no-root

FROM base as final

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=venv $VIRTUAL_ENV $VIRTUAL_ENV

COPY . ./
RUN pip install --no-deps  -e .

USER app

ENTRYPOINT ["docker/start.sh"]