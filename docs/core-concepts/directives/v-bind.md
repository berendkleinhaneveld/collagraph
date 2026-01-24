# Attribute Binding (v-bind, :)

> **TODO**: Document attribute binding with v-bind and : shorthand.

## Overview

The `v-bind` directive (or `:` shorthand) dynamically binds attributes to expressions.

## Topics to Cover

- Basic attribute binding
- Shorthand syntax (`:`)
- Binding multiple attributes
- Dynamic attribute names
- Class and style binding (if applicable)
- Binding objects

## Basic Usage

```html
<!-- Full syntax -->
<label v-bind:text="message" />

<!-- Shorthand -->
<label :text="message" />
```

## Dynamic Expressions

```html
<label :text="f'Count: {count}'" />
<button :enabled="count > 0" />
```

## See Also

- [Template Syntax](../template-syntax.md)
- [Props](../props.md)
