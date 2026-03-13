# App Template

[![Python](https://img.shields.io/badge/python-v3.13-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-compose-2496ED?logo=docker)](https://www.docker.com/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

A template app for the development of dockerised Python-based projects.
It is set up with Docker Compose and includes pre-commit hooks, tests, coverage calculation, pipeline checks, a Makefile, static checking and formatting.


### Key features

- **FastAPI** with security headers, [TrustedHost](https://www.starlette.io/middleware/#trustedhost-middleware) validation, and optional CORS (set `CORS_ORIGINS`)
- **Request correlation IDs** — every request receives an `X-Request-ID` header (generated or propagated); the ID is bound to all log records for that request
- **Structured JSON logging** in production (`ENVIRONMENT=production`) for log aggregation tools; human-readable coloured logs in development
- **Strict production guards** — wildcard `ALLOWED_HOSTS` and debug log levels are rejected at startup when `ENVIRONMENT=production`
- **uv** for fast, reproducible dependency management and packaging
- **mypy** (strict mode), **ruff** (format + lint), and **bandit** static analysis

## Starting a New Project from This Template

### 1. Change the App Name

Replace every occurrence of `template-app` with your project name:
- `pyproject.toml` → `name` field under `[project]`
- `src/app/settings.py` → `app_name` default value in the `Settings` class

### 2. Reset Git History

1. Remove the existing git history:

```bash
rm -rf .git
```

2. Initialize a new git repository:

```bash
git init
```

3. Make your initial commit:

```bash
git add .
git commit -m "Initial commit from template"
```

This ensures your new project starts with a clean commit history, independent from the template.

### 3. [Optional] Enable Pre-commit hooks

Some pre-commits hooks that run code checks with 'ruff' and 'mypy' are provided.
To set them up with git, copy the pre-commit file containing the hooks to the .git folder:

```bash
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

To skip the pre-commit checks, use the `--no-verify` flag when committing:

```bash
git commit --no-verify
```

### 4. Set your Environment Variables

Copy `sample.env` to a `.env` environment variables file:

```bash
cp sample.env .env
```

Add your own environment variables to `.env`

### 5. Build the Docker Container

Build and start the app:

```bash
make build
```

Or without the Makefile: `docker compose up --build`


## Developing the App

### Makefile

A `Makefile` is provided with shortcuts for common tasks. Run `make help` to see all available targets:

| Target             | Description                                        |
| ------------------ | -------------------------------------------------- |
| `make build`       | Build images and start containers                  |
| `make up`          | Start containers (no rebuild)                      |
| `make upd`         | Start containers in detached mode                  |
| `make down`        | Stop and remove containers                         |
| `make restart`     | Restart containers (no rebuild)                    |
| `make logs`        | Tail container logs                                |
| `make shell`       | Open a bash shell inside the running app container |
| `make format`      | Auto-format code with ruff                         |
| `make code-checks` | Run all static checks (ruff, mypy, bandit)         |
| `make run-tests`   | Run the test suite with coverage                   |
