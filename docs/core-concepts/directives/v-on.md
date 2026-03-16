# Event Handling (v-on, @)

## Overview

The `v-on` directive attaches event listeners to elements, allowing your components to respond to user interactions and custom events. The `@` prefix is a convenient shorthand for `v-on:` and is the preferred syntax in most cases.

## Basic Usage

The simplest form of `v-on` attaches a method as an event handler:

```html
<!-- Full syntax -->
<button text="Click Me" v-on:clicked="handle_click" />

<!-- Shorthand syntax (preferred) -->
<button text="Click Me" @clicked="handle_click" />
```

```python
class MyComponent(cg.Component):
    def handle_click(self):
        print("Button was clicked!")
```

## Event Handler Types

### Method Handlers

The most common pattern is to reference a component method by name:

```html
<button text="Save" @clicked="save_data" />
<input @changed="on_input_change" />
<form @submitted="handle_submit" />
```

```python
class FormComponent(cg.Component):
    def save_data(self):
        print("Saving data...")

    def on_input_change(self):
        print("Input changed")

    def handle_submit(self):
        print("Form submitted")
```

### Lambda Expressions

For simple inline handlers or to pass arguments, use lambda expressions:

```html
<button text="Increment" @clicked="lambda: increment()" />
<button text="Add 5" @clicked="lambda: add_value(5)" />
<button text="Delete" @clicked="lambda: delete_item(item['id'])" />
```

```python
class Counter(cg.Component):
    def init(self):
        self.state['count'] = 0

    def increment(self):
        self.state['count'] += 1

    def add_value(self, value):
        self.state['count'] += value

    def delete_item(self, item_id):
        print(f"Deleting item {item_id}")
```

### Function References

You can reference module-level functions or pass function props:

```html
<button text="Process" @clicked="process_data" />
<button text="Custom" @clicked="props['on_custom_action']" />
```

```python
def process_data():
    print("Processing...")

class MyComponent(cg.Component):
    pass
```

## Event Arguments

Most UI events pass arguments to the handler. You can access these in your handler:

### Receiving Event Data

```html
<button text="Click" @clicked="handle_click" />
```

```python
class MyComponent(cg.Component):
    def handle_click(self, event=None):
        # Event data (if any) is passed as the first argument
        print(f"Event: {event}")
```

### Using Lambda to Capture Arguments

When using lambdas in loops or with specific data, capture the context:

```html
<button
  v-for="item in items"
  :key="item['id']"
  :text="item['name']"
  @clicked="lambda: handle_item_click(item)"
/>
```

```python
class ItemList(cg.Component):
    def handle_item_click(self, item):
        print(f"Clicked: {item['name']}")
```

### Passing Multiple Arguments

Lambdas allow you to pass multiple arguments or combine event data with custom data:

```html
<button text="Action" @clicked="lambda event: process_action(event, 'custom_data')" />
```

```python
class MyComponent(cg.Component):
    def process_action(self, event, custom_data):
        print(f"Event: {event}, Data: {custom_data}")
```

## Common Event Patterns

### State Updates

```html
<button text="Increment" @clicked="increment" />
<button text="Decrement" @clicked="decrement" />
<button text="Reset" @clicked="reset" />
```

```python
from observ import reactive

class Counter(cg.Component):
    def init(self):
        self.state['count'] = reactive(0)

    def increment(self):
        self.state['count'] += 1

    def decrement(self):
        self.state['count'] -= 1

    def reset(self):
        self.state['count'] = 0
```

### Form Handling

```html
<input :value="email" @changed="on_email_change" />
<button text="Submit" @clicked="submit_form" />
```

```python
class FormComponent(cg.Component):
    def init(self):
        self.state['email'] = ""

    def on_email_change(self, event):
        # Update state based on input
        self.state['email'] = event.text if hasattr(event, 'text') else event

    def submit_form(self):
        print(f"Submitting: {self.state['email']}")
```

### Navigation

```html
<button text="Home" @clicked="lambda: navigate('home')" />
<button text="Settings" @clicked="lambda: navigate('settings')" />
```

```python
class Navigation(cg.Component):
    def navigate(self, page):
        self.state['current_page'] = page
        print(f"Navigating to {page}")
```

### Dialog Control

```html
<button text="Open Dialog" @clicked="open_dialog" />
<dialog v-if="show_dialog">
  <button text="Close" @clicked="close_dialog" />
</dialog>
```

```python
class DialogExample(cg.Component):
    def init(self):
        self.state['show_dialog'] = False

    def open_dialog(self):
        self.state['show_dialog'] = True

    def close_dialog(self):
        self.state['show_dialog'] = False
```

## Event Handling in Lists

When rendering lists with `v-for`, use lambdas to capture the loop item:

```html
<widget v-for="user in users" :key="user['id']">
  <label :text="user['name']" />
  <button text="Edit" @clicked="lambda: edit_user(user)" />
  <button text="Delete" @clicked="lambda: delete_user(user['id'])" />
</widget>
```

```python
class UserList(cg.Component):
    def edit_user(self, user):
        print(f"Editing user: {user['name']}")
        self.state['editing_user'] = user

    def delete_user(self, user_id):
        print(f"Deleting user ID: {user_id}")
        self.state['users'] = [u for u in self.state['users'] if u['id'] != user_id]
```

### Alternative: Passing Callbacks

You can also pass callback functions in the loop:

```html
<button
  v-for="name, callback in buttons"
  :key="name"
  :text="name"
  @clicked="callback"
/>
```

```python
class Buttons(cg.Component):
    def init(self):
        self.state['buttons'] = [
            ('Save', self.save),
            ('Cancel', self.cancel),
            ('Delete', self.delete),
        ]

    def save(self):
        print("Save clicked")

    def cancel(self):
        print("Cancel clicked")

    def delete(self):
        print("Delete clicked")
```

## Component Events

Components can emit custom events that parent components can listen to:

### Child Component Emitting Events

```python
class ChildComponent(cg.Component):
    def do_something(self):
        # Emit event to parent through props
        if 'on_custom_event' in self.props:
            self.props['on_custom_event']('some data')
```

```html
<!-- In child template -->
<button text="Trigger Event" @clicked="do_something" />
```

### Parent Component Listening

```html
<ChildComponent @custom_event="handle_child_event" />
```

```python
class ParentComponent(cg.Component):
    def handle_child_event(self, data):
        print(f"Child emitted: {data}")
```

The naming convention typically uses `on_` prefix for props that are event handlers:

```html
<ChildComponent :on_custom_event="handle_child_event" />
```

## Event Propagation

Events in Collagraph follow the patterns of the underlying UI framework (PySide, pygfx, etc.). Event propagation behavior depends on the renderer being used.

### Stopping Propagation (Renderer-Dependent)

Some renderers may support stopping event propagation. Check your renderer's documentation:

```python
def handle_click(self, event):
    # Process event
    print("Clicked")
    # Stop propagation (if supported by renderer)
    if hasattr(event, 'accept'):
        event.accept()
```

## Best Practices

### Use Descriptive Handler Names

Name your handlers clearly to indicate what they do:

```python
# Good
def save_form(self)
def delete_item(self)
def toggle_visibility(self)

# Less clear
def click(self)
def do_stuff(self)
def handler(self)
```

### Keep Handlers Focused

Each handler should have a single, clear responsibility:

```python
# Good - focused handlers
def validate_email(self):
    # Just validation
    return '@' in self.state['email']

def submit_form(self):
    if self.validate_email():
        # Submit logic
        self.send_data()

# Less good - doing too much
def submit_form(self):
    # Validation
    if '@' not in self.state['email']:
        return
    # Formatting
    email = self.state['email'].strip().lower()
    # Sending
    # ... lots of code
```

### Use Lambda for Closures

When you need to capture context (especially in loops), use lambda:

```html
<!-- Correct - captures the specific item -->
<button
  v-for="item in items"
  :key="item['id']"
  @clicked="lambda: process(item)"
/>

<!-- Incorrect - 'item' reference may be stale -->
<button
  v-for="item in items"
  :key="item['id']"
  @clicked="process(item)"
/>
```

### Avoid Complex Logic in Templates

Keep templates clean by moving logic to methods:

```html
<!-- Avoid -->
<button @clicked="lambda: (self.state.__setitem__('count', count + 1), print('incremented'), self.save())" />

<!-- Better -->
<button @clicked="increment_and_save" />
```

```python
def increment_and_save(self):
    self.state['count'] += 1
    print('incremented')
    self.save()
```

### Handle Errors Gracefully

Event handlers should handle potential errors:

```python
def save_data(self):
    try:
        # Save operation
        result = self.save_to_database()
        self.state['status'] = 'success'
    except Exception as e:
        self.state['status'] = 'error'
        self.state['error_message'] = str(e)
        print(f"Save failed: {e}")
```

## Unsupported Syntax

Collagraph does **not** support inline statements in event handlers. You must use method references or lambda expressions:

### Not Supported

```html
<!-- These will raise SyntaxError -->
<button @clicked="count += 1" />
<button @clicked="count = 0" />
<button @clicked="print('hello')" />
```

### Supported Alternatives

```html
<!-- Use lambda with method call -->
<button @clicked="lambda: increment()" />
<button @clicked="lambda: reset()" />

<!-- Or reference method directly -->
<button @clicked="increment" />
<button @clicked="reset" />
```

```python
def increment(self):
    self.state['count'] += 1

def reset(self):
    self.state['count'] = 0
    print('hello')
```

## Advanced Patterns

### Debouncing Events

For events that fire frequently (like input changes), implement debouncing:

```python
import time

class SearchComponent(cg.Component):
    def init(self):
        self.state['query'] = ""
        self._last_search_time = 0
        self._debounce_delay = 0.3  # 300ms

    def on_input_change(self, event):
        self.state['query'] = event.text
        current_time = time.time()

        if current_time - self._last_search_time > self._debounce_delay:
            self.perform_search()
            self._last_search_time = current_time
```

### Event Chaining

Chain multiple actions in response to an event:

```python
def handle_submit(self):
    if not self.validate():
        return

    self.save_data()
    self.show_success_message()
    self.reset_form()
```

### Conditional Event Handlers

Only attach handlers under certain conditions:

```html
<button
  text="Submit"
  @clicked="submit_form if form_valid else show_validation_errors"
/>
```

Or more explicitly:

```python
@property
def submit_handler(self):
    return self.submit_form if self.form_valid else self.show_validation_errors
```

```html
<button text="Submit" @clicked="submit_handler" />
```

### Event Handler Composition

Create reusable event handling logic:

```python
class BaseFormComponent(cg.Component):
    def with_loading_state(self, handler):
        """Wrapper that sets loading state during handler execution"""
        def wrapped(*args, **kwargs):
            self.state['loading'] = True
            try:
                return handler(*args, **kwargs)
            finally:
                self.state['loading'] = False
        return wrapped

    def save_data(self):
        # Actual save logic
        print("Saving...")

# Usage
@clicked="with_loading_state(save_data)"
```

## Testing Event Handlers

Event handlers are regular Python methods and can be tested easily:

```python
def test_increment():
    component = Counter({})
    component.init()

    assert component.state['count'] == 0

    component.increment()
    assert component.state['count'] == 1

    component.increment()
    assert component.state['count'] == 2
```

## Performance Considerations

### Avoid Creating New Functions in Render

Creating new lambda functions in templates is fine, but avoid doing expensive work:

```html
<!-- Fine - lambda is lightweight -->
<button @clicked="lambda: delete_item(item['id'])" />

<!-- Avoid - creates new object every render -->
<button @clicked="lambda: expensive_calculation_that_creates_objects()" />
```

### Batch State Updates

If a handler updates multiple state properties, batch them if possible:

```python
# Less efficient - triggers multiple updates
def update_user(self):
    self.state['name'] = new_name
    self.state['email'] = new_email
    self.state['age'] = new_age

# More efficient - single update
def update_user(self):
    self.state.update({
        'name': new_name,
        'email': new_email,
        'age': new_age,
    })
```

## Common Pitfalls

### Forgetting to Call Methods

```html
<!-- Wrong - reference to method object, not called -->
<button @clicked="lambda: increment" />

<!-- Correct - call the method -->
<button @clicked="lambda: increment()" />

<!-- Also correct - reference method directly -->
<button @clicked="increment" />
```

### Incorrect Lambda Scope

```html
<!-- Wrong - 'item' is not captured -->
<button
  v-for="item in items"
  @clicked="lambda: process(item)"  <!-- Works, but be aware of closure -->
/>

<!-- Safer with default argument -->
<button
  v-for="item in items"
  @clicked="lambda item=item: process(item)"
/>
```

### Modifying State Incorrectly

```python
# Wrong - doesn't trigger reactivity
def add_item(self):
    self.state['items'].append(new_item)  # Only works if 'items' is reactive

# Correct - reassign or use reactive list
from observ import reactive

def init(self):
    self.state['items'] = reactive([])

def add_item(self):
    self.state['items'].append(new_item)  # Now triggers updates
```

## Renderer-Specific Events

Different renderers provide different events. Check your renderer's documentation:

### PySide Renderer Common Events
- `@clicked` - Button clicks
- `@toggled` - Checkbox/switch toggle
- `@changed` - Input value changes
- `@activated` - Item activation (lists, etc.)
- `@currentChanged` - Current item changed

### Custom Renderer Events
Custom renderers can define their own event types. Refer to the renderer's documentation.

## See Also

- [Events](../events.md)
- [Template Syntax](../template-syntax.md)
- [Component Lifecycle](../lifecycle.md)
- [v-bind Directive](v-bind.md)
- [Reactivity](../reactivity.md)
