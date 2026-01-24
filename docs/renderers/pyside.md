# PySide Renderer

The PySide renderer enables you to build powerful Qt desktop applications using Collagraph's reactive component model. It provides a declarative way to create Qt UIs while leveraging all of Qt's widgets and features.

## Overview

The PySide renderer allows you to build Qt desktop applications using Collagraph. It translates Collagraph's component structure into PySide6 (Qt) widgets, handling:

- Widget creation and lifecycle
- Layout management
- Event handling via Qt signals
- Property updates via Qt setters
- Integration with Qt's event loop

## Installation

```bash
pip install collagraph[pyside]
```

## Basic Usage

### Simple Counter Example

```python
import collagraph as cg
from collagraph.renderers import PySideRenderer

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

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

app = cg.Collagraph(Counter, PySideRenderer)
app.run()
```

### Using CGX Template Syntax

You can also use Collagraph's CGX template syntax for a more declarative approach:

```xml
<!-- counter.cgx -->
<widget>
  <label :text="f'Count: {count}'" />
  <button text="Increment" @clicked="bump" />
</widget>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def bump(self):
        self.state["count"] += 1
</script>
```

Run with: `collagraph counter.cgx`

## Attribute Binding

### Static Attributes

Use static values for attributes that don't change:

```python
{"type": "label", "text": "Hello World"}
```

### Dynamic Attributes

Bind attributes to reactive state using `:` prefix (in CGX) or direct values (in Python):

```python
# Python dict syntax
{"type": "slider", "value": self.state["volume"]}

# CGX syntax
# <slider :value="volume" />
```

### Attribute Name Conversion

Attribute names are automatically converted to Qt setter methods:
- `text` → `setText()`
- `enabled` → `setEnabled()`
- `window-title` or `window_title` → `setWindowTitle()`
- `minimum` → `setMinimum()`
- `maximum` → `setMaximum()`

## Event Handling

Events use the `@` prefix and connect to Qt signals:

```python
def render(self):
    return {
        "type": "button",
        "text": "Click me",
        "@clicked": self.on_click
    }

def on_click(self):
    print("Button clicked!")
```

### Common Events

- `@clicked` - Button clicks
- `@value-changed` - Value changes (sliders, spinboxes, etc.)
- `@text-changed` - Text input changes
- `@current-index-changed` - Selection changes (combo boxes, tabs)
- `@toggled` - Checkbox/radio button state changes
- `@selection-changed` - Selection model changes

## Widget Types

The PySide renderer supports many Qt widget types. You can specify them using:

1. **Short names**: `"button"`, `"label"`, `"line-edit"`
2. **Qt class names**: `"QPushButton"`, `"QLabel"`, `"QLineEdit"`

See [Available Widgets](pyside-widgets.md) for a complete list.

## Accessing Qt Objects

Sometimes you need access to the underlying Qt widget. Use `self.element`:

```python
class MyComponent(cg.Component):
    def mounted(self):
        # Access the Qt widget after it's created
        print(f"Widget created: {self.element}")

    def some_method(self):
        # Call Qt methods directly
        self.element.setFocus()
```

## Custom Qt Widgets

You can register custom Qt widgets with the renderer:

```python
from PySide6.QtWidgets import QWidget
import collagraph as cg

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Custom widget implementation

# Register the widget
cg.PySideRenderer.register_element("custom-widget", CustomWidget)

# Now use it in your components
class MyApp(cg.Component):
    def render(self):
        return {"type": "custom-widget"}
```

## Async Support

The PySide renderer supports asyncio integration:

```python
import asyncio
import collagraph as cg

class AsyncApp(cg.Component):
    async def init(self):
        self.state["data"] = "Loading..."
        # Async initialization
        await self.load_data()

    async def load_data(self):
        await asyncio.sleep(1)
        self.state["data"] = "Loaded!"

    def render(self):
        return {"type": "label", "text": self.state["data"]}
```

## See Also

- [Available Widgets](pyside-widgets.md)
- [Layouts](pyside-layouts.md)
- [Dialogs & Windows](pyside-dialogs.md)
- [Advanced Components](pyside-advanced.md)
