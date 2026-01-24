# List Rendering (v-for)

> **TODO**: Document v-for directive for rendering lists.

## Overview

The `v-for` directive renders a list of elements based on an array or iterable.

## Topics to Cover

- Basic list rendering
- Accessing index
- Using keys for performance
- Nested v-for loops
- v-for with objects
- v-for with ranges

## Basic Usage

```html
<label v-for="item in items" :text="item.name" :key="item.id" />
```

## With Index

```html
<label v-for="(item, index) in items" :text="f'{index}: {item}'" />
```

## See Also

- [Template Syntax](../template-syntax.md)
- [v-if Directive](v-if.md)
