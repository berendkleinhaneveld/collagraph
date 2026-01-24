# Single-File Components (.cgx)

> **TODO**: Document .cgx file format and usage.

## Overview

`.cgx` files allow you to define components with template and code in a single file, similar to Vue's `.vue` files.

## Topics to Cover

- File structure
- `<script>` tag
- Template section
- Importing components
- Module system
- Hot reloading support
- Syntax highlighting setup

## Basic Structure

```html
<template-content>
  <label :text="message" />
</template-content>

<script>
import collagraph as cg

class MyComponent(cg.Component):
    def init(self):
        self.state["message"] = "Hello"
</script>
```

## See Also

- [Installation](../getting-started/installation.md) (for editor setup)
- [Template Syntax](template-syntax.md)
