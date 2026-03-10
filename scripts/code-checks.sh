#!/bin/bash
# -e: abort immediately if any command exits non-zero
# -u: treat unset variables as errors instead of silently expanding to empty string
# -o pipefail: a pipeline fails if any command in it fails (not just the last one)
set -euo pipefail
HIGHLIGHT='\033[0;33m'
TEXT_RED='\033[0;31m'
TEXT_GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Resolve the project root (one level up from this script) so tools that
# accept a config-file path always receive an absolute path, regardless of
# the working directory at invocation time (e.g. inside Docker).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "${SCRIPT_DIR}")"

# Use arguments if provided, otherwise default to Docker paths
APP_DIR="${1:-/app/app}"
TEST_DIR="${2:-/app/tests}"

echo -e "${HIGHLIGHT}Running ruff format check on ${APP_DIR} and ${TEST_DIR}:${NC}"
if ! uv run ruff format --check "${APP_DIR}" "${TEST_DIR}"; then
    echo -e "${TEXT_RED}Ruff needs to be run before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Ruff format check passed.${NC}"
fi


echo -e "${HIGHLIGHT}Running ruff lint check on ${APP_DIR} and ${TEST_DIR}:${NC}"
if ! uv run ruff check "${APP_DIR}" "${TEST_DIR}"; then
    echo -e "${TEXT_RED}Ruff lint errors must be resolved before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Ruff lint check passed.${NC}"
fi


echo -e "${HIGHLIGHT}Running mypy on ${APP_DIR} and ${TEST_DIR}...${NC}"
if ! uv run mypy "${APP_DIR}" "${TEST_DIR}"; then
    echo -e "${TEXT_RED}Mypy errors must be resolved before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Mypy passed.${NC}"
fi


echo -e "${HIGHLIGHT}Running bandit on ${APP_DIR}...${NC}"
# -c: absolute path so bandit can find the config regardless of working directory.
if ! uv run bandit -c "${PROJECT_ROOT}/pyproject.toml" -r "${APP_DIR}"; then
    echo -e "${TEXT_RED}Bandit security issues must be resolved before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Bandit passed.${NC}"
fi

echo -e "${TEXT_GREEN}All checks passed.${NC}"