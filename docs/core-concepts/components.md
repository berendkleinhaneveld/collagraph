# Components

> **TODO**: Comprehensive guide to Collagraph components.

## Overview

Components are the building blocks of Collagraph applications. Each component is a Python class that extends `cg.Component`.

## Topics to Cover

- Component class structure
- The `render()` method
- Component registration
- Component composition
- Props vs State
- Component communication
- Best practices

## Basic Structure

```python
import collagraph as cg

class MyComponent(cg.Component):
    def init(self):
        # Initialize component state
        pass

    def render(self):
        # Return UI definition
        return {"type": "label", "text": "Hello"}
```

## See Also

- [Props](props.md)
- [State Management](state-management.md)
- [Lifecycle Hooks](lifecycle.md)
