#!/bin/bash
# Project-specific Setup Script

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Project Setup ===${NC}"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}ERROR: Virtual environment not found${NC}"
    echo "Please run setup_python.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install project in editable mode
echo ""
echo "Installing project package in editable mode..."
if command -v uv &> /dev/null; then
    uv pip install -e "."
    echo -e "${GREEN}✓ Project installed successfully${NC}"
else
    echo -e "${YELLOW}⚠ uv not found, using pip...${NC}"
    pip install -e "."
    echo -e "${GREEN}✓ Project installed successfully${NC}"
fi

# Create outputs directory if it doesn't exist
mkdir -p outputs
echo -e "${GREEN}✓ Outputs directory ready${NC}"

# Create working branch for development
echo ""
echo -e "${BLUE}Let's create a working branch for you!${NC}"
echo "The branch will be named: ${YELLOW}user/<branch_name>${NC}"
echo ""
read -p "Enter your branch name (e.g., 'my-graphs', 'jan-2024-study'): " BRANCH_NAME

# Validate branch name is not empty
while [ -z "$BRANCH_NAME" ]; do
    echo -e "${RED}Branch name cannot be empty!${NC}"
    read -p "Enter your branch name: " BRANCH_NAME
done

# Create full branch name with user/ prefix
FULL_BRANCH_NAME="user/$BRANCH_NAME"

# Check if branch already exists
if git rev-parse --verify "$FULL_BRANCH_NAME" &>/dev/null; then
    echo -e "${YELLOW}⚠ Branch '$FULL_BRANCH_NAME' already exists${NC}"
    echo "Current branch: $(git branch --show-current)"
    read -p "Do you want to switch to it? (y/n): " SWITCH_BRANCH
    if [[ "$SWITCH_BRANCH" == "y" || "$SWITCH_BRANCH" == "Y" ]]; then
        git checkout "$FULL_BRANCH_NAME"
        echo -e "${GREEN}✓ Switched to branch '$FULL_BRANCH_NAME'${NC}"
    fi
else
    echo ""
    echo "Creating working branch '$FULL_BRANCH_NAME'..."
    git checkout -b "$FULL_BRANCH_NAME"
    echo -e "${GREEN}✓ Switched to branch '$FULL_BRANCH_NAME'${NC}"
fi

echo ""
echo -e "${GREEN}=== Project setup complete! ===${NC}"
echo ""
echo "You can now:"
echo "1. Place your Excel files in the ${BLUE}resources/${NC} directory"
echo "2. Use ${BLUE}claude${NC} to generate graphs with natural language"
echo "3. Find generated graphs in the ${BLUE}outputs/${NC} directory"
echo ""
echo "Example prompts to try:"
echo "  'Generate a timeline chart showing when each person spoke'"
echo "  'Create a bar chart comparing speaking time per person'"
echo "  'Show all ideas mentioned by Person 1 across all time periods'"
echo ""

echo -e "${BLUE}=== Project Setup Complete ===${NC}"
