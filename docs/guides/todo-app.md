# Building a Todo App

This guide walks you through building a complete todo application with Collagraph, demonstrating core concepts like state management, event handling, list rendering, and conditional rendering.

## Overview

In this tutorial, you'll build a fully functional todo application that allows users to:
- Add new todo items
- Mark items as complete/incomplete
- Delete items
- Filter between all, active, and completed todos
- See the count of remaining active items

By the end of this guide, you'll understand how to combine Collagraph's reactive state, directives, and event system to build interactive applications.

## What We'll Build

The final application will have:
- An input field to add new todos
- A list of todos with checkboxes to mark them complete
- A delete button for each todo
- Filter buttons (All / Active / Completed)
- A counter showing remaining active items
- A button to clear all completed items

## Step 1: Project Setup

First, create a new file called `todo.cgx`. This single-file component will contain our entire todo application.

## Step 2: Basic Component Structure

Let's start with the basic structure of our component:

```html
<widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
  <label text="Todo App" />
</widget>

<script>
import collagraph as cg


class TodoApp(cg.Component):
    def init(self):
        # We'll add state here soon
        pass
</script>
```

This creates a simple widget with a vertical layout and a title label.

## Step 3: Setting Up State

Now let's add the state to manage our todos. Update the `init` method:

```python
def init(self):
    self.state["todos"] = []
    self.state["new_todo_text"] = ""
    self.state["filter"] = "all"  # all, active, or completed
    self.state["next_id"] = 1
```

Our state includes:
- `todos`: List of todo items (each with `id`, `text`, and `completed` properties)
- `new_todo_text`: The text in the input field
- `filter`: Current filter selection
- `next_id`: Auto-incrementing ID for new todos

## Step 4: Adding the Input Field

Let's add an input field to create new todos. Update the template:

```html
<widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
  <label text="Todo App" />

  <!-- Input section -->
  <widget :layout="{'type': 'box', 'direction': 'left-to-right'}">
    <lineedit
      :text="new_todo_text"
      placeholder-text="What needs to be done?"
      @text-changed="on_input_change"
      @return-pressed="add_todo"
    />
    <button
      text="Add"
      @clicked="add_todo"
    />
  </widget>
</widget>
```

Now add the corresponding methods in the script section:

```python
def on_input_change(self, text):
    self.state["new_todo_text"] = text

def add_todo(self):
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
```

## Step 5: Displaying the Todo List

Now let's render the list of todos using the `v-for` directive:

```html
<!-- Add this after the input section -->
<widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
  <widget
    v-for="todo in filtered_todos"
    :key="todo['id']"
    :layout="{'type': 'box', 'direction': 'left-to-right'}"
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
  </widget>
</widget>
```

We'll use a computed property to filter todos. Add this to your component class:

```python
@property
def filtered_todos(self):
    todos = self.state["todos"]
    filter_type = self.state["filter"]

    if filter_type == "active":
        return [t for t in todos if not t["completed"]]
    elif filter_type == "completed":
        return [t for t in todos if t["completed"]]
    else:  # all
        return todos
```

And add the event handler methods:

```python
def toggle_todo(self, todo_id, checked):
    for todo in self.state["todos"]:
        if todo["id"] == todo_id:
            todo["completed"] = checked
            break

def delete_todo(self, todo_id):
    self.state["todos"] = [
        t for t in self.state["todos"] if t["id"] != todo_id
    ]
```

## Step 6: Adding Filter Buttons

Add filter buttons to switch between viewing all, active, or completed todos:

```html
<!-- Add this after the todo list -->
<widget :layout="{'type': 'box', 'direction': 'left-to-right'}">
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
</widget>
```

Add the filter method:

```python
def set_filter(self, filter_type):
    self.state["filter"] = filter_type
```

## Step 7: Adding Status Information

Let's add a footer showing the count of active items and a button to clear completed todos:

```html
<!-- Add this at the end, before closing the main widget -->
<widget :layout="{'type': 'box', 'direction': 'left-to-right'}">
  <label :text="f'{active_count} item(s) left'" />
  <button
    text="Clear completed"
    @clicked="clear_completed"
    :enabled="has_completed"
  />
</widget>
```

Add the corresponding properties and methods:

```python
@property
def active_count(self):
    return sum(1 for t in self.state["todos"] if not t["completed"])

@property
def has_completed(self):
    return any(t["completed"] for t in self.state["todos"])

def clear_completed(self):
    self.state["todos"] = [
        t for t in self.state["todos"] if not t["completed"]
    ]
```

## Step 8: The Complete Application

Here's the complete `todo.cgx` file:

```html
<widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
  <label text="Todo App" />

  <!-- Input section -->
  <widget :layout="{'type': 'box', 'direction': 'left-to-right'}">
    <lineedit
      :text="new_todo_text"
      placeholder-text="What needs to be done?"
      @text-changed="on_input_change"
      @return-pressed="add_todo"
    />
    <button
      text="Add"
      @clicked="add_todo"
    />
  </widget>

  <!-- Todo list -->
  <widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
    <widget
      v-for="todo in filtered_todos"
      :key="todo['id']"
      :layout="{'type': 'box', 'direction': 'left-to-right'}"
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
    </widget>
  </widget>

  <!-- Filter buttons -->
  <widget :layout="{'type': 'box', 'direction': 'left-to-right'}">
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
  </widget>

  <!-- Footer -->
  <widget :layout="{'type': 'box', 'direction': 'left-to-right'}">
    <label :text="f'{active_count} item(s) left'" />
    <button
      text="Clear completed"
      @clicked="clear_completed"
      :enabled="has_completed"
    />
  </widget>
</widget>

<script>
import collagraph as cg


class TodoApp(cg.Component):
    def init(self):
        self.state["todos"] = []
        self.state["new_todo_text"] = ""
        self.state["filter"] = "all"
        self.state["next_id"] = 1

    @property
    def filtered_todos(self):
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
        return sum(1 for t in self.state["todos"] if not t["completed"])

    @property
    def has_completed(self):
        return any(t["completed"] for t in self.state["todos"])

    def on_input_change(self, text):
        self.state["new_todo_text"] = text

    def add_todo(self):
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
        for todo in self.state["todos"]:
            if todo["id"] == todo_id:
                todo["completed"] = checked
                break

    def delete_todo(self, todo_id):
        self.state["todos"] = [
            t for t in self.state["todos"] if t["id"] != todo_id
        ]

    def set_filter(self, filter_type):
        self.state["filter"] = filter_type

    def clear_completed(self):
        self.state["todos"] = [
            t for t in self.state["todos"] if not t["completed"]
        ]
</script>
```

## Running the Application

You can run the application directly with the Collagraph CLI:

```bash
uv run collagraph todo.cgx
```

Or create a Python entry point:

```python
from PySide6 import QtWidgets
import collagraph as cg
from todo import TodoApp

app = QtWidgets.QApplication()
gui = cg.Collagraph(renderer=cg.PySideRenderer())
gui.render(TodoApp, app)
app.exec()
```

## Key Concepts Demonstrated

### Reactive State
The `self.state` dictionary is reactive. Any changes to it automatically update the UI:
- Adding/removing items from `self.state["todos"]` updates the list
- Changing `self.state["filter"]` updates which todos are shown

### List Rendering with v-for
The `v-for` directive creates a widget for each todo in `filtered_todos`:
```html
<widget
  v-for="todo in filtered_todos"
  :key="todo['id']"
  ...
>
```

The `:key` attribute is crucial for performance - it helps Collagraph track which items have changed.

### Computed Properties
Python `@property` decorators create computed values that automatically update:
```python
@property
def filtered_todos(self):
    # Automatically recomputes when state["todos"] or state["filter"] changes
    ...
```

### Event Handling
Events are handled with the `@` syntax:
```html
<button @clicked="add_todo" />
<checkbox @toggled="lambda checked: toggle_todo(todo['id'], checked)" />
```

Lambdas let you pass arguments to event handlers.

## Common Pitfalls

### 1. Forgetting to Update State Correctly
```python
# Wrong - mutating without reassignment
self.state["todos"][0]["completed"] = True  # This works

# Also works, but be aware
todo = self.state["todos"][0]
todo["completed"] = True  # This works because dicts are mutable

# For arrays, reassignment ensures reactivity
self.state["todos"] = [t for t in self.state["todos"] if t["id"] != todo_id]
```

### 2. Not Using Keys in v-for
Always provide a unique `:key` when using `v-for`:
```html
<!-- Bad -->
<widget v-for="todo in todos">

<!-- Good -->
<widget v-for="todo in todos" :key="todo['id']">
```

### 3. Modifying State in Computed Properties
Computed properties should only read state, never modify it:
```python
# Wrong
@property
def filtered_todos(self):
    self.state["count"] += 1  # Don't do this!
    return self.state["todos"]

# Right
@property
def filtered_todos(self):
    return [t for t in self.state["todos"] if not t["completed"]]
```

## Next Steps

Now that you've built a todo app, you can:
1. Add persistence with local storage or a database
2. Add editing functionality for todo text
3. Add drag-and-drop reordering
4. Split the app into multiple components
5. Add animations for adding/removing items

## See Also

- [State Management](../core-concepts/state-management.md)
- [v-for Directive](../core-concepts/directives/v-for.md)
- [v-if Directive](../core-concepts/directives/v-if.md)
- [Events](../core-concepts/events.md)
- [Computed Properties](../core-concepts/computed.md)
