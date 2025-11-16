# Contributing to Excel to Graph

Thank you for your interest in contributing! This document provides guidelines for developers.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- WSL (if on Windows)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone git@github.com:MaxenceBouvier/ez_excel_graph.git excel_to_graph
   cd excel_to_graph
   ```

2. **Run the setup scripts**
   ```bash
   # Setup Python environment and dependencies
   ./scripts/setup_python.sh

   # Setup development tools (pre-commit, linters, etc.)
   ./scripts/dev_setup.sh
   ```

3. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
   ```

You're ready to develop!

## Development Workflow

### Code Quality Tools

We use several tools to maintain code quality:

- **Black**: Code formatter
- **Ruff**: Fast Python linter
- **mypy**: Static type checker
- **pre-commit**: Git hook framework

These run automatically on `git commit` thanks to pre-commit hooks.

### Running Tools Manually

```bash
# Format code with Black
black src/

# Lint with Ruff
ruff check src/
ruff check src/ --fix  # Auto-fix issues

# Type check with mypy
mypy src/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/excel_to_graph --cov-report=term-missing

# Run specific test file
pytest tests/test_utils.py

# Run with verbose output
pytest -v
```

### Adding New Features

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run quality checks**
   ```bash
   black src/
   ruff check src/ --fix
   mypy src/
   pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```
   Pre-commit hooks will run automatically!

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Testing Guidelines

- Write tests for new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow the existing test structure

### Test Structure

```
tests/
├── __init__.py
├── test_utils.py       # Utility function tests
├── test_reader.py      # Excel reader tests (add as needed)
├── test_converter.py   # Converter tests (add as needed)
└── test_cli.py         # CLI tests (add as needed)
```

## Continuous Integration

We use GitHub Actions for CI/CD:

- **Lint job**: Checks code formatting and linting
- **Test job**: Runs tests on Python 3.10, 3.11, 3.12
- **Build job**: Verifies package builds correctly

CI runs automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

View the CI configuration in `.github/workflows/ci.yml`

## Code Style

- Follow PEP 8 (enforced by Black and Ruff)
- Use type hints where appropriate
- Write docstrings for public functions
- Keep functions focused and small
- Use descriptive variable names

### Docstring Format

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When and why this is raised

    Examples:
        >>> my_function("test", 42)
        True
    """
    pass
```

## Git Commit Messages

Use clear, descriptive commit messages:

```
Add: New feature description
Fix: Bug description
Update: What was updated and why
Refactor: What was refactored
Docs: Documentation changes
Test: Test additions or changes
```

## Pre-commit Hooks

The following hooks run on every commit:

- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with newline
- **check-yaml/json/toml**: Validates config files
- **black**: Formats Python code
- **ruff**: Lints Python code
- **mypy**: Type checks Python code

If hooks fail, the commit is blocked. Fix the issues and commit again.

### Skipping Hooks (Not Recommended)

Only in rare cases:
```bash
git commit --no-verify
```

## Project Structure

```
excel_to_graph/
├── .github/workflows/    # CI/CD configurations
├── scripts/              # Setup and utility scripts
├── src/excel_to_graph/   # Main package code
├── tests/                # Test files
├── resources/            # Excel file storage (git-ignored)
├── outputs/              # Generated graphs (git-ignored)
└── docs/                 # Documentation (future)
```

## Questions?

- Open an issue on GitHub
- Check existing issues and PRs
- Read the main README.md

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
