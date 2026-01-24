# Example: Counter

> **TODO**: Complete counter example with explanations.

## Overview

A simple counter application demonstrating state management and event handling.

## Code

```html
<window title="Counter">
  <v-box>
    <label :text="f'Count: {count}'" />
    <h-box>
      <button text="Increment" @clicked="increment" />
      <button text="Decrement" @clicked="decrement" />
      <button text="Reset" @clicked="reset" />
    </h-box>
  </v-box>
</window>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1

    def decrement(self):
        self.state["count"] -= 1

    def reset(self):
        self.state["count"] = 0
</script>
```

## Topics Covered

- State management
- Event handling
- Reactive bindings
- Layout components

## See Also

- [Quick Start](../getting-started/quick-start.md)
- [State Management](../core-concepts/state-management.md)
