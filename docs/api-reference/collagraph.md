# Collagraph Class

> **TODO**: Complete API reference for the Collagraph class.

## Class: `cg.Collagraph`

Main class for running Collagraph applications.

## Constructor

```python
Collagraph(
    component: Type[Component],
    renderer: Type[Renderer],
    event_loop_type: EventLoopType = EventLoopType.NATIVE
)
```

### Parameters

- `component`: The root component class
- `renderer`: The renderer class (e.g., `PySideRenderer`)
- `event_loop_type`: Type of event loop to use (default: `EventLoopType.NATIVE`)

## Methods

### `run(self, **props)`
Start the application.

```python
app = cg.Collagraph(MyApp, PySideRenderer)
app.run(title="My App")
```

## Event Loop Types

- `EventLoopType.NATIVE`: Use the renderer's native event loop
- `EventLoopType.ASYNCIO`: Use Python's asyncio event loop

## Example

```python
import collagraph as cg
from collagraph.renderers import PySideRenderer

class App(cg.Component):
    def render(self):
        return {"type": "label", "text": "Hello, World!"}

if __name__ == "__main__":
    app = cg.Collagraph(App, PySideRenderer)
    app.run()
```

## See Also

- [Quick Start](../getting-started/quick-start.md)
- [Renderers](../renderers/overview.md)
