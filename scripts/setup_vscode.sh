#!/bin/bash
# VSCode Setup Helper Script

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== VSCode Setup Check ===${NC}"

# Check if code command is available
CODE_CMD=""
if command -v code &> /dev/null; then
    CODE_CMD="code"
elif command -v code.exe &> /dev/null; then
    CODE_CMD="code.exe"
fi

if [ -n "$CODE_CMD" ]; then
    echo -e "${GREEN}✓ VSCode command found: ${CODE_CMD}${NC}"
    echo ""
    echo "To open this project in VSCode, run:"
    echo -e "  ${BLUE}${CODE_CMD} .${NC}"
    echo ""
    echo "VSCode will open in the current directory with WSL integration."
else
    echo -e "${YELLOW}⚠ VSCode command not found${NC}"
    echo ""
    echo "To use VSCode with WSL, you need to:"
    echo ""
    echo "1. Install VSCode on Windows:"
    echo "   Download from: https://code.visualstudio.com/"
    echo ""
    echo "2. Install the 'Remote - WSL' extension:"
    echo "   - Open VSCode"
    echo "   - Go to Extensions (Ctrl+Shift+X)"
    echo "   - Search for 'Remote - WSL'"
    echo "   - Install the extension from Microsoft"
    echo ""
    echo "3. After installation, open this project from WSL:"
    echo "   - In your WSL terminal, navigate to this directory"
    echo "   - Run: ${BLUE}code .${NC}"
    echo ""
    echo "VSCode will automatically connect to WSL and open the project."
    echo ""
fi

echo -e "${YELLOW}=== Using Windows Commands from WSL ===${NC}"
echo ""
echo "You can use Windows applications from WSL terminal:"
echo ""
echo "Open File Explorer in current directory:"
echo -e "  ${BLUE}explorer.exe .${NC}"
echo ""
echo "Open VSCode in current directory:"
echo -e "  ${BLUE}code .${NC} or ${BLUE}code.exe .${NC}"
echo ""
echo "Note: Always use '.exe' extension for Windows executables"
echo ""

echo -e "${BLUE}=== VSCode Setup Check Complete ===${NC}"
