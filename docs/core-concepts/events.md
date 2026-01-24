# Events

> **TODO**: Document event handling and custom events.

## Overview

Events allow components to communicate with their parents and respond to user interactions.

## Topics to Cover

- Event handlers with `@event` syntax
- Built-in events (clicked, changed, etc.)
- Custom events with `self.emit()`
- Event arguments
- Event modifiers (if supported)
- Event bubbling

## Basic Usage

```html
<button text="Click" @clicked="handle_click" />

<script>
class MyComponent(cg.Component):
    def handle_click(self):
        print("Button clicked!")
        self.emit("custom-event", {"data": "value"})
</script>
```

## See Also

- [Template Syntax](template-syntax.md)
- [v-on Directive](directives/v-on.md)
