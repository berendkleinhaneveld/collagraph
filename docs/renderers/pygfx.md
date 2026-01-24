# Pygfx Renderer

> **TODO**: Complete guide to the Pygfx renderer for 3D graphics.

## Overview

The Pygfx renderer enables 3D graphics and visualization using the Pygfx library.

## Installation

```bash
pip install collagraph[pygfx]
```

## Basic Usage

```python
import collagraph as cg
from collagraph.renderers import PygfxRenderer

class Scene3D(cg.Component):
    def render(self):
        return {
            "type": "scene",
            "children": [
                {
                    "type": "mesh",
                    "geometry": "sphere",
                    "material": {"color": "red"}
                }
            ]
        }

app = cg.Collagraph(Scene3D, PygfxRenderer)
app.run()
```

## Topics to Cover

- Available 3D objects
- Materials and textures
- Lighting
- Cameras
- Animations
- Combining with PySide
- Performance optimization

## See Also

- [3D Graphics Guide](../guides/pygfx-3d.md)
- [Examples](../examples/3d-visualization.md)
