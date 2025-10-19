HIGHLIGHT='\033[0;33m'
TEXT_RED='\e[31m'
TEXT_GREEN='\e[32m'
NC='\033[0m' # No Color

# Use argument if provided, otherwise default to Docker path
APP_DIR="${1:-/app/src/app}"

echo -e "${HIGHLIGHT}Running ruff format check:${NC}"
uv run ruff format --check "${APP_DIR}"
if [ $? -ne 0 ]; then
    echo -e "${TEXT_RED}Ruff needs to be run before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Ruff format check passed.${NC}"
fi;


echo -e "${HIGHLIGHT}Running ruff lint check:${NC}"
uv run ruff check "${APP_DIR}"
if [ $? -ne 0 ]; then
    echo -e "${TEXT_RED}Ruff lint errors must be resolved before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Ruff lint check passed.${NC}"
fi;


echo -e "${HIGHLIGHT}Running mypy...${NC}"
uv run mypy --check "${APP_DIR}"
if [ $? -ne 0 ]; then
    echo -e "${TEXT_RED}Mypy errors must be resolved before committing.${NC}"
    exit 1
else
    echo -e "${TEXT_GREEN}Mypy passed.${NC}"
fi