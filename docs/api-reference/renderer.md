# Renderer Interface

## Abstract Class: `Renderer`

Base class for all renderers. The Renderer is responsible for translating Collagraph's virtual UI representation into actual UI elements for a specific rendering target (e.g., Qt widgets, 3D graphics, or simple dictionaries).

To create a custom renderer, subclass `Renderer` and implement all abstract methods.

## Overview

The Renderer interface defines how Collagraph creates, updates, and manages UI elements. Each renderer implementation handles:

- **Element Creation**: Creating native UI elements (widgets, nodes, etc.)
- **DOM Manipulation**: Inserting, removing, and organizing elements
- **Attribute Management**: Setting and removing element attributes
- **Event Handling**: Attaching and detaching event listeners
- **Event Loop Integration**: Coordinating with the native event system

## Abstract Methods

All methods below **must** be implemented by custom renderers.

### `create_element(self, type: str) -> Any`

Create a native element for the given type name.

**Parameters:**
- `type` (str): Element type name (e.g., "button", "label", "widget")

**Returns:** The created native element (type depends on renderer)

**Example (DictRenderer):**
```python
def create_element(self, type: str) -> dict:
    return {"type": type}
```

**Example (PySideRenderer):**
```python
def create_element(self, type_name: str) -> Any:
    # Map type name to Qt class
    if type_name == "button":
        return QtWidgets.QPushButton()
    elif type_name == "label":
        return QtWidgets.QLabel()
    # ... etc
```

---

### `create_text_element(self) -> Any`

Create a native text element.

**Returns:** A text element (type depends on renderer)

**Example (DictRenderer):**
```python
def create_text_element(self):
    return {"type": "TEXT_ELEMENT"}
```

**Note:** Not all renderers support text elements. PySideRenderer raises `NotImplementedError` since Qt doesn't have standalone text elements.

---

### `insert(self, el: Any, parent: Any, anchor: Any = None)`

Insert an element as a child of a parent element.

**Parameters:**
- `el` (Any): Element to insert
- `parent` (Any): Parent element to insert into
- `anchor` (Any, optional): If provided, insert `el` before this anchor element

**Example (DictRenderer):**
```python
def insert(self, el, parent, anchor=None):
    children = parent.setdefault("children", [])
    anchor_idx = children.index(anchor) if anchor else len(children)
    children.insert(anchor_idx, el)
```

**Example (PySideRenderer):**
```python
def insert(self, el: Any, parent: Any, anchor: Any = None):
    if isinstance(parent, QtWidgets.QApplication):
        # Top-level widget
        el.show()
    else:
        parent.insert(el, anchor=anchor)  # Custom method
```

---

### `remove(self, el: Any, parent: Any)`

Remove an element from its parent.

**Parameters:**
- `el` (Any): Element to remove
- `parent` (Any): Parent element to remove from

**Example (DictRenderer):**
```python
def remove(self, el, parent):
    children = parent["children"]
    children.remove(el)
    if not children:
        del parent["children"]
```

---

### `set_element_text(self, el: Any, value: str)`

Set the text content of a text element.

**Parameters:**
- `el` (Any): Text element
- `value` (str): Text content to set

**Example (DictRenderer):**
```python
def set_element_text(self, el: dict, value: str):
    el["text"] = value
```

---

### `set_attribute(self, el: Any, attr: str, value: Any)`

Set an attribute on an element.

**Parameters:**
- `el` (Any): Element to update
- `attr` (str): Attribute name
- `value` (Any): Attribute value

**Example (DictRenderer):**
```python
def set_attribute(self, obj, attr: str, value):
    attributes = obj.setdefault("attrs", {})
    attributes[attr] = value
```

**Example (PySideRenderer):**
```python
def set_attribute(self, el: Any, attr: str, value: Any):
    # Map attribute names to Qt properties/methods
    if attr == "text":
        el.setText(value)
    elif attr == "enabled":
        el.setEnabled(value)
    # ... etc
```

---

### `remove_attribute(self, el: Any, attr: str, value: Any)`

Remove an attribute from an element.

**Parameters:**
- `el` (Any): Element to update
- `attr` (str): Attribute name to remove
- `value` (Any): Current value (may be used for cleanup)

**Example (DictRenderer):**
```python
def remove_attribute(self, obj, attr: str, value):
    attributes = obj["attrs"]
    if attr in attributes:
        del attributes[attr]
```

**Note:** Often involves resetting to a default value rather than completely removing.

---

### `add_event_listener(self, el: Any, event_type: str, value: Callable)`

Attach an event listener to an element.

**Parameters:**
- `el` (Any): Element to attach listener to
- `event_type` (str): Event name (e.g., "clicked", "changed")
- `value` (Callable): Event handler function

**Example (DictRenderer):**
```python
def add_event_listener(self, el, event_type, value):
    event_listeners = el.setdefault("handlers", defaultdict(set))
    event_listeners[event_type].add(value)
```

**Example (PySideRenderer):**
```python
def add_event_listener(self, el: Any, event_type: str, value: Callable):
    # Convert event name to Qt signal name
    signal_name = camel_case(event_type, "_")
    signal = getattr(el, signal_name, None)
    if signal and hasattr(signal, "connect"):
        slot = QtCore.Slot()(value)
        signal.connect(slot)
```

---

### `remove_event_listener(self, el: Any, event_type: str, value: Callable)`

Remove an event listener from an element.

**Parameters:**
- `el` (Any): Element to remove listener from
- `event_type` (str): Event name
- `value` (Callable): Event handler to remove

**Example (DictRenderer):**
```python
def remove_event_listener(self, el, event_type, value):
    event_listeners = el.get("handlers", None)
    if event_listeners:
        event_listeners[event_type].remove(value)
```

## Optional Methods

These methods have default implementations but can be overridden for custom behavior.

### `preferred_event_loop_type(self) -> Optional[EventLoopType]`

Indicate the preferred event loop type for this renderer.

**Returns:** An `EventLoopType` or `None`

**Default:** Returns `None`

```python
def preferred_event_loop_type(self):
    return EventLoopType.DEFAULT
```

---

### `register_asyncio(self) -> None`

Called when Collagraph registers with asyncio. Perform any renderer-specific asyncio setup here.

**Default:** Does nothing

**Example (PySideRenderer):**
```python
def register_asyncio(self):
    import asyncio
    from PySide6.QtAsyncio import QAsyncioEventLoopPolicy

    policy = asyncio.get_event_loop_policy()
    if not isinstance(policy, QAsyncioEventLoopPolicy):
        asyncio.set_event_loop_policy(QAsyncioEventLoopPolicy())
```

## Complete Example: Simple DictRenderer

Here's the complete implementation of the `DictRenderer`, which renders to plain Python dictionaries:

```python
from collections import defaultdict
from collagraph.renderers import Renderer

class DictRenderer(Renderer):
    """Renderer that renders to a simple dict object"""

    def create_element(self, type: str) -> dict:
        return {"type": type}

    def create_text_element(self):
        return {"type": "TEXT_ELEMENT"}

    def insert(self, el, parent, anchor=None):
        children = parent.setdefault("children", [])
        anchor_idx = children.index(anchor) if anchor else len(children)
        children.insert(anchor_idx, el)

    def remove(self, el, parent):
        children = parent["children"]
        children.remove(el)
        if not children:
            del parent["children"]

    def set_element_text(self, el: dict, value: str):
        el["text"] = value

    def set_attribute(self, obj, attr: str, value):
        attributes = obj.setdefault("attrs", {})
        attributes[attr] = value

    def remove_attribute(self, obj, attr: str, value):
        attributes = obj["attrs"]
        if attr in attributes:
            del attributes[attr]

    def add_event_listener(self, el, event_type, value):
        event_listeners = el.setdefault("handlers", defaultdict(set))
        event_listeners[event_type].add(value)

    def remove_event_listener(self, el, event_type, value):
        event_listeners = el.get("handlers", None)
        if event_listeners:
            event_listeners[event_type].remove(value)
```

## Implementing a Custom Renderer

### Step 1: Choose Your Rendering Target

Decide what you're rendering to:
- UI framework (Qt, GTK, etc.)
- 3D graphics (pygfx, three.js, etc.)
- Canvas or SVG
- Virtual representation (dict, JSON, etc.)

### Step 2: Create the Renderer Class

```python
from collagraph.renderers import Renderer

class MyCustomRenderer(Renderer):
    def __init__(self):
        super().__init__()
        # Initialize any renderer-specific state
```

### Step 3: Implement Element Creation

```python
    def create_element(self, type: str):
        # Map type names to native elements
        if type == "button":
            return MyNativeButton()
        elif type == "label":
            return MyNativeLabel()
        # ... etc

    def create_text_element(self):
        return MyNativeTextElement()
```

### Step 4: Implement DOM Manipulation

```python
    def insert(self, el, parent, anchor=None):
        # Add el as child of parent
        # If anchor provided, insert before anchor
        parent.add_child(el, before=anchor)

    def remove(self, el, parent):
        # Remove el from parent
        parent.remove_child(el)
```

### Step 5: Implement Attributes and Events

```python
    def set_attribute(self, el, attr, value):
        # Set attribute on element
        # Map attribute names to native properties
        el.set_property(attr, value)

    def remove_attribute(self, el, attr, value):
        # Remove or reset attribute
        el.reset_property(attr)

    def add_event_listener(self, el, event_type, handler):
        # Attach event listener
        el.on(event_type, handler)

    def remove_event_listener(self, el, event_type, handler):
        # Detach event listener
        el.off(event_type, handler)
```

### Step 6: (Optional) Event Loop Integration

```python
    def preferred_event_loop_type(self):
        return EventLoopType.DEFAULT

    def register_asyncio(self):
        # Perform asyncio-specific setup
        pass
```

## Best Practices

1. **Error Handling**: Wrap operations in try/except to provide useful error messages
2. **Type Mapping**: Use a dictionary to map type names to native classes
3. **Attribute Defaults**: Track default values so `remove_attribute` can reset properly
4. **Event Cleanup**: Ensure event listeners are properly removed to prevent memory leaks
5. **Performance**: Cache expensive operations (type lookups, etc.)

## Advanced: PySideRenderer Registration System

The `PySideRenderer` provides a registration system for custom elements, layouts, and attributes:

```python
from collagraph.renderers import PySideRenderer

# Register custom widget
@PySideRenderer.register_element("my-widget")
class MyCustomWidget(QWidget):
    pass

# Register custom layout
@PySideRenderer.register_layout("my-layout")
class MyCustomLayout(QLayout):
    pass

# Register custom attribute handler
@PySideRenderer.register_custom_attribute("my-attr")
def handle_my_attr(element, attr, value):
    # Custom attribute handling
    pass
```

## See Also

- [Creating Custom Renderers](../renderers/custom-renderer.md)
- [PySide Renderer](../renderers/pyside.md)
