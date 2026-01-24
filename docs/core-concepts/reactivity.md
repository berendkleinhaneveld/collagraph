# Reactivity System

## Overview

Collagraph uses the `observ` library to provide reactive state management. When state changes, the UI automatically updates. This reactivity is at the heart of Collagraph's declarative programming model.

## How Reactivity Works

When you modify `self.state`, Collagraph automatically:

1. Detects the change through the `observ` library
2. Marks the component as dirty
3. Schedules a re-render
4. Updates only the parts of the UI that changed

This happens transparently - you just modify your data and the UI updates.

## The `self.state` Dictionary

Every component has a `self.state` dictionary that is reactive:

```python
class MyComponent(cg.Component):
    def init(self):
        # Initialize reactive state
        self.state["count"] = 0
        self.state["items"] = []
        self.state["user"] = {"name": "Alice", "age": 30}

    def increment(self):
        # Modifying state triggers re-render
        self.state["count"] += 1

    def add_item(self, item):
        # Modifications to nested structures are also reactive
        self.state["items"].append(item)

    def update_user(self):
        # Nested property changes are detected
        self.state["user"]["age"] += 1
```

## Observable Collections

The `observ` library makes dictionaries and lists observable:

### Observable Dictionaries

```python
def init(self):
    self.state["user"] = {"name": "Alice"}

def update_name(self):
    # This triggers a re-render
    self.state["user"]["name"] = "Bob"
```

### Observable Lists

```python
def init(self):
    self.state["todos"] = []

def add_todo(self, text):
    # List modifications trigger updates
    self.state["todos"].append({"text": text, "done": False})

def remove_todo(self, index):
    del self.state["todos"][index]
```

## Reactive Dependencies

Collagraph tracks which state values your template uses. When those values change, the component re-renders:

```html
<v-box>
  <!-- This will only re-render when 'count' changes -->
  <label :text="f'Count: {count}'" />

  <!-- This re-renders when 'user' changes -->
  <label :text="f'User: {user[\"name\"]}'" />
</v-box>

<script>
import collagraph as cg

class Example(cg.Component):
    def init(self):
        self.state["count"] = 0
        self.state["user"] = {"name": "Alice"}
</script>
```

## Computed Properties

Computed properties automatically recompute when their dependencies change:

```python
from observ import computed

class ShoppingCart(cg.Component):
    def init(self):
        self.state["items"] = [
            {"name": "Apple", "price": 1.0, "quantity": 3},
            {"name": "Banana", "price": 0.5, "quantity": 5}
        ]

        # Computed property that recalculates when items change
        self.total = computed(lambda: sum(
            item["price"] * item["quantity"]
            for item in self.state["items"]
        ))

    def render(self):
        return {
            "type": "label",
            "text": f"Total: ${self.total.value:.2f}"
        }
```

See [Computed Properties](computed.md) for more details.

## Watchers

Watch for changes to specific state values and react to them:

```python
from observ import watch

class Logger(cg.Component):
    def init(self):
        self.state["count"] = 0

        # Watch for changes to count
        watch(
            lambda: self.state["count"],
            lambda new_val, old_val: print(f"Count changed from {old_val} to {new_val}")
        )

    def increment(self):
        self.state["count"] += 1  # This triggers the watcher
```

See [Watchers](watchers.md) for more details.

## Performance Considerations

### Batch Updates

Collagraph batches multiple state changes into a single re-render:

```python
def update_multiple(self):
    self.state["first_name"] = "Alice"
    self.state["last_name"] = "Smith"
    self.state["age"] = 30
    # Only one re-render happens, not three
```

### Avoid Unnecessary Reactivity

Not everything needs to be reactive. Use regular instance variables for non-reactive data:

```python
def init(self):
    # Reactive state
    self.state["count"] = 0

    # Non-reactive instance variable
    self.api_client = MyAPIClient()
    self.constants = {"MAX_ITEMS": 100}
```

### Deep vs Shallow Reactivity

The `observ` library provides deep reactivity by default, meaning nested changes are detected:

```python
def init(self):
    self.state["user"] = {
        "name": "Alice",
        "address": {
            "city": "New York",
            "country": "USA"
        }
    }

def update_city(self):
    # Deep reactivity: this triggers a re-render
    self.state["user"]["address"]["city"] = "Los Angeles"
```

## Integration with Observ Library

Collagraph is built on top of the `observ` library (v0.17.1+). You can use all of `observ`'s features directly:

```python
from observ import reactive, computed, watch

class AdvancedComponent(cg.Component):
    def init(self):
        # Use observ's reactive() directly
        self.custom_reactive = reactive({"data": []})

        # Create computed values
        self.computed_value = computed(
            lambda: len(self.custom_reactive["data"])
        )

        # Set up watchers
        watch(
            lambda: self.computed_value.value,
            lambda new, old: print(f"Length changed: {old} -> {new}")
        )
```

For more information about `observ`, see its [documentation](https://github.com/berendkleinhaneveld/observ).

## Common Patterns

### Form Input Binding

```python
def init(self):
    self.state["form"] = {
        "name": "",
        "email": "",
        "message": ""
    }

def handle_name_change(self, event):
    self.state["form"]["name"] = event.text
```

### Toggle State

```python
def init(self):
    self.state["is_open"] = False

def toggle(self):
    self.state["is_open"] = not self.state["is_open"]
```

### List Management

```python
def init(self):
    self.state["items"] = []

def add_item(self, text):
    self.state["items"].append({"id": len(self.state["items"]), "text": text})

def remove_item(self, index):
    del self.state["items"][index]

def clear_all(self):
    self.state["items"].clear()
```

## See Also

- [State Management](state-management.md)
- [Computed Properties](computed.md)
- [Watchers](watchers.md)
