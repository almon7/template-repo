#!/bin/bash
# run-tests.sh
# This script runs the test suite for the codebase and checks coverage.
#
# Usage:
#   bash src/scripts/run-tests.sh [TEST_DIR] [APP_DIR]
#
# Arguments:
#   TEST_DIR   Directory containing test files (default: /app/src/tests)
#   APP_DIR    Directory containing application code for coverage (default: /app/src/app)
#
# Example:
#   bash src/scripts/run-tests.sh src/tests src/app

# Use argument if provided, otherwise default to Docker path
TEST_DIR="${1:-/app/src/tests}"
APP_DIR="${2:-/app/src/app}"

echo "Running tests..."
uv run pytest --cov="${APP_DIR}" "${TEST_DIR}"
