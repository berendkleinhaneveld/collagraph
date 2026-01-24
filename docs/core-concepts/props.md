# Props

> **TODO**: Document how to pass data to components via props.

## Overview

Props allow parent components to pass data to child components.

## Topics to Cover

- Accessing props via `self.props`
- Prop validation
- Default values
- Prop types
- One-way data flow
- Props vs state

## Basic Usage

```html
<!-- Parent component -->
<ChildComponent name="Alice" age="30" />

<!-- Child component -->
<script>
class ChildComponent(cg.Component):
    def init(self):
        self.name = self.props.get("name", "Guest")
        self.age = self.props.get("age", 0)
</script>
```

## See Also

- [Components](components.md)
- [State Management](state-management.md)
