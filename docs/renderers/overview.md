# Renderers Overview

Collagraph uses a renderer system that separates your component logic from the actual UI implementation. This allows you to write components once and render them to different targets.

## What are Renderers?

Renderers are backends that convert Collagraph's component tree into actual UI elements. Each renderer implements a standard interface that handles:

- **Creating elements** - Converting type strings (like "button", "label") into actual UI objects
- **Managing hierarchy** - Inserting and removing elements from their parents
- **Setting attributes** - Updating properties on elements (text, enabled, value, etc.)
- **Event handling** - Connecting event listeners to UI events

When you write a component, you define the structure using dictionaries:

```python
def render(self):
    return {
        "type": "button",
        "text": "Click me",
        "@clicked": self.handle_click
    }
```

The renderer interprets this structure and creates the corresponding UI elements for its target platform.

## Available Renderers

### PySide Renderer
For building desktop Qt applications.
- **Use case**: Desktop GUI applications
- **Install**: `pip install collagraph[pyside]`
- [Learn more](pyside.md)

### Pygfx Renderer
For 3D graphics and visualizations.
- **Use case**: 3D visualization, scientific graphics
- **Install**: `pip install collagraph[pygfx]`
- [Learn more](pygfx.md)

### Dict Renderer
Returns nested dictionaries representing the UI.
- **Use case**: Testing, debugging, serialization
- **Install**: Included with collagraph
- [Learn more](dict.md)

## Choosing a Renderer

- **Desktop applications** → PySide Renderer
- **3D graphics** → Pygfx Renderer
- **Testing** → Dict Renderer
- **Custom needs** → [Create your own](custom-renderer.md)

## Using a Renderer

There are two main ways to use a renderer with Collagraph:

### Method 1: Using the Collagraph Class

```python
import collagraph as cg
from collagraph.renderers import PySideRenderer

class MyApp(cg.Component):
    def render(self):
        return {"type": "window", "title": "My App", "children": [
            {"type": "label", "text": "Hello World"}
        ]}

app = cg.Collagraph(MyApp, PySideRenderer)
app.run()
```

### Method 2: Direct Rendering

```python
import collagraph as cg
from collagraph.renderers import DictRenderer

class MyComponent(cg.Component):
    def render(self):
        return {"type": "label", "text": "Hello"}

renderer = DictRenderer()
gui = cg.Collagraph(renderer=renderer)
result = gui.render(MyComponent, {})
print(result)
```

## Renderer Features

### Element Creation

Renderers create elements based on type strings. The PySide renderer supports:
- Built-in Qt widgets (button, label, line-edit, etc.)
- Custom registered widgets
- Full Qt class names (QWidget, QPushButton, etc.)

### Attribute Mapping

Attributes are automatically mapped to Qt properties using camel case conversion:
- `text="Hello"` → `setText("Hello")`
- `enabled=False` → `setEnabled(False)`
- `window-title="App"` → `setWindowTitle("App")`

### Event Handling

Events use the `@` prefix and map to Qt signals:
- `@clicked` → `clicked` signal
- `@value-changed` → `valueChanged` signal
- `@selection-changed` → `selectionChanged` signal

## See Also

- [Creating Custom Renderers](custom-renderer.md)
- [Renderer API](../api-reference/renderer.md)
