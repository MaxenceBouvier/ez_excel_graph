#!/bin/bash
# Claude Code CLI Setup Script

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

echo -e "${BLUE}=== Claude Code CLI Setup ===${NC}"

# Check if Claude Code is already installed
if command -v claude &> /dev/null; then
    echo -e "${GREEN}✓ Claude Code CLI is already installed${NC}"
    claude --version 2>/dev/null || echo "  Version info not available"
    echo ""
    echo "To authenticate or re-authenticate, run: claude"
    echo "Then use the command: /login"
else
    echo "Installing Claude Code CLI..."
    echo ""
    echo "Running: curl -fsSL https://claude.ai/install.sh | bash"
    echo ""

    # Download and run the installation script
    if curl -fsSL https://claude.ai/install.sh | bash; then
        echo -e "${GREEN}✓ Claude Code CLI installed successfully${NC}"
        echo ""
        echo "You may need to restart your terminal or run:"
        echo "  source ~/.bashrc"
        echo ""
    else
        echo -e "${RED}ERROR: Failed to install Claude Code CLI${NC}"
        echo "Please try manually:"
        echo "  curl -fsSL https://claude.ai/install.sh | bash"
        exit 1
    fi
fi

# Configure Claude Code permissions
echo ""
echo -e "${BLUE}=== Configuring Claude Code Permissions ===${NC}"

# Get the project root (parent of scripts directory)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Create .claude directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/.claude"

# Copy and configure settings if example exists
if [ -f "$PROJECT_ROOT/.claude.settings.example.json" ]; then
    # Get current username
    CURRENT_USER=$(whoami)

    # Copy and replace YOUR_USERNAME with actual username
    sed "s|YOUR_USERNAME|$CURRENT_USER|g" "$PROJECT_ROOT/.claude.settings.example.json" > "$PROJECT_ROOT/.claude/settings.local.json"

    echo -e "${GREEN}✓ Claude Code permissions configured${NC}"
    echo "  Settings file: .claude/settings.local.json"
    echo "  This allows Claude to run common commands without asking for approval"
else
    echo -e "${YELLOW}⚠ Settings example file not found${NC}"
    echo "  Skipping automatic permissions setup"
fi

echo ""
echo -e "${YELLOW}=== First-Time Authentication ===${NC}"
echo "To use Claude Code, you need to authenticate:"
echo ""
echo "1. Run: ${BLUE}claude${NC}"
echo "2. Claude will prompt you to log in automatically on first startup"
echo "3. ${YELLOW}IMPORTANT:${NC} Use your ${BLUE}Claude.ai account${NC} (free web version)"
echo "   ${RED}Do NOT use 'Claude Console with API' - that's a paid option!${NC}"
echo ""
echo "If Claude doesn't prompt automatically, you can use: ${BLUE}/login${NC}"
echo ""
echo "After authentication, you can use Claude Code by running:"
echo "  ${BLUE}claude${NC}  (interactive mode)"
echo "  ${BLUE}claude -c${NC}  (continue last conversation)"
echo ""

echo -e "${BLUE}=== Claude Code Setup Complete ===${NC}"
