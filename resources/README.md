# Resources Directory

This directory is for your Excel data files.

## ⚠️ IMPORTANT - DATA PRIVACY ⚠️

**NEVER commit your actual Excel data files to GitHub!**

All Excel files (`.xlsx`, `.xls`, `.xlsm`, `.csv`) in this directory are automatically ignored by git and **WILL NOT** be pushed to GitHub. This protects your private data.

### What gets committed:
- ✅ `example_template.xlsx` - Generic template showing example data structure
- ✅ This README file
- ✅ Project-specific READMEs (in subdirectories)

### What does NOT get committed:
- ❌ Any other Excel files with your actual data
- ❌ CSV files (converted from Excel)
- ❌ Any files containing real research/analysis data

### Multiple layers of protection:

1. **`.gitignore`**: All Excel files are blocked (except the template)
2. **Pre-commit hook**: Automatically prevents committing Excel data files
3. **This warning**: Reminds you to keep data local

## Working with Excel Files

### Option 1: Quick Start (Single Project)

For simple, one-off work, just place your Excel files directly here:

```bash
# Add your file
cp ~/my_data.xlsx resources/

# Convert to CSV for easier inspection by Claude
excel-to-graph convert resources/my_data.xlsx

# Use Claude Code to analyze
claude
> "Show me the structure of my_data.xlsx"
> "Generate visualizations from this data"
```

### Option 2: Project-Based Organization (Recommended)

For multiple projects or organized work, create separate project folders:

```bash
# Initialize a new project
excel-to-graph init my-research-2024

# This creates:
# - resources/my-research-2024/
# - outputs/my-research-2024/
# - scripts/my-research-2024/
```

Then add your files to the project directory:

```bash
# Add Excel files to your project
cp ~/survey_data.xlsx resources/my-research-2024/

# Convert all Excel files in the project
excel-to-graph convert resources/my-research-2024
```

### Multiple Projects Example:

```
resources/
├── example_template.xlsx          # Generic template (committed to git)
├── README.md                       # This file
├── interview-study/                # Project 1
│   ├── README.md
│   ├── participants.xlsx
│   ├── participants_Sheet1.csv    # Auto-converted
│   └── responses.xlsx
├── survey-analysis/                # Project 2
│   ├── README.md
│   ├── survey_2024.xlsx
│   └── demographics.xlsx
└── focus-groups/                   # Project 3
    ├── README.md
    ├── session1.xlsx
    └── session2.xlsx
```

## Converting Excel to CSV

CSV files are easier for Claude to inspect and understand. Convert your Excel files:

```bash
# Convert a single file
excel-to-graph convert resources/my_data.xlsx

# Convert all Excel files in a directory
excel-to-graph convert resources/my-project/

# Convert and save CSVs elsewhere
excel-to-graph convert resources/data.xlsx -o /tmp/csvs/
```

Each Excel sheet becomes a separate CSV file named: `<filename>_<sheetname>.csv`

## Using Your Data with Claude Code

Once your Excel files are in resources (and optionally converted to CSV):

```bash
# Activate the environment
source .venv/bin/activate

# Start Claude Code
claude
```

Then use natural language:

### English prompts:
```
"List all Excel files in resources/"
"Show me the column structure of my_data.xlsx"
"Convert all Excel files in resources/interview-study/ to CSV"
"Create a bar chart from the survey data"
"Generate visualizations and save to outputs/my-project/"
```

### French prompts (Français):
```
"Liste tous les fichiers Excel dans resources/"
"Montre-moi la structure des colonnes de mes_données.xlsx"
"Convertis tous les fichiers Excel de resources/etude-interviews/ en CSV"
"Crée un graphique en barres à partir des données de sondage"
```

## Managing Projects

```bash
# List all initialized projects
excel-to-graph list

# Each project has its own:
# - resources/<project>/ - Excel files
# - outputs/<project>/   - Generated graphs
# - scripts/<project>/   - Custom scripts
```

## Questions?

Ask Claude Code for help:
```bash
claude
> "How do I organize my Excel files?"
> "Explain the project structure"
> "How do I convert Excel to CSV?"
```
