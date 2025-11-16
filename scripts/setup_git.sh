#!/bin/bash
# Git Setup Script

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

echo -e "${BLUE}=== Git Setup ===${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}ERROR: Git is not installed${NC}"
    echo "Install git with: sudo apt update && sudo apt install -y git"
    exit 1
fi

echo -e "${GREEN}✓ Git is installed${NC}"

# Check if already a git repository
if [ -d .git ]; then
    echo -e "${YELLOW}⚠ Git repository already initialized${NC}"
else
    echo "Initializing git repository..."
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}"
fi

# Configure git if not set
if [ -z "$(git config --global user.name)" ]; then
    echo -e "${YELLOW}⚠ Git user.name not configured${NC}"
    echo "Please run: git config --global user.name 'Your Name'"
else
    echo -e "${GREEN}✓ Git user.name configured: $(git config --global user.name)${NC}"
fi

if [ -z "$(git config --global user.email)" ]; then
    echo -e "${YELLOW}⚠ Git user.email not configured${NC}"
    echo "Please run: git config --global user.email 'your.email@example.com'"
else
    echo -e "${GREEN}✓ Git user.email configured: $(git config --global user.email)${NC}"
fi

# Create pre-commit hook to prevent Excel file commits
HOOK_DIR=".git/hooks"
HOOK_FILE="$HOOK_DIR/pre-commit"

mkdir -p "$HOOK_DIR"

cat > "$HOOK_FILE" << 'HOOK_EOF'
#!/bin/bash
# Pre-commit hook to prevent committing Excel data files

# Check for Excel files being committed (except the template)
EXCEL_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(xlsx|xls|xlsm|xlsb|csv)$' | grep -v 'example_template.xlsx' || true)

if [ -n "$EXCEL_FILES" ]; then
    echo "ERROR: Attempting to commit Excel data files!"
    echo "The following files are blocked for privacy:"
    echo "$EXCEL_FILES"
    echo ""
    echo "Excel data files should NEVER be committed to GitHub."
    echo "Only resources/example_template.xlsx (empty template) is allowed."
    echo ""
    echo "These files are already in .gitignore - please check your git add commands."
    exit 1
fi

exit 0
HOOK_EOF

chmod +x "$HOOK_FILE"
echo -e "${GREEN}✓ Pre-commit hook installed (blocks Excel data files)${NC}"

echo -e "${BLUE}=== Git Setup Complete ===${NC}"
