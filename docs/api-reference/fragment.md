# Fragment System

## Overview

Fragments are Collagraph's internal representation of the UI tree. They form a virtual DOM-like structure that sits between the component tree and the actual rendered elements. This is an **advanced topic** for those implementing custom renderers, contributing to Collagraph, or understanding its architecture.

**Target Audience:**
- Collagraph contributors
- Advanced users debugging rendering issues
- Those implementing custom renderers
- Developers interested in Collagraph's internals

## What are Fragments?

A Fragment is a node in Collagraph's virtual UI tree. Each fragment represents:
- An element (button, label, etc.)
- A component instance
- A control flow construct (if/else, for loop)
- A virtual container (template, slot)

Fragments manage:
- Creation and destruction of native elements
- Reactive attribute bindings
- Event listeners
- Lifecycle coordination
- Parent-child relationships

## Fragment Lifecycle

Fragments go through three main lifecycle stages:

### 1. Creation (`create()`)

Creates the native element and sets up reactivity:

```python
fragment.create()
# - Creates native element via renderer
# - Applies static attributes
# - Attaches event listeners
# - Sets up watchers for dynamic attributes
```

### 2. Mounting (`mount(target, anchor=None)`)

Inserts the fragment into the DOM:

```python
fragment.mount(target, anchor=None)
# - Calls create() if not already created
# - Inserts element into parent via renderer
# - Mounts all child fragments
# - Registers refs with parent component
# - Marks fragment as mounted
```

### 3. Unmounting (`unmount(destroy=True)`)

Removes the fragment from the DOM:

```python
fragment.unmount(destroy=True)
# - Unregisters refs
# - Unmounts all children
# - Removes element from parent
# - Optionally destroys watchers and state (if destroy=True)
```

## Fragment Types

### `Fragment`

Base fragment class for standard DOM elements.

**Key Attributes:**
- `tag` (str): Element type name
- `element` (Any): Native element instance
- `target` (Any): Parent element to render into
- `parent` (Fragment): Parent fragment
- `children` (list[Fragment]): Child fragments
- `_attributes` (dict): Static attributes
- `_binds` (list): Dynamic attribute expressions
- `_events` (dict): Event handlers
- `_watchers` (dict): Active reactive watchers
- `_condition` (Callable): Conditional expression for v-if
- `_ref_name` (str): Template ref name
- `_mounted` (bool): Whether fragment is mounted

**Example:**
```python
# Fragment for: <button text="Click me" @clicked="handler" />
fragment = Fragment(renderer, tag="button")
fragment.set_attribute("text", "Click me")
fragment.set_event("clicked", handler)
fragment.mount(parent_element)
```

---

### `ComponentFragment`

Fragment that wraps a component instance.

**Additional Attributes:**
- `component` (Component): Component instance
- `fragment` (Fragment): Root fragment from component's render
- `props` (dict): Reactive props dictionary
- `slots` (dict): Named slot fragments
- `slot_contents` (list): Slot content from parent

**Lifecycle:**
1. `create()`: Instantiates component, calls `render()`, sets up props
2. `mount()`: Mounts component's root fragment, finds element, calls `component.mounted()`
3. `unmount()`: Calls `component.before_unmount()`, unmounts fragment

**Example:**
```python
# Fragment for: <MyComponent title="Hello" @event="handler" />
fragment = ComponentFragment(
    renderer,
    tag=MyComponent,
    props={"title": "Hello"}
)
fragment.set_event("event", handler)
fragment.mount(parent_element)
# Now fragment.component is the MyComponent instance
```

---

### `ControlFlowFragment`

Fragment for conditional rendering (v-if/v-else-if/v-else).

**How It Works:**
- Children are conditional branches
- Only one child is mounted at a time
- Watches conditions and switches active child

**Example:**
```python
# Fragment for: <div v-if="condition">...</div>
control_fragment = ControlFlowFragment(renderer)
if_fragment = Fragment(renderer, tag="div")
if_fragment.set_condition(lambda: state["condition"])
control_fragment.register_child(if_fragment)
control_fragment.mount(parent_element)
# Automatically mounts/unmounts based on condition
```

---

### `ListFragment`

Fragment for list rendering (v-for).

**Modes:**
- **Index-based**: Reuses fragments by index
- **Key-based**: Reuses fragments by key (more efficient for reordering)

**Key Attributes:**
- `create_fragment` (Callable): Factory for creating item fragments
- `expression` (Callable): Expression that returns the list
- `is_keyed` (bool): Whether to use key-based reconciliation
- `key_extractor` (Callable): Function to extract key from item

**Example:**
```python
# Fragment for: <div v-for="item in items" :key="item.id">...</div>
list_fragment = ListFragment(renderer)
list_fragment.set_expression(lambda: state["items"])
list_fragment.set_create_fragment(
    create_fragment=create_item_fragment,
    is_keyed=True,
    key_extractor=lambda item: item["id"]
)
list_fragment.mount(parent_element)
# Automatically creates/updates/removes item fragments
```

---

### `SlotFragment`

Fragment representing a slot in a component.

**How It Works:**
- Registered with parent ComponentFragment
- When mounted, renders slot content from parent
- Falls back to default content if no slot content provided

**Example:**
```python
# Fragment for: <slot name="header">Default Header</slot>
slot_fragment = SlotFragment(renderer, name="header")
# ... add default content as children ...
slot_fragment.mount(target)
# Renders parent's slot content or default content
```

---

### `DynamicFragment`

Fragment for dynamic component tags (`<component :is="expr" />`).

**How It Works:**
- Watches expression to determine current tag
- Creates ComponentFragment or Fragment based on tag type
- Switches fragments when expression changes

**Example:**
```python
# Fragment for: <component :is="currentComponent" />
dynamic_fragment = DynamicFragment(
    renderer,
    expression=lambda: state["currentComponent"]
)
dynamic_fragment.mount(parent_element)
# Automatically switches component when currentComponent changes
```

## Reactive Attributes

Fragments support both static and dynamic attributes:

### Static Attributes

Set once during creation:

```python
fragment.set_attribute("text", "Hello")
```

### Dynamic Attributes (Bindings)

Watched expressions that update automatically:

```python
fragment.set_bind("text", lambda: f"Count: {state['count']}")
# When state["count"] changes, attribute updates automatically
```

### Dynamic Attribute Dictionaries

Bind multiple attributes from a dictionary:

```python
fragment.set_bind_dict("attrs", lambda: state["attributes"])
# When keys in state["attributes"] change, attributes update
```

## Template Refs

Fragments support template refs for accessing elements/components:

### Static Refs

```python
fragment.set_attribute("ref", "myButton")
# After mounting, component.refs["myButton"] = element
```

### Dynamic Refs

```python
fragment.set_bind("ref", lambda: state["ref_name"])
# Ref updates when expression changes
```

### Function Refs

```python
def ref_callback(element):
    if element:
        print(f"Element mounted: {element}")
    else:
        print("Element unmounted")

fragment.set_attribute("ref", ref_callback)
```

## Fragment Tree Navigation

Fragments maintain parent-child relationships:

```python
# Access parent
parent = fragment.parent  # Weak reference

# Find parent component
component = fragment._component_parent()

# Find anchor (next sibling for insertion)
anchor = fragment.anchor()

# Get first DOM element
element = fragment.first()
```

## Implementation Details

### Weak References

Fragments use weak references to parents to prevent circular references and memory leaks:

```python
self._parent = ref(parent) if parent else None
```

### Watcher Management

Fragments create watchers for dynamic attributes:

```python
def _watch_bind(self, attr, expression):
    @weak(self)
    def update(self, new):
        self._set_attr(attr, new)

    self._watchers[f"bind:{attr}"] = watch(
        expression,
        update,
        immediate=True,
        deep=True,
    )
```

### Cleanup

When unmounting with `destroy=True`, fragments clean up:
- Stop all watchers
- Clear references
- Remove from parent
- Recursively unmount children

## Debugging Fragments

### Print Fragment Tree

```python
fragment.debug(indent=0)
# Prints:
# <widget>
#   <label>
#   <button>
```

### Inspect Fragment

```python
print(fragment)
# <Fragment(button-[140234567890])>

print(f"Tag: {fragment.tag}")
print(f"Mounted: {fragment._mounted}")
print(f"Element: {fragment.element}")
print(f"Children: {len(fragment.children)}")
print(f"Watchers: {list(fragment._watchers.keys())}")
```

## Common Patterns

### Creating a Fragment Programmatically

```python
from collagraph.fragment import Fragment

# Create fragment
fragment = Fragment(renderer, tag="button", parent=parent_fragment)
fragment.set_attribute("text", "Click me")
fragment.set_event("clicked", lambda: print("Clicked!"))

# Mount it
fragment.mount(target_element)
```

### Conditional Mounting

```python
# Check if already mounted before mounting
if not fragment._mounted:
    fragment.mount(target)

# Remount after unmount (destroy=False)
fragment.unmount(destroy=False)
# ... later ...
fragment.mount(target)  # Remounts same fragment
```

### Traversing Fragment Tree

```python
def find_fragments_by_tag(fragment, tag):
    """Recursively find all fragments with given tag"""
    results = []
    if fragment.tag == tag:
        results.append(fragment)
    for child in fragment.children:
        results.extend(find_fragments_by_tag(child, tag))
    return results
```

## Relationship to Virtual DOM

Fragments are similar to Virtual DOM nodes but with key differences:

**Similarities:**
- Intermediate representation between components and native elements
- Support diffing and updates
- Manage element lifecycle

**Differences:**
- Fragments are **stateful** (maintain watchers, refs, etc.)
- Fragments handle **reactivity** directly (via observ watchers)
- No explicit diffing algorithm - updates are reactive
- Fragments can be **remounted** (destroy=False)

## Performance Considerations

1. **Keyed Lists**: Use `key` in v-for for efficient list updates
2. **Watcher Cleanup**: Always unmount with `destroy=True` when done
3. **Deep Watching**: Be careful with deep watchers on large objects
4. **Conditional Rendering**: v-if unmounts/remounts, v-show just hides (when implemented)

## Advanced: Custom Fragment Types

You can create custom fragment types for special behavior:

```python
from collagraph.fragment import Fragment

class CustomFragment(Fragment):
    def create(self):
        # Custom creation logic
        super().create()
        # Additional setup

    def mount(self, target, anchor=None):
        # Custom mounting logic
        super().mount(target, anchor)
        # Additional setup

    def unmount(self, destroy=True):
        # Custom cleanup
        super().unmount(destroy)
        # Additional cleanup
```

## See Also

- [Renderer Interface](renderer.md)
- [Architecture Overview](../contributing/architecture.md)
