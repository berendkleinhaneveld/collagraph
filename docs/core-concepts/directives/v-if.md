# Conditional Rendering (v-if)

> **TODO**: Document v-if, v-else-if, v-else directives.

## Overview

The `v-if` directive conditionally renders elements based on a boolean expression.

## Topics to Cover

- Basic `v-if` usage
- `v-else-if` for multiple conditions
- `v-else` for fallback
- Performance considerations
- v-if vs v-show (if applicable)

## Basic Usage

```html
<label text="Logged in" v-if="is_authenticated" />
<label text="Please log in" v-else />
```

## Multiple Conditions

```html
<label text="Admin" v-if="role == 'admin'" />
<label text="User" v-else-if="role == 'user'" />
<label text="Guest" v-else />
```

## See Also

- [Template Syntax](../template-syntax.md)
- [v-for Directive](v-for.md)
