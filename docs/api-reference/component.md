# Component API

## Class: `cg.Component`

Abstract base class for all Collagraph components. Components encapsulate reusable UI logic and state management.

## Constructor

```python
Component(props=None, parent=None)
```

### Parameters

- `props` (dict, optional): Properties passed from the parent component. Becomes a read-only reactive object.
- `parent` (Component, optional): Reference to the parent component in the component tree.

**Note:** You typically don't call the constructor directly. Collagraph creates component instances when rendering the component tree.

## Lifecycle Methods

### `init(self)`

Called automatically at the end of the component's `__init__` method. Use this to set up initial state and perform setup operations.

```python
def init(self):
    self.state["count"] = 0
    self.state["items"] = []
```

**When Called:** During component instantiation, before the first render.

**Best Practices:**
- Initialize state variables
- Set up initial data
- Don't perform side effects that depend on the DOM

---

### `render(self, renderer: Renderer) -> ComponentFragment`

**Abstract method** that must be implemented by all components. Returns the component's UI definition as a fragment.

**Note:** When using `.cgx` template files, the `render` method is automatically generated from the template, so you don't need to implement it manually.

```python
# When writing components in Python (not .cgx files)
def render(self, renderer):
    # Manual rendering logic
    # Most users use .cgx templates instead
    pass
```

**Returns:** A `ComponentFragment` representing the rendered UI tree.

---

### `mounted(self)`

Called after the component has been mounted to the DOM.

**When Called:**
- After all child components have been mounted
- After the component's DOM tree has been created and inserted into the parent container
- After refs are populated

```python
def mounted(self):
    # Access refs, DOM elements, perform side effects
    print("Component is now in the DOM")
    if self.element:
        print(f"Root element: {self.element}")
```

**Use Cases:**
- Accessing DOM elements via refs
- Starting timers or animations
- Fetching initial data
- Setting up third-party integrations

---

### `updated(self)`

Called after the component has updated its DOM tree due to reactive state changes.

**When Called:**
- After reactive state or props change
- After child components have been updated
- Called on every reactive update

```python
def updated(self):
    print(f"State changed: {self.state['count']}")
```

**Note:** This hook is called frequently. Avoid heavy operations here.

---

### `before_unmount(self)`

Called right before a component instance is unmounted from the DOM.

```python
def before_unmount(self):
    # Clean up resources
    if hasattr(self, 'timer'):
        self.timer.stop()
```

**Use Cases:**
- Cleaning up timers or intervals
- Removing event listeners
- Closing connections
- Releasing resources

**Important:**
- The order of `before_unmount` calls is not guaranteed
- A parent's `before_unmount` might be called before or after its children's

## Component Communication Methods

### `emit(self, event_name: str, *args, **kwargs)`

Emit a custom event that parent components can listen to. All registered event handlers for the given event will be called with the provided arguments.

**Parameters:**
- `event_name` (str): Name of the event to emit
- `*args`: Positional arguments to pass to event handlers
- `**kwargs`: Keyword arguments to pass to event handlers

```python
class ChildComponent(cg.Component):
    def handle_click(self):
        # Emit event with data
        self.emit("item-selected", {"id": 123, "name": "Item"})

    def handle_change(self):
        # Emit event with multiple arguments
        self.emit("change", "new_value", index=5)
```

**Parent component listening to events:**

```xml
<template>
  <ChildComponent @item-selected="on_item_selected" />
</template>

<script>
def on_item_selected(self, data):
    print(f"Item selected: {data}")
</script>
```

---

### `add_event_handler(self, event: str, handler: Callable)`

Programmatically add an event handler for a custom event. This is typically done by the framework when using `@event-name` syntax in templates.

**Parameters:**
- `event` (str): Event name
- `handler` (Callable): Function to call when event is emitted

```python
def my_handler(data):
    print(data)

component.add_event_handler("custom-event", my_handler)
```

---

### `remove_event_handler(self, event: str, handler: Callable)`

Remove a previously registered event handler.

**Parameters:**
- `event` (str): Event name
- `handler` (Callable): The handler function to remove

```python
component.remove_event_handler("custom-event", my_handler)
```

## Dependency Injection

### `provide(self, key: str, value: Any)`

Provide a value that can be injected by descendant components at any depth in the component tree.

**Parameters:**
- `key` (str): Unique key for the provided value
- `value` (Any): Value to provide

```python
class AppComponent(cg.Component):
    def init(self):
        # Provide configuration to all descendants
        self.provide("theme", {"mode": "dark", "primary": "#007bff"})
        self.provide("api_client", APIClient())
```

**Use Cases:**
- Sharing configuration across many components
- Dependency injection for services
- Avoiding prop drilling through many component levels

---

### `inject(self, key: str, default=None) -> Any`

Inject a value that was provided by an ancestor component.

**Parameters:**
- `key` (str): Key of the provided value
- `default` (Any, optional): Default value if key is not found

**Returns:** The provided value, or the default if not found.

```python
class DescendantComponent(cg.Component):
    def init(self):
        # Inject values from ancestors
        theme = self.inject("theme", {"mode": "light"})
        self.state["mode"] = theme["mode"]

        api_client = self.inject("api_client")
        if api_client:
            self.state["data"] = api_client.fetch_data()
```

**How It Works:**
- Walks up the component tree from the current component
- Returns the first matching value found in an ancestor
- Returns the default if no ancestor provides the key

## Properties

### `self.state: dict`

Reactive state dictionary. Any changes to this dictionary automatically trigger component re-renders.

**Type:** Reactive dictionary (from `observ` library)

```python
def init(self):
    # Initialize state
    self.state["count"] = 0
    self.state["items"] = []
    self.state["user"] = {"name": "Alice", "age": 30}

def increment(self):
    # Modifying state triggers re-render
    self.state["count"] += 1

def add_item(self, item):
    # Array modifications are reactive
    self.state["items"].append(item)

def update_user(self):
    # Nested property updates are reactive
    self.state["user"]["age"] += 1
```

**Important Notes:**
- State is reactive - changes automatically update the UI
- State is local to the component
- Deep mutations (nested objects/arrays) are tracked
- Don't reassign `self.state` itself (raises RuntimeError)

**Read-Only:** The `state` property itself cannot be overwritten:
```python
# This will raise RuntimeError
self.state = {}  # ❌ Not allowed
```

---

### `self.props: dict`

Properties passed from the parent component. Props are **read-only** and reactive.

**Type:** Read-only reactive dictionary

```python
class ChildComponent(cg.Component):
    def init(self):
        # Access props
        title = self.props["title"]
        count = self.props.get("count", 0)

    def render(self, renderer):
        # Props can be used in rendering
        # When using .cgx templates, access props directly
        pass
```

**In .cgx templates:**
```xml
<template>
  <label :text="title" />  <!-- Accesses self.props["title"] -->
  <label :text="f'Count: {count}'" />
</template>
```

**Important Notes:**
- Props are passed from parent components
- Props are read-only (attempting to modify raises an error)
- When parent updates props, component automatically re-renders
- Don't reassign `self.props` itself (raises RuntimeError)

---

### `self.refs: dict`

Dictionary containing references to child elements and components marked with `ref` attribute.

**Type:** Reactive dictionary

```xml
<template>
  <button ref="myButton" text="Click me" />
  <ChildComponent ref="childComp" />
</template>

<script>
def mounted(self):
    # Access element refs after mounting
    button = self.refs["myButton"]
    print(f"Button element: {button}")

    # Access component refs
    child = self.refs["childComp"]
    print(f"Child component: {child}")
</script>
```

**Function Refs:**

You can also use function refs for more control:

```xml
<template>
  <button :ref="save_button_ref" text="Save" />
</template>

<script>
def save_button_ref(self, element):
    # Called when ref is set/unset
    if element:
        print(f"Button mounted: {element}")
        self.state["button"] = element
    else:
        print("Button unmounted")
        self.state["button"] = None
</script>
```

**Important Notes:**
- Refs are only populated after the component is mounted
- Access refs in `mounted()` or later lifecycle hooks
- For component refs, you get the component instance (not its DOM element)
- Don't reassign `self.refs` itself (raises RuntimeError)

---

### `self.element: Any`

The root DOM element of this component. Available after the component is mounted.

**Type:** Any (depends on renderer)

```python
def mounted(self):
    # Access the root element
    if self.element:
        print(f"Root element: {self.element}")
```

**Important Notes:**
- Only available after component is mounted
- Returns `None` before mounting
- For PySide renderer, this is a QWidget or similar Qt object
- Read-only property (raises RuntimeError if reassigned)

---

### `self.parent: Component | None`

Reference to the parent component in the component tree. Returns `None` for the root component.

**Type:** Component or None

```python
def some_method(self):
    if self.parent:
        print(f"Parent component: {self.parent}")
        # Can access parent's state, methods, etc.
    else:
        print("This is the root component")
```

**Important Notes:**
- Uses weak reference internally (won't prevent garbage collection)
- Returns `None` for root component
- Read-only property (raises RuntimeError if reassigned)
- Useful for component communication (though `emit` is preferred)

## See Also

- [Components Guide](../core-concepts/components.md)
- [Lifecycle Hooks](../core-concepts/lifecycle.md)
