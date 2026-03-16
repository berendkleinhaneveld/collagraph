# Example: Counter

A simple counter application demonstrating state management and event handling.

## Overview

This example demonstrates the fundamentals of building interactive applications with Collagraph. You'll learn how to manage state, handle user events, and create reactive UI bindings. The counter is the perfect starting point for understanding Collagraph's core concepts.

### What You'll Learn

- How to initialize and manage component state
- How to handle button click events
- How to create reactive text bindings
- How to structure layouts with v-box and h-box
- The basics of single-file components (.cgx files)

## Complete Code

Create a file called `counter.cgx`:

```html
<window title="Counter">
  <v-box>
    <label :text="f'Count: {count}'" />
    <h-box>
      <button text="Increment" @clicked="increment" />
      <button text="Decrement" @clicked="decrement" />
      <button text="Reset" @clicked="reset" />
    </h-box>
  </v-box>
</window>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1

    def decrement(self):
        self.state["count"] -= 1

    def reset(self):
        self.state["count"] = 0
</script>
```

## Step-by-Step Breakdown

### 1. Template Structure

The template defines the UI structure using HTML-like syntax:

```html
<window title="Counter">
  <v-box>
    <!-- content -->
  </v-box>
</window>
```

- `<window>` creates a top-level application window with a title
- `<v-box>` creates a vertical layout container that stacks children top-to-bottom

### 2. Reactive Text Binding

```html
<label :text="f'Count: {count}'" />
```

The `:text` attribute creates a reactive binding. The colon (`:`) prefix indicates this is a dynamic binding that will automatically update when the `count` state changes. We use a Python f-string to format the display text.

### 3. Layout with h-box

```html
<h-box>
  <button text="Increment" @clicked="increment" />
  <button text="Decrement" @clicked="decrement" />
  <button text="Reset" @clicked="reset" />
</h-box>
```

The `<h-box>` arranges the three buttons horizontally (left-to-right).

### 4. Event Handling

```html
<button text="Increment" @clicked="increment" />
```

The `@clicked` attribute connects the button's click event to the `increment` method. The `@` prefix indicates this is an event binding.

### 5. State Initialization

```python
def init(self):
    self.state["count"] = 0
```

The `init()` lifecycle method runs when the component is created. Here we initialize the `count` state to 0. The `state` dictionary is reactive - any changes trigger UI updates.

### 6. Event Handler Methods

```python
def increment(self):
    self.state["count"] += 1

def decrement(self):
    self.state["count"] -= 1

def reset(self):
    self.state["count"] = 0
```

Each method modifies the `count` state. When the state changes, Collagraph automatically re-renders the label with the new value.

## How to Run

### Using the CLI

```bash
uv run collagraph counter.cgx
```

Or with Python:

```bash
python -m collagraph counter.cgx
```

### Creating a Python Entry Point

You can also create a separate Python file to run the component:

```python
# main.py
from PySide6 import QtWidgets
import collagraph as cg
from counter import Counter

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    gui = cg.Collagraph(renderer=cg.PySideRenderer())
    gui.render(Counter, app)
    app.exec()
```

Run it with:

```bash
python main.py
```

## Key Concepts

### Reactive State

The `self.state` dictionary is the heart of Collagraph's reactivity system:

```python
self.state["count"] = 0  # Initialize
self.state["count"] += 1  # Update triggers re-render
```

Any modification to `state` automatically updates all UI elements bound to that state.

### Event Binding Syntax

- `@clicked` - Button click event
- `@text-changed` - Text input change
- `@toggled` - Checkbox toggle

Events connect UI interactions to Python methods.

### Attribute Binding Syntax

- `text="static"` - Static attribute (won't change)
- `:text="dynamic"` - Dynamic attribute (reactive, evaluates as Python expression)

## Possible Extensions

### 1. Add Step Size Control

Add a number input to control the increment/decrement step:

```html
<spin-box :value="step" @value-changed="set_step" minimum="1" maximum="10" />
```

```python
def init(self):
    self.state["count"] = 0
    self.state["step"] = 1

def set_step(self, value):
    self.state["step"] = value

def increment(self):
    self.state["count"] += self.state["step"]
```

### 2. Add Min/Max Limits

Prevent the counter from going below/above certain values:

```python
def increment(self):
    if self.state["count"] < 100:
        self.state["count"] += 1

def decrement(self):
    if self.state["count"] > 0:
        self.state["count"] -= 1
```

### 3. Add Visual Feedback

Change the label color based on the count value:

```html
<label
  :text="f'Count: {count}'"
  :style-sheet="label_style"
/>
```

```python
@property
def label_style(self):
    count = self.state["count"]
    if count < 0:
        return "color: red;"
    elif count > 10:
        return "color: green;"
    return "color: black;"
```

### 4. Add Keyboard Shortcuts

Handle keyboard events for faster interaction:

```html
<window title="Counter" @key-press="handle_key">
  <!-- content -->
</window>
```

```python
def handle_key(self, event):
    if event.key() == QtCore.Qt.Key_Up:
        self.increment()
    elif event.key() == QtCore.Qt.Key_Down:
        self.decrement()
```

### 5. Add History Tracking

Keep track of all counter changes:

```python
def init(self):
    self.state["count"] = 0
    self.state["history"] = [0]

def increment(self):
    self.state["count"] += 1
    self.state["history"].append(self.state["count"])
```

## Topics Covered

- State management with `self.state`
- Event handling with `@` syntax
- Reactive bindings with `:` prefix
- Layout components (v-box, h-box)
- Component lifecycle (`init` method)
- Single-file components (.cgx files)

## See Also

- [Quick Start](../getting-started/quick-start.md)
- [State Management](../core-concepts/state-management.md)
- [Event Handling](../core-concepts/events.md)
- [Components](../core-concepts/components.md)
- [Template Syntax](../core-concepts/template-syntax.md)
