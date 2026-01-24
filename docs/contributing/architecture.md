# Architecture Overview

This document provides a high-level overview of Collagraph's architecture to help contributors understand how the system works.

## System Overview

Collagraph is a reactive UI framework inspired by Vue.js. It provides a component-based architecture with reactive state management, virtual DOM-like fragments, and pluggable renderers.

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│              (.cgx files, Component classes)             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                   Collagraph Core                        │
│  ┌──────────┐  ┌──────────┐  ┌─────────────────────┐   │
│  │Component │  │ Fragment │  │   SFC Compiler      │   │
│  │  System  │  │  System  │  │   (.cgx → AST)      │   │
│  └──────────┘  └──────────┘  └─────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 Reactivity Layer                         │
│              (observ library - reactive/computed)        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Renderer Layer                          │
│   ┌──────────┐  ┌──────────┐  ┌──────────────────┐     │
│   │ PySide   │  │  Pygfx   │  │  Dict (Testing)  │     │
│   │ Renderer │  │ Renderer │  │    Renderer      │     │
│   └──────────┘  └──────────┘  └──────────────────┘     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Backend Layer                           │
│              (PySide6, Pygfx, or custom)                 │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Component System

**Location**: `collagraph/component.py`

The `Component` class is the base class for all Collagraph components.

#### Key Responsibilities

- **State management**: Local reactive state via `self.state`
- **Props management**: Read-only properties via `self.props`
- **Lifecycle hooks**: `init()`, `mounted()`, `updated()`, `before_unmount()`
- **Event handling**: `emit()`, `add_event_handler()`, `remove_event_handler()`
- **Dependency injection**: `provide()` and `inject()`
- **Template refs**: Access to DOM elements via `self.refs`

#### Structure

```python
class Component:
    def __init__(self, props=None, parent=None):
        self._props = readonly(props or {})     # Immutable props
        self._state = reactive({})               # Reactive state
        self._refs = reactive({})                # Template refs
        self._event_handlers = defaultdict(set)  # Event system
        self._parent = ref(parent) if parent else None
        self.init()  # User-defined initialization

    @abstractmethod
    def render(self, renderer: Renderer) -> ComponentFragment:
        """Must be implemented by subclasses or SFC compiler"""
        raise NotImplementedError
```

#### Lookup Mechanism

Components use a `_lookup()` method to resolve names in templates:

1. Check `self.props`
2. Check `self.state`
3. Check `self.refs`
4. Check `self` attributes (methods)
5. Check global context

This enables template syntax like `{{ count }}` instead of `{{ self.state.count }}`.

### 2. Fragment System

**Location**: `collagraph/fragment.py`

Fragments are virtual DOM nodes that describe the structure of the UI. They serve as an intermediary between the Component system and the Renderer.

#### Fragment Types

1. **Fragment** - Base class for all fragments
2. **ComponentFragment** - Wraps a component instance
3. **TextFragment** - Text nodes
4. **ConditionalFragment** - For v-if/v-else-if/v-else
5. **ForFragment** - For v-for loops

#### Key Concepts

**Mounting**: Creating and inserting DOM elements
```python
def mount(self, target, anchor=None):
    """Create DOM elements and insert into target"""
    if self.tag:
        self.element = self.renderer.create_element(self.tag)
    # Mount children, apply attributes, register watchers
    self.renderer.insert(self.element, target, anchor)
    self._mounted = True
```

**Patching**: Updating existing DOM elements
```python
def patch(self):
    """Update DOM to match current state"""
    # Compare old and new children
    # Update attributes
    # Re-render if needed
```

**Unmounting**: Cleanup and removal
```python
def unmount(self):
    """Remove from DOM and cleanup"""
    self.before_unmount()  # Call lifecycle hook
    # Remove watchers, event listeners
    # Unmount children
    self.renderer.remove(self.element, self.target)
```

#### Fragment Tree

Fragments form a tree structure mirroring the component hierarchy:

```
ComponentFragment (App)
├── Fragment (div)
│   ├── TextFragment ("Count: ")
│   └── Fragment (span)
│       └── TextFragment (computed value)
└── Fragment (button)
    └── TextFragment ("Increment")
```

### 3. Renderer Architecture

**Location**: `collagraph/renderers/`

Renderers abstract the underlying UI framework, allowing Collagraph to work with different backends.

#### Renderer Interface

```python
class Renderer(metaclass=ABCMeta):
    """Abstract base class for renderers"""

    def create_element(self, type: str) -> Any:
        """Create an element of the given type"""
        pass

    def create_text_element(self) -> Any:
        """Create a text node"""
        pass

    def insert(self, el: Any, parent: Any, anchor: Any = None):
        """Insert element into parent"""
        pass

    def remove(self, el: Any, parent: Any):
        """Remove element from parent"""
        pass

    def set_element_text(self, el: Any, value: str):
        """Set text content"""
        pass

    def set_attribute(self, el: Any, attr: str, value: Any):
        """Set attribute/property"""
        pass

    def remove_attribute(self, el: Any, attr: str, value: Any):
        """Remove attribute/property"""
        pass

    def add_event_listener(self, el: Any, event_type: str, value: Callable):
        """Add event listener"""
        pass

    def remove_event_listener(self, el: Any, event_type: str, value: Callable):
        """Remove event listener"""
        pass
```

#### Built-in Renderers

**DictRenderer** (`dict_renderer.py`)
- For testing and debugging
- Renders to Python dictionaries
- No external dependencies

**PySideRenderer** (`pyside_renderer.py`)
- Renders to PySide6 (Qt) widgets
- Handles Qt-specific behaviors (signals, layouts, etc.)
- Event loop integration

**PygfxRenderer** (`pygfx_renderer.py`)
- Renders 3D graphics scenes
- Uses pygfx library
- Camera, lights, meshes, etc.

#### Renderer Specifics: PySide

The PySide renderer has special handling for:

1. **Layouts**: Automatic layout management for QWidget children
2. **Signals**: Mapping Qt signals to Collagraph events (`@clicked`, etc.)
3. **Properties**: Setting widget properties via `set_attribute`
4. **Dialogs**: Special handling for QDialog and modal windows

Example from `pyside_renderer.py`:
```python
def set_attribute(self, el, attr, value):
    """Set Qt widget property"""
    # Block signals during update to prevent loops
    el.blockSignals(True)
    try:
        if hasattr(el, f"set_{attr}"):
            getattr(el, f"set_{attr}")(value)
        else:
            el.setProperty(attr, value)
    finally:
        el.blockSignals(False)
```

### 4. Reactivity Implementation

**Library**: [observ](https://github.com/fork-tongue/observ)

Collagraph uses the `observ` library for reactivity, which provides:

#### Core Primitives

**reactive()**: Makes objects reactive
```python
self._state = reactive({})
self._state["count"] = 0  # Tracked
self._state["count"] += 1  # Triggers watchers
```

**readonly()**: Creates immutable reactive objects
```python
self._props = readonly(props or {})
# self._props["key"] = "value"  # Raises ReadonlyError
```

**computed()**: Computed values that update automatically
```python
from observ import computed

@computed
def full_name(self):
    return f"{self.state['first']} {self.state['last']}"
```

**watch()** and **watch_effect()**: React to state changes
```python
from observ import watch_effect

def setup_watcher(self):
    watch_effect(lambda: print(self.state["count"]))
```

#### Scheduler Integration

The scheduler manages when reactive updates are flushed:

```python
from observ import scheduler

# Synchronous mode (for testing)
scheduler.register_request_flush(scheduler.flush)

# Async mode (default)
scheduler.register_asyncio()
```

Event loops:
- **DEFAULT** (EventLoopType.DEFAULT): Uses asyncio
- **SYNC** (EventLoopType.SYNC): Synchronous updates for testing

### 5. SFC Compilation Pipeline

**Location**: `collagraph/sfc/`

Single-File Components (`.cgx` files) are compiled to Python at import time.

#### Pipeline Stages

1. **Parsing** (`parser.py`)
   - Parse HTML-like template syntax
   - Extract `<template>`, `<script>`, `<style>` sections
   - Build element tree

2. **Script Processing** (`compiler.py`)
   - Parse `<script>` tag with Python's AST module
   - Extract component class definition
   - Collect imported names

3. **Template Compilation** (`compiler.py`)
   - Convert template elements to Fragment creation code
   - Process directives (v-if, v-for, v-bind, v-on)
   - Generate `render()` method AST

4. **AST Injection**
   - Inject generated `render()` method into component class
   - Compile final AST to bytecode
   - Execute in namespace

5. **Module Import** (`importer.py`)
   - Hook into Python's import system
   - Intercept `.cgx` file imports
   - Run compilation pipeline
   - Return compiled module

#### Example Transformation

**Input** (`counter.cgx`):
```html
<widget>
  <label :text="f'Count: {count}'" />
  <button text="Bump" @clicked="bump" />
</widget>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def bump(self):
        self.state["count"] += 1
</script>
```

**Generated `render()` method** (conceptual):
```python
def render(self, renderer):
    _f = self._renderer.h

    widget = _f("widget")

    label = _f("label")
    # Bind reactive text attribute
    label.bind("text", lambda: f'Count: {self._lookup("count", globals())}')
    widget.register_child(label)

    button = _f("button")
    button.set_attribute("text", "Bump")
    button.on("clicked", lambda: self._lookup("bump", globals())())
    widget.register_child(button)

    return widget
```

#### Directive Processing

**v-bind / :**
```python
# <div :title="message">
div.bind("title", lambda: self._lookup("message", globals()))
```

**v-on / @**
```python
# <button @clicked="handler">
button.on("clicked", lambda: self._lookup("handler", globals())())
```

**v-if**
```python
# <div v-if="show">
fragment.set_condition(lambda: self._lookup("show", globals()))
```

**v-for**
```python
# <div v-for="item in items">
ForFragment(
    items_fn=lambda: self._lookup("items", globals()),
    item_name="item",
    template_fn=lambda item: create_div(item)
)
```

### 6. Collagraph Orchestrator

**Location**: `collagraph/collagraph.py`

The `Collagraph` class ties everything together.

```python
class Collagraph:
    def __init__(self, renderer: Renderer, *, event_loop_type: EventLoopType | None = None):
        self.renderer = renderer
        self.event_loop_type = event_loop_type or renderer.preferred_event_loop_type()

        # Setup scheduler based on event loop type
        if self.event_loop_type is EventLoopType.DEFAULT:
            scheduler.register_asyncio()
            renderer.register_asyncio()
        else:
            scheduler.register_request_flush(scheduler.flush)

    def render(self, component_class, target, state=None):
        """Render a component into a target element"""
        # Create root component
        component = component_class(state or {})

        # Generate fragment tree
        self.fragment = component.render(renderer=self.renderer)
        self.fragment.component = component

        # Mount to target
        self.fragment.mount(target)
```

## Data Flow

### Initialization Flow

1. User creates `Collagraph` instance with a renderer
2. User calls `gui.render(ComponentClass, target, props)`
3. Collagraph instantiates the component with props
4. Component's `__init__()` runs, calls `init()` hook
5. Component's `render()` method is called, returns Fragment tree
6. Fragment tree is mounted to target
7. DOM elements are created and inserted
8. `mounted()` lifecycle hooks are called bottom-up

### Update Flow

1. User or event handler updates `component.state["key"]`
2. Observ tracks the mutation
3. Watchers that depend on that key are queued
4. Scheduler flushes updates (async or sync)
5. Watchers re-run, updating attributes
6. Renderer applies changes to DOM
7. `updated()` lifecycle hooks are called

### Unmount Flow

1. Fragment's `unmount()` is called
2. `before_unmount()` hooks are called (no guaranteed order)
3. Watchers and event listeners are cleaned up
4. Child fragments are unmounted recursively
5. DOM elements are removed
6. References are cleared for garbage collection

## Module Structure

```
collagraph/
├── __init__.py           # Public API exports
├── __main__.py           # CLI entry point
├── collagraph.py         # Main orchestrator
├── component.py          # Component base class
├── constants.py          # Enums and constants
├── fragment.py           # Fragment system (largest file ~900 lines)
├── weak.py               # Weak reference utilities
├── sfc/                  # Single-File Component support
│   ├── __init__.py       # SFC public API
│   ├── compiler.py       # Template → AST compilation
│   ├── importer.py       # Import hook for .cgx files
│   └── parser.py         # HTML-like template parser
├── renderers/            # Renderer implementations
│   ├── __init__.py       # Renderer base class
│   ├── dict_renderer.py  # Testing renderer
│   ├── pyside_renderer.py # Qt renderer
│   ├── pygfx_renderer.py  # 3D graphics renderer
│   └── pyside/           # PySide-specific helpers
│       ├── __init__.py
│       ├── objects.py    # Qt object registry
│       └── layouts/      # Layout-specific code
└── __pyinstaller/        # PyInstaller integration
```

## Key Design Patterns

### 1. Abstract Factory (Renderer)

Renderers implement a common interface, allowing different backends to be swapped:

```python
gui = cg.Collagraph(cg.PySideRenderer())  # Qt
# or
gui = cg.Collagraph(cg.PygfxRenderer())   # 3D graphics
```

### 2. Composite (Fragment Tree)

Fragments form a tree structure where each node can have children:

```python
class Fragment:
    def __init__(self, parent=None):
        self.children = []
        self._parent = ref(parent) if parent else None

    def register_child(self, child):
        self.children.append(child)
```

### 3. Observer (Reactivity)

Watchers observe reactive state and update DOM automatically:

```python
# When state changes
self.state["count"] += 1

# Watcher automatically runs
watch_effect(lambda: renderer.set_attribute(el, "text", f"Count: {self.state['count']}"))
```

### 4. Template Method (Lifecycle Hooks)

Component lifecycle is defined with hooks that subclasses can override:

```python
class Component:
    def mounted(self):
        pass  # Override in subclass

    def updated(self):
        pass  # Override in subclass
```

### 5. Weak References

Prevent circular references and memory leaks:

```python
# Parent-child relationships use weak refs
self._parent = ref(parent) if parent else None

@property
def parent(self):
    return self._parent() if self._parent else None
```

## Performance Considerations

### 1. Fragment Reuse

The ForFragment with keying reuses fragments when possible:

```html
<!-- With key -->
<div v-for="item in items" :key="item.id">
```

### 2. Lazy Evaluation

Bindings use lambda functions for lazy evaluation:

```python
label.bind("text", lambda: f"Count: {self.state['count']}")
# Only evaluated when count changes
```

### 3. Batched Updates

The observ scheduler batches reactive updates:

```python
self.state["a"] = 1  # Queued
self.state["b"] = 2  # Queued
# Both updates flushed together
```

### 4. Conditional Rendering

v-if unmounts fragments when false, freeing resources:

```html
<expensive-component v-if="show" />
<!-- Completely unmounted when show=false -->
```

## Extension Points

### Creating Custom Renderers

Implement the `Renderer` interface:

```python
class MyRenderer(cg.Renderer):
    def create_element(self, type: str):
        return MyElement(type)

    # ... implement other required methods
```

### Custom Directives

Currently not directly supported, but can be achieved by:
1. Extending the SFC compiler
2. Adding custom fragment types
3. Using render functions directly

### Custom Components

Extend the `Component` class:

```python
class MyComponent(cg.Component):
    def init(self):
        # Setup
        pass

    def render(self, renderer):
        # Return fragment tree
        return renderer.h("div")
```

## Testing Architecture

See [Testing Guidelines](testing.md) for details on:
- Using `DictRenderer` for tests
- Test fixtures (`parse_source`, `process_events`)
- Testing components, directives, and renderers
- Coverage requirements

## Further Reading

- [Component API](../api-reference/component.md)
- [Fragment System](../api-reference/fragment.md)
- [Renderer Interface](../api-reference/renderer.md)
- [Reactivity (observ docs)](https://github.com/fork-tongue/observ)
- [Single-File Components](../core-concepts/single-file-components.md)

## See Also

- [Fragment System](../api-reference/fragment.md)
- [Renderer Interface](../api-reference/renderer.md)
