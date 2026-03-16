# Testing Guidelines

Collagraph uses pytest for testing. This guide covers how to write and run tests for the project.

## Running Tests

### Basic Test Execution

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_component.py

# Run tests matching a pattern
uv run pytest -k "test_directive"

# Run tests in a specific directory
uv run pytest tests/pyside/
```

### Coverage Reporting

```bash
# Run with coverage
uv run pytest --cov=collagraph --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov=collagraph --cov-report=html

# View coverage report
open htmlcov/index.html
```

### PySide6 Tests

PySide6 tests require a display. Use offscreen rendering in headless environments:

```bash
QT_QPA_PLATFORM=offscreen uv run pytest tests/pyside/
```

## Test Structure

### Directory Layout

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── data/                    # Test data files
│   └── *.cgx               # Sample .cgx files for testing
├── pyside/                  # PySide-specific tests
│   └── test_*.py
├── test_component.py        # Component tests
├── test_directive_*.py      # Directive tests
├── test_fragment.py         # Fragment tests
└── test_sfc_*.py           # Single-file component tests
```

### File Naming

- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

Example:

```python
# tests/test_component.py

def test_component_initialization():
    """Test that components initialize correctly."""
    pass

class TestComponentLifecycle:
    def test_mounted_hook(self):
        """Test that mounted() hook is called."""
        pass
```

## Writing Tests

### Basic Test Structure

```python
import collagraph as cg

def test_component_state():
    """Test component state management."""
    class Counter(cg.Component):
        def init(self):
            self.state["count"] = 0

        def render(self, renderer):
            return renderer.h("div")

    component = Counter()
    assert component.state["count"] == 0
    component.state["count"] += 1
    assert component.state["count"] == 1
```

### Using Fixtures

Common fixtures are defined in `conftest.py`:

```python
def test_with_parse_source(parse_source):
    """Test using the parse_source fixture."""
    Item, _ = parse_source("""
        <item />

        <script>
        import collagraph as cg

        class Item(cg.Component):
            pass
        </script>
    """)

    gui = cg.Collagraph(cg.DictRenderer(), event_loop_type=cg.EventLoopType.SYNC)
    container = {"type": "root"}
    gui.render(Item, container)
```

### Available Fixtures

#### `parse_source`

Parses a CGX template string and returns the component class:

```python
def test_component_rendering(parse_source):
    Counter, _ = parse_source("""
        <div>Count: {{ count }}</div>

        <script>
        import collagraph as cg

        class Counter(cg.Component):
            def init(self):
                self.state["count"] = 0
        </script>
    """)
```

#### `process_events`

Runs the asyncio event loop for testing reactive updates:

```python
def test_reactive_updates(parse_source, process_events):
    # ... setup component ...
    component.state["count"] = 1
    process_events()  # Process reactive updates
    # ... assert changes ...
```

#### `cleanup` (autouse)

Automatically cleans up between tests:
- Clears the observ scheduler
- Resets the proxy database
- Runs garbage collection

## Testing Components

### Testing Component Initialization

```python
def test_component_props(parse_source):
    """Test that props are passed correctly."""
    Item, _ = parse_source("""
        <item />

        <script>
        import collagraph as cg

        class Item(cg.Component):
            pass
        </script>
    """)

    component = Item({"name": "test"})
    assert component.props["name"] == "test"
```

### Testing Lifecycle Hooks

```python
def test_mounted_hook(parse_source):
    """Test that mounted() hook is called."""
    mounted_called = False

    Item, _ = parse_source("""
        <item />

        <script>
        import collagraph as cg

        class Item(cg.Component):
            def mounted(self):
                self.state["mounted"] = True
        </script>
    """)

    gui = cg.Collagraph(cg.DictRenderer(), event_loop_type=cg.EventLoopType.SYNC)
    container = {"type": "root"}
    gui.render(Item, container)

    # Access the component to check state
    fragment = gui.fragment
    assert fragment.component.state.get("mounted") == True
```

### Testing State and Reactivity

```python
def test_reactive_state(parse_source, process_events):
    """Test that state changes trigger updates."""
    Item, _ = parse_source("""
        <div :text="count" />

        <script>
        import collagraph as cg

        class Item(cg.Component):
            def init(self):
                self.state["count"] = 0
        </script>
    """)

    gui = cg.Collagraph(cg.DictRenderer(), event_loop_type=cg.EventLoopType.SYNC)
    container = {"type": "root"}
    gui.render(Item, container)

    # Get the rendered element
    div = container["children"][0]
    assert div["text"] == 0

    # Update state
    gui.fragment.component.state["count"] = 1
    process_events()

    assert div["text"] == 1
```

## Testing Directives

### v-if Directive

```python
def test_directive_if(parse_source, process_events):
    """Test v-if conditional rendering."""
    Item, _ = parse_source("""
        <div v-if="show">Visible</div>

        <script>
        import collagraph as cg

        class Item(cg.Component):
            def init(self):
                self.state["show"] = True
        </script>
    """)

    gui = cg.Collagraph(cg.DictRenderer(), event_loop_type=cg.EventLoopType.SYNC)
    container = {"type": "root"}
    gui.render(Item, container)

    assert len(container["children"]) == 1

    gui.fragment.component.state["show"] = False
    process_events()

    assert len(container["children"]) == 0
```

### v-for Directive

```python
def test_directive_for(parse_source):
    """Test v-for list rendering."""
    Item, _ = parse_source("""
        <div v-for="item in items">{{ item }}</div>

        <script>
        import collagraph as cg

        class Item(cg.Component):
            def init(self):
                self.state["items"] = ["a", "b", "c"]
        </script>
    """)

    gui = cg.Collagraph(cg.DictRenderer(), event_loop_type=cg.EventLoopType.SYNC)
    container = {"type": "root"}
    gui.render(Item, container)

    assert len(container["children"]) == 3
```

## Testing Renderers

### Using DictRenderer

`DictRenderer` is the test renderer that outputs Python dictionaries:

```python
def test_renderer_create_element():
    """Test renderer element creation."""
    renderer = cg.DictRenderer()
    element = renderer.create_element("div")

    assert element["type"] == "div"
    assert element["children"] == []
```

### Testing Custom Renderers

```python
def test_custom_renderer():
    """Test custom renderer implementation."""
    class MyRenderer(cg.Renderer):
        def create_element(self, type):
            return {"tag": type}

        def create_text_element(self):
            return {"tag": "text"}

        # ... implement other required methods ...

    renderer = MyRenderer()
    element = renderer.create_element("button")
    assert element["tag"] == "button"
```

### Testing PySide Renderer

```python
# tests/pyside/test_renderer.py
import pytest
from PySide6 import QtWidgets

def test_pyside_renderer(qtbot):
    """Test PySide renderer with Qt test bot."""
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    Item, _ = parse_source("""
        <widget>
            <label text="Hello" />
        </widget>

        <script>
        import collagraph as cg

        class Item(cg.Component):
            pass
        </script>
    """)

    gui = cg.Collagraph(cg.PySideRenderer())
    widget = QtWidgets.QWidget()
    gui.render(Item, widget)

    # Use qtbot for Qt-specific testing
    qtbot.addWidget(widget)
```

## Testing Single-File Components

### Compilation Tests

```python
def test_sfc_compilation():
    """Test that .cgx files compile correctly."""
    from collagraph.sfc import load_from_string

    source = """
        <div>Hello</div>

        <script>
        import collagraph as cg

        class Hello(cg.Component):
            pass
        </script>
    """

    Hello, namespace = load_from_string(source)
    assert Hello is not None
    assert issubclass(Hello, cg.Component)
```

### Import Tests

```python
def test_sfc_import():
    """Test importing .cgx files."""
    # Assumes test file exists at tests/data/simple.cgx
    from tests.data.simple import Simple

    assert issubclass(Simple, cg.Component)
```

## Parametrized Tests

Use `pytest.mark.parametrize` for testing multiple cases:

```python
@pytest.mark.parametrize("attr", ["props", "state", "element", "parent"])
def test_component_no_override(parse_source, attr):
    """Test that component attributes cannot be overridden."""
    Item, _ = parse_source(f"""
        <item />

        <script>
        import collagraph as cg

        class Item(cg.Component):
            def init(self):
                self.{attr} = {{}}
        </script>
    """)

    gui = cg.Collagraph(cg.DictRenderer(), event_loop_type=cg.EventLoopType.SYNC)
    container = {"type": "root"}

    with pytest.raises(RuntimeError):
        gui.render(Item, container)
```

## Test Assertions

### Common Assertions

```python
# Equality
assert actual == expected

# Containment
assert "key" in dictionary
assert element in list

# Type checking
assert isinstance(obj, Component)

# Exceptions
with pytest.raises(ValueError):
    do_something()

# Approximate equality (for floats)
assert actual == pytest.approx(expected)
```

### Custom Assertions

```python
def assert_rendered_correctly(container, expected_children):
    """Custom assertion for rendered output."""
    actual = len(container["children"])
    expected = expected_children
    assert actual == expected, f"Expected {expected} children, got {actual}"
```

## Coverage Requirements

### Current Coverage

Coverage configuration is in `.coveragerc`:

```ini
[run]
omit =
    collagraph/renderers/dom_renderer.py
```

### Coverage Goals

- Aim for 80%+ coverage on new code
- Core components and fragments: 90%+ coverage
- Test both success and failure paths
- Test edge cases and boundary conditions

### Checking Coverage

```bash
# Run tests with coverage
uv run pytest --cov=collagraph --cov-report=term-missing

# View uncovered lines
uv run pytest --cov=collagraph --cov-report=html
open htmlcov/index.html
```

## Debugging Tests

### Using pytest Options

```bash
# Stop on first failure
pytest -x

# Enter debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l

# Increase verbosity
pytest -vv
```

### Print Debugging

```python
def test_with_debug_output():
    """Test with debug output."""
    component = create_component()

    # pytest captures output, use -s to see it
    print(f"Component state: {component.state}")

    assert component.state["key"] == "value"
```

Run with: `pytest -s tests/test_file.py`

### CGX Debugging

Enable CGX debug mode:

```bash
CGX_DEBUG=1 pytest tests/test_sfc_*.py
```

## Best Practices

### DO

- Test one thing per test function
- Use descriptive test names
- Clean up resources (handled by `cleanup` fixture)
- Test edge cases and error conditions
- Use fixtures for common setup
- Test public APIs, not implementation details

### DON'T

- Test multiple unrelated things in one test
- Rely on test execution order
- Use global state
- Skip cleanup
- Test private methods directly (test through public API)
- Commit failing tests

## See Also

- [Development Setup](setup.md)
- [Testing Guide](../guides/testing.md)
