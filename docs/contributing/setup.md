# Development Setup

This guide will help you set up your development environment for contributing to Collagraph.

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Git

## Quick Start

```bash
# Clone the repository
git clone https://github.com/fork-tongue/collagraph.git
cd collagraph

# Basic dev setup (no pygfx or pyside)
uv sync

# Full dev setup (includes all optional dependencies)
uv sync --all-groups

# Install pre-commit hooks
uv run pre-commit install
```

## Installation Options

Collagraph uses [uv](https://docs.astral.sh/uv/) for dependency management. There are several installation options depending on what you're working on:

### Basic Development Setup

For working on the core framework without renderer-specific features:

```bash
uv sync --group dev
```

This installs:
- `observ` (core reactivity library)
- Development tools: `ruff`, `pytest`, `pytest-cov`, `pre-commit`, `twine`

### PySide Development

For working on PySide6 renderer features:

```bash
uv sync --group dev --group pyside --group pyside-dev
```

This additionally installs:
- `PySide6` (Qt bindings)
- `pytest-qt` (Qt testing support)
- `pytest-xvfb` (headless testing)

Note: PySide6 6.8.3 and 6.9.0 are excluded due to known issues.

### Pygfx Development

For working on Pygfx renderer features:

```bash
uv sync --group dev --group pygfx
```

This additionally installs:
- `pygfx` (3D graphics library)

### Full Installation

To install everything:

```bash
uv sync --all-groups
```

## Running Examples

After installation, you can run examples to verify your setup:

```bash
# Using the CLI (for .cgx files)
uv run collagraph examples/pyside/counter.cgx

# Using Python directly
uv run python examples/pyside/layout_example.cgx
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest -v --cov=collagraph --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_component.py

# Run tests matching a pattern
uv run pytest -k "test_directive"
```

For PySide tests, you may need to set the Qt platform:

```bash
QT_QPA_PLATFORM=offscreen uv run pytest tests/pyside/
```

## Pre-commit Hooks

Pre-commit hooks ensure code quality before committing. Install them with:

```bash
uv run pre-commit install
```

The hooks will automatically run:
1. **Linting** - `ruff check` to catch code issues
2. **Formatting** - `ruff format --check` to ensure consistent style
3. **Tests** - `pytest` to ensure tests pass

You can manually run the hooks on all files:

```bash
uv run pre-commit run --all-files
```

## Development Tools

### Ruff

Collagraph uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Check for linting issues
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check formatting without changes
uv run ruff format --check .
```

### Pytest

Test suite is built with pytest. Key plugins:
- `pytest-cov` - Code coverage reporting
- `pytest-qt` - PySide6 testing support
- `pytest-xvfb` - Headless display for GUI tests

## Editor Setup

### VS Code

For `.cgx` (Single-File Component) syntax highlighting, install the [Collagraph LSP for VSCode](https://github.com/fork-tongue/collagraph-lsp-vscode).

Recommended settings (`.vscode/settings.json`):

```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "none",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": true,
      "source.organizeImports": true
    }
  }
}
```

### Sublime Text

For `.cgx` syntax highlighting, install the [Collagraph LSP for Sublime Text](https://github.com/fork-tongue/collagraph-lsp-sublime).

### Formatting .cgx Files

Use [ruff-cgx](https://github.com/fork-tongue/ruff-cgx) to format and lint `.cgx` files:

```bash
pip install ruff-cgx
ruff-cgx format mycomponent.cgx
ruff-cgx check mycomponent.cgx
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you've installed the correct dependency groups:

```bash
# Check what's installed
uv pip list

# Reinstall dependencies
uv sync --all-groups
```

### PySide6 Issues

If PySide6 tests fail, ensure you have the correct version and Qt platform set:

```bash
# Check version
uv run python -c "import PySide6; print(PySide6.__version__)"

# Run with offscreen rendering
QT_QPA_PLATFORM=offscreen uv run pytest tests/pyside/
```

### Pre-commit Hook Failures

If pre-commit hooks fail, you can:

```bash
# Run individual checks
uv run ruff check .
uv run ruff format --check .
uv run pytest

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

## See Also

- [Testing Guidelines](testing.md)
- [Code Style Guide](code-style.md)
