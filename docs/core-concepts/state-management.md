# State Management

> **TODO**: Document how to manage component state.

## Overview

State is data that belongs to a component and can change over time. Collagraph provides reactive state management through `self.state`.

## Topics to Cover

- Creating state with `self.state`
- Reactive updates
- State initialization in `init()`
- Nested state objects
- State immutability
- Sharing state between components
- When to use state vs props

## Basic Usage

```python
class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0
        self.state["user"] = {"name": "Alice"}

    def increment(self):
        self.state["count"] += 1
```

## See Also

- [Reactivity System](reactivity.md)
- [Props](props.md)
- [Provide/Inject](provide-inject.md)
