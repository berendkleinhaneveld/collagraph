# Your First Component

Learn how to create reusable components in Collagraph.

## Component Basics

A Collagraph component is a Python class that extends `cg.Component`:

```python
import collagraph as cg

class MyComponent(cg.Component):
    def render(self):
        return {"type": "label", "text": "Hello, World!"}
```

## Single-File Components (.cgx)

The recommended way to create components is using `.cgx` files:

```html
<label text="Hello, World!" />

<script>
import collagraph as cg

class MyComponent(cg.Component):
    pass
</script>
```

## Adding State

Components can have reactive state:

```html
<label :text="message" />

<script>
import collagraph as cg

class Greeting(cg.Component):
    def init(self):
        self.state["message"] = "Hello, World!"
</script>
```

## Accepting Props

Components can receive data from their parent:

```html
<label :text="f'Hello, {name}!'" />

<script>
import collagraph as cg

class Greeting(cg.Component):
    def init(self):
        self.name = self.props.get("name", "Guest")
</script>
```

Usage:

```html
<Greeting name="Alice" />
```

## Handling Events

Add interactivity with event handlers:

```html
<v-box>
  <label :text="f'Count: {count}'" />
  <button text="Click me" @clicked="handle_click" />
</v-box>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def handle_click(self):
        self.state["count"] += 1
</script>
```

## Lifecycle Hooks

Components have lifecycle hooks you can use:

```python
class MyComponent(cg.Component):
    def init(self):
        # Called when component is created
        self.state["data"] = []

    def mounted(self):
        # Called after component is added to the DOM
        print("Component mounted!")

    def updated(self):
        # Called after component updates
        print("Component updated!")

    def before_unmount(self):
        # Called before component is removed
        print("Cleaning up...")
```

## Composing Components

Build complex UIs by combining components:

```html
<window title="User Profile">
  <v-box>
    <UserHeader :user="user" />
    <UserDetails :user="user" />
    <UserActions @edit="handle_edit" />
  </v-box>
</window>

<script>
import collagraph as cg
from .user_header import UserHeader
from .user_details import UserDetails
from .user_actions import UserActions

class UserProfile(cg.Component):
    def init(self):
        self.state["user"] = {
            "name": "Alice",
            "email": "alice@example.com"
        }

    def handle_edit(self):
        print("Edit user")
</script>
```

## Next Steps

- Learn about [Props](../core-concepts/props.md)
- Understand [State Management](../core-concepts/state-management.md)
- Explore [Lifecycle Hooks](../core-concepts/lifecycle.md)
