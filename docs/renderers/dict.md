# Dict Renderer

> **TODO**: Guide to the Dict renderer for testing.

## Overview

The Dict renderer converts components into nested Python dictionaries, useful for testing and debugging.

## Usage

```python
import collagraph as cg
from collagraph.renderers import DictRenderer

class MyComponent(cg.Component):
    def render(self):
        return {"type": "label", "text": "Hello"}

result = cg.Collagraph(MyComponent, DictRenderer).run()
print(result)
# Output: {"type": "label", "text": "Hello"}
```

## Use Cases

- Unit testing components
- Debugging component structure
- Serializing UI definitions
- Validating component output

## Topics to Cover

- Testing with DictRenderer
- Inspecting component output
- Validation

## See Also

- [Testing Guide](../guides/testing.md)
- [Renderers Overview](overview.md)
