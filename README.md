# Excel to Graph

*[English](#) | [Français](README.fr.md)*

**AI-Assisted Excel to Graph for Simplifying the Life of Many Social Science Ph.D. Students**

Generate beautiful graphs from Excel data using Python and Claude Code - no programming experience required!

This project helps social science researchers visualize data from Excel spreadsheets. Perfect for analyzing interviews, focus groups, surveys, discourse analysis, and other qualitative or quantitative data. Works with any Excel structure - just describe what you want to visualize in natural language.

## 📑 Table of Contents

- [🎯 Features](#-features)
- [📋 Prerequisites](#-prerequisites)
- [🚀 Complete Setup Guide](#-complete-setup-guide)
  - [Step 1: Install WSL (Windows Subsystem for Linux)](#step-1-install-wsl-windows-subsystem-for-linux)
  - [Step 2: Setup Git in WSL](#step-2-setup-git-in-wsl)
  - [Step 3: Clone This Repository](#step-3-clone-this-repository)
  - [Step 4: Run Complete Setup](#step-4-run-complete-setup)
  - [Step 5: Authenticate Claude Code](#step-5-authenticate-claude-code)
  - [Step 6: Open in VSCode (Highly Recommended!)](#step-6-open-in-vscode-highly-recommended)
  - [Step 7: Setup GitHub Authentication (Optional)](#step-7-setup-github-authentication-optional)
- [📊 Using the Tool](#-using-the-tool)
  - [Working with Your Excel Data](#working-with-your-excel-data)
  - [Generating Graphs with Claude Code](#generating-graphs-with-claude-code)
  - [Using the Command-Line Interface](#using-the-command-line-interface)
- [📂 Project Structure](#-project-structure)
- [🪟 Windows Commands from WSL](#-windows-commands-from-wsl)
- [🔧 Troubleshooting](#-troubleshooting)
- [🤝 Contributing & Getting Help](#-contributing--getting-help)
- [📝 License](#-license)

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

2. **Install WSL with Ubuntu 24.04**
   ```powershell
   wsl --install Ubuntu-24.04
   ```

   **Note:** If you already have WSL installed but need Ubuntu 24.04, use:
   ```powershell
   wsl --install -d Ubuntu-24.04
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
git clone https://github.com/MaxenceBouvier/ez_excel_graph.git excel_to_graph

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

---

**⚠️ IMPORTANT: Restart Your Terminal After Setup! ⚠️**

After the setup script finishes, you **MUST** restart your terminal for the new commands to work:

1. **Close the terminal window completely**
2. **Open a new Ubuntu terminal**
3. **Navigate back to the project:**
   ```bash
   cd ~/proj/excel_to_graph
   ```

**Why?** The setup script installs new programs (`claude` and `uv`), but your current terminal session doesn't know about them yet. Restarting the terminal fixes this.

---

**🔧 If Setup Failed or Had Errors:**

If you saw errors like `uv: command not found` or `Virtual environment not found`, don't worry! Just:

1. **Restart your terminal** (close and reopen Ubuntu)
2. **Navigate back:**
   ```bash
   cd ~/proj/excel_to_graph
   ```
3. **Complete the Python setup:**
   ```bash
   ./scripts/setup_python.sh
   ```

This will finish what the main script started.

### Step 5: Authenticate Claude Code

**Make sure you've restarted your terminal first!** (See Step 4 above)

Start Claude Code:

```bash
# Start Claude Code
claude
```

**If you get "command not found":**
- You forgot to restart your terminal! Close the terminal and open a new one.
- Or manually update your PATH:
  ```bash
  source ~/.bashrc
  ```

**Once `claude` starts:**

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
- 🤖 **Use Claude Code with a chat interface** - no terminal commands needed!
- 📸 **Share screenshots** with Claude by copy/pasting images to get better help

**Setup VSCode:**

1. **Install VSCode on Windows** from https://code.visualstudio.com/

2. **Install the Remote-WSL extension**
   - Open VSCode
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Remote - WSL"
   - Install it

   ![WSL Extension in VSCode Marketplace](docs/images/image.png)

3. **Open the project from WSL terminal**
   ```bash
   code .
   ```

VSCode will open with full WSL integration! You can now drag and drop your Excel files into the `resources/` folder or any project subfolder.

**Bonus:** Once in VSCode, you can access Claude Code through the command palette (`Ctrl+Shift+P`) and interact with it in a user-friendly chat interface. You can even paste screenshots of your data or errors to get more precise help!

### Step 7: Setup GitHub Authentication (Optional)

**Only needed if you want to push changes back to GitHub!** If you just want to use the tool to create graphs, you can skip this step.

The easiest way to authenticate with GitHub from WSL is using the `gh` CLI tool:

1. **Install GitHub CLI**
   ```bash
   # Install gh CLI
   sudo apt update
   sudo apt install -y gh
   ```

2. **Authenticate with GitHub**
   ```bash
   # Start authentication (this will open your browser)
   gh auth login
   ```

3. **Follow the prompts:**
   - Select: **GitHub.com**
   - Select: **HTTPS** (easiest for beginners)
   - Authenticate Git with GitHub credentials? **Yes**
   - How would you like to authenticate? **Login with a web browser**
   - Copy the one-time code shown, press Enter
   - Your browser will open - paste the code and authorize

That's it! Now you can push changes without being prompted for credentials.

**What can you do after authentication?**
- Push your changes: `git push`
- Create pull requests: `gh pr create`
- View issues: `gh issue list`

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

#### 🌟 Using Claude Code in VSCode (Recommended!)

**The easiest way to work with Claude Code is through the VSCode interface!** This gives you a user-friendly chat interface with powerful capabilities:

✨ **Key Benefits:**
- 💬 **Natural chat interface** - No command-line needed!
- 📸 **Share screenshots** - Copy/paste images directly to show Claude what you need
- 👁️ **Visual feedback** - See file changes and graphs as they're created
- 🖱️ **Point and click** - Easy navigation between files

**How to use Claude Code in VSCode:**

1. **Open VSCode** (if you haven't already):
   ```bash
   code .
   ```

2. **Access Claude Code** through the VSCode command palette:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type "Claude Code" and select the appropriate command
   - Or use the Claude Code icon in your VSCode sidebar (if available)

3. **Chat naturally with Claude** in the VSCode panel:
   ```
   "Show me the structure of my Excel data in resources/"

   "Create a bar chart from the data in resources/my-project/survey.xlsx"

   "Help me understand this error message"
   ```

4. **Share screenshots to get better help!**
   - Take a screenshot of your Excel data, error message, or graph
   - Simply **copy and paste** the image into the Claude Code chat
   - Claude can see the image and provide specific guidance
   - Example: "Claude, here's a screenshot of my data [paste image]. Can you create a timeline visualization from columns B and C?"

#### 💻 Using Claude Code from Terminal (Alternative)

If you prefer the command-line or need to use terminal commands:

```bash
# Activate Python environment
source .venv/bin/activate

# Start Claude Code
claude
```

#### Example Prompts (English):
```
"Show me the structure of my Excel data in resources/"

"Convert all Excel files in resources/interview-study/ to CSV"

"Create a bar chart comparing column A values across all rows"

"Generate a scatter plot of age vs response_time from survey_data.xlsx"

"Make an interactive HTML visualization I can explore"

"Save all visualizations as PDF in outputs/my-project/"
```

#### Example Prompts (French / Français):
```
"Montre-moi la structure de mes données Excel dans resources/"

"Convertis tous les fichiers Excel de resources/etude-interviews/ en CSV"

"Crée un graphique en barres comparant les valeurs de la colonne A"

"Génère un nuage de points âge vs temps_réponse depuis sondage.xlsx"

"Crée une visualisation HTML interactive que je peux explorer"
```

**💡 Pro Tip:** Whether using VSCode or terminal, you can ask Claude to explain anything in the project. Claude has full context of the codebase and can help troubleshoot, suggest improvements, and guide you through complex tasks!

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

### Setup Script Issues

#### "command not found: claude" or "command not found: uv"

**This is the most common issue!** It happens because the setup script installed new programs, but your terminal session hasn't loaded them yet.

**Solution:**
1. **Close your terminal completely**
2. **Open a new Ubuntu terminal**
3. **Try again:**
   ```bash
   cd ~/proj/excel_to_graph
   claude --help
   ```

**Alternative (without restarting):**
```bash
source ~/.bashrc
```

#### "uv: command not found" during setup_all.sh

If the setup script showed this error, it means the Python environment wasn't created. This is normal - it happens because `uv` was installed but not loaded yet.

**Solution:**
1. **Restart your terminal** (close and reopen)
2. **Navigate back:**
   ```bash
   cd ~/proj/excel_to_graph
   ```
3. **Run the Python setup:**
   ```bash
   ./scripts/setup_python.sh
   ```

This completes the setup!

#### "Virtual environment not found" at end of setup

This happens if the Python setup step failed (usually because of the `uv` issue above).

**Solution:** Same as above - restart terminal and run `./scripts/setup_python.sh`

#### Setup script seems stuck or asks for password

- If it asks for your Ubuntu password, type it and press Enter (you won't see the password as you type - this is normal!)
- Press Enter when prompted to continue
- Press Ctrl+C if you need to cancel

#### Want to re-run the setup script?

**Yes, it's safe!** The script checks what's already installed and won't break anything. You can run `./scripts/setup_all.sh` as many times as needed.

**Better approach:** If only the Python part failed, just run:
```bash
./scripts/setup_python.sh
```

### Usage Issues

#### "Virtual environment not activated"

Always activate the Python environment before using the tools:
```bash
source .venv/bin/activate
```

You'll see `(.venv)` in your prompt when activated.

#### "Excel file not found"

Make sure your Excel files are in the `resources/` directory:
```bash
ls resources/
```

#### Git won't let me commit

If you try to commit an Excel file (except the template), the pre-commit hook will block it. This is intentional to protect your data privacy!

### VSCode Issues

#### "code: command not found"

VSCode needs to be installed on **Windows**, not in WSL:

1. Download from https://code.visualstudio.com/ (Windows version)
2. Install the "Remote - WSL" extension in VSCode
3. Then from WSL terminal: `code .`

**Note:** VSCode is optional - you can use any text editor you prefer!

### Still Having Issues?

1. **Read the error message carefully** - it often tells you what's wrong
2. **Check you're in the right directory:**
   ```bash
   pwd
   # Should show: /home/your-username/proj/excel_to_graph
   ```
3. **Verify Python environment exists:**
   ```bash
   ls .venv
   # Should show files/directories
   ```
4. **Ask Claude Code for help:**
   ```bash
   claude
   > "I'm getting this error: [paste error message]"
   ```
5. **Create a GitHub issue** with your error details

## 🤝 Contributing & Getting Help

If you encounter issues or want to suggest improvements:

1. **Check existing issues** on GitHub
2. **Create a new issue** with details about your problem. (Ask Claude to create a report.)
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
