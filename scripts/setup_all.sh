#!/bin/bash
# Main Setup Script - Orchestrates all setup steps

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

echo -e "${BOLD}${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║        Excel to Graph - Complete Setup Script         ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Change to project root
cd "$PROJECT_ROOT"

echo -e "${YELLOW}This script will set up your entire development environment.${NC}"
echo ""
echo "The following steps will be performed:"
echo "  1. Check WSL environment"
echo "  2. Initialize Git repository and install hooks"
echo "  3. Install Claude Code CLI"
echo "  4. Set up Python environment with uv"
echo "  5. Check VSCode integration"
echo "  6. Install project package"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."
echo ""

# Function to run a setup script
run_setup() {
    local script_name=$1
    local script_path="$SCRIPT_DIR/$script_name"

    if [ ! -f "$script_path" ]; then
        echo -e "${RED}ERROR: Script not found: $script_path${NC}"
        return 1
    fi

    chmod +x "$script_path"
    bash "$script_path"
    echo ""
}

# Step 1: WSL Check
echo -e "${BOLD}Step 1/6: Checking WSL Environment${NC}"
run_setup "setup_wsl_check.sh" || { echo -e "${RED}WSL check failed${NC}"; exit 1; }

# Step 2: Git Setup
echo -e "${BOLD}Step 2/6: Setting up Git${NC}"
run_setup "setup_git.sh" || { echo -e "${YELLOW}Git setup had warnings, continuing...${NC}"; }

# Step 3: Claude Code Setup
echo -e "${BOLD}Step 3/6: Setting up Claude Code CLI${NC}"
run_setup "setup_claude.sh" || { echo -e "${YELLOW}Claude Code setup had warnings, continuing...${NC}"; }

# Step 4: Python Environment
echo -e "${BOLD}Step 4/6: Setting up Python Environment${NC}"
run_setup "setup_python.sh" || { echo -e "${RED}Python setup failed${NC}"; exit 1; }

# Step 5: VSCode Check
echo -e "${BOLD}Step 5/6: Checking VSCode Integration${NC}"
run_setup "setup_vscode.sh" || { echo -e "${YELLOW}VSCode check had warnings, continuing...${NC}"; }

# Step 6: Project Setup
echo -e "${BOLD}Step 6/6: Final Project Setup${NC}"
run_setup "setup_project.sh" || { echo -e "${RED}Project setup failed${NC}"; exit 1; }

# Optional: Auto-update check setup
echo ""
echo -e "${BOLD}${BLUE}Optional: Daily Update Check${NC}"
echo "Would you like to set up automatic daily checks for repository updates?"
echo "This will safely fetch updates once per day and notify you if new changes are available."
echo "(This does NOT auto-merge - it just notifies you when updates exist)"
echo ""
read -p "Enable daily update checks? [y/N]: " ENABLE_AUTO_UPDATE

if [[ "$ENABLE_AUTO_UPDATE" == "y" || "$ENABLE_AUTO_UPDATE" == "Y" ]]; then
    echo ""
    run_setup "setup_auto_update_check.sh" || { echo -e "${YELLOW}Auto-update setup had warnings, continuing...${NC}"; }
else
    echo -e "${YELLOW}Skipping auto-update setup. You can enable it later with:${NC}"
    echo "  ./scripts/setup_auto_update_check.sh"
fi

# Final summary
echo ""
echo -e "${BOLD}${GREEN}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║              🎉 Setup Complete! 🎉                     ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo -e "${YELLOW}=== Next Steps ===${NC}"
echo ""
echo "1. ${BOLD}Authenticate Claude Code:${NC}"
echo "   Run: ${BLUE}claude${NC}"
echo "   Then use: ${BLUE}/login${NC}"
echo ""
echo "2. ${BOLD}Add your Excel files:${NC}"
echo "   Place them in: ${BLUE}resources/${NC}"
echo ""
echo "3. ${BOLD}Activate Python environment:${NC}"
echo "   Run: ${BLUE}source .venv/bin/activate${NC}"
echo ""
echo "4. ${BOLD}Start using Claude Code:${NC}"
echo "   Run: ${BLUE}claude${NC}"
echo "   Try: 'Generate a timeline chart from my Excel data'"
echo ""
echo "5. ${BOLD}Open in VSCode (optional):${NC}"
echo "   Run: ${BLUE}code .${NC}"
echo ""
echo -e "${GREEN}Happy graphing! 📊${NC}"
echo ""
