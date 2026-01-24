# Renderers Overview

> **TODO**: Overview of Collagraph's renderer system.

## What are Renderers?

Renderers are backends that convert Collagraph's component tree into actual UI elements. Collagraph supports multiple renderers for different use cases.

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

```python
import collagraph as cg
from collagraph.renderers import PySideRenderer

app = cg.Collagraph(MyComponent, PySideRenderer)
app.run()
```

## See Also

- [Creating Custom Renderers](custom-renderer.md)
- [Renderer API](../api-reference/renderer.md)
