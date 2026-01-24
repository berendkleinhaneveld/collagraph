# Slots (v-slot)

> **TODO**: Document slot system for component composition.

## Overview

Slots allow parent components to pass content to child components.

## Topics to Cover

- Default slots
- Named slots
- Scoped slots
- Slot props
- Fallback content
- Multiple slots

## Basic Usage

```html
<!-- Parent -->
<Card>
  <label text="Card content" />
</Card>

<!-- Card component -->
<v-box>
  <slot />
</v-box>
```

## Named Slots

```html
<!-- Parent -->
<Card>
  <template v-slot:header>
    <label text="Header" />
  </template>
  <template v-slot:footer>
    <label text="Footer" />
  </template>
</Card>

<!-- Card component -->
<v-box>
  <slot name="header" />
  <slot />
  <slot name="footer" />
</v-box>
```

## See Also

- [Components](../components.md)
- [Template Syntax](../template-syntax.md)
