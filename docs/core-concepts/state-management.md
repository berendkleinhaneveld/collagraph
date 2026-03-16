# State Management

## Overview

State is data that belongs to a component and can change over time. Collagraph provides reactive state management through `self.state`, powered by the [observ](https://github.com/fork-tongue/observ) library. When state changes, the UI automatically updates to reflect those changes.

## Creating State

### Initializing State in `init()`

State should always be initialized in the `init()` lifecycle hook:

```python
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        # Initialize state properties
        self.state["count"] = 0
        self.state["message"] = "Hello"
        self.state["is_active"] = True
```

### Why `init()` and Not `__init__()`?

Collagraph components use `init()` instead of Python's `__init__()` because:
1. The base component initialization happens in `__init__()`
2. `init()` is called automatically after the component is fully set up
3. You can safely access `self.props`, `self.state`, and other component properties in `init()`

```python
class MyComponent(cg.Component):
    def init(self):
        # Safe to access props here
        initial_value = self.props.get("initial", 0)
        self.state["value"] = initial_value
```

## Reactive Updates

### Automatic Reactivity

State in Collagraph is reactive, meaning changes to state automatically trigger UI updates:

```python
class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        # This modification automatically triggers a re-render
        self.state["count"] += 1
```

In your template:

```html
<label :text="f'Count: {count}'" />
<button text="Increment" @clicked="increment" />
```

When you click the button, the label automatically updates.

### How Reactivity Works

Collagraph uses the `observ` library to make state reactive:

1. `self.state` is a reactive dictionary
2. Reading from `self.state` tracks dependencies
3. Writing to `self.state` triggers updates to all dependent UI elements
4. Only affected parts of the UI re-render

```python
from observ import reactive

class Example(cg.Component):
    def init(self):
        # self.state is created as reactive({})
        # by the Component base class
        self.state["data"] = []
```

## Nested State Objects

State can contain nested objects, and they remain reactive:

```python
class UserProfile(cg.Component):
    def init(self):
        self.state["user"] = {
            "name": "Alice",
            "email": "alice@example.com",
            "preferences": {
                "theme": "dark",
                "notifications": True
            }
        }

    def update_theme(self, new_theme):
        # Nested updates are reactive
        self.state["user"]["preferences"]["theme"] = new_theme
```

### Lists and Arrays

State can also contain reactive lists:

```python
class TodoList(cg.Component):
    def init(self):
        self.state["todos"] = []

    def add_todo(self, text):
        # List mutations trigger updates
        self.state["todos"].append({
            "text": text,
            "completed": False
        })

    def remove_todo(self, index):
        # Removing items triggers updates
        self.state["todos"].pop(index)

    def toggle_todo(self, index):
        # Modifying nested properties triggers updates
        self.state["todos"][index]["completed"] = not self.state["todos"][index]["completed"]
```

### Reactive List Methods

All standard list methods work reactively:

```python
# Append
self.state["items"].append(new_item)

# Extend
self.state["items"].extend([item1, item2])

# Insert
self.state["items"].insert(0, first_item)

# Remove
self.state["items"].remove(item)

# Pop
self.state["items"].pop(index)

# Clear
self.state["items"].clear()

# Sort
self.state["items"].sort()

# Reverse
self.state["items"].reverse()

# Item assignment
self.state["items"][0] = new_value

# Slice assignment
self.state["items"][1:3] = [new_item1, new_item2]
```

## State vs Props

Understanding the difference between state and props is crucial:

### State
- **Owned by the component**
- **Mutable** - can be changed by the component
- **Private** - not accessible to parent components
- **Reactive** - changes trigger re-renders
- Initialized in `init()`

```python
class Counter(cg.Component):
    def init(self):
        # State is private and mutable
        self.state["count"] = 0

    def increment(self):
        # Component can modify its own state
        self.state["count"] += 1
```

### Props
- **Passed from parent component**
- **Read-only** - cannot be modified by the component
- **Public** - defined by parent
- **Reactive** - changes from parent trigger re-renders
- Accessed via `self.props`

```python
class ChildComponent(cg.Component):
    def init(self):
        # Props are read-only
        title = self.props.get("title", "Default")

        # If you need a mutable version, copy to state
        self.state["title"] = title
```

### When to Use State vs Props

Use **state** when:
- The data is owned and managed by this component
- The data changes in response to user interactions or internal logic
- The data is not needed by parent components

Use **props** when:
- The data comes from a parent component
- The component is being configured or controlled by its parent
- Multiple components need to share the same data

```python
# Parent component manages shared state
class Parent(cg.Component):
    def init(self):
        self.state["shared_data"] = []

# Child component receives data via props
class Child(cg.Component):
    def init(self):
        # Use props for data from parent
        data = self.props.get("data", [])

        # Use state for component's own data
        self.state["selected_index"] = 0
```

## Sharing State Between Components

### Parent-Child Communication

Pass state from parent to child via props:

```html
<!-- Parent template -->
<widget>
  <Counter :count="count" @increment="handle_increment" />
</widget>
```

```python
# Parent component
class Parent(cg.Component):
    def init(self):
        self.state["count"] = 0

    def handle_increment(self):
        self.state["count"] += 1
```

### Provide/Inject for Deep Hierarchies

For passing data through multiple component levels, use `provide` and `inject`:

```python
# Ancestor component
class Theme Provider(cg.Component):
    def init(self):
        self.state["theme"] = "dark"
        # Provide theme to all descendants
        self.provide(key="theme", value=self.state["theme"])

# Deeply nested descendant
class StyledWidget(cg.Component):
    def init(self):
        # Inject the theme from any ancestor
        theme = self.inject("theme", default="light")
        self.state["theme"] = theme
```

### Global State

For truly global state, you can pass it to `gui.render()`:

```python
from observ import reactive
import collagraph as cg

# Create global state
global_state = reactive({
    "current_user": None,
    "settings": {}
})

# Pass to render
gui = cg.Collagraph(renderer=cg.PySideRenderer())
gui.render(App, container, state=global_state)
```

Access global state in templates:

```html
<label :text="f'User: {current_user['name']}'" v-if="current_user" />
```

## State Update Patterns

### Direct Assignment

```python
self.state["count"] = 10
self.state["message"] = "Updated"
```

### Increment/Decrement

```python
self.state["count"] += 1
self.state["score"] -= 5
```

### Toggle Boolean

```python
self.state["is_active"] = not self.state["is_active"]
```

### Update Object Properties

```python
self.state["user"]["name"] = "Bob"
self.state["user"]["age"] += 1
```

### Replace Entire Object

```python
self.state["user"] = {
    "name": "Charlie",
    "email": "charlie@example.com"
}
```

### Conditional Updates

```python
def update_status(self, new_status):
    if new_status in ["active", "inactive", "pending"]:
        self.state["status"] = new_status
```

## Common Patterns

### Form State

```python
class LoginForm(cg.Component):
    def init(self):
        self.state["username"] = ""
        self.state["password"] = ""
        self.state["errors"] = {}
        self.state["is_submitting"] = False

    def update_username(self, value):
        self.state["username"] = value

    def update_password(self, value):
        self.state["password"] = value

    def submit(self):
        self.state["errors"] = {}
        self.state["is_submitting"] = True

        # Validation logic...
        if not self.state["username"]:
            self.state["errors"]["username"] = "Required"

        if len(self.state["errors"]) == 0:
            # Submit form...
            pass

        self.state["is_submitting"] = False
```

### Loading States

```python
class DataLoader(cg.Component):
    def init(self):
        self.state["data"] = []
        self.state["loading"] = False
        self.state["error"] = None

    def load_data(self):
        self.state["loading"] = True
        self.state["error"] = None

        try:
            # Load data...
            data = fetch_data()
            self.state["data"] = data
        except Exception as e:
            self.state["error"] = str(e)
        finally:
            self.state["loading"] = False
```

### Pagination State

```python
class PaginatedList(cg.Component):
    def init(self):
        self.state["items"] = []
        self.state["current_page"] = 1
        self.state["items_per_page"] = 10

    @property
    def total_pages(self):
        return len(self.state["items"]) // self.state["items_per_page"] + 1

    @property
    def current_items(self):
        start = (self.state["current_page"] - 1) * self.state["items_per_page"]
        end = start + self.state["items_per_page"]
        return self.state["items"][start:end]

    def next_page(self):
        if self.state["current_page"] < self.total_pages:
            self.state["current_page"] += 1

    def prev_page(self):
        if self.state["current_page"] > 1:
            self.state["current_page"] -= 1
```

## Best Practices

### 1. Initialize All State in `init()`

Always declare all state properties upfront:

```python
def init(self):
    # Good: All state initialized
    self.state["count"] = 0
    self.state["items"] = []
    self.state["loading"] = False

# Avoid: Creating state properties later
def some_method(self):
    self.state["new_property"] = value  # Not recommended
```

### 2. Use Descriptive State Names

Choose clear, descriptive names for state properties:

```python
# Good
self.state["is_loading"] = True
self.state["selected_user_id"] = 42
self.state["validation_errors"] = {}

# Less clear
self.state["flag"] = True
self.state["id"] = 42
self.state["errs"] = {}
```

### 3. Keep State Minimal

Only store what needs to be reactive. Derive other values using properties or methods:

```python
class TodoList(cg.Component):
    def init(self):
        # Store only the essential state
        self.state["todos"] = []

    # Derive computed values
    @property
    def completed_count(self):
        return sum(1 for todo in self.state["todos"] if todo["completed"])

    @property
    def incomplete_count(self):
        return len(self.state["todos"]) - self.completed_count
```

### 4. Avoid Direct State Mutations in Templates

Keep state mutations in methods, not templates:

```html
<!-- Good: Call a method -->
<button @clicked="increment" text="Increment" />

<!-- Less maintainable: Direct mutation in template -->
<button @clicked="lambda: state.__setitem__('count', count + 1)" text="Increment" />
```

### 5. Group Related State

Group related state properties together:

```python
def init(self):
    # Group user-related state
    self.state["user"] = {
        "id": None,
        "name": "",
        "email": "",
        "is_authenticated": False
    }

    # Group UI-related state
    self.state["ui"] = {
        "sidebar_open": True,
        "theme": "light",
        "notifications_enabled": True
    }
```

## See Also

- [Reactivity System](reactivity.md)
- [Props](props.md)
- [Provide/Inject](provide-inject.md)
