# ─── base stage ──────────────────────────────────────────────────────────────
# Shared environment: Python, uv, system deps, non-root user, dependency install.
FROM python:3.13-slim-bookworm AS base

# Ensure that the Python output is sent straight to terminal (e.g., for logging)
ENV PYTHONUNBUFFERED=1

# Copy uv files from the cache instead of linking so as not to cause issues with bind mounts
ENV UV_LINK_MODE=copy

# Compile Python files to bytecode when installing dependencies. Improves startup time at the cost of installation time.
ENV UV_COMPILE_BYTECODE=1

# Install uv binaries from the official image
COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /uvx /bin/

# Create a non-root user and switch to it.
# ARG defaults match sample.env so plain `docker build .` works without --build-arg.
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} nonroot && \
    useradd -u ${UID} -g nonroot -m nonroot
USER nonroot

# Set working directory
WORKDIR /app

# Copy dependency files
COPY --chown=nonroot:nonroot pyproject.toml uv.lock /app/


# ─── dev stage ────────────────────────────────────────────────────────────────
# Contains application code, tests, and scripts.
# Used for local development and running pre-commit hooks.
FROM base AS dev

# ARG must be redeclared in each stage that uses it (Docker ARGs are stage-scoped).
ARG UID=1000
ARG GID=1000

# Install all dependencies including the dev group
RUN --mount=type=cache,target=/home/nonroot/.cache/uv,uid=${UID},gid=${GID} \
    uv sync --locked --no-install-project

COPY --chown=nonroot:nonroot src/app     /app/app/
COPY --chown=nonroot:nonroot tests/   /app/tests/
COPY --chown=nonroot:nonroot scripts/ /app/scripts/

# Ensure all scripts are executable
RUN chmod +x /app/scripts/*.sh

# Install the project
RUN --mount=type=cache,target=/home/nonroot/.cache/uv,uid=${UID},gid=${GID} \
    uv sync --locked

# Activate the uv virtual environment
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

ENTRYPOINT ["/app/scripts/dev-entrypoint.sh"]


# ─── production stage ─────────────────────────────────────────────────────────
# Lean image with no tests and no dev tooling. Used for deployment.
FROM base AS production

# ARG must be redeclared in each stage that uses it (Docker ARGs are stage-scoped).
ARG UID=1000
ARG GID=1000

# Install production dependencies only (no dev group)
RUN --mount=type=cache,target=/home/nonroot/.cache/uv,uid=${UID},gid=${GID} \
    uv sync --locked --no-install-project --no-dev

COPY --chown=nonroot:nonroot src/app /app/app/
COPY --chown=nonroot:nonroot scripts/prod-entrypoint.sh /usr/local/bin/entrypoint.sh

# Install the project (no dev group)
RUN --mount=type=cache,target=/home/nonroot/.cache/uv,uid=${UID},gid=${GID} \
    uv sync --locked --no-dev

# Activate the uv virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Ensure the entrypoint is executable
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR /app

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
