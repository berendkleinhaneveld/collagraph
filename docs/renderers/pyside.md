# PySide Renderer

> **TODO**: Complete guide to the PySide renderer.

## Overview

The PySide renderer allows you to build Qt desktop applications using Collagraph.

## Installation

```bash
pip install collagraph[pyside]
```

## Basic Usage

```python
import collagraph as cg
from collagraph.renderers import PySideRenderer

class App(cg.Component):
    def render(self):
        return {
            "type": "window",
            "title": "My App",
            "children": [{"type": "label", "text": "Hello"}]
        }

app = cg.Collagraph(App, PySideRenderer)
app.run()
```

## Topics to Cover

- Available widgets
- Layouts (v-box, h-box, grid, etc.)
- Windows and dialogs
- Menus and toolbars
- Advanced widgets (tree view, table, etc.)
- Custom Qt widgets
- Accessing raw Qt objects
- Styling and themes

## See Also

- [Available Widgets](pyside-widgets.md)
- [Layouts](pyside-layouts.md)
- [Dialogs & Windows](pyside-dialogs.md)
- [Advanced Components](pyside-advanced.md)
