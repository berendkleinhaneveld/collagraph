# Collagraph Class

## Class: `cg.Collagraph`

Main class for running Collagraph applications. This class manages the rendering lifecycle, coordinates with the renderer, and handles event loop integration.

## Constructor

```python
Collagraph(
    renderer: Renderer,
    *,
    event_loop_type: EventLoopType | None = None
)
```

### Parameters

- `renderer` (Renderer): An instance of a renderer (e.g., `PySideRenderer()`, `DictRenderer()`)
- `event_loop_type` (EventLoopType, optional): Type of event loop to use. If `None`, uses the renderer's preferred event loop type, or `EventLoopType.DEFAULT` if the renderer has no preference.

### Example

```python
import collagraph as cg

# Create Collagraph instance with PySide renderer
gui = cg.Collagraph(renderer=cg.PySideRenderer())

# Create with specific event loop type
gui = cg.Collagraph(
    renderer=cg.PySideRenderer(),
    event_loop_type=cg.EventLoopType.DEFAULT
)
```

**Note:** You pass a renderer **instance**, not a class.

## Methods

### `render(self, component_class: Callable[[dict], Component], target: Any, state: dict | None = None)`

Render a component tree into the target container.

**Parameters:**
- `component_class` (Callable): The root component class to render
- `target` (Any): The target container to render into (type depends on renderer)
  - For `PySideRenderer`: A `QApplication` instance
  - For `DictRenderer`: A dictionary like `{"root": None}`
  - For `PygfxRenderer`: A `gfx.Scene` instance
- `state` (dict, optional): Initial state/props to pass to the root component

**Returns:** None

**Example with PySide:**

```python
from PySide6 import QtWidgets
import collagraph as cg

class MyApp(cg.Component):
    def init(self):
        self.state["title"] = self.props.get("title", "Default Title")

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    gui = cg.Collagraph(renderer=cg.PySideRenderer())
    gui.render(MyApp, app, state={"title": "My Application"})
    app.exec()
```

**Example with DictRenderer:**

```python
import collagraph as cg

class MyApp(cg.Component):
    # component definition...
    pass

container = {"root": None}
gui = cg.Collagraph(
    renderer=cg.DictRenderer(),
    event_loop_type=cg.EventLoopType.SYNC
)
gui.render(MyApp, container, state={})
```

**How It Works:**
1. Creates an instance of the root component with the provided state as props
2. Calls `component.render(renderer)` to get the fragment tree
3. Mounts the fragment into the target container
4. Sets up reactivity and event handling

## Event Loop Types

The event loop type determines how Collagraph handles asynchronous operations and reactivity.

### `EventLoopType.DEFAULT`

Uses Python's asyncio event loop. This is the recommended mode for most applications.

```python
from collagraph.constants import EventLoopType

gui = cg.Collagraph(
    renderer=cg.PySideRenderer(),
    event_loop_type=EventLoopType.DEFAULT
)
```

**When to use:**
- When you need async/await support
- For most modern PySide6 applications
- When using asyncio-based libraries

**Behavior:**
- Registers the observ scheduler with asyncio
- Calls `renderer.register_asyncio()` for renderer-specific setup
- For PySide, uses `QAsyncioEventLoopPolicy`

### `EventLoopType.SYNC`

Synchronous event loop mode. Updates are processed immediately without asyncio.

```python
gui = cg.Collagraph(
    renderer=cg.DictRenderer(),
    event_loop_type=EventLoopType.SYNC
)
```

**When to use:**
- For testing
- For simple synchronous applications
- When using the DictRenderer for debugging

**Behavior:**
- No asyncio integration
- Reactive updates are processed synchronously
- Simpler but less flexible than DEFAULT mode

## Complete Examples

### Basic PySide Application

```python
from PySide6 import QtWidgets
import collagraph as cg

class CounterApp(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1

# In practice, you'd use a .cgx template file
# This example shows the programmatic approach

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    gui = cg.Collagraph(renderer=cg.PySideRenderer())
    gui.render(CounterApp, app)
    app.exec()
```

### Using .cgx Component Files

The recommended way to use Collagraph is with `.cgx` component files:

**counter.cgx:**
```xml
<template>
  <widget>
    <label :text="f'Count: {count}'" />
    <button text="Increment" @clicked="increment" />
  </widget>
</template>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1
</script>
```

**Run with CLI:**
```bash
python -m collagraph counter.cgx
```

**Or programmatically:**
```python
from PySide6 import QtWidgets
import collagraph as cg
from counter import Counter  # Imported from counter.cgx

app = QtWidgets.QApplication()
gui = cg.Collagraph(renderer=cg.PySideRenderer())
gui.render(Counter, app)
app.exec()
```

## See Also

- [Quick Start](../getting-started/quick-start.md)
- [Renderers](../renderers/overview.md)
