#!/bin/bash
# format.sh
# This script runs code formatting tools on the codebase.

APP_DIR="/app/src/app"

echo "Running ruff format..."
uv run ruff format "${APP_DIR}"

echo "Running ruff lint --fix..."
uv run ruff check --fix "${APP_DIR}"