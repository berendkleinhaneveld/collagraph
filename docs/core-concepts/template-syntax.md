# Template Syntax

> **TODO**: Document Collagraph's Vue-like template syntax.

## Overview

Collagraph uses HTML-like template syntax similar to Vue.js, with special directives for dynamic behavior.

## Topics to Cover

- Basic HTML-like syntax
- Attribute binding (`:attribute`)
- Event handling (`@event`)
- Directives (`v-if`, `v-for`, etc.)
- Template expressions
- Python f-strings in templates
- Comments

## Basic Syntax

```html
<label :text="message" />
<button text="Click" @clicked="handle_click" />
<div v-if="show_content">Content</div>
```

## See Also

- [v-if Directive](directives/v-if.md)
- [v-for Directive](directives/v-for.md)
- [v-bind Directive](directives/v-bind.md)
- [v-on Directive](directives/v-on.md)
