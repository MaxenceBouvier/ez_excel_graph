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
   - If Ubuntu doesn't open automatically:
     - Press `Windows` key and type "Ubuntu"
     - Click on "Ubuntu" (or "Ubuntu 24.04 LTS")
     - This is also how you'll start Ubuntu in the future!
   - You'll be asked to create a username and password
   - Remember these credentials!

5. **About the terminal commands below**
   - All commands that follow must be typed in the Ubuntu terminal
   - Don't be frightened - just copy and paste them one by one
   - Press `Enter` after each command to run it
   - The terminal is your friend!

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
```

Claude Code will typically prompt you to log in automatically on first startup. Just follow the authentication instructions on screen.

**IMPORTANT:** Use your **Claude.ai account** (the free web version). Do NOT use "Claude Console account with API access" as this option is paid and will charge you money!

**Note:** If Claude doesn't prompt automatically, you can manually trigger authentication with `/login`

**Permissions:** The setup script has already configured Claude Code to run common commands (Python, git, file operations, etc.) without asking for approval each time.

### Step 6: Open in VSCode (Highly Recommended!)

**VSCode makes your life MUCH easier!** With VSCode you can:
- 📁 **Drag and drop** your Excel files directly into the `resources/` folder
- 📂 **Browse files** visually instead of using command-line
- ✏️ **Edit files** with a friendly interface
- 👀 **See your project structure** at a glance

**Setup VSCode:**

1. **Install VSCode on Windows** from https://code.visualstudio.com/

2. **Install the Remote-WSL extension**
   - Open VSCode
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Remote - WSL"
   - Install it

   <img src="docs/images/image.png" alt="WSL Extension in VSCode Marketplace" width="600">

3. **Open the project from WSL terminal**
   ```bash
   code .
   ```

VSCode will open with full WSL integration! You can now drag and drop your Excel files into the `resources/` folder or any project subfolder.

## 📊 Using the Tool

### Working with Your Excel Data

**IMPORTANT:** This tool uses a **project-based workflow** to keep your work organized. Each research project gets its own folder.


**🔒 Privacy Note:** Your Excel files stay on your computer and are NEVER uploaded to GitHub!

#### Creating a New Project

```bash
# Create a new project (choose a meaningful name)
excel-to-graph init my-research-2024

# This creates: resources/my-research-2024/
```

#### Adding Your Excel Files

**With VSCode (easiest way):**
1. Open VSCode with `code .`
2. Navigate to `resources/my-research-2024/` in the file explorer
3. Drag and drop your Excel files into the folder

**Or with command-line:**
```bash
# Copy your Excel file to the project folder
cp ~/my_data.xlsx resources/my-research-2024/
```

#### Converting to CSV

Claude Code can inspect CSV files more easily than Excel:

```bash
# Activate environment
source .venv/bin/activate

# Convert all Excel files in your project to CSV
excel-to-graph convert resources/my-research-2024/
```

Each Excel sheet becomes a separate CSV file: `<filename>_<sheetname>.csv`

**🔒 Privacy Note:** Your Excel files stay on your computer and are NEVER uploaded to GitHub!

#### Managing Multiple Projects

```bash
# List all your projects
excel-to-graph list

# Each project can have its own Excel files and outputs
resources/
├── project-1/
│   ├── data.xlsx
│   └── data_Sheet1.csv
├── project-2/
│   ├── survey.xlsx
│   └── survey_Sheet1.csv
└── ...
```

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

# Convert all Excel files in a project to CSV
excel-to-graph convert resources/my-project/

# List all projects
excel-to-graph list

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
