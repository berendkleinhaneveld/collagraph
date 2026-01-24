# Component API

> **TODO**: Complete API reference for the Component class.

## Class: `cg.Component`

Base class for all Collagraph components.

## Methods

### `init(self)`
Called when the component is initialized. Use this to set up initial state.

```python
def init(self):
    self.state["count"] = 0
```

### `render(self) -> dict`
Returns the component's UI definition.

```python
def render(self):
    return {"type": "label", "text": "Hello"}
```

### `mounted(self)`
Called after the component is mounted to the DOM.

### `updated(self)`
Called after the component updates.

### `before_unmount(self)`
Called before the component is unmounted.

### `emit(self, event_name: str, *args, **kwargs)`
Emit a custom event to the parent component.

```python
self.emit("custom-event", {"data": "value"})
```

### `provide(self, key: str, value: Any)`
Provide a value to descendant components.

```python
self.provide("theme", "dark")
```

### `inject(self, key: str, default=None) -> Any`
Inject a value provided by an ancestor component.

```python
theme = self.inject("theme", "light")
```

## Properties

### `self.state: dict`
Reactive state dictionary. Changes trigger re-renders.

### `self.props: dict`
Props passed from the parent component (read-only).

### `self.refs: dict`
References to child elements and components.

## See Also

- [Components Guide](../core-concepts/components.md)
- [Lifecycle Hooks](../core-concepts/lifecycle.md)
