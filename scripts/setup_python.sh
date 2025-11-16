#!/bin/bash
# Python Environment Setup Script using uv

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

echo -e "${BLUE}=== Python Environment Setup ===${NC}"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo "Install Python with: sudo apt update && sudo apt install -y python3 python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Python installed: ${PYTHON_VERSION}${NC}"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    echo ""

    # Install uv using the official installation script
    if curl -LsSf https://astral.sh/uv/install.sh | sh; then
        echo -e "${GREEN}✓ uv installed successfully${NC}"

        # Source the shell configuration to make uv available
        if [ -f "$HOME/.cargo/env" ]; then
            source "$HOME/.cargo/env"
        fi

        # Check if uv is now available
        if ! command -v uv &> /dev/null; then
            echo -e "${YELLOW}⚠ uv installed but not in PATH yet${NC}"
            echo "Please run: source ~/.cargo/env"
            echo "Or restart your terminal"
        fi
    else
        echo -e "${RED}ERROR: Failed to install uv${NC}"
        echo "Please try manually:"
        echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
else
    echo -e "${GREEN}✓ uv is already installed${NC}"
    uv --version
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating Python virtual environment..."
    uv venv .venv
    echo -e "${GREEN}✓ Virtual environment created at .venv/${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment and install dependencies
echo ""
echo "Installing project dependencies..."
echo ""

# Install dependencies using uv
if command -v uv &> /dev/null; then
    source .venv/bin/activate
    uv pip install -e "."
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ uv not available in PATH, skipping dependency installation${NC}"
    echo "After reloading your shell, run:"
    echo "  source .venv/bin/activate"
    echo "  uv pip install -e ."
fi

echo ""
echo -e "${YELLOW}=== To activate the virtual environment, run: ===${NC}"
echo -e "${BLUE}source .venv/bin/activate${NC}"
echo ""

echo -e "${BLUE}=== Python Setup Complete ===${NC}"
