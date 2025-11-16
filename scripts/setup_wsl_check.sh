#!/bin/bash
# WSL Environment Check Script

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

echo -e "${BLUE}=== WSL Environment Check ===${NC}"

# Check if running in WSL
if ! grep -qi microsoft /proc/version; then
    echo -e "${RED}ERROR: This script must be run in WSL (Windows Subsystem for Linux)${NC}"
    echo "Please install WSL first using the instructions in README.md"
    exit 1
fi

echo -e "${GREEN}✓ Running in WSL${NC}"

# Check WSL version
if grep -qi "WSL2" /proc/version || grep -qi "microsoft-standard" /proc/version; then
    echo -e "${GREEN}✓ WSL2 detected${NC}"
else
    echo -e "${YELLOW}⚠ WSL1 detected. WSL2 is recommended for better performance.${NC}"
fi

# Check Linux distribution
if [ -f /etc/os-release ]; then
    DISTRO=$(. /etc/os-release && echo "$NAME")
    echo -e "${GREEN}✓ Distribution: ${DISTRO}${NC}"
fi

# Check if Windows interoperability is enabled
if grep -qi "appendWindowsPath.*false" /etc/wsl.conf 2>/dev/null; then
    echo -e "${YELLOW}⚠ Windows PATH is disabled in /etc/wsl.conf${NC}"
    echo "  Windows commands like 'explorer.exe' and 'code.exe' may not work"
    echo "  To enable, edit /etc/wsl.conf and set appendWindowsPath=true"
else
    echo -e "${GREEN}✓ Windows interoperability enabled${NC}"
fi

# Test if Windows commands work
if command -v explorer.exe &> /dev/null; then
    echo -e "${GREEN}✓ Windows commands accessible (explorer.exe found)${NC}"
else
    echo -e "${YELLOW}⚠ Windows commands not found in PATH${NC}"
    echo "  You may need to add them manually or check /etc/wsl.conf"
fi

# Check if code command is available (VSCode)
if command -v code &> /dev/null || command -v code.exe &> /dev/null; then
    echo -e "${GREEN}✓ VSCode command found${NC}"
else
    echo -e "${YELLOW}⚠ VSCode command not found${NC}"
    echo "  Install VSCode and the Remote-WSL extension for the best experience"
fi

echo -e "${BLUE}=== WSL Check Complete ===${NC}"
