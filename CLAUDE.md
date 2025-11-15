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
python -c "from excel_to_graph import ExcelReader, GraphVisualizer; print('✓ Imports OK')"
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
Entry point for the `excel-to-graph` command. Provides three main commands:
- `init <project_name>` - Create new project structure
- `convert <path>` - Convert Excel → CSV
- `list` - Show all projects
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

#### `utils.py` - Helper Functions
Utilities for:
- **Project detection:** `detect_project_from_path()` identifies which project a file belongs to
- **Project management:** `create_project_structure()`, `list_projects()`
- **Project naming validation:** Only allows alphanumeric, hyphens, underscores
- **Output organization:** Auto-organizes outputs by project and file type
- **Filename sanitization:** Ensures filesystem-safe names

### Available Graphic Libraries

This project includes several powerful visualization libraries to create a wide variety of charts and graphs:

#### Matplotlib (>=3.8.0)
**Purpose:** Core static plotting library for Python
**Best for:**
- Static publication-quality figures (PNG, PDF)
- Fine-grained control over every plot element
- Traditional chart types: line plots, scatter plots, histograms, bar charts

**Example use cases:**
```python
import matplotlib.pyplot as plt

# Simple line plot
plt.plot(x, y)
plt.savefig('output.png')

# Bar chart with custom styling
fig, ax = plt.subplots()
ax.bar(categories, values)
ax.set_title('My Chart')
plt.savefig('output.pdf')
```

#### Plotly (>=5.18.0)
**Purpose:** Interactive web-based visualizations
**Best for:**
- Interactive HTML charts with zoom, pan, hover tooltips
- 3D visualizations
- Dashboards and web applications
- Sharing visualizations that users can explore

**Key features:**
- Export to HTML for standalone interactive charts
- Export to static images via Kaleido (PNG, PDF)
- Built-in templates and themes

**Example use cases:**
```python
import plotly.express as px
import plotly.graph_objects as go

# Quick interactive scatter plot
fig = px.scatter(df, x='age', y='response_time')
fig.write_html('outputs/project/html/scatter.html')

# Custom interactive timeline
fig = go.Figure(data=[go.Scatter(x=dates, y=values)])
fig.update_layout(title='Timeline')
fig.write_html('outputs/project/html/timeline.html')
```

#### Seaborn (>=0.13.0)
**Purpose:** Statistical data visualization built on matplotlib
**Best for:**
- Statistical plots: distributions, regressions, correlations
- Beautiful default styles and color palettes
- Multi-plot grids (FacetGrid, PairGrid)
- Heatmaps and cluster maps

**Key features:**
- Integrates seamlessly with pandas DataFrames
- Automatic computation of statistical aggregates
- Attractive default themes

**Example use cases:**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# Distribution plot with multiple variables
sns.histplot(data=df, x='age', hue='category')
plt.savefig('outputs/project/png/distribution.png')

# Correlation heatmap
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.savefig('outputs/project/png/correlation.png')

# Box plot for statistical comparison
sns.boxplot(data=df, x='group', y='score')
plt.savefig('outputs/project/png/boxplot.png')
```

#### Dash (>=2.14.0)
**Purpose:** Framework for building interactive web-based dashboards
**Best for:**
- Multi-page analytical dashboards
- Real-time data monitoring
- Interactive data exploration tools
- Web applications with complex user interactions

**Key features:**
- Built on top of Plotly for interactive charts
- Reactive callbacks for interactivity
- Professional-looking layouts without HTML/CSS knowledge
- Can be deployed as standalone web apps

**Example use cases:**
```python
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Simple interactive dashboard
app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(id='dropdown', options=['Option A', 'Option B']),
    dcc.Graph(id='graph')
])

@app.callback(Output('graph', 'figure'), Input('dropdown', 'value'))
def update_graph(selected_value):
    # Update graph based on user selection
    fig = px.bar(df[df['category'] == selected_value], x='x', y='y')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
```

#### Choosing the Right Library

**Use Matplotlib when:**
- You need static publication-quality images
- You want fine control over every visual element
- You're creating traditional academic charts

**Use Plotly when:**
- Users need to interact with the visualization (zoom, pan, hover)
- You want to create standalone HTML visualizations
- You're building 3D visualizations

**Use Seaborn when:**
- You're doing statistical analysis and visualization
- You want beautiful plots with minimal code
- You're exploring correlations and distributions in your data

**Use Dash when:**
- You want to build a complete interactive dashboard
- You need multiple linked visualizations
- You want users to filter/explore data through dropdowns and controls
- You're creating a data exploration tool

**Note:** All libraries work well with pandas DataFrames, making it easy to visualize Excel data after conversion.

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

```
"Show me the structure of my Excel data in resources/"
"Convert all Excel files in resources/interview-study/ to CSV"
"Create a bar chart comparing column A across all rows"
"Generate a scatter plot of age vs response_time"
```

When implementing features or helping users, prioritize the natural language workflow over direct CLI usage.

## Important Implementation Notes

### When Creating Visualizations
1. Always check if the data contains the required columns
2. Handle missing data gracefully with clear error messages
3. Support both French and English column names when reasonable
4. Auto-detect project context from file paths to organize outputs properly

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
