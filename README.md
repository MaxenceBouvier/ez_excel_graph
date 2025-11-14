# Excel to Graph

**AI-Assisted Excel to Graph for Simplifying the Life of Many Social Science Ph.D. Students**

Generate beautiful graphs from Excel data using Python and Claude Code - no programming experience required!

This project helps social science researchers visualize data from Excel spreadsheets. Perfect for analyzing interviews, focus groups, surveys, discourse analysis, and other qualitative or quantitative data. Works with any Excel structure - just describe what you want to visualize in natural language.

## 🎯 Features

- 📊 Flexible visualization: Bar charts, Line plots, Scatter plots, Heatmaps, and more
- 📁 Project-based organization: Manage multiple research projects separately
- 🔄 Excel to CSV conversion: Easy data inspection for Claude
- 🇫🇷 Full support for international text (French accents: é, è, à, ô, etc.)
- 📤 Multiple output formats: PNG, PDF, Interactive HTML
- 🤖 Natural language interface via Claude Code CLI
- 🔒 Privacy-first: Excel data files never committed to GitHub
- 📦 Easy setup with automated scripts

## 📋 Prerequisites

Before starting, you need:
- Windows 10 (version 2004+, Build 19041+) or Windows 11
- Administrator access to install WSL

## 🚀 Complete Setup Guide

### Step 1: Install WSL (Windows Subsystem for Linux)

If you don't have WSL installed yet:

1. **Open PowerShell as Administrator**
   - Press `Windows + X`
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Install WSL with Ubuntu**
   ```powershell
   wsl --install
   ```

3. **Restart your computer** when prompted

4. **Create your Linux user account**
   - After restart, Ubuntu will open automatically
   - You'll be asked to create a username and password
   - Remember these credentials!

### Step 2: Setup Git in WSL

Open your WSL terminal (Ubuntu) and configure git:

```bash
# Install git if not already installed
sudo apt update
sudo apt install -y git

# Configure your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Clone This Repository

In your WSL terminal:

```bash
# Create the projects directory
mkdir -p ~/proj
cd ~/proj

# Clone the repository
git clone https://github.com/YOUR_USERNAME/excel_to_graph.git

# Navigate into the project
cd excel_to_graph
```

### Step 4: Run Complete Setup

Run the all-in-one setup script:

```bash
./scripts/setup_all.sh
```

This script will:
1. ✅ Check your WSL environment
2. ✅ Initialize git and install pre-commit hooks
3. ✅ Install Claude Code CLI
4. ✅ Set up Python environment with uv
5. ✅ Check VSCode integration
6. ✅ Install the project package
7. ✅ Create a working branch for you

**Note:** The script may ask for confirmation at certain steps. Just press Enter to continue.

### Step 5: Authenticate Claude Code

After setup completes:

```bash
# Start Claude Code
claude

# In the Claude Code prompt, authenticate
/login
```

Follow the authentication instructions. You can use either:
- Your Claude.ai account (recommended)
- Claude Console account with API access

#### Optional: Setup Claude Code Permissions

To avoid repeatedly approving common commands, you can copy the example settings file:

```bash
# Copy the example settings to your .claude directory
cp .claude.settings.example.json .claude/settings.local.json

# Update the path in the file to match your username
# Edit line 41 to replace YOUR_USERNAME with your actual username
```

This allows Claude Code to run common commands (Python, git, file operations, etc.) without asking for approval each time.

### Step 6: Open in VSCode (Optional)

For a better editing experience:

1. **Install VSCode on Windows** from https://code.visualstudio.com/

2. **Install the Remote-WSL extension**
   - Open VSCode
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Remote - WSL"
   - Install it

3. **Open the project from WSL terminal**
   ```bash
   code .
   ```

VSCode will open with full WSL integration!

## 📊 Using the Tool

### Working with Your Excel Data

You have two options for organizing your work:

#### Option 1: Quick Start (Simple Use)

Just add your Excel files directly to `resources/`:

```bash
# Add your file
cp ~/my_data.xlsx resources/

# Convert to CSV for easier inspection
excel-to-graph convert resources/my_data.xlsx
```

#### Option 2: Project-Based (Recommended)

For organized, multi-project work:

```bash
# Create a new project
excel-to-graph init my-research-2024

# Add Excel files to your project
cp ~/survey_data.xlsx resources/my-research-2024/

# Convert all Excel files in the project
excel-to-graph convert resources/my-research-2024
```

**🔒 Privacy Note:** Your Excel files stay on your computer and are NEVER uploaded to GitHub!

### Converting Excel to CSV

Claude Code can inspect CSV files more easily than Excel. Convert your files:

```bash
# Activate environment
source .venv/bin/activate

# Convert a single file
excel-to-graph convert resources/my_data.xlsx

# Convert all files in a project
excel-to-graph convert resources/my-project/

# List all your projects
excel-to-graph list
```

Each Excel sheet becomes a separate CSV file: `<filename>_<sheetname>.csv`

### Generating Graphs with Claude Code

Start Claude Code and use natural language:

```bash
# Activate Python environment
source .venv/bin/activate

# Start Claude Code
claude
```

#### English Prompts:
```
"Show me the structure of my Excel data in resources/"

"Convert all Excel files in resources/interview-study/ to CSV"

"Create a bar chart comparing column A values across all rows"

"Generate a scatter plot of age vs response_time from survey_data.xlsx"

"Make an interactive HTML visualization I can explore"

"Save all visualizations as PDF in outputs/my-project/"
```

#### French Prompts (Français):
```
"Montre-moi la structure de mes données Excel dans resources/"

"Convertis tous les fichiers Excel de resources/etude-interviews/ en CSV"

"Crée un graphique en barres comparant les valeurs de la colonne A"

"Génère un nuage de points âge vs temps_réponse depuis sondage.xlsx"

"Crée une visualisation HTML interactive que je peux explorer"
```

### Using the Command-Line Interface

For quick operations without Claude Code:

```bash
# Activate environment
source .venv/bin/activate

# Create a new project
excel-to-graph init my-project

# Convert Excel to CSV
excel-to-graph convert resources/my_data.xlsx
excel-to-graph convert resources/my-project/

# List all projects
excel-to-graph list

# Generate visualizations (legacy timeline format)
excel-to-graph visualize resources/data.xlsx --all

# See all options
excel-to-graph --help
excel-to-graph init --help
excel-to-graph convert --help
```

## 📂 Project Structure

```
excel_to_graph/
├── README.md                     # This file
├── resources/                    # Excel files (never committed to git)
│   ├── README.md                # Organization guide
│   ├── example_template.xlsx    # Generic template
│   ├── project-1/               # Your projects...
│   │   ├── README.md
│   │   ├── data.xlsx
│   │   └── data_Sheet1.csv      # Auto-generated CSV
│   └── project-2/
├── outputs/                      # Generated graphs (auto-created)
│   ├── png/                     # PNG images
│   ├── pdf/                     # PDF files
│   ├── html/                    # Interactive HTML
│   ├── project-1/               # Project-specific outputs
│   └── project-2/
├── scripts/                      # Setup & project scripts
│   ├── setup_all.sh             # Main setup script
│   ├── project-1/               # Custom scripts per project
│   └── ...
└── src/excel_to_graph/          # Python source code
```

## 🪟 Windows Commands from WSL

You can use Windows applications from your WSL terminal:

```bash
# Open File Explorer in current directory
explorer.exe .

# Open VSCode in current directory
code .

# Open a file with Windows Notepad
notepad.exe filename.txt
```

## 🔧 Troubleshooting

### "command not found: claude"

After installing Claude Code, you may need to reload your shell:
```bash
source ~/.bashrc
```

Or simply close and reopen your terminal.

### "Virtual environment not activated"

Always activate the Python environment before using the tools:
```bash
source .venv/bin/activate
```

You'll see `(.venv)` in your prompt when activated.

### "Excel file not found"

Make sure your Excel files are in the `resources/` directory:
```bash
ls resources/
```

### Git won't let me commit

If you try to commit an Excel file (except the template), the pre-commit hook will block it. This is intentional to protect your data privacy!

## 🤝 Contributing & Getting Help

If you encounter issues or want to suggest improvements:

1. **Check existing issues** on GitHub
2. **Create a new issue** with details about your problem
3. **Ask Claude Code** for help:
   ```bash
   claude
   > "I'm having trouble with [describe your issue]"
   ```

## 📝 License

MIT License - See LICENSE file for details

## 🎉 Happy Graphing!

Once setup is complete, you can generate beautiful visualizations from your Excel data using simple natural language commands!

For more advanced usage and examples, explore the `src/excel_to_graph/` code or ask Claude Code for help.
