# Attribute Binding (v-bind, :)

## Overview

The `v-bind` directive dynamically binds element attributes to JavaScript expressions. Instead of using static attribute values, `v-bind` allows you to use reactive data, computed values, and complex expressions. The `:` prefix is a convenient shorthand for `v-bind:`.

## Basic Usage

The most common use of `v-bind` is to bind a single attribute to an expression:

```html
<!-- Full syntax -->
<label v-bind:text="message" />

<!-- Shorthand syntax (preferred) -->
<label :text="message" />
```

Both forms are equivalent, but the `:` shorthand is more concise and commonly used.

## Binding to Different Data Sources

### Component State

```html
<label :text="state['message']" />
```

```python
class MyComponent(cg.Component):
    def init(self):
        self.state['message'] = "Hello, World!"
```

### Component Props

```html
<label :text="props['title']" />
```

Props are passed to the component from its parent:

```html
<MyComponent title="Hello" />
```

### Component Properties

```html
<label :text="message" />
```

```python
class MyComponent(cg.Component):
    def __init__(self, props):
        super().__init__(props)
        self.message = "Hello from property"
```

### Component Methods

```html
<label :text="get_greeting()" />
```

```python
class MyComponent(cg.Component):
    def get_greeting(self):
        return f"Hello, {self.props.get('name', 'World')}"
```

### Module-Level Variables

```html
<label :text="GREETING" />
```

```python
GREETING = "Hello from module"

class MyComponent(cg.Component):
    pass
```

## Dynamic Expressions

You can use any Python expression in a binding:

### String Formatting

```html
<label :text="f'Count: {count}'" />
<label :text="f'{user['name']} ({user['email']})'" />
```

### Conditional Expressions

```html
<button :enabled="count > 0" />
<label :text="'Active' if is_active else 'Inactive'" />
```

### Arithmetic Operations

```html
<label :text="f'Total: {price * quantity}'" />
<progress :value="completed / total * 100" />
```

### Boolean Logic

```html
<button :enabled="is_loaded and not has_errors" />
<widget :visible="user and user['is_premium']" />
```

### List/Dict Operations

```html
<label :text="f'Items: {len(items)}'" />
<button :enabled="'admin' in user['roles']" />
```

## Binding Objects and Dictionaries

You can bind complete dictionaries or objects to attributes:

```html
<widget :layout="{'type': 'box', 'direction': Direction.LeftToRight}" />
<label :style="style_config" />
```

```python
from enum import Enum

class Direction(Enum):
    LeftToRight = 0
    RightToLeft = 1

class MyComponent(cg.Component):
    def init(self):
        self.state['style_config'] = {
            'color': 'blue',
            'size': 'large'
        }
```

## Binding Multiple Attributes

### Using v-bind Without an Argument

You can bind all properties from an object to an element using `v-bind` without specifying an attribute name:

```html
<widget v-bind="config" />
```

```python
class MyComponent(cg.Component):
    def init(self):
        self.state['config'] = {
            'width': 300,
            'height': 200,
            'title': 'My Widget'
        }
```

This is equivalent to:

```html
<widget :width="300" :height="200" :title="'My Widget'" />
```

### Combining Individual and Spread Binding

You can combine `v-bind` (spread) with individual attribute bindings. The order matters:

```html
<!-- Individual binding takes precedence (text='other') -->
<label v-bind="props" :text="other" />

<!-- Spread binding takes precedence (text from props) -->
<label :text="other" v-bind="props" />
```

```python
# If props = {"text": "foo", "color": "red"}
# and other = "bar"

# First example: text="bar", color="red"
# Second example: text="foo", color="red"
```

## Reactive Updates

Bindings are reactive, meaning they automatically update when the bound data changes:

```python
from observ import reactive

class Counter(cg.Component):
    def init(self):
        self.state['count'] = reactive(0)

    def increment(self):
        self.state['count'] += 1  # Automatically updates the view
```

```html
<label :text="f'Count: {count}'" />
<button text="Increment" @clicked="increment" />
```

When `count` changes, the label's text is automatically updated.

## Binding with v-for

Bindings work seamlessly inside `v-for` loops, with access to the loop variable:

```html
<label
  v-for="user in users"
  :key="user['id']"
  :text="user['name']"
  :enabled="user['active']"
/>
```

You can also use the index:

```html
<label
  v-for="i, item in enumerate(items)"
  :key="item['id']"
  :text="f'{i + 1}. {item['name']}'"
/>
```

## Common Binding Patterns

### Computed Values

```html
<label :text="full_name" />
```

```python
class UserProfile(cg.Component):
    @property
    def full_name(self):
        return f"{self.state['first_name']} {self.state['last_name']}"
```

### Conditional Attributes

```html
<button
  :enabled="form_is_valid"
  :text="'Submit' if form_is_valid else 'Please complete form'"
/>
```

### Formatted Data

```html
<label :text="format_date(created_at)" />
<label :text="format_currency(price)" />
```

```python
from datetime import datetime

class MyComponent(cg.Component):
    def format_date(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    def format_currency(self, amount):
        return f'${amount:.2f}'
```

### Nested Property Access

```html
<label :text="user['profile']['bio']" />
<image :src="product['images'][0]['url']" />
```

### Using External Libraries

```html
<label :text="cg.__version__" />
```

```python
import collagraph as cg

class MyComponent(cg.Component):
    pass
```

## Best Practices

### Use Descriptive Property Names

Make your component's data structure clear and meaningful:

```python
# Good
self.state['user_email'] = "user@example.com"
self.state['is_loading'] = True
self.state['error_message'] = None

# Less clear
self.state['e'] = "user@example.com"
self.state['l'] = True
self.state['err'] = None
```

### Prefer Properties for Computed Values

Instead of complex expressions in templates, use properties:

**Less maintainable:**
```html
<label :text="f'{state['first']} {state['last']} ({state['email']})' if state['show_full'] else state['first']" />
```

**More maintainable:**
```python
@property
def display_name(self):
    if self.state['show_full']:
        return f"{self.state['first']} {self.state['last']} ({self.state['email']})"
    return self.state['first']
```

```html
<label :text="display_name" />
```

### Handle Missing Data Gracefully

Use `.get()` with defaults for optional props:

```html
<label :text="props.get('title', 'Untitled')" />
<widget :enabled="props.get('interactive', True)" />
```

### Keep Expressions Simple

If an expression is complex, move it to a method or property:

```html
<!-- Avoid -->
<label :text="' '.join([item['name'] for item in items if item['active'] and item['priority'] > 5])" />

<!-- Better -->
<label :text="get_high_priority_names()" />
```

```python
def get_high_priority_names(self):
    active_high_priority = [
        item['name']
        for item in self.state['items']
        if item['active'] and item['priority'] > 5
    ]
    return ' '.join(active_high_priority)
```

### Use Type-Safe Access

When accessing nested data, consider safety:

```python
# Unsafe - may raise KeyError or AttributeError
:text="user['profile']['bio']"

# Safer
:text="user.get('profile', {}).get('bio', 'No bio available')"

# Or use a method
@property
def user_bio(self):
    return self.state.get('user', {}).get('profile', {}).get('bio', 'No bio available')
```

## Edge Cases and Gotchas

### Binding to None

Binding an attribute to `None` may behave differently depending on the renderer:

```html
<label :text="None" />  <!-- May render as empty or "None" -->
```

It's often better to use empty strings or check for None:

```html
<label :text="message or ''" />
<label :text="message if message is not None else ''" />
```

### Truthiness in Bindings

Python's truthiness rules apply:

```html
<button :enabled="[]" />  <!-- False - empty list -->
<button :enabled="[1]" />  <!-- True - non-empty list -->
<button :enabled="0" />    <!-- False -->
<button :enabled="1" />    <!-- True -->
```

### String Concatenation

Be careful with string concatenation—use f-strings instead:

```html
<!-- Avoid -->
<label :text="'Hello, ' + name + '!'" />

<!-- Prefer -->
<label :text="f'Hello, {name}!'" />
```

### Binding to Mutable Objects

When binding to mutable objects (lists, dicts), mutations won't always trigger updates unless using reactive objects:

```python
# Won't trigger update
self.state['items'].append(new_item)  # Only works if items is reactive

# Will trigger update
from observ import reactive
self.state['items'] = reactive([...])
self.state['items'].append(new_item)  # Now it updates
```

### Expression Evaluation Errors

If an expression raises an error, it can break rendering. Handle potential errors:

```html
<!-- May raise KeyError -->
<label :text="user['email']" />

<!-- Safer -->
<label :text="user.get('email', 'No email')" />
```

### Dictionary Key Names

When using `v-bind` to spread a dictionary, keys must be valid attribute names:

```python
# This works
config = {"width": 100, "height": 200}

# This might not work (invalid attribute name)
config = {"my-custom-attr": "value"}  # Hyphens may cause issues
```

## Advanced Patterns

### Binding with Fallbacks

```html
<label :text="props.get('title') or state.get('title') or 'Default Title'" />
```

### Binding to Imported Constants

```html
<widget :mode="AppMode.ADVANCED" />
```

```python
from enum import Enum

class AppMode(Enum):
    BASIC = 1
    ADVANCED = 2

class MyComponent(cg.Component):
    pass
```

### Binding with Transformations

```html
<label :text="title.upper()" />
<label :text="description[:100]" />  <!-- Truncate -->
<list :items="sorted(items, key=lambda x: x['name'])" />
```

### Conditional Binding

```html
<widget
  :title="title if show_title else None"
  :enabled="not is_disabled"
/>
```

### Deep Merging Configurations

```html
<widget v-bind="default_config" v-bind="custom_config" />
```

This applies `default_config` first, then `custom_config`, with `custom_config` values overriding defaults.

## Comparison with Static Attributes

### Static Attributes

```html
<label text="Hello, World!" />
```

The value is fixed and never changes.

### Dynamic Bindings

```html
<label :text="message" />
```

The value updates when `message` changes.

### Mixed Usage

You can mix static and dynamic attributes:

```html
<widget
  type="container"
  :title="dynamic_title"
  color="blue"
  :width="calculated_width"
/>
```

## Performance Considerations

### Avoid Complex Expressions

Complex expressions are re-evaluated on every render. Cache results when possible:

```python
# Inefficient - recalculated every render
<label :text="expensive_calculation()" />

# Better - calculate once and cache
@property
def display_text(self):
    if not hasattr(self, '_cached_text'):
        self._cached_text = self.expensive_calculation()
    return self._cached_text
```

### Spread Binding Performance

Using `v-bind` to spread many attributes can impact performance. Be selective:

```html
<!-- If config has many attributes you don't need -->
<widget v-bind="config" />  <!-- May bind unnecessary attributes -->

<!-- Better - bind only what you need -->
<widget :width="config['width']" :height="config['height']" />
```

## See Also

- [Template Syntax](../template-syntax.md)
- [Component Props](../props.md)
- [Reactivity](../reactivity.md)
- [v-on Directive](v-on.md)
