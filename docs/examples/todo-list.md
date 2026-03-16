# Example: Todo List

A complete todo list application demonstrating list rendering, forms, and advanced state management.

## Overview

This example builds upon the counter to demonstrate working with lists, forms, and more complex state management. You'll learn how to render dynamic lists, handle form inputs, filter data, and work with computed properties.

### What You'll Learn

- How to render lists with the `v-for` directive
- How to handle text input and form submission
- How to work with arrays in reactive state
- How to implement filtering with computed properties
- How to use lambda functions in event handlers
- How to conditionally enable/disable buttons
- Best practices for keyed lists

## Complete Code

Create a file called `todo.cgx`:

```html
<window title="Todo List">
  <v-box>
    <label text="Todo List" />

    <!-- Input section -->
    <h-box>
      <line-edit
        :text="new_todo_text"
        placeholder-text="What needs to be done?"
        @text-changed="on_input_change"
        @return-pressed="add_todo"
      />
      <button
        text="Add"
        @clicked="add_todo"
        :enabled="can_add_todo"
      />
    </h-box>

    <!-- Filter buttons -->
    <h-box>
      <button
        text="All"
        @clicked="lambda: set_filter('all')"
        :enabled="filter != 'all'"
      />
      <button
        text="Active"
        @clicked="lambda: set_filter('active')"
        :enabled="filter != 'active'"
      />
      <button
        text="Completed"
        @clicked="lambda: set_filter('completed')"
        :enabled="filter != 'completed'"
      />
    </h-box>

    <!-- Todo list -->
    <v-box>
      <h-box
        v-for="todo in filtered_todos"
        :key="todo['id']"
      >
        <checkbox
          :checked="todo['completed']"
          @toggled="lambda checked: toggle_todo(todo['id'], checked)"
        />
        <label :text="todo['text']" />
        <button
          text="Delete"
          @clicked="lambda: delete_todo(todo['id'])"
        />
      </h-box>
    </v-box>

    <!-- Footer with stats and actions -->
    <h-box>
      <label :text="f'{active_count} item(s) left'" />
      <button
        text="Clear Completed"
        @clicked="clear_completed"
        :enabled="has_completed"
      />
    </h-box>
  </v-box>
</window>

<script>
import collagraph as cg


class TodoApp(cg.Component):
    def init(self):
        self.state["todos"] = []
        self.state["new_todo_text"] = ""
        self.state["filter"] = "all"  # all, active, or completed
        self.state["next_id"] = 1

    @property
    def filtered_todos(self):
        """Compute filtered list based on current filter."""
        todos = self.state["todos"]
        filter_type = self.state["filter"]

        if filter_type == "active":
            return [t for t in todos if not t["completed"]]
        elif filter_type == "completed":
            return [t for t in todos if t["completed"]]
        else:  # all
            return todos

    @property
    def active_count(self):
        """Count of uncompleted todos."""
        return sum(1 for t in self.state["todos"] if not t["completed"])

    @property
    def has_completed(self):
        """Check if any todos are completed."""
        return any(t["completed"] for t in self.state["todos"])

    @property
    def can_add_todo(self):
        """Check if a todo can be added."""
        return len(self.state["new_todo_text"].strip()) > 0

    def on_input_change(self, text):
        """Handle text input changes."""
        self.state["new_todo_text"] = text

    def add_todo(self):
        """Add a new todo to the list."""
        text = self.state["new_todo_text"].strip()
        if not text:
            return

        todo = {
            "id": self.state["next_id"],
            "text": text,
            "completed": False,
        }
        self.state["todos"].append(todo)
        self.state["next_id"] += 1
        self.state["new_todo_text"] = ""

    def toggle_todo(self, todo_id, checked):
        """Toggle a todo's completed state."""
        for todo in self.state["todos"]:
            if todo["id"] == todo_id:
                todo["completed"] = checked
                break

    def delete_todo(self, todo_id):
        """Delete a todo from the list."""
        self.state["todos"] = [
            t for t in self.state["todos"] if t["id"] != todo_id
        ]

    def set_filter(self, filter_type):
        """Change the current filter."""
        self.state["filter"] = filter_type

    def clear_completed(self):
        """Remove all completed todos."""
        self.state["todos"] = [
            t for t in self.state["todos"] if not t["completed"]
        ]
</script>
```

## Step-by-Step Breakdown

### 1. State Structure

```python
def init(self):
    self.state["todos"] = []
    self.state["new_todo_text"] = ""
    self.state["filter"] = "all"
    self.state["next_id"] = 1
```

The state manages:
- `todos`: Array of todo objects (each has `id`, `text`, `completed`)
- `new_todo_text`: Current input field value
- `filter`: Active filter ("all", "active", or "completed")
- `next_id`: Auto-incrementing ID for new todos

### 2. Input Handling

```html
<line-edit
  :text="new_todo_text"
  placeholder-text="What needs to be done?"
  @text-changed="on_input_change"
  @return-pressed="add_todo"
/>
```

The line-edit widget binds to `new_todo_text` and handles two events:
- `@text-changed`: Updates state when user types
- `@return-pressed`: Adds todo when user presses Enter

### 3. List Rendering with v-for

```html
<h-box
  v-for="todo in filtered_todos"
  :key="todo['id']"
>
  <checkbox :checked="todo['completed']" ... />
  <label :text="todo['text']" />
  <button text="Delete" ... />
</h-box>
```

The `v-for` directive creates a widget for each todo:
- Iterates over the `filtered_todos` computed property
- `:key="todo['id']"` helps Collagraph track items efficiently
- Each todo gets a checkbox, label, and delete button

### 4. Computed Properties

```python
@property
def filtered_todos(self):
    todos = self.state["todos"]
    filter_type = self.state["filter"]

    if filter_type == "active":
        return [t for t in todos if not t["completed"]]
    elif filter_type == "completed":
        return [t for t in todos if t["completed"]]
    else:
        return todos
```

Computed properties automatically recalculate when dependencies change. This filters the todo list based on the current filter setting.

### 5. Lambda Functions in Event Handlers

```html
<button
  text="Delete"
  @clicked="lambda: delete_todo(todo['id'])"
/>
```

Lambda functions allow passing arguments to event handlers. Without lambda, we couldn't pass the specific `todo['id']` to the delete method.

### 6. Conditional Button States

```html
<button
  text="Add"
  :enabled="can_add_todo"
/>
```

Buttons can be enabled/disabled based on state. The Add button is only enabled when there's text to add.

### 7. Array Manipulation

```python
# Append to array
self.state["todos"].append(todo)

# Replace array (triggers reactivity)
self.state["todos"] = [
    t for t in self.state["todos"] if t["id"] != todo_id
]

# Modify object in array (also reactive)
for todo in self.state["todos"]:
    if todo["id"] == todo_id:
        todo["completed"] = checked
```

## How to Run

### Using the CLI

```bash
uv run collagraph todo.cgx
```

Or:

```bash
python -m collagraph todo.cgx
```

### With a Python Entry Point

```python
# main.py
from PySide6 import QtWidgets
import collagraph as cg
from todo import TodoApp

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    gui = cg.Collagraph(renderer=cg.PySideRenderer())
    gui.render(TodoApp, app)
    app.exec()
```

## Key Concepts

### The v-for Directive

The `v-for` directive creates elements for each item in a list:

```html
<widget v-for="item in items" :key="item['id']">
```

**Always use `:key`** with a unique identifier for each item. This helps Collagraph:
- Track which items changed, added, or removed
- Optimize rendering performance
- Preserve component state correctly

### Computed Properties

Use `@property` decorators for values derived from state:

```python
@property
def active_count(self):
    return sum(1 for t in self.state["todos"] if not t["completed"])
```

Benefits:
- Automatically recalculate when dependencies change
- Can be used in templates like regular state
- Keep complex logic out of templates

### Working with Arrays

When modifying arrays, you have options:

```python
# Option 1: Mutate in place (works for append, extend, etc.)
self.state["todos"].append(new_todo)

# Option 2: Replace entire array (ensures reactivity)
self.state["todos"] = self.state["todos"] + [new_todo]

# Option 3: Modify objects within array (works due to deep reactivity)
self.state["todos"][0]["completed"] = True
```

All three trigger reactivity, but replacing the array is safest for complex operations.

## Possible Extensions

### 1. Add Todo Editing

Allow users to edit existing todo text:

```html
<line-edit
  v-if="todo['id'] == editing_id"
  :text="todo['text']"
  @text-changed="lambda text: update_todo_text(todo['id'], text)"
  @return-pressed="stop_editing"
/>
<label
  v-else
  :text="todo['text']"
  @double-clicked="lambda: start_editing(todo['id'])"
/>
```

```python
def init(self):
    # ... existing state
    self.state["editing_id"] = None

def start_editing(self, todo_id):
    self.state["editing_id"] = todo_id

def stop_editing(self):
    self.state["editing_id"] = None

def update_todo_text(self, todo_id, text):
    for todo in self.state["todos"]:
        if todo["id"] == todo_id:
            todo["text"] = text
            break
```

### 2. Add Persistence

Save todos to a JSON file:

```python
import json

def init(self):
    self.load_todos()

def load_todos(self):
    try:
        with open("todos.json", "r") as f:
            data = json.load(f)
            self.state["todos"] = data.get("todos", [])
            self.state["next_id"] = data.get("next_id", 1)
    except FileNotFoundError:
        self.state["todos"] = []
        self.state["next_id"] = 1

def save_todos(self):
    with open("todos.json", "w") as f:
        json.dump({
            "todos": self.state["todos"],
            "next_id": self.state["next_id"]
        }, f)

def updated(self):
    # Save after each update
    self.save_todos()
```

### 3. Add Priority Levels

Add priority to each todo:

```python
todo = {
    "id": self.state["next_id"],
    "text": text,
    "completed": False,
    "priority": "normal"  # low, normal, high
}
```

```html
<qcombobox
  :items="['low', 'normal', 'high']"
  :current-text="todo['priority']"
  @activated="lambda idx: set_priority(todo['id'], ['low', 'normal', 'high'][idx])"
/>
```

### 4. Add Due Dates

Include date picker for due dates:

```html
<date-edit
  :date="todo['due_date']"
  @date-changed="lambda date: set_due_date(todo['id'], date)"
/>
```

### 5. Add Categories/Tags

Organize todos with tags:

```python
def init(self):
    # ... existing state
    self.state["tags"] = []

# Each todo has a "tags" list
todo = {
    "id": 1,
    "text": "Learn Collagraph",
    "completed": False,
    "tags": ["learning", "programming"]
}
```

## Topics Covered

- v-for directive for list rendering
- Form input handling with line-edit
- Array manipulation in reactive state
- Computed properties with `@property`
- Lambda functions in event handlers
- Conditional rendering with v-if
- Conditional button enabling
- List filtering and searching
- Key attribute for list optimization

## See Also

- [Building a Todo App](../guides/todo-app.md) - More detailed tutorial
- [v-for Directive](../core-concepts/directives/v-for.md)
- [v-if Directive](../core-concepts/directives/v-if.md)
- [State Management](../core-concepts/state-management.md)
- [Computed Properties](../core-concepts/computed.md)
- [Events](../core-concepts/events.md)
