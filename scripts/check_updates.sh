#!/bin/bash
# Check for Repository Updates Script
# Safely fetches from origin and notifies if updates are available

set -e  # Exit on error

# Detect color support
if [ -t 1 ] && command -v tput &> /dev/null && [ $(tput colors) -ge 8 ]; then
    GREEN=$(tput setaf 2)
    YELLOW=$(tput setaf 3)
    BLUE=$(tput setaf 4)
    BOLD=$(tput bold)
    NC=$(tput sgr0)
else
    GREEN=''
    YELLOW=''
    BLUE=''
    BOLD=''
    NC=''
fi

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Change to project root
cd "$PROJECT_ROOT"

# Check if this is a git repository
if [ ! -d .git ]; then
    echo -e "${YELLOW}⚠ Not a git repository, skipping update check${NC}"
    exit 0
fi

# Check if we have a remote configured
if ! git remote get-url origin &> /dev/null; then
    echo -e "${YELLOW}⚠ No remote 'origin' configured, skipping update check${NC}"
    exit 0
fi

# Fetch updates from origin (doesn't merge anything)
echo -e "${BLUE}Checking for repository updates...${NC}"
git fetch origin --quiet 2>/dev/null || {
    echo -e "${YELLOW}⚠ Could not fetch updates (network issue?)${NC}"
    exit 0
}

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Check if current branch has an upstream
if ! git rev-parse --abbrev-ref @{upstream} &> /dev/null; then
    echo -e "${YELLOW}⚠ Current branch '$CURRENT_BRANCH' has no upstream${NC}"
    exit 0
fi

# Get upstream branch
UPSTREAM_BRANCH=$(git rev-parse --abbrev-ref @{upstream})

# Check if local is behind upstream
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{upstream})

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}✓ Repository is up to date${NC}"
elif git merge-base --is-ancestor "$LOCAL" "$REMOTE" 2>/dev/null; then
    # Local is behind remote
    COMMITS_BEHIND=$(git rev-list --count HEAD.."$UPSTREAM_BRANCH")
    echo ""
    echo -e "${BOLD}${YELLOW}═══════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${YELLOW}  📦 Updates Available!${NC}"
    echo -e "${BOLD}${YELLOW}═══════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "Your branch '${BLUE}$CURRENT_BRANCH${NC}' is ${YELLOW}$COMMITS_BEHIND commit(s)${NC} behind '${BLUE}$UPSTREAM_BRANCH${NC}'"
    echo ""
    echo "To update, run:"
    echo -e "  ${BOLD}git pull${NC}"
    echo ""
    echo "Recent updates:"
    git log --oneline HEAD.."$UPSTREAM_BRANCH" --max-count=5
    echo ""
    echo -e "${BOLD}${YELLOW}═══════════════════════════════════════════════════${NC}"
    echo ""
else
    # Local has diverged from remote
    echo -e "${YELLOW}⚠ Your branch has diverged from upstream${NC}"
    echo "You may need to merge or rebase. Run 'git status' for details."
fi
