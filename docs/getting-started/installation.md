# Installation

## Requirements

- Python 3.10 or higher

## Install from PyPI

```bash
pip install collagraph
```

## Optional Dependencies

Collagraph supports multiple rendering backends. Install the ones you need:

### PySide6 (Qt Desktop Applications)

```bash
pip install collagraph[pyside]
```

Or install PySide6 separately:

```bash
pip install PySide6>=6.6.2
```

### Pygfx (3D Graphics)

```bash
pip install collagraph[pygfx]
```

Or install pygfx separately:

```bash
pip install pygfx>=0.13.0
```

### All Optional Dependencies

```bash
pip install collagraph[all]
```

## Development Installation

If you want to contribute to Collagraph or modify the source code:

```bash
git clone https://github.com/berendkleinhaneveld/collagraph.git
cd collagraph
pip install -e ".[dev]"
```

## Verify Installation

```python
import collagraph as cg
print(cg.__version__)
```

## Editor Setup

### Syntax Highlighting

For `.cgx` (Collagraph single-file component) files:

#### VS Code
Install the [Collagraph extension](https://marketplace.visualstudio.com/items?itemName=berendkleinhaneveld.collagraph)

#### Sublime Text
See the [collagraph-sublime](https://github.com/berendkleinhaneveld/collagraph-sublime) repository

### Linting

Install `ruff-cgx` for linting `.cgx` files:

```bash
pip install ruff-cgx
```

## Next Steps

- [Quick Start Guide](quick-start.md)
- [Your First Component](first-component.md)
