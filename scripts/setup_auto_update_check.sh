#!/bin/bash
# Setup Automatic Daily Update Check
# Configures a cron job to check for repository updates once per day

set -e  # Exit on error

# Detect color support
if [ -t 1 ] && command -v tput &> /dev/null && [ $(tput colors) -ge 8 ]; then
    GREEN=$(tput setaf 2)
    YELLOW=$(tput setaf 3)
    RED=$(tput setaf 1)
    BLUE=$(tput setaf 4)
    BOLD=$(tput bold)
    NC=$(tput sgr0)
else
    GREEN=''
    YELLOW=''
    RED=''
    BLUE=''
    BOLD=''
    NC=''
fi

echo -e "${BLUE}=== Setup Automatic Update Check ===${NC}"
echo ""

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Absolute path to the check script
CHECK_SCRIPT="$SCRIPT_DIR/check_updates.sh"

# Make sure check_updates.sh is executable
chmod +x "$CHECK_SCRIPT"

# Check if cron is available
if ! command -v crontab &> /dev/null; then
    echo -e "${RED}ERROR: crontab command not found${NC}"
    echo "Cron may not be installed. On Ubuntu/WSL, install with:"
    echo "  sudo apt update && sudo apt install -y cron"
    exit 1
fi

# Check if cron service is running (WSL specific)
if ! service cron status &> /dev/null; then
    echo -e "${YELLOW}⚠ Cron service is not running${NC}"
    echo ""
    echo "On WSL, you need to start the cron service:"
    echo -e "  ${BOLD}sudo service cron start${NC}"
    echo ""
    echo "To auto-start cron on WSL startup, add this to your ~/.bashrc:"
    echo -e "  ${BOLD}sudo service cron start &> /dev/null${NC}"
    echo ""
    read -p "Would you like to start cron now? (requires sudo) [y/N]: " START_CRON
    if [[ "$START_CRON" == "y" || "$START_CRON" == "Y" ]]; then
        sudo service cron start
        echo -e "${GREEN}✓ Cron service started${NC}"
    else
        echo -e "${YELLOW}⚠ Skipping auto-update setup (cron not running)${NC}"
        exit 0
    fi
fi

# Create a log directory
LOG_DIR="$PROJECT_ROOT/.git/update-check-logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/last-check.log"

# Create cron job entry
# Runs daily at 9:00 AM
CRON_TIME="0 9 * * *"
CRON_JOB="$CRON_TIME cd $PROJECT_ROOT && $CHECK_SCRIPT >> $LOG_FILE 2>&1"

# Check if this cron job already exists
if crontab -l 2>/dev/null | grep -F "$CHECK_SCRIPT" > /dev/null; then
    echo -e "${YELLOW}⚠ Update check cron job already exists${NC}"
    echo ""
    echo "Current crontab entry:"
    crontab -l | grep -F "$CHECK_SCRIPT"
    echo ""
    read -p "Do you want to update it? [y/N]: " UPDATE_CRON
    if [[ "$UPDATE_CRON" != "y" && "$UPDATE_CRON" != "Y" ]]; then
        echo "Keeping existing cron job"
        exit 0
    fi
    # Remove old entry
    crontab -l | grep -v -F "$CHECK_SCRIPT" | crontab -
fi

# Add the cron job
# Use || true to handle the case where user has no existing crontab
(crontab -l 2>/dev/null || true; echo "$CRON_JOB") | crontab -

echo -e "${GREEN}✓ Daily update check configured!${NC}"
echo ""
echo "Configuration:"
echo "  Schedule: ${BLUE}Daily at 9:00 AM${NC}"
echo "  Script: ${BLUE}$CHECK_SCRIPT${NC}"
echo "  Logs: ${BLUE}$LOG_FILE${NC}"
echo ""
echo "To test immediately, run:"
echo -e "  ${BOLD}$CHECK_SCRIPT${NC}"
echo ""
echo "To view configured cron jobs:"
echo -e "  ${BOLD}crontab -l${NC}"
echo ""
echo "To disable automatic checks:"
echo -e "  ${BOLD}crontab -e${NC}"
echo "  (then remove the line containing 'check_updates.sh')"
echo ""
echo -e "${GREEN}=== Setup Complete ===${NC}"
