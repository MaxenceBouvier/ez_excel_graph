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

### Professional Visualization Standards

**CRITICAL:** All visualizations created for users must meet academic/research publication standards. Always strive to make graphs both visually appealing AND professionally presentable.

#### Required Elements for Every Graph

**1. Axis Labels (MANDATORY)**
- Every x-axis and y-axis MUST have a descriptive label with units if applicable
- Labels should be clear and meaningful (not just column names)
- Use proper capitalization and formatting

```python
# Matplotlib/Seaborn
plt.xlabel('Time (minutes)', fontsize=12)
plt.ylabel('Response Rate (%)', fontsize=12)

# Plotly
fig.update_xaxes(title_text='Time (minutes)')
fig.update_yaxes(title_text='Response Rate (%)')
```

**2. Colorbar Labels (when applicable)**
- If a heatmap or color-coded plot has a colorbar, it MUST be labeled
- Indicate what the color scale represents with units

```python
# Matplotlib/Seaborn heatmap
sns.heatmap(data, cbar_kws={'label': 'Correlation Coefficient'})

# Plotly
fig.update_layout(coloraxis_colorbar=dict(title='Frequency'))
```

**3. Meaningful Legends**
- Include legends when multiple data series are plotted
- Use descriptive labels, not just variable names
- Position legends to avoid obscuring data

```python
# Matplotlib
plt.legend(['Control Group', 'Treatment Group'], loc='best')

# Plotly
fig.update_traces(name='Control Group', selector=dict(type='scatter'))
```

**4. Graph Titles and Descriptions**
- ALWAYS suggest a descriptive title to the user
- Titles should be publication-ready (clear, concise, informative)
- Offer to help refine the title for their specific research context

```python
# Good title suggestion workflow:
# 1. Generate graph with a descriptive working title
# 2. Suggest 2-3 alternative titles to the user
# 3. Explain what the graph shows in 1-2 sentences (for figure caption)
```

#### Professional Styling Checklist

When creating ANY visualization, ensure:

- ✓ **Clear axis labels** with units (e.g., "Age (years)", "Temperature (°C)")
- ✓ **Readable font sizes** (minimum 10-12pt for publication)
- ✓ **Appropriate figure size** (not too small, not too large)
- ✓ **High DPI for static images** (minimum 300 DPI for publications)
- ✓ **Color schemes** that are colorblind-friendly when possible
- ✓ **Grid lines** (if they improve readability)
- ✓ **No overlapping text** or cluttered elements
- ✓ **Consistent styling** across all graphs in a project

#### Example: Professional vs Basic Graph

**Basic (AVOID):**
```python
plt.scatter(df['col1'], df['col2'])
plt.savefig('output.png')
```

**Professional (ALWAYS DO):**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set professional style
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6), dpi=300)

# Create plot
plt.scatter(df['age'], df['response_time'], alpha=0.6, s=50)

# Add professional elements
plt.xlabel('Participant Age (years)', fontsize=12)
plt.ylabel('Response Time (seconds)', fontsize=12)
plt.title('Response Time by Participant Age', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# Save with high quality
plt.tight_layout()
plt.savefig('outputs/project/png/age_vs_response.png', dpi=300, bbox_inches='tight')
plt.close()
```

#### Suggesting Titles to Users

After creating a graph, ALWAYS:

1. **Propose a title** based on what the graph shows
2. **Offer alternatives** (e.g., "Would you prefer 'Distribution of Interview Durations' or 'Interview Length Across Participants'?")
3. **Suggest a caption** (e.g., "Figure caption: Scatter plot showing the relationship between participant age and response time (n=45). Pearson correlation r=0.67, p<0.001.")
4. **Ask about context** (e.g., "Is this for a specific section of your paper? I can tailor the title accordingly.")

#### Helper Function Template

When creating visualizations, consider using this template:

```python
def create_professional_plot(data, x_col, y_col, plot_type='scatter',
                            title=None, x_label=None, y_label=None,
                            output_path=None):
    """Create a publication-ready plot with all professional elements."""

    plt.figure(figsize=(8, 6), dpi=300)

    if plot_type == 'scatter':
        plt.scatter(data[x_col], data[y_col], alpha=0.6)
    elif plot_type == 'line':
        plt.plot(data[x_col], data[y_col], linewidth=2)
    # ... other plot types

    # Professional elements
    plt.xlabel(x_label or x_col, fontsize=12)
    plt.ylabel(y_label or y_col, fontsize=12)
    if title:
        plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')

    return plt.gcf()
```

#### Code Documentation and Comments

**CRITICAL:** All generated graph scripts must be **heavily commented** to serve as educational resources for users who may be learning Python and data visualization.

**Three Core Principles:**
1. **Code must work** - Test before providing to users
2. **Follow best practices** - Use pandas DataFrames, avoid hard-coded values, use meaningful variable names
3. **Be human-understandable** - Users should be able to learn from reading the code

**Commenting Guidelines:**

**1. File-Level Documentation**
Every script should start with a comprehensive header:

```python
"""
Graph Generation Script: [Descriptive Title]

Purpose:
    This script creates a [type] plot showing [what the visualization displays].
    Generated for [project name] research project.

Input:
    - CSV file: [filename]
    - Columns used: [list relevant columns]

Output:
    - PNG: outputs/[project]/png/[filename].png (300 DPI, publication-ready)
    - PDF: outputs/[project]/pdf/[filename].pdf (vector format)

Author: Generated by Claude Code
Date: [YYYY-MM-DD]
"""
```

**2. Section Headers**
Break code into logical sections with clear headers:

```python
# =============================================================================
# STEP 1: Load and Prepare Data
# =============================================================================

# =============================================================================
# STEP 2: Create Visualization
# =============================================================================

# =============================================================================
# STEP 3: Customize and Style
# =============================================================================

# =============================================================================
# STEP 4: Save Output
# =============================================================================
```

**3. Inline Comments for Every Major Operation**
Explain WHAT and WHY, not just WHAT:

```python
# Load the CSV data using pandas
# We use UTF-8 encoding to handle French accents (é, è, à, etc.)
df = pd.read_csv('data.csv', encoding='utf-8')

# Remove rows with missing response times
# Missing data can skew correlation analysis
df = df.dropna(subset=['response_time'])

# Create figure with publication-ready size
# 8x6 inches is standard for academic journals, 300 DPI ensures print quality
plt.figure(figsize=(8, 6), dpi=300)
```

**4. Explain Parameters and Choices**
Help users understand why specific values were chosen:

```python
# Alpha=0.6 makes points semi-transparent to show overlapping data
# s=50 sets point size - adjust if you have many/few data points
plt.scatter(df['age'], df['response_time'], alpha=0.6, s=50, color='steelblue')

# Position legend in 'best' location to avoid covering data points
# Try 'upper right', 'lower left', etc. if 'best' doesn't work well
plt.legend(['Control Group', 'Treatment Group'], loc='best', fontsize=10)
```

**5. Educational Notes for Pandas Operations**
Since users may be learning pandas, explain DataFrame operations:

```python
# Filter data to only include participants aged 18-65
# The & operator combines conditions (both must be true)
# Use | for "or" conditions
adult_df = df[(df['age'] >= 18) & (df['age'] <= 65)]

# Group by category and calculate mean response time
# This creates a new DataFrame with category as index and mean values
grouped = df.groupby('category')['response_time'].mean()

# Sort values in descending order to show highest first
# ascending=False means largest to smallest
sorted_data = df.sort_values('response_time', ascending=False)
```

**6. Customization Suggestions**
Provide guidance for users to modify the code:

```python
# === CUSTOMIZATION OPTIONS ===
# Color scheme: Try 'viridis', 'plasma', 'coolwarm', or 'RdYlBu'
# For colorblind-friendly palettes, use 'cividis' or 'colorblind'
cmap = 'coolwarm'

# Figure size: Adjust if needed for your paper layout
# Common sizes: (8,6), (10,6), (12,8)
figsize = (8, 6)

# Font sizes: Increase if text appears too small
title_fontsize = 14
label_fontsize = 12
```

**7. Error Prevention and Debugging Help**
Add comments that help users troubleshoot:

```python
# Check if required columns exist in the DataFrame
required_cols = ['age', 'response_time']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    print(f"Error: Missing columns: {missing_cols}")
    print(f"Available columns: {df.columns.tolist()}")
    exit()

# Display first few rows to verify data loaded correctly
print("Data preview:")
print(df.head())
print(f"\nDataset size: {len(df)} rows, {len(df.columns)} columns")
```

**Complete Example: Professional, Well-Commented Script**

```python
"""
Scatter Plot: Age vs Response Time Analysis

Purpose:
    Creates a scatter plot showing the relationship between participant age
    and response time in the interview study.

Input:
    - CSV file: resources/interview-study/data_Sheet1.csv
    - Columns: age (years), response_time (seconds)

Output:
    - PNG: outputs/interview-study/png/age_vs_response.png (300 DPI)
    - PDF: outputs/interview-study/pdf/age_vs_response.pdf (vector)

Author: Generated by Claude Code
Date: 2025-11-15
"""

# =============================================================================
# STEP 1: Import Required Libraries
# =============================================================================

import pandas as pd  # For data manipulation and analysis
import matplotlib.pyplot as plt  # For creating static visualizations
import seaborn as sns  # For enhanced styling and statistical plots
import numpy as np  # For numerical operations

# Set seaborn style for professional-looking plots
# Other styles: 'darkgrid', 'white', 'dark', 'ticks'
sns.set_style("whitegrid")

# =============================================================================
# STEP 2: Load and Prepare Data
# =============================================================================

# Load CSV data with UTF-8 encoding for international characters
data_path = 'resources/interview-study/data_Sheet1.csv'
df = pd.read_csv(data_path, encoding='utf-8')

# Display data summary for verification
print("Data loaded successfully!")
print(f"Dataset size: {len(df)} participants\n")
print("First 5 rows:")
print(df.head())
print("\nColumn names and types:")
print(df.dtypes)

# Remove rows with missing values in key columns
# This ensures clean data for analysis
df = df.dropna(subset=['age', 'response_time'])
print(f"\nAfter removing missing values: {len(df)} participants")

# =============================================================================
# STEP 3: Create Visualization
# =============================================================================

# Create figure with publication-ready dimensions
# 8x6 inches is standard for journals, 300 DPI ensures print quality
plt.figure(figsize=(8, 6), dpi=300)

# Create scatter plot
# - x-axis: participant age
# - y-axis: response time
# - alpha=0.6: semi-transparent to show overlapping points
# - s=50: point size (increase for emphasis, decrease if crowded)
# - color='steelblue': professional blue color (try 'coral', 'forestgreen', etc.)
plt.scatter(df['age'], df['response_time'],
           alpha=0.6, s=50, color='steelblue', edgecolors='navy')

# =============================================================================
# STEP 4: Add Professional Elements
# =============================================================================

# Add descriptive axis labels with units
# Always include units in parentheses for clarity
plt.xlabel('Participant Age (years)', fontsize=12, fontweight='bold')
plt.ylabel('Response Time (seconds)', fontsize=12, fontweight='bold')

# Add informative title
# Keep titles concise but descriptive
plt.title('Response Time by Participant Age', fontsize=14, fontweight='bold', pad=20)

# Add subtle grid for easier reading
# alpha=0.3 makes gridlines subtle, not distracting
plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# Optional: Add trend line to show correlation
# Uncomment the following lines to add a linear regression line:
# z = np.polyfit(df['age'], df['response_time'], 1)
# p = np.poly1d(z)
# plt.plot(df['age'], p(df['age']), "r--", alpha=0.8, label='Trend line')
# plt.legend(fontsize=10)

# =============================================================================
# STEP 5: Finalize and Save
# =============================================================================

# Apply tight layout to prevent label cutoff
# This automatically adjusts spacing to fit all elements
plt.tight_layout()

# Save as PNG (high resolution for papers/presentations)
output_png = 'outputs/interview-study/png/age_vs_response.png'
plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\nSaved PNG: {output_png}")

# Save as PDF (vector format, infinitely scalable)
output_pdf = 'outputs/interview-study/pdf/age_vs_response.pdf'
plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')
print(f"Saved PDF: {output_pdf}")

# Close the plot to free memory
# Important when generating multiple plots in sequence
plt.close()

print("\n✓ Graph created successfully!")
print("\nNext steps:")
print("1. Review the graph to ensure it meets your needs")
print("2. Adjust colors, sizes, or labels by editing this script")
print("3. Run this script again after making changes")
```

**When Writing Comments:**
- ✓ Explain WHY choices are made, not just WHAT the code does
- ✓ Provide alternative values users can try
- ✓ Include units and context
- ✓ Add educational notes about pandas/matplotlib concepts
- ✓ Suggest customization options
- ✓ Help users debug with informative print statements
- ✗ Don't state the obvious (e.g., "# import pandas" is not helpful)
- ✗ Don't assume users know technical jargon - explain it

**Remember:** These scripts are learning tools. A well-commented script helps users:
- Understand how their data was processed
- Modify the visualization for their specific needs
- Learn Python and data visualization best practices
- Build confidence to create their own scripts

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

### Custom Slash Commands

This project includes custom Claude Code slash commands to streamline common workflows:

#### `/pro-graph` - Professional Publication-Ready Graphs

**Purpose:** Generate publication-quality visualizations with all required professional elements.

**What it does:**
- Guides the creation of graphs meeting academic publication standards
- Ensures all mandatory elements are included (axis labels, legends, colorbars)
- Suggests multiple title options for the user to choose from
- Drafts publication-ready figure captions
- Applies professional styling (300 DPI, readable fonts, proper sizing)
- Saves to the appropriate project output directory

**When to use:**
- User asks for any graph/visualization from their data
- User mentions "publication", "paper", "article", or "thesis"
- User wants a "professional" or "good-looking" graph
- You're creating any visualization (always prefer professional standards)

**Example usage:**
```
User: "Create a scatter plot of age vs response time from my data"
Claude: [Invokes /pro-graph slash command]
```

The command will guide you through creating a professional graph with proper labels, titles, and styling.

## Important Implementation Notes

### When Creating Visualizations
1. **ALWAYS follow Professional Visualization Standards** (see section above)
   - Include axis labels with units
   - Add colorbar labels when applicable
   - Create meaningful legends
   - Suggest publication-ready titles and captions to the user
2. Check if the data contains the required columns
3. Handle missing data gracefully with clear error messages
4. Support both French and English column names when reasonable
5. Auto-detect project context from file paths to organize outputs properly
6. Consider using the `/pro-graph` slash command for guided professional graph creation

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
