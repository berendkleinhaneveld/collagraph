# Reactivity System

> **TODO**: Document how Collagraph's reactivity system works, based on the `observ` library.

## Overview

Collagraph uses the `observ` library to provide reactive state management. When state changes, the UI automatically updates.

## Topics to Cover

- How reactivity works under the hood
- Observable dictionaries and lists
- Reactive dependencies
- Performance considerations
- Integration with the `observ` library
- Computed properties
- Watchers

## Basic Example

```python
class MyComponent(cg.Component):
    def init(self):
        # This creates a reactive state
        self.state["count"] = 0

    def increment(self):
        # Modifying state triggers re-render
        self.state["count"] += 1
```

## See Also

- [State Management](state-management.md)
- [Computed Properties](computed.md)
- [Watchers](watchers.md)
