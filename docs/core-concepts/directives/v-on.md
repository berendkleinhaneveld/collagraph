# Event Handling (v-on, @)

> **TODO**: Document event handling with v-on and @ shorthand.

## Overview

The `v-on` directive (or `@` shorthand) attaches event listeners to elements.

## Topics to Cover

- Basic event handling
- Shorthand syntax (`@`)
- Event arguments
- Event modifiers (if supported)
- Inline handlers vs method handlers
- Custom events

## Basic Usage

```html
<!-- Full syntax -->
<button text="Click" v-on:clicked="handle_click" />

<!-- Shorthand -->
<button text="Click" @clicked="handle_click" />
```

## Inline Handlers

```html
<button text="Increment" @clicked="lambda: self.state.__setitem__('count', count + 1)" />
```

## See Also

- [Events](../events.md)
- [Template Syntax](../template-syntax.md)
