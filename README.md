# App Template
[![Python](https://img.shields.io/badge/python-v3.13-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview
A template app for the development of dockerised python-based projects.
It is set up with docker-compose and includes pre-commit hooks, tests, coverage calculation, pipeline checks, a Makefile, static checking and formatting.

## Running the App

1. Copy `sample.env` to a `.env` environment variables file:
    ```bash
    cp sample.env .env
    ```
    Add your own environment variables.

2. Build and start the app:
    ```bash
    make build
    ```
    Or without the Makefile: `docker compose up --build`

## Developing the App

#### Makefile
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

#### Pre-commit hooks
Some pre-commits hooks that run code checks with 'ruff' and 'mypy' are provided.
To set them up with git, copy the pre-commit file containing the hooks to the .git folder:
```bash
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```
To skip the pre-commit checks, use the `--no-verify` flag when committing:
```
git commit --no-verify
```

## Starting a New Project from This Template

To start a new project without carrying over this repository's commit history:

1. Download or clone this template repository.
2. Remove the existing git history:
    ```bash
    rm -rf .git
    ```
3. Initialize a new git repository:
    ```bash
    git init
    ```
4. Rename the app — replace every occurrence of `template-app` with your project name:
    - `pyproject.toml` → `name` field under `[project]`
    - `src/app/settings.py` → `app_name` default value in the `Settings` class
5. Make your initial commit:
    ```bash
    git add .
    git commit -m "Initial commit from template"
    ```

This ensures your new project starts with a clean commit history, independent from the template.
