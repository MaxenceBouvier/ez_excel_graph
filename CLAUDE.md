# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Target Audience

This project is designed for social science researchers (particularly Ph.D. students) who may have **limited command-line and Linux experience**. When communicating with users:
- Use clear, friendly language
- Explain technical steps when needed
- Avoid assuming advanced technical knowledge
- Remember that users interact via WSL2 on Windows

## Common Development Commands

### Environment Setup
```bash
# Activate the Python virtual environment (ALWAYS do this first)
source .venv/bin/activate

# Install package in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Code Quality
```bash
# Format code with Ruff
ruff format src/

# Lint with Ruff
ruff check src/

# Lint and auto-fix
ruff check --fix src/

# Run pre-commit hooks manually (handles both formatting and linting)
pre-commit run --all-files
```

### Testing
```bash
# Run all tests (if tests/ directory exists)
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=src/excel_to_graph --cov-report=term-missing

# Smoke test - verify imports work
python -c "from excel_to_graph import ExcelReader, GraphVisualizer, StatisticalAnalyzer; print('✓ Imports OK')"
```

### CLI Usage
```bash
# IMPORTANT: Always activate venv first!
source .venv/bin/activate

# Initialize a new project
excel-to-graph init my-project-name

# Convert Excel files to CSV
excel-to-graph convert resources/my-project/

# List all projects
excel-to-graph list

# Perform statistical analysis (designed for use with Claude Code)
excel-to-graph analyze resources/my-project/data.xlsx

# Quick descriptive statistics
excel-to-graph analyze resources/my-project/data.csv --describe

# See all CLI options
excel-to-graph --help
```

### Building and Distribution
```bash
# Build the package
python -m build

# Check package with twine
pip install twine
twine check dist/*
```

## Project Architecture

### Project-Based Workflow

This tool uses a **project-based organization** where each research project gets its own isolated folder structure:

```
resources/
├── project-1/        # User's Excel files and auto-generated CSVs
│   ├── data.xlsx
│   └── data_Sheet1.csv
outputs/
├── project-1/        # Generated visualizations
│   ├── png/
│   ├── pdf/
│   └── html/
scripts/
└── project-1/        # Custom analysis scripts (optional)
```

**Key Principle:** Each project is self-contained. Files from one project should not mix with another.

### Core Modules

#### `cli.py` - Command-Line Interface
Entry point for the `excel-to-graph` command. Provides main commands:
- `init <project_name>` - Create new project structure
- `convert <path>` - Convert Excel → CSV
- `list` - Show all projects
- `analyze <file>` - Perform statistical analysis (ANOVA, correlations, t-tests, etc.)
- `visualize` - Legacy direct visualization command

#### `reader.py` - Excel Data Loading
`ExcelReader` class handles reading Excel files via pandas/openpyxl. Supports:
- Multiple sheets
- International text (UTF-8, French accents)
- Timeline data preparation for visualizations

#### `converter.py` - Excel to CSV Conversion
Converts Excel files to CSV format so Claude can more easily inspect data content. Each Excel sheet becomes a separate CSV file named `<filename>_<sheetname>.csv`.

**Important:** Sheet names are sanitized for filesystem safety (special characters → underscores).

#### `visualizer.py` - Graph Generation
`GraphVisualizer` class creates charts using matplotlib and plotly:
- Timeline charts (Gantt-style)
- Bar charts (intervention frequency)
- Distribution plots
- Heatmaps (person × time)

**Output Formats:** PNG, PDF (via matplotlib), HTML (interactive via plotly)

**Font Support:** Uses DejaVu Sans for international character rendering (é, è, à, etc.)

#### `analyzer.py` - Statistical Analysis
`StatisticalAnalyzer` class provides advanced statistical tests for social science research:
- **Descriptive statistics:** Mean, std, quartiles for numeric columns
- **Correlation analysis:** Pearson and Spearman correlations with p-values and heatmaps
- **t-tests:** Independent samples t-tests between two groups
- **ANOVA:** One-way ANOVA with optional post-hoc pairwise comparisons (Bonferroni correction)
- **Chi-square tests:** Test independence between categorical variables
- **Normality tests:** Shapiro-Wilk test to check distribution assumptions

**Output Organization:** Saves reports to `outputs/<project>/analyses/reports/` and plots to `outputs/<project>/analyses/plots/`

**Font Support:** Uses DejaVu Sans for international character rendering

#### `utils.py` - Helper Functions
Utilities for:
- **Project detection:** `detect_project_from_path()` identifies which project a file belongs to
- **Project management:** `create_project_structure()`, `list_projects()`
- **Project naming validation:** Only allows alphanumeric, hyphens, underscores
- **Output organization:** Auto-organizes outputs by project and file type
- **Filename sanitization:** Ensures filesystem-safe names

### Data Privacy Protection

**Critical:** Excel files (except `example_template.xlsx`) must NEVER be committed to git.

**Protection Mechanisms:**
1. `.gitignore` excludes `resources/**/*.xlsx` (and other Excel formats)
2. Pre-commit hooks block accidental commits of Excel files
3. README repeatedly emphasizes that Excel data stays local

When helping users, remind them their data is safe and never uploaded to GitHub.

## Code Style Standards

- **Line length:** 100 characters (configured in Ruff)
- **Python version:** 3.10+ (type hints using modern syntax like `list[str]`)
- **Formatting:** Ruff (enforced via pre-commit and CI)
- **Linting:** Ruff (enforced via pre-commit and CI)
- **Type hints:** Used but not strictly enforced (mypy configured loosely)

## CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on push/PR to main/develop:

1. **Lint job:** Ruff formatting check + Ruff linting
2. **Test job:** Runs on Python 3.10, 3.11, 3.12
   - Smoke tests (import checks)
   - CLI command tests
   - Pytest if `tests/` exists
3. **Build job:** Package building and validation

## Natural Language Interface

The **primary way users interact** with this tool is through Claude Code using natural language prompts. Example prompts:

**Data exploration and conversion:**
```
"Show me the structure of my Excel data in resources/"
"Convert all Excel files in resources/interview-study/ to CSV"
```

**Visualization:**
```
"Create a bar chart comparing column A across all rows"
"Generate a scatter plot of age vs response_time"
```

**Statistical analysis:**
```
"Run a correlation analysis on all numeric variables in my data"
"Perform an ANOVA comparing response times across different groups"
"Do a t-test between treatment and control groups"
"Test if my age variable follows a normal distribution"
"Check for statistical relationships between gender and outcome using chi-square"
```

When implementing features or helping users, prioritize the natural language workflow over direct CLI usage.

## Important Implementation Notes

### When Creating Visualizations
1. Always check if the data contains the required columns
2. Handle missing data gracefully with clear error messages
3. Support both French and English column names when reasonable
4. Auto-detect project context from file paths to organize outputs properly

### When Performing Statistical Analysis
1. Always check data assumptions (normality, sample size) before running tests
2. Report both the test statistic and p-value for transparency
3. Provide clear interpretation of results for non-statistical users
4. Save both numerical reports and visual outputs (correlation heatmaps, etc.)
5. Auto-detect project context to organize analysis outputs properly
6. Handle missing data appropriately (report removed observations)
7. Use appropriate corrections for multiple comparisons (e.g., Bonferroni for post-hoc tests)

### When Adding CLI Commands
1. Update both `cli.py` and the README.md
2. Ensure `--help` text is beginner-friendly
3. Test that commands work from a fresh virtual environment

### When Modifying Project Structure
The project structure creation is handled by `utils.create_project_structure()`. Any changes to project organization should update this function and the README examples.

### CSV Encoding
Always use UTF-8 encoding for CSV files to support international characters properly (`df.to_csv(..., encoding='utf-8')`).

## Windows Integration (WSL2)

Users run this tool in WSL2 but may want to interact with Windows:

```bash
# Open Windows File Explorer
explorer.exe .

# Open VSCode from WSL
code .

# Open file with Windows app
notepad.exe filename.txt
```

When suggesting file operations, consider recommending VSCode for drag-and-drop file management.
