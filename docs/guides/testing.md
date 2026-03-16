# Testing Components

This comprehensive guide covers testing Collagraph components using pytest and the DictRenderer, from simple unit tests to complex integration scenarios.

## Overview

Testing Collagraph components involves:
- **Unit tests** - Test individual components in isolation
- **Integration tests** - Test component interactions
- **Event testing** - Verify event handlers work correctly
- **State testing** - Ensure reactive state behaves as expected
- **Lifecycle testing** - Test lifecycle hook execution

The **DictRenderer** is the key to testing - it renders components to simple Python dictionaries instead of actual UI, making tests fast and deterministic.

## Setting Up Testing

### Install pytest

```bash
pip install pytest pytest-cov
```

### Basic Test Structure

**tests/test_counter.py:**
```python
import pytest
import collagraph as cg
from collagraph.sfc import load_from_string

def test_counter_initial_state():
    """Test counter starts at 0"""
    # Load component from string
    Counter, _ = load_from_string("""
        <widget>
          <label :text="f'Count: {count}'" />
          <button text="Increment" @clicked="increment" />
        </widget>

        <script>
        import collagraph as cg

        class Counter(cg.Component):
            def init(self):
                self.state["count"] = 0

            def increment(self):
                self.state["count"] += 1
        </script>
    """)

    # Create GUI with DictRenderer
    gui = cg.Collagraph(
        cg.DictRenderer(),
        event_loop_type=cg.EventLoopType.SYNC
    )

    # Render component
    container = {"type": "root"}
    gui.render(Counter, container)

    # Get rendered DOM
    dom = container["children"][0]

    # Assert structure
    assert dom["type"] == "widget"
    assert len(dom["children"]) == 2

    # Check label text
    label = dom["children"][0]
    assert label["type"] == "label"
    assert label["attrs"]["text"] == "Count: 0"
```

## Using pytest Fixtures

### Common Fixtures

**tests/conftest.py:**
```python
import pytest
import collagraph as cg
from collagraph.sfc import load_from_string
import textwrap

@pytest.fixture
def gui():
    """Create Collagraph instance with DictRenderer"""
    return cg.Collagraph(
        cg.DictRenderer(),
        event_loop_type=cg.EventLoopType.SYNC
    )

@pytest.fixture
def container():
    """Create container for rendering"""
    return {"type": "root"}

@pytest.fixture
def load_component():
    """Helper to load component from string"""
    def _load(source):
        source = textwrap.dedent(source)
        component, namespace = load_from_string(source)
        return component, namespace
    return _load

@pytest.fixture
def render_component(gui, container):
    """Helper to render component"""
    def _render(component_class, props=None):
        gui.render(component_class, container, props=props or {})
        return container["children"][0] if container.get("children") else None
    return _render
```

**Using fixtures:**
```python
def test_with_fixtures(load_component, render_component):
    """Test using fixtures"""
    Counter, _ = load_component("""
        <widget>
          <label :text="f'Count: {count}'" />
        </widget>

        <script>
        import collagraph as cg

        class Counter(cg.Component):
            def init(self):
                self.state["count"] = self.props.get("count", 0)
        </script>
    """)

    # Render with props
    dom = render_component(Counter, props={"count": 5})

    # Assert
    label = dom["children"][0]
    assert label["attrs"]["text"] == "Count: 5"
```

## Testing Component Structure

### Test Rendering

```python
def test_user_card_structure(load_component, render_component):
    """Test UserCard renders correctly"""
    UserCard, _ = load_component("""
        <widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
          <label :text="name" />
          <label :text="email" />
          <label :text="role" />
        </widget>

        <script>
        import collagraph as cg

        class UserCard(cg.Component):
            pass
        </script>
    """)

    dom = render_component(UserCard, props={
        "name": "Alice",
        "email": "alice@example.com",
        "role": "Developer"
    })

    # Check structure
    assert dom["type"] == "widget"
    assert len(dom["children"]) == 3

    # Check labels
    assert dom["children"][0]["attrs"]["text"] == "Alice"
    assert dom["children"][1]["attrs"]["text"] == "alice@example.com"
    assert dom["children"][2]["attrs"]["text"] == "Developer"
```

### Test Conditional Rendering

```python
def test_conditional_rendering(load_component, render_component):
    """Test v-if directive"""
    Component, _ = load_component("""
        <widget>
          <label v-if="show_message" text="Hello" />
          <label v-else text="Goodbye" />
        </widget>

        <script>
        import collagraph as cg

        class Component(cg.Component):
            pass
        </script>
    """)

    # Test with show_message = True
    dom = render_component(Component, props={"show_message": True})
    assert len(dom["children"]) == 1
    assert dom["children"][0]["attrs"]["text"] == "Hello"

    # Test with show_message = False
    dom = render_component(Component, props={"show_message": False})
    assert len(dom["children"]) == 1
    assert dom["children"][0]["attrs"]["text"] == "Goodbye"
```

### Test List Rendering

```python
def test_list_rendering(load_component, render_component):
    """Test v-for directive"""
    ItemList, _ = load_component("""
        <widget>
          <label
            v-for="item in items"
            :key="item"
            :text="item"
          />
        </widget>

        <script>
        import collagraph as cg

        class ItemList(cg.Component):
            pass
        </script>
    """)

    items = ["Apple", "Banana", "Cherry"]
    dom = render_component(ItemList, props={"items": items})

    # Check all items rendered
    assert len(dom["children"]) == 3

    for i, item in enumerate(items):
        assert dom["children"][i]["attrs"]["text"] == item
```

## Testing Event Handlers

### Test Event Handler Exists

```python
def test_button_has_click_handler(load_component, render_component):
    """Test button has click handler"""
    Button, _ = load_component("""
        <button text="Click" @clicked="handle_click" />

        <script>
        import collagraph as cg

        class Button(cg.Component):
            def handle_click(self):
                pass
        </script>
    """)

    dom = render_component(Button)

    # Check handler exists
    assert "clicked" in dom["handlers"]
    assert len(dom["handlers"]["clicked"]) == 1
```

### Test Event Handler Execution

```python
def test_counter_increment(load_component, gui, container):
    """Test counter increment works"""
    Counter, _ = load_component("""
        <widget>
          <label :text="f'Count: {count}'" />
          <button text="+" @clicked="increment" />
        </widget>

        <script>
        import collagraph as cg

        class Counter(cg.Component):
            def init(self):
                self.state["count"] = 0

            def increment(self):
                self.state["count"] += 1
        </script>
    """)

    gui.render(Counter, container)
    dom = container["children"][0]

    # Initial state
    label = dom["children"][0]
    assert label["attrs"]["text"] == "Count: 0"

    # Click button
    button = dom["children"][1]
    for handler in button["handlers"]["clicked"]:
        handler()

    # Check state updated
    assert label["attrs"]["text"] == "Count: 1"

    # Click again
    for handler in button["handlers"]["clicked"]:
        handler()

    assert label["attrs"]["text"] == "Count: 2"
```

### Test Event Emission

```python
def test_child_emits_event(load_component, gui, container):
    """Test child component emits events to parent"""
    # Define child
    Child, namespace = load_component("""
        <button text="Save" @clicked="handle_save" />

        <script>
        import collagraph as cg

        class Child(cg.Component):
            def handle_save(self):
                self.emit("saved", {"data": "value"})
        </script>
    """)

    # Define parent
    Parent, _ = load_component("""
        <widget>
          <Child @saved="handle_child_saved" />
        </widget>

        <script>
        import collagraph as cg
        try:
            import Child
        except ImportError:
            pass

        class Parent(cg.Component):
            saved_data = None

            def handle_child_saved(self, data):
                Parent.saved_data = data
        </script>
    """, namespace=namespace)

    gui.render(Parent, container)
    dom = container["children"][0]

    # Get child button
    child_dom = dom["children"][0]
    assert child_dom["type"] == "button"

    # Click button to trigger event
    for handler in child_dom["handlers"]["clicked"]:
        handler()

    # Check parent received event
    assert Parent.saved_data == {"data": "value"}
```

## Testing State

### Test State Initialization

```python
def test_state_initialization(load_component, gui, container):
    """Test state initialized correctly"""
    Component, _ = load_component("""
        <label :text="message" />

        <script>
        import collagraph as cg

        class Component(cg.Component):
            def init(self):
                self.state["message"] = "Hello, World!"
        </script>
    """)

    gui.render(Component, container)
    dom = container["children"][0]

    assert dom["attrs"]["text"] == "Hello, World!"
```

### Test State Updates

```python
def test_state_updates(load_component, gui, container):
    """Test state updates trigger re-render"""
    Form, _ = load_component("""
        <widget>
          <lineedit
            :text="text"
            @text-changed="handle_change"
          />
          <label :text="f'You typed: {text}'" />
        </widget>

        <script>
        import collagraph as cg

        class Form(cg.Component):
            def init(self):
                self.state["text"] = ""

            def handle_change(self, new_text):
                self.state["text"] = new_text
        </script>
    """)

    gui.render(Form, container)
    dom = container["children"][0]

    label = dom["children"][1]
    assert label["attrs"]["text"] == "You typed: "

    # Trigger text change
    lineedit = dom["children"][0]
    for handler in lineedit["handlers"]["text_changed"]:
        handler("Hello")

    assert label["attrs"]["text"] == "You typed: Hello"
```

### Test Computed Properties

```python
def test_computed_property(load_component, render_component):
    """Test computed properties"""
    Component, _ = load_component("""
        <label :text="full_name" />

        <script>
        import collagraph as cg

        class Component(cg.Component):
            @property
            def full_name(self):
                first = self.props.get("first_name", "")
                last = self.props.get("last_name", "")
                return f"{first} {last}".strip()
        </script>
    """)

    dom = render_component(Component, props={
        "first_name": "Alice",
        "last_name": "Smith"
    })

    assert dom["attrs"]["text"] == "Alice Smith"
```

## Testing Lifecycle Hooks

### Test init() Hook

```python
def test_init_hook(load_component, gui, container):
    """Test init() is called"""
    Component, _ = load_component("""
        <label :text="message" />

        <script>
        import collagraph as cg

        class Component(cg.Component):
            init_called = False

            def init(self):
                Component.init_called = True
                self.state["message"] = "Initialized"
        </script>
    """)

    # Before render
    assert not Component.init_called

    # Render
    gui.render(Component, container)

    # After render
    assert Component.init_called

    dom = container["children"][0]
    assert dom["attrs"]["text"] == "Initialized"
```

### Test mounted() Hook

```python
def test_mounted_hook(load_component, gui, container):
    """Test mounted() is called"""
    Component, _ = load_component("""
        <label :text="status" />

        <script>
        import collagraph as cg

        class Component(cg.Component):
            mounted_called = False

            def init(self):
                self.state["status"] = "Not mounted"

            def mounted(self):
                Component.mounted_called = True
                self.state["status"] = "Mounted"
        </script>
    """)

    gui.render(Component, container)

    assert Component.mounted_called

    dom = container["children"][0]
    assert dom["attrs"]["text"] == "Mounted"
```

## Testing with Props

### Test Default Props

```python
def test_default_props(load_component, render_component):
    """Test component with default props"""
    Component, _ = load_component("""
        <label :text="title" />

        <script>
        import collagraph as cg

        class Component(cg.Component):
            def init(self):
                self.state["title"] = self.props.get("title", "Default Title")
        </script>
    """)

    # Without props
    dom = render_component(Component)
    assert dom["attrs"]["text"] == "Default Title"

    # With props
    dom = render_component(Component, props={"title": "Custom Title"})
    assert dom["attrs"]["text"] == "Custom Title"
```

### Test Props Validation

```python
def test_props_validation(load_component, gui, container):
    """Test props validation"""
    Component, _ = load_component("""
        <label :text="message" />

        <script>
        import collagraph as cg

        class Component(cg.Component):
            def init(self):
                age = self.props.get("age")

                if age is not None and not isinstance(age, int):
                    raise TypeError("age must be an integer")

                if age is not None and age < 0:
                    raise ValueError("age must be non-negative")

                self.state["message"] = f"Age: {age}" if age else "No age"
        </script>
    """)

    # Valid prop
    gui.render(Component, container, props={"age": 25})
    dom = container["children"][0]
    assert dom["attrs"]["text"] == "Age: 25"

    # Invalid type
    with pytest.raises(TypeError, match="age must be an integer"):
        container.clear()
        gui.render(Component, container, props={"age": "25"})

    # Invalid value
    with pytest.raises(ValueError, match="age must be non-negative"):
        container.clear()
        gui.render(Component, container, props={"age": -5})
```

## Mocking Dependencies

### Mocking Services

```python
from unittest.mock import Mock, patch

def test_with_mocked_service(load_component, gui, container):
    """Test component with mocked service"""
    Component, _ = load_component("""
        <widget>
          <label :text="f'Users: {user_count}'" />
          <button text="Load" @clicked="load_users" />
        </widget>

        <script>
        import collagraph as cg

        class Component(cg.Component):
            def init(self):
                self.api = self.props.get("api")
                self.state["user_count"] = 0

            def load_users(self):
                users = self.api.get_users()
                self.state["user_count"] = len(users)
        </script>
    """)

    # Create mock API
    mock_api = Mock()
    mock_api.get_users.return_value = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]

    # Render with mock
    gui.render(Component, container, props={"api": mock_api})
    dom = container["children"][0]

    label = dom["children"][0]
    assert label["attrs"]["text"] == "Users: 0"

    # Click button
    button = dom["children"][1]
    for handler in button["handlers"]["clicked"]:
        handler()

    # Check mock was called
    mock_api.get_users.assert_called_once()

    # Check state updated
    assert label["attrs"]["text"] == "Users: 2"
```

### Mocking External Functions

```python
def test_with_mocked_function(load_component, gui, container):
    """Test with mocked external function"""
    Component, _ = load_component("""
        <label :text="formatted_date" />

        <script>
        import collagraph as cg
        from datetime import datetime

        def format_date(date):
            return date.strftime("%Y-%m-%d")

        class Component(cg.Component):
            @property
            def formatted_date(self):
                return format_date(datetime.now())
        </script>
    """)

    # Mock datetime.now()
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 15)

        gui.render(Component, container)
        dom = container["children"][0]

        assert dom["attrs"]["text"] == "2024-01-15"
```

## Parametrized Tests

### Test Multiple Scenarios

```python
@pytest.mark.parametrize("count,expected", [
    (0, "Count: 0"),
    (1, "Count: 1"),
    (5, "Count: 5"),
    (100, "Count: 100"),
])
def test_counter_values(load_component, render_component, count, expected):
    """Test counter with different values"""
    Counter, _ = load_component("""
        <label :text="f'Count: {count}'" />

        <script>
        import collagraph as cg

        class Counter(cg.Component):
            pass
        </script>
    """)

    dom = render_component(Counter, props={"count": count})
    assert dom["attrs"]["text"] == expected


@pytest.mark.parametrize("email,is_valid", [
    ("alice@example.com", True),
    ("bob.smith@company.co.uk", True),
    ("invalid", False),
    ("@example.com", False),
    ("alice@", False),
])
def test_email_validation(email, is_valid):
    """Test email validation"""
    import re

    def validate_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    assert validate_email(email) == is_valid
```

## Integration Tests

### Test Component Composition

```python
def test_parent_child_integration(load_component, gui, container):
    """Test parent and child components working together"""
    # Child component
    Child, namespace = load_component("""
        <button
          :text="text"
          @clicked="handle_click"
        />

        <script>
        import collagraph as cg

        class Child(cg.Component):
            def handle_click(self):
                self.emit("clicked", self.props.get("id"))
        </script>
    """)

    # Parent component
    Parent, _ = load_component("""
        <widget>
          <Child
            v-for="item in items"
            :key="item['id']"
            v-bind="item"
            @clicked="handle_item_click"
          />
          <label :text="f'Clicked: {clicked_id}'" />
        </widget>

        <script>
        import collagraph as cg
        try:
            import Child
        except ImportError:
            pass

        class Parent(cg.Component):
            def init(self):
                self.state["items"] = [
                    {"id": 1, "text": "Item 1"},
                    {"id": 2, "text": "Item 2"},
                    {"id": 3, "text": "Item 3"}
                ]
                self.state["clicked_id"] = None

            def handle_item_click(self, item_id):
                self.state["clicked_id"] = item_id
        </script>
    """, namespace=namespace)

    gui.render(Parent, container)
    dom = container["children"][0]

    # Check buttons rendered
    assert len([c for c in dom["children"] if c["type"] == "button"]) == 3

    # Click second button
    second_button = dom["children"][1]
    for handler in second_button["handlers"]["clicked"]:
        handler()

    # Check label updated
    label = dom["children"][-1]
    assert label["attrs"]["text"] == "Clicked: 2"
```

## Test Coverage

### Generate Coverage Reports

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

### Coverage Configuration

**pyproject.toml:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/test_*.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## Best Practices

1. **Test behavior, not implementation** - Test what components do, not how
2. **Use descriptive test names** - Name tests clearly (test_counter_increments_on_click)
3. **One assertion per concept** - Keep tests focused
4. **Use fixtures for setup** - Reduce duplication with pytest fixtures
5. **Test edge cases** - Empty lists, null values, boundary conditions
6. **Mock external dependencies** - Isolate component from services/APIs
7. **Test events thoroughly** - Ensure events are emitted with correct data
8. **Use parametrize for variants** - Test multiple scenarios efficiently
9. **Keep tests fast** - Use DictRenderer, avoid real UI operations
10. **Maintain test coverage** - Aim for >80% coverage

## Common Testing Patterns

### Test Setup/Teardown

```python
class TestUserComponent:
    """Test user component"""

    def setup_method(self):
        """Run before each test"""
        self.gui = cg.Collagraph(
            cg.DictRenderer(),
            event_loop_type=cg.EventLoopType.SYNC
        )
        self.container = {"type": "root"}

    def teardown_method(self):
        """Run after each test"""
        self.container.clear()

    def test_user_display(self):
        """Test user display"""
        # Test implementation
        pass
```

### Testing Errors

```python
def test_error_handling(load_component, gui, container):
    """Test component handles errors"""
    Component, _ = load_component("""
        <label :text="error_message" />

        <script>
        import collagraph as cg

        class Component(cg.Component):
            def init(self):
                self.state["error_message"] = ""

                try:
                    self.risky_operation()
                except Exception as e:
                    self.state["error_message"] = str(e)

            def risky_operation(self):
                raise ValueError("Something went wrong")
        </script>
    """)

    gui.render(Component, container)
    dom = container["children"][0]

    assert dom["attrs"]["text"] == "Something went wrong"
```

## See Also

- [Dict Renderer](../renderers/dict.md)
- [Components](../core-concepts/components.md)
- [Events](../core-concepts/events.md)
- [State Management](../core-concepts/state-management.md)
