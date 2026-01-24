# Template Refs

> **TODO**: Document template refs for accessing DOM elements.

## Overview

Template refs provide a way to directly access rendered elements and child components.

## Topics to Cover

- Creating refs with `ref` attribute
- Accessing refs via `self.refs`
- Refs to components vs elements
- When to use refs
- Limitations and best practices

## Basic Usage

```html
<input ref="inputField" />
<CustomComponent ref="childComponent" />

<script>
class MyComponent(cg.Component):
    def mounted(self):
        # Access the input element
        input_element = self.refs["inputField"]
        # Access the child component
        child = self.refs["childComponent"]
</script>
```

## See Also

- [Components](components.md)
- [Lifecycle Hooks](lifecycle.md)
