#!/bin/bash
# Claude Code CLI Setup Script

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

echo -e "${YELLOW}=== First-Time Authentication ===${NC}"
echo "To use Claude Code, you need to authenticate:"
echo ""
echo "1. Run: ${BLUE}claude${NC}"
echo "2. When prompted, use the command: ${BLUE}/login${NC}"
echo "3. Follow the authentication instructions"
echo "4. You can authenticate with either:"
echo "   - Claude.ai account (recommended)"
echo "   - Claude Console account with API access"
echo ""
echo "After authentication, you can use Claude Code by running:"
echo "  ${BLUE}claude${NC}  (interactive mode)"
echo "  ${BLUE}claude -c${NC}  (continue last conversation)"
echo ""

echo -e "${BLUE}=== Claude Code Setup Complete ===${NC}"
