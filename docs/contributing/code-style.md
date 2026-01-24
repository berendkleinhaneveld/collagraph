# Code Style Guide

Collagraph follows Python best practices and uses automated tools to maintain code quality and consistency.

## Python Style Guidelines

We follow [PEP 8](https://peps.python.org/pep-0008/) with some project-specific conventions enforced by ruff.

### General Principles

- Write clear, readable code over clever code
- Use descriptive variable names
- Keep functions focused and small
- Prefer explicit over implicit
- Follow the existing codebase patterns

## Using Ruff

[Ruff](https://docs.astral.sh/ruff/) is our primary tool for both linting and formatting. It's fast, comprehensive, and configured in `pyproject.toml`.

### Running Ruff

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

### Ruff Configuration

Our ruff configuration (from `pyproject.toml`):

```toml
[tool.ruff.lint]
select = [
    "E4",   # Import errors
    "E5",   # Line length and whitespace
    "E7",   # Statement errors
    "E9",   # Runtime errors
    "F",    # Pyflakes (undefined names, unused imports)
    "I",    # isort (import sorting)
    "N",    # pep8-naming
    "T10",  # flake8-debugger (no debugger statements)
    "T20",  # flake8-print (no print statements)
    "RUF",  # Ruff-specific rules
]
```

### Per-File Ignores

Some files have specific exceptions:

- **Examples**: Relaxed naming rules (`N999`, `N802`)
- **Tests**: Relaxed variable naming (`N806`, `N802`)
- **`__init__.py`**: Allows specific import patterns (`F401`, `I001`, `E402`)

These are configured in `pyproject.toml` under `tool.ruff.lint.per-file-ignores`.

## Formatting Standards

### Line Length

- Maximum line length: **88 characters** (Black's default)
- Ruff will automatically format to this length

### Imports

Imports are automatically sorted by ruff using isort-compatible rules:

```python
# Standard library imports
from __future__ import annotations
import sys
from pathlib import Path

# Third-party imports
from observ import reactive, computed

# Local imports
from collagraph.component import Component
from collagraph.fragment import Fragment
```

### Quotes

- Use double quotes for strings: `"hello"`
- Ruff will automatically normalize quotes

### Whitespace

- 2 blank lines between top-level definitions
- 1 blank line between methods in a class
- No trailing whitespace

## Naming Conventions

Follow PEP 8 naming conventions:

### Variables and Functions

```python
# Good
user_name = "Alice"
def calculate_total(items):
    pass

# Bad
UserName = "Alice"  # Should be lowercase
def CalculateTotal(items):  # Should be lowercase
    pass
```

### Classes

```python
# Good
class Component:
    pass

class PySideRenderer:
    pass

# Bad
class component:  # Should be PascalCase
    pass
```

### Constants

```python
# Good
MAX_RETRIES = 3
EVENT_LOOP_TYPE = "default"

# Bad
maxRetries = 3  # Should be UPPER_CASE
```

### Private Members

```python
class Component:
    def __init__(self):
        self._state = {}      # Internal, may change
        self.__private = {}   # Name-mangled private
        self.public = {}      # Public API
```

### Module Names

- Use lowercase with underscores: `pyside_renderer.py`
- For packages: `__init__.py`

## Type Hints

Use type hints for function signatures and complex variables:

```python
from __future__ import annotations

from typing import Any, Callable

def create_element(self, type: str) -> Any:
    """Create an element of the given type."""
    pass

def mount(self, target: Any, anchor: Any | None = None) -> None:
    """Mount the fragment to a target."""
    pass
```

### Future Annotations

Always include `from __future__ import annotations` at the top of files to enable:
- Forward references without quotes
- Better IDE support
- Deferred annotation evaluation

### TYPE_CHECKING

Use `TYPE_CHECKING` to avoid circular imports:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collagraph.fragment import ComponentFragment
    from collagraph.renderers import Renderer
```

### Generic Types

```python
from collections.abc import Callable

# Good
def watch(self, callback: Callable[[Any], None]) -> None:
    pass

# Bad - using old typing module
from typing import Callable  # Use collections.abc instead
```

## Documentation Strings

### Docstring Style

We use concise docstrings following PEP 257:

```python
def mount(self, target):
    """Mount the fragment to the target element.

    This creates the DOM elements and inserts them into the
    target container, then calls lifecycle hooks.
    """
    pass
```

### When to Document

- All public classes and their methods
- All public functions
- Complex algorithms or non-obvious logic
- Public API surfaces

### What to Include

```python
def render(
    self,
    component_class: Callable[[dict], Component],
    target: Any,
    state: dict | None = None,
):
    """Render a component into a target element.

    Args:
        component_class: The component class to instantiate
        target: DOM element/instance to render into
        state: Initial state passed as top-level props
    """
    pass
```

## Comments

### Inline Comments

Use sparingly and only when the code alone isn't clear:

```python
# Good - explains why
# Work around PySide6 bug in versions 6.8.3 and 6.9.0
if version not in ["6.8.3", "6.9.0"]:
    pass

# Bad - explains what (obvious from code)
# Increment counter by 1
counter += 1
```

### TODO Comments

Format TODO comments with context:

```python
# TODO: Cache component parent to avoid repeated traversal
# TODO(username): Add support for async lifecycle hooks
```

## Code Organization

### File Structure

```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library imports
import sys
from pathlib import Path

# 3. Third-party imports
from observ import reactive

# 4. Local imports
from collagraph.component import Component

# 5. TYPE_CHECKING imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from collagraph.fragment import Fragment

# 6. Constants
DIRECTIVE_PREFIX = "v-"

# 7. Classes and functions
class MyClass:
    pass
```

### Class Organization

```python
class Component:
    # 1. Class variables
    __lookup_cache__: ClassVar = defaultdict(dict)

    # 2. __init__ and initialization
    def __init__(self):
        pass

    # 3. Properties
    @property
    def state(self):
        pass

    # 4. Public methods
    def render(self):
        pass

    # 5. Private methods
    def _lookup(self):
        pass
```

## Anti-Patterns to Avoid

### Don't Use Print Statements

```python
# Bad
print("Debug info")

# Good
import logging
logger.debug("Debug info")
```

### Don't Leave Debugging Code

```python
# Bad
import pdb; pdb.set_trace()
breakpoint()

# Good - Remove before committing
# (pre-commit hooks will catch this)
```

### Don't Use Mutable Default Arguments

```python
# Bad
def __init__(self, props={}):
    pass

# Good
def __init__(self, props=None):
    self._props = props if props is not None else {}
```

### Don't Override Built-ins

```python
# Bad
def filter(list, type):  # 'filter' and 'list' are built-ins
    pass

# Good
def filter_items(items, item_type):
    pass
```

## Pre-commit Integration

The pre-commit hooks automatically enforce these standards:

```yaml
# .pre-commit-config.yaml
- id: lint
  entry: uv run ruff check

- id: format
  entry: uv run ruff format --check
```

Run manually:

```bash
uv run pre-commit run --all-files
```

## See Also

- [Development Setup](setup.md)
- [Pull Request Process](pull-requests.md)
