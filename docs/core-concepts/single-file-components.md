# Single-File Components (.cgx)

## Overview

`.cgx` (Collagraph eXtension) files allow you to define components with template and code in a single file, similar to Vue's `.vue` files. This approach keeps related template markup and component logic together, making components more maintainable and easier to understand.

## File Structure

A `.cgx` file consists of two main sections:

1. **Template section**: The HTML-like markup that defines the component's UI
2. **`<script>` section**: The Python code that defines the component class

```html
<!-- Template section (outside <script> tag) -->
<widget>
  <label :text="message" />
  <button text="Click me" @clicked="increment" />
</widget>

<!-- Script section -->
<script>
import collagraph as cg

class MyComponent(cg.Component):
    def init(self):
        self.state["message"] = "Hello"
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1
</script>
```

## The `<script>` Tag

The `<script>` tag contains Python code that defines your component class and any imports:

```html
<widget>
  <label text="Counter Example" />
</widget>

<script>
import collagraph as cg
from typing import Optional

# You can import other modules
import json

# Import other components
from child_component import ChildComponent

class Counter(cg.Component):
    """Component docstrings are preserved"""

    def init(self):
        self.state["count"] = self.props.get("initial", 0)

    def increment(self):
        self.state["count"] += 1

    def decrement(self):
        self.state["count"] -= 1
</script>
```

### Script Tag Attributes

The `<script>` tag optionally supports a `lang` attribute (though only Python is currently supported):

```html
<script lang="python">
import collagraph as cg

class MyComponent(cg.Component):
    pass
</script>
```

### Multiple Classes

You can define multiple classes in the `<script>` section, but only one should extend `cg.Component`. The component class should be defined last or be the main class:

```html
<script>
import collagraph as cg

class DataProcessor:
    """Helper class"""
    def process(self, data):
        return data.upper()

class MyComponent(cg.Component):
    """Main component class"""
    def init(self):
        self.processor = DataProcessor()
</script>
```

## Template Section

Everything outside the `<script>` tag is the template. The template must have a root element (or multiple root elements will be wrapped in a fragment):

### Single Root Element

```html
<widget>
  <label text="Title" />
  <button text="Click" @clicked="handle_click" />
</widget>

<script>
import collagraph as cg

class MyComponent(cg.Component):
    def handle_click(self):
        print("Clicked!")
</script>
```

### Multiple Root Elements

If you have multiple root elements, they will be rendered as a fragment:

```html
<label text="First element" />
<button text="Second element" />
<input value="Third element" />

<script>
import collagraph as cg

class MyComponent(cg.Component):
    pass
</script>
```

### Comments in Templates

You can add comments in the template section:

```html
<!--
  This is a template comment.
  It will be stripped during compilation.
-->
<widget>
  <label text="Hello" />
  <!-- Inline comment -->
</widget>

<script>
import collagraph as cg

class MyComponent(cg.Component):
    pass
</script>
```

## Importing Components

After importing collagraph, you can import `.cgx` files directly as if they were Python modules:

```python
# main.py
import collagraph as cg

# Import .cgx components like regular Python modules
from counter import Counter
from user_profile import UserProfile

gui = cg.Collagraph(renderer=cg.PySideRenderer())
app = QtWidgets.QApplication()
gui.render(Counter, app)
app.exec()
```

### Importing in Templates

You can also import components within `.cgx` files:

```html
<widget>
  <Counter initial="0" />
  <UserProfile :user="current_user" />
</widget>

<script>
import collagraph as cg

# Import other .cgx components
from counter import Counter
from user_profile import UserProfile

class Dashboard(cg.Component):
    def init(self):
        self.state["current_user"] = {"name": "Alice", "age": 30}
</script>
```

## Module System

### File Paths

Collagraph's import system works with Python's standard import mechanism. The `.cgx` files must be in your Python path:

```
my_project/
├── main.py
├── components/
│   ├── __init__.py
│   ├── counter.cgx
│   └── user_profile.cgx
└── utils/
    └── helpers.py
```

Import them using standard Python imports:

```python
from components.counter import Counter
from components.user_profile import UserProfile
```

### The `__file__` Variable

Inside `.cgx` files, you can use `__file__` to get the current file's path:

```html
<label :text="current_file" />

<script>
import collagraph as cg
import os

class FileInfo(cg.Component):
    def init(self):
        # __file__ is available in .cgx files
        self.state["current_file"] = os.path.basename(__file__)
</script>
```

### Relative Imports

Relative imports work as expected:

```html
<script>
import collagraph as cg

# Relative imports
from .utils import helper_function
from ..common import BaseComponent

class MyComponent(BaseComponent):
    pass
</script>
```

## Running .cgx Files Directly

Collagraph provides a CLI that allows you to run `.cgx` files directly without writing a separate entry point:

```bash
# Run a .cgx component directly
uv run collagraph examples/pyside/counter.cgx

# Specify the renderer (defaults to PySide)
uv run collagraph --renderer pyside examples/pyside/counter.cgx

# Run with PyGfx renderer
uv run collagraph --renderer pygfx examples/pygfx/scene.cgx

# Pass initial state as JSON
uv run collagraph --state '{"count": 100}' examples/pyside/counter.cgx
```

This is extremely convenient for quick prototyping and testing components in isolation.

## Syntax Highlighting

Collagraph provides syntax highlighting extensions for popular editors:

### Visual Studio Code

Install the [CGX syntax highlight for VSCode](https://github.com/fork-tongue/cgx-syntax-highlight-vscode) extension:

1. Open VSCode
2. Search for "CGX" in the extensions marketplace
3. Install the extension
4. `.cgx` files will now have proper syntax highlighting

### Sublime Text

Install the [CGX syntax highlight for Sublime Text](https://github.com/fork-tongue/cgx-syntax-highlight-sublime) package:

1. Open Sublime Text
2. Open Package Control (`Cmd+Shift+P` on Mac, `Ctrl+Shift+P` on Windows/Linux)
3. Select "Package Control: Install Package"
4. Search for "CGX Syntax Highlight"
5. Install the package

### Features

Both extensions provide:
- Template syntax highlighting
- Python syntax highlighting in `<script>` sections
- Proper indentation
- Code folding
- Autocomplete support (in some editors)

## Linting and Formatting

You can lint and format `.cgx` files using [ruff-cgx](https://github.com/fork-tongue/ruff-cgx), a specialized tool for Collagraph files:

```bash
# Install ruff-cgx
pip install ruff-cgx

# Format a .cgx file
ruff-cgx format my_component.cgx

# Lint a .cgx file
ruff-cgx check my_component.cgx

# Auto-fix issues
ruff-cgx check --fix my_component.cgx
```

## Best Practices

### 1. One Component Per File

Keep each `.cgx` file focused on a single component:

```html
<!-- counter.cgx -->
<widget>
  <label :text="f'Count: {count}'" />
  <button text="Increment" @clicked="increment" />
</widget>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1
</script>
```

### 2. Name Files After Components

Use descriptive filenames that match your component class names:

```
counter.cgx          → Counter
user_profile.cgx     → UserProfile
todo_list.cgx        → TodoList
```

### 3. Organize with Folders

Group related components in folders:

```
components/
├── layout/
│   ├── header.cgx
│   ├── footer.cgx
│   └── sidebar.cgx
├── forms/
│   ├── input.cgx
│   ├── button.cgx
│   └── checkbox.cgx
└── widgets/
    ├── card.cgx
    └── modal.cgx
```

### 4. Keep Templates Readable

Format your templates for readability:

```html
<!-- Good: Readable, well-indented -->
<widget>
  <label text="User Profile" />
  <widget :layout="{'type': 'Box', 'direction': 'LeftToRight'}">
    <label text="Name:" />
    <line-edit :value="name" />
  </widget>
  <button text="Save" @clicked="save" />
</widget>

<!-- Less readable: All on one line -->
<widget><label text="User Profile" /><widget :layout="{'type': 'Box', 'direction': 'LeftToRight'}"><label text="Name:" /><line-edit :value="name" /></widget><button text="Save" @clicked="save" /></widget>
```

### 5. Add Documentation

Use docstrings and comments to document your components:

```html
<widget>
  <label :text="title" />
</widget>

<script>
import collagraph as cg

class UserCard(cg.Component):
    """
    Displays a user's information in a card format.

    Props:
        user (dict): User data with 'name', 'email', and 'avatar' keys
        editable (bool): Whether the card is editable

    Events:
        - edit: Emitted when the edit button is clicked
        - delete: Emitted when the delete button is clicked
    """

    def init(self):
        user = self.props.get("user", {})
        self.state["title"] = user.get("name", "Unknown User")
</script>
```

## Complete Example

Here's a complete example showing a todo list component in a `.cgx` file:

```html
<!--
  A simple todo list component
  Run with: uv run collagraph examples/todo_list.cgx
-->
<window title="Todo List" width="400" height="500">
  <widget>
    <!-- Input area -->
    <widget :layout="{'type': 'Box', 'direction': 'LeftToRight'}">
      <line-edit
        ref="todoInput"
        placeholder="Enter a todo..."
        @return-pressed="add_todo"
      />
      <button text="Add" @clicked="add_todo" />
    </widget>

    <!-- Todo items -->
    <widget v-for="idx, todo in enumerate(todos)">
      <widget :layout="{'type': 'Box', 'direction': 'LeftToRight'}">
        <checkbox
          :checked="todo['completed']"
          @toggled="lambda: toggle_todo(idx)"
        />
        <label :text="todo['text']" />
        <button
          text="Delete"
          @clicked="lambda: delete_todo(idx)"
        />
      </widget>
    </widget>

    <!-- Status -->
    <label :text="f'{remaining_count} items remaining'" />
  </widget>
</window>

<script>
import collagraph as cg

class TodoList(cg.Component):
    """A simple todo list application"""

    def init(self):
        self.state["todos"] = []

    @property
    def remaining_count(self):
        """Count of incomplete todos"""
        return sum(1 for todo in self.state["todos"] if not todo["completed"])

    def add_todo(self):
        """Add a new todo from the input field"""
        if "todoInput" in self.refs:
            text = self.refs["todoInput"].text()
            if text.strip():
                self.state["todos"].append({
                    "text": text,
                    "completed": False
                })
                self.refs["todoInput"].clear()

    def toggle_todo(self, idx):
        """Toggle todo completion status"""
        self.state["todos"][idx]["completed"] = not self.state["todos"][idx]["completed"]

    def delete_todo(self, idx):
        """Delete a todo"""
        self.state["todos"].pop(idx)
</script>
```

## See Also

- [Installation](../getting-started/installation.md) (for editor setup)
- [Template Syntax](template-syntax.md)
