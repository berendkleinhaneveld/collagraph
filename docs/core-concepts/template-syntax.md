# Template Syntax

## Overview

Collagraph uses HTML-like template syntax similar to Vue.js, making it familiar to web developers while bringing reactive UI patterns to Python desktop and graphics applications. Templates are defined in `.cgx` (Collagraph eXtension) files and support dynamic attribute binding, event handling, and control flow directives.

## Basic HTML-Like Syntax

Templates use XML/HTML-like syntax to define UI elements:

```html
<widget>
  <label text="Hello, World!" />
  <button text="Click me" />
  <input value="Type here..." />
</widget>
```

Elements can be self-closing or have closing tags:

```html
<!-- Self-closing -->
<label text="Title" />

<!-- With closing tag -->
<widget>
  <label text="Content" />
</widget>
```

## Attribute Binding

### Static Attributes

Static attributes are defined with plain attribute syntax:

```html
<label text="Static text" />
<button enabled="True" width="100" />
```

### Dynamic Attributes (`:attribute`)

Use the `:` prefix to bind attributes to reactive data. The attribute value is evaluated as a Python expression:

```html
<label :text="message" />
<button :enabled="is_active" />
<input :value="user_input" />
```

You can use any Python expression:

```html
<label :text="f'Count: {count}'" />
<button :disabled="count >= max_count" />
<widget :style="{'background': 'red' if error else 'green'}" />
```

### v-bind Directive

The `v-bind` directive spreads all properties from an object as attributes:

```html
<!-- Spread all props from an object -->
<ChildComponent v-bind="user_data" />

<!-- Equivalent to manually passing each prop -->
<ChildComponent
  :name="user_data['name']"
  :age="user_data['age']"
  :email="user_data['email']"
/>
```

You can also combine `v-bind` with explicit props:

```html
<!-- Spread props and override specific ones -->
<ChildComponent
  v-bind="default_props"
  :name="custom_name"
/>
```

## Event Handling

### Basic Event Handling (`@event`)

Use the `@` prefix to attach event handlers:

```html
<button text="Click me" @clicked="handle_click" />
<input @changed="handle_change" />
<list-view @selection-changed="handle_selection" />
```

In your component:

```python
class MyComponent(cg.Component):
    def handle_click(self):
        print("Button clicked!")

    def handle_change(self):
        print("Input changed!")
```

### Inline Event Handlers

You can use inline expressions or lambda functions:

```html
<!-- Inline lambda -->
<button @clicked="lambda: state['count'] += 1" text="Increment" />

<!-- Call method with arguments -->
<button @clicked="lambda: set_value(42)" text="Set to 42" />

<!-- Multiple statements -->
<button
  @clicked="lambda: [state['count'] += 1, print('Clicked!')]"
  text="Click"
/>
```

### Event Arguments

Events can pass arguments to handlers:

```html
<!-- In v-for, capture loop variable in lambda -->
<button
  v-for="item in items"
  :text="item"
  @clicked="lambda: handle_item_click(item)"
/>
```

In your component:

```python
class MyComponent(cg.Component):
    def handle_item_click(self, item):
        print(f"Clicked on {item}")
```

## Directives

### v-if Directive

Conditionally render elements based on an expression:

```html
<label v-if="show_message" text="Hello!" />
<label v-if="count > 10" text="Count is high" />
<widget v-if="user is not None">
  <label :text="user['name']" />
</widget>
```

When the condition is `False`, the element is not rendered at all (removed from the DOM).

### v-else and v-else-if Directives

Chain conditional rendering:

```html
<label v-if="status == 'loading'" text="Loading..." />
<label v-else-if="status == 'error'" text="Error occurred" />
<label v-else text="Content loaded" />
```

### v-for Directive

Render elements in a loop:

```html
<!-- Iterate over a list -->
<label
  v-for="item in items"
  :text="item"
/>

<!-- Iterate with index -->
<label
  v-for="idx, item in enumerate(items)"
  :text="f'{idx}: {item}'"
/>

<!-- Iterate over dictionaries -->
<label
  v-for="key, value in data.items()"
  :text="f'{key}: {value}'"
/>

<!-- Iterate over ranges -->
<button
  v-for="i in range(5)"
  :text="f'Button {i}'"
/>
```

### Keyed Lists

For better performance with dynamic lists, use the `:key` attribute:

```html
<item
  v-for="item in items"
  :key="item['id']"
  v-bind="item"
/>
```

Keys help Collagraph identify which items have changed, been added, or been removed.

### Combining Directives

Directives can be combined on the same element:

```html
<!-- Only render button in loop if condition is met -->
<button
  v-for="item in items"
  v-if="item['enabled']"
  :text="item['label']"
  @clicked="lambda: handle_click(item)"
/>
```

## Template Expressions

Template expressions are Python code evaluated in the component's context. You can access:

- **State**: `state['variable']` or just `variable` (via automatic lookup)
- **Props**: `props['name']` or just `name`
- **Methods**: `method_name()`
- **Refs**: `refs['refName']` or just `refName`
- **Global context**: Any variables passed to `gui.render()`

### Automatic Variable Lookup

Collagraph automatically looks up variables in this order:
1. Component props (`self.props`)
2. Component state (`self.state`)
3. Component refs (`self.refs`)
4. Component attributes (`self.attribute`)
5. Global context

This means you can write:

```html
<!-- Instead of self.state['message'] -->
<label :text="message" />

<!-- Instead of self.props['title'] -->
<label :text="title" />

<!-- Methods work too -->
<button @clicked="increment" text="Click" />
```

### Python Expressions

You can use full Python expressions:

```html
<!-- String formatting -->
<label :text="f'Total: {sum(items)}'" />

<!-- List comprehensions -->
<widget :data="[x * 2 for x in range(10)]" />

<!-- Conditionals -->
<label :text="'Even' if count % 2 == 0 else 'Odd'" />

<!-- Function calls -->
<label :text="str.upper(message)" />

<!-- Dictionary/list access -->
<label :text="users[0]['name']" />
```

## Python f-strings in Templates

You can use Python f-strings directly in dynamic attributes:

```html
<label :text="f'Hello, {name}!'" />
<label :text="f'Count: {count} / {max_count}'" />
<label :text="f'{percentage:.2f}%'" />
```

F-strings are especially useful for formatting complex expressions:

```html
<label :text="f'User {user['id']}: {user['name']} ({user['status']})'"/>
```

## Text Interpolation

For text content within elements, use dynamic text binding:

```html
<!-- Using :text attribute -->
<label :text="message" />

<!-- Using f-strings for complex formatting -->
<label :text="f'Total: ${total:.2f}'" />
```

## Comments

Use HTML-style comments in templates:

```html
<!-- This is a comment -->
<widget>
  <!-- Components can have comments too -->
  <label text="Visible" />
  <!-- <label text="Commented out" /> -->
</widget>
```

Comments are stripped during compilation and don't affect the rendered output.

## Complete Example

Here's a comprehensive example showing various template syntax features:

```html
<window title="Template Syntax Demo" width="400" height="300">
  <widget>
    <!-- Static and dynamic attributes -->
    <label text="Welcome!" />
    <label :text="f'Hello, {username}!'" />

    <!-- Conditional rendering -->
    <label v-if="is_logged_in" text="You are logged in" />
    <label v-else text="Please log in" />

    <!-- List rendering with events -->
    <widget v-for="idx, item in enumerate(items)">
      <label :text="f'{idx + 1}. {item['name']}'" />
      <button
        text="Delete"
        @clicked="lambda: delete_item(idx)"
      />
    </widget>

    <!-- Event handling -->
    <button text="Add Item" @clicked="add_item" />
    <button text="Clear All" @clicked="clear_items" />

    <!-- Dynamic styling -->
    <label
      :text="status_message"
      :style="{'color': 'green' if success else 'red'}"
    />
  </widget>
</window>

<script>
import collagraph as cg

class TemplateSyntaxDemo(cg.Component):
    def init(self):
        self.state["username"] = "Alice"
        self.state["is_logged_in"] = True
        self.state["items"] = [
            {"name": "Item 1"},
            {"name": "Item 2"},
        ]
        self.state["success"] = True
        self.state["status_message"] = "All good!"

    def add_item(self):
        new_id = len(self.state["items"]) + 1
        self.state["items"].append({"name": f"Item {new_id}"})

    def delete_item(self, idx):
        self.state["items"].pop(idx)

    def clear_items(self):
        self.state["items"].clear()
</script>
```

## See Also

- [v-if Directive](directives/v-if.md)
- [v-for Directive](directives/v-for.md)
- [v-bind Directive](directives/v-bind.md)
- [v-on Directive](directives/v-on.md)
