# Events

## Overview

Events are the primary mechanism for components to respond to user interactions and communicate with parent components. Collagraph provides a simple, intuitive event system that allows components to listen to built-in UI events and emit custom events.

Events flow **upward** from child to parent, complementing the downward flow of props to create a complete communication pattern.

## Event Handling with `@event` Syntax

### Basic Event Handlers

Use the `@` prefix in templates to attach event handlers:

```html
<button text="Click me" @clicked="handle_click" />
<input placeholder="Type..." @changed="handle_change" />
<checkbox @toggled="handle_toggle" />
```

In your component:

```python
import collagraph as cg

class MyComponent(cg.Component):
    def handle_click(self):
        print("Button was clicked!")

    def handle_change(self):
        print("Input changed!")

    def handle_toggle(self):
        print("Checkbox toggled!")
```

### Inline Event Handlers

You can use inline expressions or lambda functions:

```html
<!-- Inline lambda -->
<button
  text="Increment"
  @clicked="lambda: state['count'] += 1"
/>

<!-- Call method with arguments -->
<button
  text="Set to 10"
  @clicked="lambda: set_count(10)"
/>

<!-- Multiple statements -->
<button
  text="Reset"
  @clicked="lambda: [state['count'] = 0, print('Reset!')]"
/>
```

## Built-in Events

Different UI elements emit different built-in events depending on the renderer (PySide, PyGfx, etc.):

### Common PySide Events

#### Button Events
```html
<button text="Click" @clicked="handle_click" />
<push-button text="Push" @clicked="handle_push" />
```

#### Input Events
```html
<line-edit
  placeholder="Enter text"
  @text-changed="handle_text_change"
  @editing-finished="handle_editing_done"
  @return-pressed="handle_enter"
/>

<text-edit
  @text-changed="handle_text_change"
/>
```

#### Checkbox/Radio Events
```html
<checkbox
  :checked="is_checked"
  @toggled="handle_toggle"
/>

<radio-button
  :checked="is_selected"
  @toggled="handle_radio"
/>
```

#### Selection Events
```html
<combo-box
  @current-index-changed="handle_selection"
  @current-text-changed="handle_text_selection"
/>

<list-view
  @selection-changed="handle_list_selection"
/>

<tree-view
  @selection-changed="handle_tree_selection"
/>
```

#### Slider Events
```html
<slider
  :value="volume"
  @value-changed="handle_slider_change"
  @slider-moved="handle_slider_move"
  @slider-pressed="handle_slider_press"
  @slider-released="handle_slider_release"
/>
```

### Event Naming Convention

Event names in templates use kebab-case:

```html
<widget @custom-event="handler" />
<widget @value-changed="handler" />
```

The corresponding signal names in PySide use camelCase or snake_case:

```python
# Collagraph automatically maps:
# @clicked -> clicked signal
# @value-changed -> valueChanged or value_changed signal
# @selection-changed -> selectionChanged or selection_changed signal
```

## Custom Events

### Emitting Custom Events

Components can emit custom events using `self.emit()`:

```python
class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1

        # Emit custom event to parent
        self.emit("incremented")

        # Emit with data
        self.emit("value-changed", self.state["count"])
```

### Listening to Custom Events

Parent components listen to custom events using the same `@event` syntax:

```html
<widget>
  <Counter
    @incremented="handle_increment"
    @value-changed="handle_value_change"
  />
</widget>
```

```python
class Parent(cg.Component):
    def handle_increment(self):
        print("Counter was incremented!")

    def handle_value_change(self, new_value):
        print(f"Counter value changed to: {new_value}")
        self.state["total"] += new_value
```

## Event Arguments

### Passing Arguments to Event Handlers

Events can pass arguments to their handlers:

```python
class TodoList(cg.Component):
    def delete_item(self, item_id):
        """Emit event with item ID"""
        self.emit("item-deleted", item_id)

    def update_item(self, item_id, new_text):
        """Emit event with multiple arguments"""
        self.emit("item-updated", item_id, new_text)

    def change_status(self, item_id, status):
        """Emit event with keyword arguments"""
        self.emit("status-changed", item_id=item_id, status=status)
```

### Receiving Event Arguments

Event handlers receive the emitted arguments:

```python
class Parent(cg.Component):
    def handle_item_deleted(self, item_id):
        print(f"Item {item_id} was deleted")

    def handle_item_updated(self, item_id, new_text):
        print(f"Item {item_id} updated to: {new_text}")

    def handle_status_changed(self, item_id, status):
        print(f"Item {item_id} status: {status}")
```

### Using Lambdas with Event Arguments

In `v-for` loops, use lambdas to capture loop variables:

```html
<widget v-for="item in items">
  <label :text="item['name']" />
  <button
    text="Delete"
    @clicked="lambda: delete_item(item['id'])"
  />
  <button
    text="Edit"
    @clicked="lambda: edit_item(item)"
  />
</widget>
```

```python
class ItemList(cg.Component):
    def delete_item(self, item_id):
        # Remove item from state
        self.state["items"] = [
            item for item in self.state["items"]
            if item["id"] != item_id
        ]

    def edit_item(self, item):
        # Edit the item
        self.state["editing_item"] = item
```

## Event Communication Patterns

### Child to Parent Communication

The most common pattern is child components emitting events that parents handle:

**Child Component (child.cgx):**
```html
<button
  text="Save"
  @clicked="handle_save"
/>

<script>
import collagraph as cg

class Child(cg.Component):
    def handle_save(self):
        data = {"name": "Alice", "age": 30}
        # Emit event to parent
        self.emit("saved", data)
</script>
```

**Parent Component (parent.cgx):**
```html
<widget>
  <Child @saved="handle_child_saved" />
</widget>

<script>
import collagraph as cg
from child import Child

class Parent(cg.Component):
    def handle_child_saved(self, data):
        print(f"Child saved data: {data}")
        self.state["saved_data"] = data
</script>
```

### Multi-Level Event Propagation

For events to propagate through multiple levels, each component must re-emit:

```python
# GrandChild component
class GrandChild(cg.Component):
    def do_something(self):
        self.emit("action-performed", "data")

# Child component
class Child(cg.Component):
    def handle_grandchild_action(self, data):
        # Re-emit to propagate to grandparent
        self.emit("action-performed", data)

# Parent component
class Parent(cg.Component):
    def handle_action(self, data):
        print(f"Received from grandchild: {data}")
```

```html
<!-- Parent template -->
<Child @action-performed="handle_action" />

<!-- Child template -->
<GrandChild @action-performed="handle_grandchild_action" />
```

### Callback Props Alternative

Alternatively, you can pass callbacks as props:

```python
# Parent component
class Parent(cg.Component):
    def handle_save(self, data):
        print(f"Saved: {data}")
```

```html
<!-- Parent template: Pass callback as prop -->
<Child :on-save="handle_save" />
```

```python
# Child component
class Child(cg.Component):
    def save_data(self):
        data = {"name": "Alice"}
        # Call the callback prop
        callback = self.props.get("on_save")
        if callback:
            callback(data)
```

## Managing Event Handlers

### Adding Event Handlers Programmatically

You can add event handlers programmatically using `add_event_handler()`:

```python
class MyComponent(cg.Component):
    def init(self):
        # Add event handler programmatically
        self.add_event_handler("custom-event", self.handle_custom)

    def handle_custom(self, data):
        print(f"Custom event: {data}")
```

### Removing Event Handlers

Remove event handlers with `remove_event_handler()`:

```python
class MyComponent(cg.Component):
    def init(self):
        self.my_handler = self.handle_custom
        self.add_event_handler("custom-event", self.my_handler)

    def before_unmount(self):
        # Clean up event handler
        self.remove_event_handler("custom-event", self.my_handler)

    def handle_custom(self, data):
        print(f"Custom event: {data}")
```

## Common Event Patterns

### Form Submission

```python
class LoginForm(cg.Component):
    def init(self):
        self.state["username"] = ""
        self.state["password"] = ""

    def handle_submit(self):
        # Validate
        if not self.state["username"]:
            return

        # Emit event with form data
        self.emit("submit", {
            "username": self.state["username"],
            "password": self.state["password"]
        })
```

```html
<LoginForm @submit="handle_login" />
```

### Data Loading

```python
class DataLoader(cg.Component):
    def load_data(self):
        self.state["loading"] = True
        self.emit("loading-started")

        try:
            data = fetch_data()
            self.state["data"] = data
            self.emit("loading-complete", data)
        except Exception as e:
            self.emit("loading-error", str(e))
        finally:
            self.state["loading"] = False
```

### Item Selection

```python
class ItemList(cg.Component):
    def select_item(self, item):
        self.state["selected_item"] = item
        self.emit("item-selected", item)

    def deselect_item(self):
        self.state["selected_item"] = None
        self.emit("item-deselected")
```

### Confirmation Dialogs

```python
class DeleteButton(cg.Component):
    def handle_click(self):
        # Emit event asking for confirmation
        self.emit("delete-requested", self.props.get("item_id"))

class Parent(cg.Component):
    def handle_delete_requested(self, item_id):
        # Show confirmation dialog
        if confirm("Are you sure?"):
            self.delete_item(item_id)
            self.emit("item-deleted", item_id)
```

## Complete Example

Here's a comprehensive example showing various event patterns:

```html
<window title="Todo List" width="400" height="500">
  <widget>
    <!-- Input with multiple events -->
    <line-edit
      ref="input"
      placeholder="Enter todo..."
      @return-pressed="add_todo"
      @text-changed="handle_text_change"
    />

    <button text="Add" @clicked="add_todo" />

    <!-- List items with custom events -->
    <TodoItem
      v-for="idx, todo in enumerate(todos)"
      :key="todo['id']"
      v-bind="todo"
      @completed="lambda: handle_complete(idx)"
      @deleted="lambda: handle_delete(idx)"
      @edited="lambda text: handle_edit(idx, text)"
    />

    <!-- Status with inline handler -->
    <label
      :text="f'{remaining} items remaining'"
      @clicked="lambda: print('Status clicked')"
    />
  </widget>
</window>

<script>
import collagraph as cg
from todo_item import TodoItem

class TodoList(cg.Component):
    def init(self):
        self.state["todos"] = []
        self.state["next_id"] = 1

    @property
    def remaining(self):
        return sum(1 for todo in self.state["todos"] if not todo["completed"])

    def add_todo(self):
        if "input" in self.refs:
            text = self.refs["input"].text()
            if text.strip():
                todo = {
                    "id": self.state["next_id"],
                    "text": text,
                    "completed": False
                }
                self.state["todos"].append(todo)
                self.state["next_id"] += 1
                self.refs["input"].clear()

                # Emit event to parent (if any)
                self.emit("todo-added", todo)

    def handle_text_change(self):
        # Could emit event for live validation
        pass

    def handle_complete(self, idx):
        self.state["todos"][idx]["completed"] = True
        self.emit("todo-completed", self.state["todos"][idx])

    def handle_delete(self, idx):
        deleted_todo = self.state["todos"].pop(idx)
        self.emit("todo-deleted", deleted_todo)

    def handle_edit(self, idx, new_text):
        self.state["todos"][idx]["text"] = new_text
        self.emit("todo-edited", self.state["todos"][idx])
</script>
```

**TodoItem component (todo_item.cgx):**
```html
<widget :layout="{'type': 'Box', 'direction': 'LeftToRight'}">
  <checkbox
    :checked="completed"
    @toggled="handle_toggle"
  />
  <label :text="text" />
  <button text="Edit" @clicked="handle_edit_click" />
  <button text="Delete" @clicked="handle_delete_click" />
</widget>

<script>
import collagraph as cg

class TodoItem(cg.Component):
    def handle_toggle(self):
        # Emit completion event to parent
        self.emit("completed")

    def handle_edit_click(self):
        # Simple prompt for demo (would use a proper dialog in production)
        new_text = input("Edit todo:")
        if new_text:
            self.emit("edited", new_text)

    def handle_delete_click(self):
        # Emit deletion event to parent
        self.emit("deleted")
</script>
```

## Best Practices

### 1. Use Descriptive Event Names

Choose clear, action-oriented names:

```python
# Good
self.emit("item-selected", item)
self.emit("form-submitted", data)
self.emit("file-uploaded", file)

# Less clear
self.emit("click", item)
self.emit("done", data)
self.emit("ok", file)
```

### 2. Document Custom Events

Document what events your component emits:

```python
class MyComponent(cg.Component):
    """
    Component description.

    Events:
        - item-selected: Emitted when an item is selected. Passes item object.
        - loading-complete: Emitted when data loading finishes. Passes data array.
        - error: Emitted on errors. Passes error message string.
    """
```

### 3. Emit Events After State Changes

Emit events after updating state, not before:

```python
def handle_submit(self):
    # Update state first
    self.state["submitted"] = True

    # Then emit event
    self.emit("submitted", self.state["form_data"])
```

### 4. Use Lambdas for Loop Variables

Always use lambdas in `v-for` to capture loop variables:

```html
<!-- Correct: Lambda captures item -->
<button
  v-for="item in items"
  @clicked="lambda: handle_click(item)"
/>

<!-- Incorrect: Will use last item for all buttons -->
<button
  v-for="item in items"
  @clicked="handle_click(item)"
/>
```

### 5. Keep Event Handlers Simple

Keep event handlers focused and delegate complex logic to methods:

```python
# Good: Handler delegates to method
def handle_click(self):
    self.process_complex_logic()

def process_complex_logic(self):
    # Complex logic here
    pass

# Less ideal: Complex logic in handler
def handle_click(self):
    # Lots of complex logic directly in handler
    pass
```

## See Also

- [Template Syntax](template-syntax.md)
- [v-on Directive](directives/v-on.md)
