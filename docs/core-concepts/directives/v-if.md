# Conditional Rendering (v-if)

## Overview

The `v-if` directive conditionally renders elements based on a boolean expression. Elements with `v-if` are only mounted when the condition is truthy and are completely removed from the DOM when the condition is falsy. This makes `v-if` a true conditional rendering mechanism.

## Basic Usage

The simplest form of `v-if` evaluates a boolean expression and renders the element only when the expression is truthy:

```html
<label text="Logged in" v-if="is_authenticated" />
```

In this example, the label will only be rendered when `is_authenticated` is truthy. When the value changes from truthy to falsy, the element is unmounted and removed from the DOM.

## Using v-else

The `v-else` directive provides an alternative element to render when the preceding `v-if` condition is falsy. The `v-else` element must immediately follow a `v-if` or `v-else-if` element:

```html
<label text="Logged in" v-if="is_authenticated" />
<label text="Please log in" v-else />
```

This pattern ensures that exactly one of the two labels is rendered at any time.

## Multiple Conditions with v-else-if

For multiple conditional branches, use `v-else-if` to chain conditions together:

```html
<label text="Admin" v-if="role == 'admin'" />
<label text="User" v-else-if="role == 'user'" />
<label text="Guest" v-else />
```

You can have multiple `v-else-if` blocks in sequence:

```html
<widget v-if="status == 'loading'">
  <label text="Loading..." />
</widget>
<widget v-else-if="status == 'error'">
  <label text="Error occurred" />
</widget>
<widget v-else-if="status == 'empty'">
  <label text="No data available" />
</widget>
<widget v-else>
  <label :text="f'Data: {data}'" />
</widget>
```

## Conditional Rendering with Children

Elements with `v-if` can contain children, and all children will be conditionally rendered:

```html
<widget v-if="show_panel">
  <label text="Panel Title" />
  <button text="Action" @clicked="handle_action" />
  <label :text="status" />
</widget>
```

When `show_panel` becomes falsy, the entire widget and all its children are unmounted.

## Combining v-if with v-for

You can use `v-if` and `v-for` together, though they should not be on the same element. Instead, wrap the `v-for` element with a container that has `v-if`:

```html
<widget v-if="items">
  <label
    v-for="item in items"
    :key="item['id']"
    :text="item['name']"
  />
</widget>
```

You can also use `v-if` on individual items within a list:

```html
<widget>
  <label
    v-for="item in items"
    :key="item['id']"
    v-if="item['visible']"
    :text="item['name']"
  />
</widget>
```

## Nested Conditional Rendering

Conditional directives can be nested to create complex conditional logic:

```html
<widget v-if="user">
  <label :text="user['name']" />
  <label text="Premium User" v-if="user['is_premium']" />
  <button text="Upgrade" v-else />
</widget>
<widget v-else>
  <label text="Please log in" />
</widget>
```

## Performance Considerations

### Efficient Mounting and Unmounting

Collagraph optimizes `v-if` by only remounting elements when the truthiness of the condition actually changes. If a condition depends on reactive state that changes but the truthiness remains the same, the element is not remounted:

```python
# Condition: count > 0
# count changes from 1 to 2: both are truthy, NO remount
# count changes from 2 to 0: truthy to falsy, remount occurs
# count changes from 0 to 5: falsy to truthy, remount occurs
```

This optimization preserves component state and avoids unnecessary lifecycle calls:

```html
<Counter v-if="count > 0" :value="count" />
```

When `count` changes from 1 to 2, the `Counter` component's `init()` and `mounted()` lifecycle hooks are not called again, but `updated()` is called because the `:value` prop changed.

### Reusing Elements

When the condition changes, Collagraph efficiently manages the DOM by:
- **Removing** elements when the condition becomes falsy
- **Adding** elements when the condition becomes truthy
- **Preserving** element order when conditions change between `v-if`, `v-else-if`, and `v-else` branches

## Best Practices

### Use v-if for Conditional Components

When you need to conditionally render entire components with their own state and lifecycle:

```html
<AdminPanel v-if="user_role == 'admin'" />
<UserDashboard v-else-if="user_role == 'user'" />
<GuestView v-else />
```

### Filter Data Instead of Using v-if in Loops

Instead of using `v-if` inside `v-for`, consider filtering your data first:

**Less efficient:**
```html
<label
  v-for="item in all_items"
  :key="item['id']"
  v-if="item['active']"
  :text="item['name']"
/>
```

**More efficient:**
```python
# In component
def init(self):
    self.active_items = [item for item in all_items if item['active']]
```

```html
<label
  v-for="item in active_items"
  :key="item['id']"
  :text="item['name']"
/>
```

### Use Meaningful Condition Names

Create computed properties or component methods for complex conditions:

```python
class MyComponent(cg.Component):
    def init(self):
        self.state['show_advanced'] = self.should_show_advanced()

    def should_show_advanced(self):
        return self.props.get('user_level') == 'expert' and self.props.get('feature_enabled')
```

```html
<AdvancedSettings v-if="show_advanced" />
```

## Edge Cases and Gotchas

### v-else and v-else-if Must Follow v-if

The `v-else` and `v-else-if` directives must immediately follow an element with `v-if` or `v-else-if`. Having any other element in between will break the conditional chain:

**Incorrect:**
```html
<label text="A" v-if="condition" />
<button text="Click" />
<label text="B" v-else />  <!-- This won't work! -->
```

**Correct:**
```html
<label text="A" v-if="condition" />
<label text="B" v-else />
<button text="Click" />
```

### Truthiness Evaluation

Collagraph uses Python's truthiness evaluation. The following values are considered falsy:
- `None`
- `False`
- `0`
- `0.0`
- `''` (empty string)
- `[]` (empty list)
- `{}` (empty dict)

All other values are truthy:

```python
v-if="[]"          # False - empty list
v-if="[1, 2]"      # True - non-empty list
v-if="0"           # False
v-if="1"           # True
v-if="''"          # False - empty string
v-if="'hello'"     # True - non-empty string
```

### Expressions in Conditions

You can use any Python expression in `v-if`:

```html
<label text="Even" v-if="count % 2 == 0" />
<label text="Ready" v-if="is_loaded and not has_errors" />
<label text="Valid" v-if="len(items) > 0 and all(item['valid'] for item in items)" />
```

### Multiple Independent v-if Chains

You can have multiple independent `v-if` chains in the same parent:

```html
<widget>
  <label text="A" v-if="show_a" />
  <label text="Not A" v-else />

  <label text="B" v-if="show_b" />
  <label text="Not B" v-else />
</widget>
```

This creates two separate conditional chains, each working independently.

## Common Patterns

### Loading States

```html
<widget v-if="is_loading">
  <label text="Loading..." />
</widget>
<widget v-else-if="error">
  <label :text="f'Error: {error}'" />
</widget>
<widget v-else>
  <DataView :data="data" />
</widget>
```

### Feature Flags

```html
<ExperimentalFeature v-if="props.get('enable_experimental', False)" />
```

### Authentication and Authorization

```html
<AdminTools v-if="user and user['role'] == 'admin'" />
<button text="Login" v-if="not user" @clicked="show_login" />
```

### Empty States

```html
<widget v-if="items">
  <label v-for="item in items" :key="item['id']" :text="item['name']" />
</widget>
<widget v-else>
  <label text="No items to display" />
</widget>
```

## See Also

- [Template Syntax](../template-syntax.md)
- [v-for Directive](v-for.md)
- [Reactivity](../reactivity.md)
- [Component Lifecycle](../lifecycle.md)
