# Provide/Inject

> **TODO**: Document dependency injection pattern.

## Overview

Provide/inject allows ancestor components to provide data to all descendants without prop drilling.

## Topics to Cover

- Providing values with `self.provide()`
- Injecting values with `self.inject()`
- Use cases
- Provide/inject vs props
- Type safety considerations

## Basic Usage

```python
# Ancestor component
class App(cg.Component):
    def init(self):
        self.provide("theme", "dark")
        self.provide("user", {"name": "Alice"})

# Descendant component (any level deep)
class ThemedButton(cg.Component):
    def init(self):
        self.theme = self.inject("theme")
        self.user = self.inject("user")
```

## See Also

- [Components](components.md)
- [Props](props.md)
- [State Management](state-management.md)
