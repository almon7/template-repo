#!/bin/bash
# -e: abort immediately if any command exits non-zero
# -u: treat unset variables as errors instead of silently expanding to empty string
# -o pipefail: a pipeline fails if any command in it fails (not just the last one)
set -euo pipefail
HIGHLIGHT='\033[0;33m'
TEXT_RED='\033[0;31m'
TEXT_GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Use argument if provided, otherwise default to Docker path
APP_DIR="${1:-/app/app}"

echo -e "${HIGHLIGHT}Running ruff format check:${NC}"
if ! uv run ruff format --check "${APP_DIR}"; then
    echo -e "${TEXT_RED}Ruff needs to be run before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Ruff format check passed.${NC}"
fi


echo -e "${HIGHLIGHT}Running ruff lint check:${NC}"
if ! uv run ruff check "${APP_DIR}"; then
    echo -e "${TEXT_RED}Ruff lint errors must be resolved before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Ruff lint check passed.${NC}"
fi


echo -e "${HIGHLIGHT}Running mypy...${NC}"
if ! uv run mypy "${APP_DIR}"; then
    echo -e "${TEXT_RED}Mypy errors must be resolved before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Mypy passed.${NC}"
fi


echo -e "${HIGHLIGHT}Running bandit...${NC}"
if ! uv run bandit -r "${APP_DIR}"; then
    echo -e "${TEXT_RED}Bandit security issues must be resolved before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Bandit passed.${NC}"
fi