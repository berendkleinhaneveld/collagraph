# Lifecycle Hooks

> **TODO**: Document component lifecycle hooks.

## Overview

Lifecycle hooks are methods that run at specific points in a component's life.

## Topics to Cover

- `init()` - Component initialization
- `mounted()` - After component is added to DOM
- `updated()` - After component updates
- `before_unmount()` - Before component is removed
- Use cases for each hook
- Async lifecycle hooks
- Best practices

## Available Hooks

```python
class MyComponent(cg.Component):
    def init(self):
        """Called when component is created"""
        self.state["data"] = []

    def mounted(self):
        """Called after component is mounted to DOM"""
        # Fetch data, set up subscriptions, etc.
        pass

    def updated(self):
        """Called after component updates"""
        # React to state/prop changes
        pass

    def before_unmount(self):
        """Called before component is unmounted"""
        # Clean up subscriptions, timers, etc.
        pass
```

## See Also

- [Components](components.md)
- [Reactivity System](reactivity.md)
