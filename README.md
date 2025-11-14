# Excel to Graph

**AI-Assisted Excel to Graph for Simplifying the Life of Many Social Science Ph.D. Students**

Generate beautiful graphs from Excel timeline data using Python and Claude Code - no programming experience required!

This project helps social science researchers visualize timeline data from Excel spreadsheets with columns like `speak_time`, `speak_person`, and multiple `idea_X` columns. Perfect for analyzing interviews, focus groups, discourse analysis, and other qualitative data.

## 🎯 Features

- 📊 Multiple chart types: Timeline/Gantt, Bar charts, Distribution plots, Heatmaps
- 🇫🇷 Full support for French text and accents (é, è, à, ô, etc.)
- 📁 Multiple output formats: PNG, PDF, Interactive HTML
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

### Adding Your Excel Data

1. Place your Excel files in the `resources/` directory
2. Your files should have this structure:

| speak_time | speak_person | idea_1 | idea_2 | idea_3 |
|------------|--------------|--------|--------|--------|
| T1 or 1    | P1 or Name   | value  | value  | value  |
| T2 or 2    | P2 or Name   | value  | value  | value  |

**🔒 Privacy Note:** Your Excel files stay on your computer and are NEVER uploaded to GitHub!

### Generating Graphs with Claude Code

Activate the Python environment and start Claude Code:

```bash
# Activate Python environment
source .venv/bin/activate

# Start Claude Code
claude
```

Then use natural language to generate graphs:

#### English Prompts:
```
"Generate a timeline chart from my Excel data in resources/"

"Create a bar chart comparing speaking time per person, save as PDF"

"Show me all ideas mentioned by Person 1 across all time periods"

"Generate all standard visualizations and save as PNG in outputs/"

"Create an interactive HTML timeline that I can zoom and explore"
```

#### French Prompts (Français):
```
"Génère un graphique chronologique à partir de mes données Excel dans resources/"

"Crée un graphique en barres comparant le temps de parole par personne, enregistre en PDF"

"Montre-moi toutes les idées mentionnées par la Personne 1 sur toutes les périodes"

"Génère toutes les visualisations standard et enregistre en PNG dans outputs/"
```

### Using the Command-Line Interface

For quick graph generation without Claude Code:

```bash
# Activate environment
source .venv/bin/activate

# Generate all charts from an Excel file
excel-to-graph resources/your_data.xlsx --all

# Generate only timeline chart as PNG
excel-to-graph resources/your_data.xlsx --timeline --format png

# Generate bar chart as interactive HTML
excel-to-graph resources/your_data.xlsx --bar --format html

# See all options
excel-to-graph --help
```

## 📂 Project Structure

```
excel_to_graph/
├── README.md                 # This file
├── resources/                # Place your Excel files here
│   ├── README.md            # Data privacy information
│   └── example_template.xlsx # Empty template
├── outputs/                  # Generated graphs (auto-created)
│   ├── png/                 # PNG images
│   ├── pdf/                 # PDF files
│   └── html/                # Interactive HTML plots
├── scripts/                  # Setup scripts
│   ├── setup_all.sh         # Main setup script
│   └── ...                  # Individual setup scripts
└── src/excel_to_graph/      # Python source code
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
