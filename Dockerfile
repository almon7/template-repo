FROM python:3.13-slim-bookworm

# Avoid writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure that the Python output is sent straight to terminal (e.g., for logging)
ENV PYTHONUNBUFFERED=1

# Copy uv files from the cache instead of linking so as not to cause issues with bind mounts
ENV UV_LINK_MODE=copy

# Compile Python files to bytecode when installing dependencies. Improves startup time at the cost of installation time.
ENV UV_COMPILE_BYTECODE=1

# Install uv binaries from the official image
COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /bin/

# Update system dependencies
RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and switch to it
ARG UID
ARG GID
RUN groupadd -g ${GID} nonroot && \
    useradd -u ${UID} -g nonroot -m nonroot
USER nonroot

# Set working directory
WORKDIR /app/src

# Install dependencies but not the project itself to leverage Docker layer caching.
# --locked ensures that uv.lock is up to date with pyproject.toml;
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy pyproject.toml and uv.lock to the container
COPY --chown=nonroot:nonroot pyproject.toml uv.lock /app/

# Copy the application source code
COPY --chown=nonroot:nonroot src/ /app/src/

# Install the project, caching uv files
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# OPTIONAL: Activate the uv virtual environment by placing its directory at the front of the PATH
# This makes it so that you don't have to prefix commands with `uv run ...`
# ENV PATH="/app/.venv/bin:$PATH"

# OPTIONAL: Add /app/src to PYTHONPATH
# This allows running code from /app/src without the -m flag
# ENV PYTHONPATH=""
# ENV PYTHONPATH="/app/src:${PYTHONPATH}"


# Run the application with auto-reload for development
# CMD [ "/usr/bin/bash", "/app/src/scripts/entrypoint.sh" ]
