# Dict Renderer

The Dict renderer converts Collagraph components into nested Python dictionaries instead of rendering to actual UI elements. This is invaluable for testing, debugging, and understanding component structure.

## Overview

The Dict renderer implements the renderer interface but produces simple dictionary structures that represent the component tree. Each element becomes a dictionary with keys like:
- `type` - The element type
- `attrs` - Attributes as a dictionary
- `children` - List of child elements
- `handlers` - Event handlers
- `text` - Text content for text elements

This makes it easy to inspect and test component output without needing a UI framework.

## Basic Usage

### Simple Component Test

```python
import collagraph as cg
from collagraph.renderers import DictRenderer

class MyComponent(cg.Component):
    def render(self):
        return {"type": "label", "text": "Hello World"}

# Render to dictionary
renderer = DictRenderer()
gui = cg.Collagraph(renderer=renderer)
result = gui.render(MyComponent, {})

print(result)
# Output: {'type': 'label', 'attrs': {'text': 'Hello World'}}
```

### Component with Children

```python
class Container(cg.Component):
    def render(self):
        return {
            "type": "widget",
            "children": [
                {"type": "label", "text": "Title"},
                {"type": "button", "text": "Click", "@clicked": self.handle_click}
            ]
        }

    def handle_click(self):
        pass

result = gui.render(Container, {})
print(result)
# Output:
# {
#     'type': 'widget',
#     'children': [
#         {'type': 'label', 'attrs': {'text': 'Title'}},
#         {
#             'type': 'button',
#             'attrs': {'text': 'Click'},
#             'handlers': {'clicked': {<function...>}}
#         }
#     ]
# }
```

## Dictionary Structure

### Element Dictionary

Each rendered element has this structure:

```python
{
    "type": "element-type",        # Required: element type
    "attrs": {                     # Optional: attributes
        "attr-name": value,
        ...
    },
    "children": [...],             # Optional: child elements
    "handlers": {                  # Optional: event handlers
        "event-name": {handler1, handler2, ...},
        ...
    },
    "text": "text content"         # Optional: for text elements only
}
```

### Text Elements

Text elements have a special structure:

```python
{
    "type": "TEXT_ELEMENT",
    "text": "The text content"
}
```

## Unit Testing

### Testing Component Structure

```python
import unittest
import collagraph as cg
from collagraph.renderers import DictRenderer

class Counter(cg.Component):
    def init(self):
        self.state["count"] = self.props.get("count", 0)

    def render(self):
        return {
            "type": "widget",
            "children": [
                {"type": "label", "text": f"Count: {self.state['count']}"},
                {"type": "button", "text": "Increment", "@clicked": self.bump}
            ]
        }

    def bump(self):
        self.state["count"] += 1


class TestCounter(unittest.TestCase):
    def setUp(self):
        self.renderer = DictRenderer()
        self.gui = cg.Collagraph(renderer=self.renderer)

    def test_initial_render(self):
        result = self.gui.render(Counter, {})

        # Check structure
        self.assertEqual(result["type"], "widget")
        self.assertEqual(len(result["children"]), 2)

        # Check label
        label = result["children"][0]
        self.assertEqual(label["type"], "label")
        self.assertEqual(label["attrs"]["text"], "Count: 0")

        # Check button
        button = result["children"][1]
        self.assertEqual(button["type"], "button")
        self.assertEqual(button["attrs"]["text"], "Increment")
        self.assertIn("clicked", button["handlers"])

    def test_with_props(self):
        result = self.gui.render(Counter, {}, props={"count": 5})

        label = result["children"][0]
        self.assertEqual(label["attrs"]["text"], "Count: 5")

    def test_event_handler_exists(self):
        result = self.gui.render(Counter, {})

        button = result["children"][1]
        self.assertIn("handlers", button)
        self.assertIn("clicked", button["handlers"])
        self.assertEqual(len(button["handlers"]["clicked"]), 1)
```

### Testing Conditional Rendering

```python
class ConditionalComponent(cg.Component):
    def init(self):
        self.state["show_details"] = self.props.get("show_details", False)

    def render(self):
        children = [{"type": "label", "text": "Title"}]

        if self.state["show_details"]:
            children.append({"type": "label", "text": "Details"})

        return {"type": "widget", "children": children}


class TestConditional(unittest.TestCase):
    def setUp(self):
        self.renderer = DictRenderer()
        self.gui = cg.Collagraph(renderer=self.renderer)

    def test_without_details(self):
        result = self.gui.render(ConditionalComponent, {})
        self.assertEqual(len(result["children"]), 1)

    def test_with_details(self):
        result = self.gui.render(
            ConditionalComponent,
            {},
            props={"show_details": True}
        )
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][1]["attrs"]["text"], "Details")
```

### Testing Lists

```python
class ListComponent(cg.Component):
    def init(self):
        self.state["items"] = self.props.get("items", [])

    def render(self):
        return {
            "type": "widget",
            "children": [
                {"type": "label", "text": item, "key": item}
                for item in self.state["items"]
            ]
        }


class TestList(unittest.TestCase):
    def setUp(self):
        self.renderer = DictRenderer()
        self.gui = cg.Collagraph(renderer=self.renderer)

    def test_empty_list(self):
        result = self.gui.render(ListComponent, {})
        self.assertEqual(result["children"], [])

    def test_with_items(self):
        items = ["A", "B", "C"]
        result = self.gui.render(ListComponent, {}, props={"items": items})

        self.assertEqual(len(result["children"]), 3)
        for i, item in enumerate(items):
            child = result["children"][i]
            self.assertEqual(child["type"], "label")
            self.assertEqual(child["attrs"]["text"], item)
```

## Debugging Component Output

### Pretty Printing

Use the `format_dict` helper to pretty-print component structure:

```python
from collagraph.renderers.dict_renderer import format_dict

result = gui.render(MyComponent, {})
print(format_dict(result))
```

Output:
```
<widget>
  <label text="Count: 0" />
  <button text="Increment" />
</widget>
```

### Inspecting Nested Components

```python
class ChildComponent(cg.Component):
    def render(self):
        return {"type": "label", "text": self.props["text"]}

class ParentComponent(cg.Component):
    def render(self):
        return {
            "type": "widget",
            "children": [
                {"type": ChildComponent, "text": "Hello"},
                {"type": ChildComponent, "text": "World"}
            ]
        }

result = gui.render(ParentComponent, {})
print(format_dict(result))
```

Output:
```
<widget>
  <label text="Hello" />
  <label text="World" />
</widget>
```

## Snapshot Testing

Create snapshots of component output for regression testing:

```python
import json
import os

class SnapshotTest(unittest.TestCase):
    def setUp(self):
        self.renderer = DictRenderer()
        self.gui = cg.Collagraph(renderer=self.renderer)
        self.snapshot_dir = "test_snapshots"
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def snapshot_path(self, name):
        return os.path.join(self.snapshot_dir, f"{name}.json")

    def assert_snapshot_matches(self, component_class, props, snapshot_name):
        result = self.gui.render(component_class, {}, props=props)

        # Convert handlers to string representation for comparison
        result_str = self.serialize_for_snapshot(result)

        snapshot_file = self.snapshot_path(snapshot_name)

        if not os.path.exists(snapshot_file):
            # Create new snapshot
            with open(snapshot_file, 'w') as f:
                json.dump(result_str, f, indent=2)
            self.skipTest(f"Created new snapshot: {snapshot_name}")
        else:
            # Compare with existing snapshot
            with open(snapshot_file, 'r') as f:
                expected = json.load(f)

            self.assertEqual(result_str, expected,
                           f"Snapshot mismatch: {snapshot_name}")

    def serialize_for_snapshot(self, obj):
        """Convert result to JSON-serializable format"""
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                if key == "handlers":
                    # Convert handler sets to counts
                    result[key] = {
                        event: len(handlers)
                        for event, handlers in value.items()
                    }
                else:
                    result[key] = self.serialize_for_snapshot(value)
            return result
        elif isinstance(obj, list):
            return [self.serialize_for_snapshot(item) for item in obj]
        else:
            return obj

    def test_counter_snapshot(self):
        self.assert_snapshot_matches(Counter, {"count": 0}, "counter_initial")
        self.assert_snapshot_matches(Counter, {"count": 5}, "counter_five")
```

## Validating Component Output

### Schema Validation

```python
def validate_structure(result, expected_type, expected_children=None):
    """Validate component structure"""
    assert result["type"] == expected_type, \
        f"Expected type {expected_type}, got {result['type']}"

    if expected_children is not None:
        actual_children = len(result.get("children", []))
        assert actual_children == expected_children, \
            f"Expected {expected_children} children, got {actual_children}"

# Usage
result = gui.render(Counter, {})
validate_structure(result, "widget", expected_children=2)
```

### Attribute Validation

```python
def has_attribute(element, attr_name, attr_value=None):
    """Check if element has attribute"""
    attrs = element.get("attrs", {})
    if attr_name not in attrs:
        return False
    if attr_value is not None:
        return attrs[attr_name] == attr_value
    return True

# Usage
result = gui.render(Counter, {})
button = result["children"][1]
assert has_attribute(button, "text", "Increment")
```

## Integration with pytest

```python
import pytest
import collagraph as cg
from collagraph.renderers import DictRenderer

@pytest.fixture
def renderer():
    return DictRenderer()

@pytest.fixture
def gui(renderer):
    return cg.Collagraph(renderer=renderer)

def test_counter_initial(gui):
    result = gui.render(Counter, {})
    assert result["type"] == "widget"
    assert len(result["children"]) == 2

def test_counter_with_value(gui):
    result = gui.render(Counter, {}, props={"count": 10})
    label = result["children"][0]
    assert label["attrs"]["text"] == "Count: 10"

@pytest.mark.parametrize("count,expected", [
    (0, "Count: 0"),
    (5, "Count: 5"),
    (100, "Count: 100"),
])
def test_counter_values(gui, count, expected):
    result = gui.render(Counter, {}, props={"count": count})
    label = result["children"][0]
    assert label["attrs"]["text"] == expected
```

## Advanced Testing Patterns

### Testing Component Updates

```python
from observ import reactive

def test_component_updates():
    renderer = DictRenderer()
    gui = cg.Collagraph(renderer=renderer)

    # Create reactive state
    state = reactive({"count": 0})

    # Initial render
    container = {}
    instance = gui.render(Counter, container, state=state)

    # Check initial state
    label = container["children"][0]
    assert label["attrs"]["text"] == "Count: 0"

    # Update state
    state["count"] = 5

    # Component should re-render
    # (In actual test, you'd need to trigger the update cycle)
    assert label["attrs"]["text"] == "Count: 5"
```

## Limitations

The Dict renderer has some limitations compared to real renderers:

1. **No visual output** - Only produces data structures
2. **No event execution** - Handlers are stored but not called
3. **No lifecycle simulation** - Mounted/unmounted callbacks don't fire automatically
4. **No actual updates** - Changes don't automatically re-render

Despite these limitations, it's perfect for:
- Unit testing component logic
- Validating component structure
- Snapshot testing
- Debugging render output

## See Also

- [Testing Guide](../guides/testing.md)
- [Renderers Overview](overview.md)
