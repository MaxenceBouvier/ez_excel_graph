#!/bin/bash
# Development Environment Setup Script

set -e  # Exit on error

# Detect color support
if [ -t 1 ] && command -v tput &> /dev/null && [ $(tput colors) -ge 8 ]; then
    # Terminal supports colors
    GREEN=$(tput setaf 2)
    YELLOW=$(tput setaf 3)
    RED=$(tput setaf 1)
    BLUE=$(tput setaf 4)
    BOLD=$(tput bold)
    NC=$(tput sgr0)
else
    # No color support, use plain text
    GREEN=''
    YELLOW=''
    RED=''
    BLUE=''
    BOLD=''
    NC=''
fi

echo -e "${BLUE}=== Development Environment Setup ===${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}ERROR: Virtual environment not found${NC}"
    echo "Please run ./scripts/setup_python.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install development dependencies
echo ""
echo "Installing development dependencies..."
if command -v uv &> /dev/null; then
    uv pip install -e ".[dev]"
else
    pip install -e ".[dev]"
fi
echo -e "${GREEN}✓ Development dependencies installed${NC}"

# Install pre-commit hooks
echo ""
echo "Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"

    # Run pre-commit on all files to verify setup
    echo ""
    echo "Running pre-commit on all files to verify setup..."
    if pre-commit run --all-files; then
        echo -e "${GREEN}✓ All pre-commit checks passed${NC}"
    else
        echo -e "${YELLOW}⚠ Some files were modified by pre-commit hooks${NC}"
        echo "  This is normal on first run. Files have been auto-formatted."
    fi
else
    echo -e "${RED}ERROR: pre-commit not found${NC}"
    echo "Please ensure development dependencies were installed correctly"
    exit 1
fi

echo ""
echo -e "${GREEN}=== Development Environment Ready! ===${NC}"
echo ""
echo "Pre-commit hooks installed. They will run automatically on git commit."
echo ""
echo "Useful commands:"
echo "  ${BLUE}pre-commit run --all-files${NC}  - Run all hooks manually"
echo "  ${BLUE}black src/${NC}                   - Format code with Black"
echo "  ${BLUE}ruff check src/${NC}               - Lint code with Ruff"
echo "  ${BLUE}mypy src/${NC}                     - Type check with mypy"
echo "  ${BLUE}pytest${NC}                        - Run tests (when added)"
echo ""
