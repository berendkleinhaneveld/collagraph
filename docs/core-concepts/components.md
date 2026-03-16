# Components

## Overview

Components are the building blocks of Collagraph applications. Each component is a Python class that extends `cg.Component`. Components encapsulate UI logic, manage state, and handle user interactions in a declarative way.

Collagraph's component model is inspired by Vue.js, providing a familiar and intuitive API for developers coming from web development backgrounds while adapting it for Python desktop and graphics applications.

## Component Class Structure

Every component in Collagraph must extend the `Component` base class and can define several lifecycle hooks and methods:

```python
import collagraph as cg

class MyComponent(cg.Component):
    def init(self):
        """
        Called when the component is created.
        Initialize state and component properties here.
        """
        self.state["message"] = "Hello, Collagraph!"
        self.state["count"] = 0

    def mounted(self):
        """
        Called after the component is mounted to the DOM.
        Use this for setup that requires DOM access.
        """
        pass

    def updated(self):
        """
        Called after the component updates.
        React to state or prop changes here.
        """
        pass

    def before_unmount(self):
        """
        Called before the component is unmounted.
        Clean up subscriptions, timers, etc.
        """
        pass
```

## The `render()` Method

In class-based components (non-.cgx files), you must implement the `render()` method. This method describes what the component should render:

```python
class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def render(self, renderer):
        # Return a fragment that describes the UI
        return renderer.create_fragment(
            tag="widget",
            children=[
                {"type": "label", "text": f"Count: {self.state['count']}"},
                {"type": "button", "text": "Increment", "on_clicked": self.increment}
            ]
        )

    def increment(self):
        self.state["count"] += 1
```

However, most users will prefer using **Single-File Components (.cgx files)** where the template syntax handles rendering declaratively.

## Component Registration

Components defined in `.cgx` files are automatically registered and can be imported like regular Python modules:

```python
# After importing collagraph, you can import .cgx files
import collagraph as cg
from counter import Counter  # counter.cgx file

# The Counter component is now available to use
```

In templates, components are used by their class name as tags:

```html
<MyComponent />
<Counter initial-count="0" />
```

## Component Composition

Components can be composed together to build complex UIs. Child components can be nested within parent components:

**Parent.cgx:**
```html
<widget>
  <label text="Parent Component" />
  <ChildComponent message="Hello from parent" />
</widget>

<script>
import collagraph as cg
from child import ChildComponent

class Parent(cg.Component):
    pass
</script>
```

**Child.cgx:**
```html
<label :text="message" />

<script>
import collagraph as cg

class ChildComponent(cg.Component):
    def init(self):
        self.state["message"] = self.props.get("message", "Default")
</script>
```

### Component Hierarchy

Components form a parent-child hierarchy. You can access the parent component using `self.parent`:

```python
class Child(cg.Component):
    def init(self):
        # Access the parent component
        parent = self.parent
        if parent:
            print(f"My parent is: {parent.__class__.__name__}")
```

## Props vs State

Understanding the distinction between props and state is crucial:

### Props
- **Data passed from parent to child**
- **Read-only** within the component
- Defined by the parent component
- Accessed via `self.props`

```python
class ChildComponent(cg.Component):
    def init(self):
        # Access props (read-only)
        name = self.props.get("name", "Guest")
        age = self.props.get("age", 0)
```

### State
- **Internal data owned by the component**
- **Mutable** and reactive
- Changes trigger re-renders
- Accessed via `self.state`

```python
class Counter(cg.Component):
    def init(self):
        # Initialize state (mutable, reactive)
        self.state["count"] = 0

    def increment(self):
        # Modifying state triggers re-render
        self.state["count"] += 1
```

### One-Way Data Flow

Collagraph enforces **one-way data flow**:
- Props flow **down** from parent to child
- Events flow **up** from child to parent
- Children cannot modify props directly

```html
<!-- Parent passes props down -->
<Counter :initial-value="startCount" @increment="handleIncrement" />
```

## Component Communication

### Parent to Child: Props

Pass data to child components via props:

```html
<ChildComponent name="Alice" :age="30" />
```

### Child to Parent: Events

Child components emit events that parents can listen to:

**Child component:**
```python
class Child(cg.Component):
    def handle_click(self):
        # Emit event to parent
        self.emit("clicked", {"data": "some value"})
```

**Parent template:**
```html
<Child @clicked="handle_child_click" />
```

**Parent component:**
```python
class Parent(cg.Component):
    def handle_child_click(self, data):
        print(f"Child clicked with data: {data}")
```

### Deeply Nested Components: Provide/Inject

For passing data through multiple component levels, use provide/inject:

**Ancestor component:**
```python
class Ancestor(cg.Component):
    def init(self):
        # Provide a value that descendants can inject
        self.provide(key="theme", value="dark")
```

**Descendant component:**
```python
class Descendant(cg.Component):
    def init(self):
        # Inject the provided value
        theme = self.inject("theme", default="light")
        self.state["theme"] = theme
```

## Component Properties

Components have several special properties:

### `self.props`
Read-only dictionary of props passed from the parent.

### `self.state`
Reactive dictionary for component's local state.

### `self.refs`
Dictionary of template refs for accessing DOM elements and child components.

### `self.element`
Reference to the root DOM element of the component.

### `self.parent`
Reference to the parent component (or `None` for root).

## Best Practices

### 1. Initialize State in `init()`

Always initialize your component state in the `init()` method:

```python
def init(self):
    self.state["data"] = []
    self.state["loading"] = False
```

### 2. Keep Components Focused

Each component should have a single, well-defined responsibility. Break down complex UIs into smaller, reusable components.

### 3. Use Props for Configuration

Make components reusable by accepting props for configuration:

```python
def init(self):
    self.state["title"] = self.props.get("title", "Default Title")
    self.state["mode"] = self.props.get("mode", "view")
```

### 4. Clean Up in `before_unmount()`

Always clean up subscriptions, timers, and other resources:

```python
def init(self):
    self.timer_id = start_timer(self.update_time)

def before_unmount(self):
    cancel_timer(self.timer_id)
```

### 5. Don't Mutate Props

Props are read-only. If you need a mutable version, copy it to state:

```python
def init(self):
    # Copy prop to state if you need to modify it
    self.state["count"] = self.props.get("initial_count", 0)
```

### 6. Use Descriptive Names

Choose clear, descriptive names for components and their props:

```python
# Good
class UserProfile(cg.Component):
    pass

# Less clear
class UP(cg.Component):
    pass
```

## See Also

- [Props](props.md)
- [State Management](state-management.md)
- [Lifecycle Hooks](lifecycle.md)
