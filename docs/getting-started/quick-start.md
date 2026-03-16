# Quick Start

This guide will help you create your first Collagraph application in minutes.

## Your First App

Create a file called `counter.cgx`:

```html
<window title="Counter App">
  <v-box>
    <label :text="f'Count: {count}'" />
    <button text="Increment" @clicked="increment" />
  </v-box>
</window>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1
</script>
```

## Run Your App

There are several ways to run your Collagraph app:

### Using the Collagraph CLI

```bash
python -m collagraph counter.cgx
```

### Using uv (no installation required)

If you have `uv` installed, you can run the app without installing Collagraph first:

```bash
uv run collagraph counter.cgx
```

This automatically handles dependencies and runs your app in an isolated environment.

### As a Python Script

Add a main block to your `counter.cgx`:

```python
# At the end of the <script> section
if __name__ == "__main__":
    import collagraph as cg
    from collagraph.renderers import PySideRenderer
    app = cg.Collagraph(Counter, PySideRenderer)
    app.run()
```

Then run:
```bash
python counter.cgx
```

That's it! You should see a window with a label showing the count and a button to increment it.

## What's Happening?

Let's break down the code to understand Collagraph's key concepts:

### 1. Template Section
```html
<window title="Counter App">
  <v-box>
    <label :text="f'Count: {count}'" />
    <button text="Increment" @clicked="increment" />
  </v-box>
</window>
```

- **HTML-like syntax**: Defines your UI structure declaratively
- **`<window>`**: The root widget (creates a Qt window with PySide)
- **`<v-box>`**: A vertical layout container
- **`<label>` and `<button>`**: PySide6 widgets

### 2. Reactive Binding
```html
:text="f'Count: {count}'"
```

- The `:` prefix creates a **reactive binding**
- The expression is re-evaluated automatically when `count` changes
- Uses Python f-strings for string formatting
- Direct access to `count` from `self.state["count"]`

### 3. Event Handling
```html
@clicked="increment"
```

- The `@` prefix binds events to methods
- `clicked` is the PySide6 button's signal name
- Calls the `increment` method when the button is clicked

### 4. Component Class
```python
class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1
```

- **`init()`**: Called when component is created (like `__init__`)
- **`self.state`**: A reactive dictionary powered by [observ](https://github.com/fork-tongue/observ)
- When `self.state` changes, the component automatically re-renders

## Using Pure Python

You can also write Collagraph apps without `.cgx` files using pure Python:

**counter.py:**
```python
import collagraph as cg
from collagraph.renderers import PySideRenderer

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1

    def render(self):
        return {
            "type": "window",
            "title": "Counter App",
            "children": [
                {
                    "type": "v-box",
                    "children": [
                        {
                            "type": "label",
                            "text": f"Count: {self.state['count']}"
                        },
                        {
                            "type": "button",
                            "text": "Increment",
                            "on_clicked": self.increment
                        }
                    ]
                }
            ]
        }

if __name__ == "__main__":
    app = cg.Collagraph(Counter, PySideRenderer)
    app.run()
```

Run it with:
```bash
python counter.py
```

### When to Use Each Approach

**Use `.cgx` files when:**
- Building UI-heavy applications
- You prefer declarative templates
- Working with designers who understand HTML
- You want syntax highlighting for templates

**Use pure Python when:**
- Building programmatic/dynamic UIs
- Integrating with existing Python codebases
- You prefer everything in Python
- Creating libraries or reusable components

## Building a Todo App

Let's create something slightly more complex - a todo list:

**todo.cgx:**
```html
<window title="Todo List" :width="400" :height="300">
  <v-box>
    <h-box>
      <line-edit
        :text="new_todo"
        @text-changed="update_input"
        placeholder="Enter a task..."
      />
      <button text="Add" @clicked="add_todo" />
    </h-box>

    <list-widget>
      <list-widget-item
        v-for="todo in todos"
        :key="todo"
        :text="todo"
      />
    </list-widget>
  </v-box>
</window>

<script>
import collagraph as cg

class TodoApp(cg.Component):
    def init(self):
        self.state["todos"] = []
        self.state["new_todo"] = ""

    def update_input(self, text):
        self.state["new_todo"] = text

    def add_todo(self):
        if self.state["new_todo"].strip():
            self.state["todos"].append(self.state["new_todo"])
            self.state["new_todo"] = ""
</script>
```

This example demonstrates:
- Multiple UI components (input field, button, list)
- The `v-for` directive for rendering lists
- Two-way data binding with input fields
- State management with multiple values

## Exploring Examples

Collagraph comes with many examples in the repository:

```bash
# Clone the repository to access examples
git clone https://github.com/fork-tongue/collagraph.git
cd collagraph

# Run examples with uv (recommended)
uv run collagraph examples/pyside/counter.cgx
uv run collagraph examples/pyside/todo_list.cgx
uv run collagraph examples/pyside/tree_view_example.cgx

# Or install and run with Python
pip install -e ".[pyside]"
python -m collagraph examples/pyside/counter.cgx
```

## Next Steps

### Core Concepts
- **[Components](../core-concepts/components.md)** - Deep dive into component architecture
- **[Template Syntax](../core-concepts/template-syntax.md)** - Master the template language
- **[Reactivity](../core-concepts/reactivity.md)** - Understand the reactive system
- **[State Management](../core-concepts/state-management.md)** - Manage application state
- **[Props](../core-concepts/props.md)** - Pass data between components
- **[Events](../core-concepts/events.md)** - Handle user interactions

### Template Directives
- **[v-if](../core-concepts/directives/v-if.md)** - Conditional rendering
- **[v-for](../core-concepts/directives/v-for.md)** - List rendering
- **[v-bind](../core-concepts/directives/v-bind.md)** - Dynamic attributes
- **[v-on](../core-concepts/directives/v-on.md)** - Event handling

### Renderers
- **[PySide Renderer](../renderers/pyside.md)** - Build Qt desktop applications
- **[Pygfx Renderer](../renderers/pygfx.md)** - Create 3D graphics and visualizations
- **[Custom Renderers](../renderers/custom-renderer.md)** - Build your own renderer

### Guides
- **[Your First Component](first-component.md)** - Component building blocks
- **[Project Structure](project-structure.md)** - Organize your code
- **[Todo App Tutorial](../guides/todo-app.md)** - Build a complete application

### Resources
- [GitHub Repository](https://github.com/fork-tongue/collagraph)
- [API Reference](../api-reference/component.md)
- [Examples Directory](../../examples/)
