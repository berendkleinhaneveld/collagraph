# Installation

## Requirements

- Python 3.10 or higher

## Install from PyPI

### Using pip

```bash
pip install collagraph
```

### Using uv

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver:

```bash
uv pip install collagraph
```

Or use uv to run Collagraph apps directly without installing:

```bash
uv run collagraph your-app.cgx
```

## Optional Dependencies

Collagraph supports multiple rendering backends. Install the ones you need:

### PySide6 (Qt Desktop Applications)

**With pip:**
```bash
pip install collagraph[pyside]
```

**With uv:**
```bash
uv pip install collagraph[pyside]
```

Or install PySide6 separately:
```bash
pip install PySide6>=6.6.2
# or
uv pip install PySide6>=6.6.2
```

### Pygfx (3D Graphics)

**With pip:**
```bash
pip install collagraph[pygfx]
```

**With uv:**
```bash
uv pip install collagraph[pygfx]
```

Or install pygfx separately:
```bash
pip install pygfx>=0.13.0
# or
uv pip install pygfx>=0.13.0
```

### Multiple Backends

To install multiple backends:

```bash
pip install collagraph[pyside,pygfx]
# or
uv pip install collagraph[pyside,pygfx]
```

## Install from Source

For the latest development version or to contribute to Collagraph:

### Clone and Install

```bash
git clone https://github.com/fork-tongue/collagraph.git
cd collagraph
pip install -e .
```

### Development Installation

**With pip:**
```bash
git clone https://github.com/fork-tongue/collagraph.git
cd collagraph
pip install -e ".[dev]"
```

**With uv (recommended for development):**
```bash
git clone https://github.com/fork-tongue/collagraph.git
cd collagraph
# Basic development setup (without renderers)
uv sync
# Or with all optional dependencies
uv sync --all-groups
```

The `uv sync` command:
- Creates a virtual environment automatically
- Installs the package in editable mode
- Installs development dependencies (pytest, ruff, pre-commit, etc.)
- `--all-groups` includes PySide6 and pygfx dependencies

## Verify Installation

Test that Collagraph is installed correctly:

```python
import collagraph as cg
print(cg.__version__)
```

Or run a simple test from the command line:

```bash
python -c "import collagraph as cg; print(f'Collagraph {cg.__version__} installed successfully')"
```

### Verify Renderers

**PySide6:**
```python
from collagraph.renderers import PySideRenderer
print("PySide6 renderer available")
```

**Pygfx:**
```python
from collagraph.renderers import PygfxRenderer
print("Pygfx renderer available")
```

## Editor Setup

### Syntax Highlighting

For `.cgx` (Collagraph single-file component) files:

#### VS Code
Install the [Collagraph extension](https://marketplace.visualstudio.com/items?itemName=berendkleinhaneveld.collagraph) from the VS Code marketplace:

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "Collagraph"
4. Click Install

Or install from command line:
```bash
code --install-extension berendkleinhaneveld.collagraph
```

#### Sublime Text
See the [collagraph-sublime](https://github.com/fork-tongue/cgx-syntax-highlight-sublime) repository for installation instructions.

### Linting and Formatting

Install `ruff-cgx` for linting and formatting `.cgx` files:

```bash
pip install ruff-cgx
# or
uv pip install ruff-cgx
```

This enables Ruff to work with `.cgx` files, providing linting and formatting for both the template and script sections.

## Troubleshooting

### Import Errors

If you see `ImportError: No module named 'collagraph'`, ensure:
- Collagraph is installed in your active Python environment
- You're using the correct Python interpreter
- Your virtual environment is activated (if using one)

### PySide6 Not Found

If running a PySide app fails:
```bash
# Install PySide6 extra
pip install collagraph[pyside]
# or verify PySide6 is installed
python -c "import PySide6; print(PySide6.__version__)"
```

### .cgx Files Not Running

Ensure you're using the Collagraph CLI or have proper import hooks set up:
```bash
python -m collagraph your-app.cgx
```

### Permission Errors on Linux

If you encounter permission errors when running GUI apps:
```bash
# May need display server access
export DISPLAY=:0
```

## Next Steps

Now that Collagraph is installed, you're ready to build your first app:

- **[Quick Start Guide](quick-start.md)** - Build your first Collagraph app in minutes
- **[Your First Component](first-component.md)** - Learn component basics
- **[Project Structure](project-structure.md)** - Organize your Collagraph projects
- **[Template Syntax](../core-concepts/template-syntax.md)** - Master the `.cgx` template syntax
- **[Examples](../../examples/)** - Explore example applications
