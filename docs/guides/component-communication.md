# Component Communication

This guide covers all the ways components can communicate with each other in Collagraph applications, from simple parent-child communication to complex cross-component messaging.

## Overview

Collagraph provides several patterns for component communication:

1. **Props** - Parent to child data flow
2. **Events** - Child to parent messaging
3. **Provide/Inject** - Ancestor to descendant sharing
4. **Global State** - Application-wide reactive state
5. **Template Refs** - Direct component access

Each pattern serves different use cases and understanding when to use each is key to building maintainable applications.

## Parent to Child Communication (Props)

### Basic Props

The most straightforward communication pattern is passing data from parent to child via props:

**Parent Component:**
```html
<widget>
  <UserCard
    :name="current_user['name']"
    :email="current_user['email']"
    :role="current_user['role']"
    :is-active="current_user['is_active']"
  />
</widget>

<script>
import collagraph as cg
from user_card import UserCard

class UserProfile(cg.Component):
    def init(self):
        self.state["current_user"] = {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "role": "Developer",
            "is_active": True
        }
</script>
```

**Child Component (user_card.cgx):**
```html
<widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
  <label :text="name" :style-sheet="'font-size: 14pt; font-weight: bold;'" />
  <label :text="email" />
  <label :text="f'Role: {role}'" />
  <label
    :text="'Active' if is_active else 'Inactive'"
    :style-sheet="'color: green;' if is_active else 'color: red;'"
  />
</widget>

<script>
import collagraph as cg

class UserCard(cg.Component):
    def init(self):
        # Access props with defaults
        self.state["name"] = self.props.get("name", "Unknown")
        self.state["email"] = self.props.get("email", "")
        self.state["role"] = self.props.get("role", "User")
        self.state["is_active"] = self.props.get("is_active", False)
</script>
```

### Reactive Props

Props are reactive - when parent state changes, child components automatically re-render:

```python
class Parent(cg.Component):
    def init(self):
        self.state["counter"] = 0

    def increment(self):
        # Changing state automatically updates child's prop
        self.state["counter"] += 1
```

```html
<!-- Child receives updated value automatically -->
<CounterDisplay :value="counter" />
<button text="Increment" @clicked="increment" />
```

### Passing Complex Data

Props can be any Python type - dictionaries, lists, objects, functions:

```html
<!-- Pass lists -->
<TodoList :items="todos" />

<!-- Pass dictionaries -->
<UserProfile :user="user_data" />

<!-- Pass functions as callbacks -->
<DataTable :row-renderer="format_row" :on-row-click="handle_row_click" />

<!-- Pass multiple props at once with v-bind -->
<UserCard v-bind="user_data" />
```

### Configuration Props

Use props to make components reusable:

```python
class DataTable(cg.Component):
    """
    Configurable data table.

    Props:
        columns (list): Column definitions
        data (list): Row data
        sortable (bool): Enable sorting
        page-size (int): Rows per page
        on-sort (callable): Sort callback
    """

    def init(self):
        self.state["columns"] = self.props.get("columns", [])
        self.state["data"] = self.props.get("data", [])
        self.state["sortable"] = self.props.get("sortable", True)
        self.state["page_size"] = self.props.get("page_size", 25)
        self.on_sort = self.props.get("on_sort")
```

## Child to Parent Communication (Events)

### Emitting Events

Children communicate with parents by emitting events:

**Child Component:**
```python
class TodoItem(cg.Component):
    def handle_complete(self):
        """Emit completion event to parent"""
        todo_id = self.props.get("id")
        self.emit("completed", todo_id)

    def handle_delete(self):
        """Emit deletion event to parent"""
        todo_id = self.props.get("id")
        self.emit("deleted", todo_id)

    def handle_edit(self, new_text):
        """Emit edit event with new text"""
        todo_id = self.props.get("id")
        self.emit("edited", {"id": todo_id, "text": new_text})
```

**Child Template:**
```html
<widget :layout="{'type': 'box', 'direction': 'left-to-right'}">
  <checkbox
    :checked="completed"
    @toggled="lambda: handle_complete()"
  />
  <label :text="text" />
  <button text="Edit" @clicked="lambda: handle_edit('New text')" />
  <button text="Delete" @clicked="handle_delete" />
</widget>
```

**Parent Component:**
```html
<widget>
  <TodoItem
    v-for="todo in todos"
    :key="todo['id']"
    v-bind="todo"
    @completed="handle_todo_completed"
    @deleted="handle_todo_deleted"
    @edited="handle_todo_edited"
  />
</widget>

<script>
import collagraph as cg
from todo_item import TodoItem

class TodoList(cg.Component):
    def init(self):
        self.state["todos"] = []

    def handle_todo_completed(self, todo_id):
        """Handle todo completion"""
        for todo in self.state["todos"]:
            if todo["id"] == todo_id:
                todo["completed"] = True
                break

    def handle_todo_deleted(self, todo_id):
        """Handle todo deletion"""
        self.state["todos"] = [
            t for t in self.state["todos"]
            if t["id"] != todo_id
        ]

    def handle_todo_edited(self, data):
        """Handle todo edit"""
        for todo in self.state["todos"]:
            if todo["id"] == data["id"]:
                todo["text"] = data["text"]
                break
</script>
```

### Event Payload Patterns

**Single Value:**
```python
self.emit("value-changed", new_value)
```

**Multiple Values:**
```python
self.emit("updated", item_id, new_data)
```

**Dictionary Payload:**
```python
self.emit("form-submitted", {
    "username": username,
    "email": email,
    "preferences": preferences
})
```

### Callback Props vs Events

Two approaches for child-to-parent communication:

**Using Events (Recommended):**
```html
<!-- Parent -->
<FileUploader @upload-complete="handle_upload" />

<!-- Child -->
<script>
def upload_file(self):
    # ... upload logic ...
    self.emit("upload-complete", file_data)
</script>
```

**Using Callback Props:**
```html
<!-- Parent -->
<FileUploader :on-upload="handle_upload" />

<!-- Child -->
<script>
def upload_file(self):
    # ... upload logic ...
    callback = self.props.get("on_upload")
    if callback:
        callback(file_data)
</script>
```

Use events for better separation and multiple listeners. Use callbacks when you need return values.

## Sibling Communication

### Via Parent State

The most common pattern for sibling communication is through shared parent state:

```html
<widget>
  <!-- Sibling 1: Filters -->
  <FilterPanel
    :filters="filters"
    @filter-changed="handle_filter_change"
  />

  <!-- Sibling 2: Data display -->
  <DataGrid
    :data="filtered_data"
    :filters="filters"
  />
</widget>

<script>
import collagraph as cg
from filter_panel import FilterPanel
from data_grid import DataGrid

class Dashboard(cg.Component):
    def init(self):
        self.state["raw_data"] = []
        self.state["filters"] = {
            "category": "all",
            "status": "active"
        }

    @property
    def filtered_data(self):
        """Filter data based on current filters"""
        data = self.state["raw_data"]

        if self.state["filters"]["category"] != "all":
            data = [d for d in data if d["category"] == self.state["filters"]["category"]]

        if self.state["filters"]["status"]:
            data = [d for d in data if d["status"] == self.state["filters"]["status"]]

        return data

    def handle_filter_change(self, filter_data):
        """Update filters when child emits change"""
        self.state["filters"].update(filter_data)
</script>
```

### Via Custom Event Coordinator

For complex sibling communication, create a coordinator:

```python
class EventCoordinator:
    """Coordinates events between components"""

    def __init__(self):
        self.listeners = {}

    def on(self, event_name, callback):
        """Register event listener"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def off(self, event_name, callback):
        """Remove event listener"""
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)

    def emit(self, event_name, *args, **kwargs):
        """Emit event to all listeners"""
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(*args, **kwargs)


class App(cg.Component):
    def init(self):
        # Create shared coordinator
        self.coordinator = EventCoordinator()

        # Provide to all descendants
        self.provide("coordinator", self.coordinator)
```

Children can use it:

```python
class ComponentA(cg.Component):
    def init(self):
        self.coordinator = self.inject("coordinator")

    def mounted(self):
        # Listen for events from other components
        self.coordinator.on("data-updated", self.handle_data_update)

    def handle_data_update(self, data):
        self.state["data"] = data

    def before_unmount(self):
        # Clean up
        self.coordinator.off("data-updated", self.handle_data_update)


class ComponentB(cg.Component):
    def init(self):
        self.coordinator = self.inject("coordinator")

    def update_data(self, new_data):
        # Notify other components
        self.coordinator.emit("data-updated", new_data)
```

## Provide/Inject Pattern

### Basic Provide/Inject

Share data with deeply nested descendants without prop drilling:

**Ancestor Component:**
```python
class App(cg.Component):
    def init(self):
        self.state["theme"] = "dark"
        self.state["user"] = {
            "name": "Alice",
            "role": "admin"
        }

        # Provide values to all descendants
        self.provide("theme", self.state["theme"])
        self.provide("user", self.state["user"])
        self.provide("api_client", ApiClient())
```

**Descendant Component (any depth):**
```python
class ThemeAwareWidget(cg.Component):
    def init(self):
        # Inject provided values
        self.state["theme"] = self.inject("theme", default="light")
        self.state["user"] = self.inject("user", default={})

    @property
    def background_color(self):
        return "#2c2c2c" if self.state["theme"] == "dark" else "#ffffff"
```

### Providing Reactive State

When you provide reactive state, descendants automatically get updates:

```python
class ThemeProvider(cg.Component):
    def init(self):
        self.state["theme"] = "light"

        # Provide the reactive state itself
        self.provide("theme_state", self.state)

    def toggle_theme(self):
        self.state["theme"] = "dark" if self.state["theme"] == "light" else "light"


class ThemedComponent(cg.Component):
    def init(self):
        # Inject the reactive state
        theme_state = self.inject("theme_state")

        # Access it reactively
        self.state["current_theme"] = theme_state.get("theme", "light")
```

### Providing Services

Provide services and utilities to descendants:

```python
class App(cg.Component):
    def init(self):
        # Create services
        self.api = ApiClient(base_url="https://api.example.com")
        self.logger = Logger()
        self.notifier = NotificationService()

        # Provide to all descendants
        self.provide("api", self.api)
        self.provide("logger", self.logger)
        self.provide("notifier", self.notifier)


class DataComponent(cg.Component):
    def init(self):
        # Inject services
        self.api = self.inject("api")
        self.logger = self.inject("logger")

        self.state["data"] = []

    def fetch_data(self):
        try:
            self.logger.info("Fetching data...")
            data = self.api.get("/data")
            self.state["data"] = data
        except Exception as e:
            self.logger.error(f"Failed to fetch data: {e}")
```

## Global State

### Using Reactive Global State

Create truly global state shared across the entire application:

```python
from observ import reactive
import collagraph as cg

# Create global state (outside any component)
global_state = reactive({
    "user": None,
    "is_authenticated": False,
    "settings": {
        "theme": "light",
        "language": "en"
    },
    "notifications": []
})


class App(cg.Component):
    def init(self):
        # Provide global state to all components
        self.provide("global_state", global_state)


# Any component can access it
class UserMenu(cg.Component):
    def init(self):
        self.global_state = self.inject("global_state")

    @property
    def username(self):
        user = self.global_state.get("user")
        return user["name"] if user else "Guest"

    def logout(self):
        self.global_state["user"] = None
        self.global_state["is_authenticated"] = False
```

### State Management Module

Create a dedicated module for global state:

**state.py:**
```python
from observ import reactive

# Application state
app_state = reactive({
    "user": None,
    "session": None,
    "cart": {
        "items": [],
        "total": 0
    }
})

# Actions to modify state
def login(user_data):
    """Login user"""
    app_state["user"] = user_data
    app_state["session"] = create_session(user_data)

def logout():
    """Logout user"""
    app_state["user"] = None
    app_state["session"] = None

def add_to_cart(item):
    """Add item to cart"""
    app_state["cart"]["items"].append(item)
    app_state["cart"]["total"] += item["price"]

def clear_cart():
    """Clear shopping cart"""
    app_state["cart"]["items"] = []
    app_state["cart"]["total"] = 0
```

**Using in components:**
```python
import collagraph as cg
from state import app_state, login, logout, add_to_cart

class ShoppingCart(cg.Component):
    def init(self):
        # Use global state directly
        self.app_state = app_state

    @property
    def cart_items(self):
        return self.app_state["cart"]["items"]

    @property
    def cart_total(self):
        return self.app_state["cart"]["total"]

    def add_item(self, item):
        # Use action to modify state
        add_to_cart(item)
```

## Template Refs for Direct Access

### Accessing Child Components

Use template refs to access child component instances directly:

```html
<widget>
  <DataGrid ref="dataGrid" :data="data" />
  <button text="Refresh" @clicked="refresh_grid" />
</widget>

<script>
import collagraph as cg
from data_grid import DataGrid

class Dashboard(cg.Component):
    def init(self):
        self.state["data"] = []

    def refresh_grid(self):
        """Call method on child component directly"""
        if "dataGrid" in self.refs:
            grid = self.refs["dataGrid"]
            # Access child component's methods
            grid.refresh()
            grid.scroll_to_top()
</script>
```

### Parent-Child Method Calls

Sometimes you need to call child methods from parent:

**Child Component:**
```python
class Modal(cg.Component):
    def init(self):
        self.state["is_open"] = False

    def open(self):
        """Open modal - can be called by parent"""
        self.state["is_open"] = True

    def close(self):
        """Close modal - can be called by parent"""
        self.state["is_open"] = False
```

**Parent Component:**
```html
<widget>
  <button text="Open Modal" @clicked="open_modal" />
  <Modal ref="modal" />
</widget>

<script>
import collagraph as cg
from modal import Modal

class Page(cg.Component):
    def open_modal(self):
        if "modal" in self.refs:
            self.refs["modal"].open()
</script>
```

## Communication Patterns Summary

### Choose the Right Pattern

| Pattern | Use When | Example |
|---------|----------|---------|
| **Props** | Parent → Child data | Passing user data to profile component |
| **Events** | Child → Parent messaging | Form submission, button clicks |
| **Provide/Inject** | Ancestor → Descendant (deep) | Theme, authentication, services |
| **Global State** | App-wide shared state | User session, shopping cart |
| **Template Refs** | Direct component access | Calling modal.open(), grid.refresh() |
| **Parent State** | Sibling communication | Filter panel updating data grid |

## Complete Example: Communication Hub

Here's a comprehensive example showing multiple communication patterns:

```html
<!-- App.cgx -->
<widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
  <!-- Header communicates user state down -->
  <Header :user="user" @logout="handle_logout" />

  <!-- Sidebar and content are siblings, communicate via parent state -->
  <widget :layout="{'type': 'box', 'direction': 'left-to-right'}">
    <Sidebar
      :current-page="current_page"
      @page-changed="handle_page_change"
    />

    <Content
      :page="current_page"
      :user="user"
      @action="handle_action"
    />
  </widget>

  <!-- Modal accessed via ref -->
  <ConfirmDialog
    ref="confirmDialog"
    @confirmed="handle_confirm"
    @cancelled="handle_cancel"
  />
</widget>

<script>
import collagraph as cg
from observ import reactive
from header import Header
from sidebar import Sidebar
from content import Content
from confirm_dialog import ConfirmDialog

# Global state
app_state = reactive({
    "theme": "light",
    "notifications": []
})

class App(cg.Component):
    def init(self):
        # Component state
        self.state["user"] = {
            "name": "Alice",
            "role": "admin"
        }
        self.state["current_page"] = "dashboard"

        # Provide global state and services
        self.provide("app_state", app_state)
        self.provide("notifier", self.notify)

    def handle_logout(self):
        """Handle logout event from header"""
        self.state["user"] = None
        self.state["current_page"] = "login"

    def handle_page_change(self, page):
        """Handle page change from sidebar"""
        self.state["current_page"] = page

    def handle_action(self, action_data):
        """Handle action from content"""
        if action_data["type"] == "delete":
            # Show confirmation dialog via ref
            if "confirmDialog" in self.refs:
                self.refs["confirmDialog"].show(
                    message=f"Delete {action_data['item']}?",
                    data=action_data
                )

    def handle_confirm(self, data):
        """Handle confirmation"""
        # Perform the action
        print(f"Confirmed: {data}")

    def handle_cancel(self):
        """Handle cancellation"""
        print("Action cancelled")

    def notify(self, message, type="info"):
        """Notification service provided to descendants"""
        app_state["notifications"].append({
            "message": message,
            "type": type,
            "timestamp": time.time()
        })
</script>
```

## Best Practices

1. **Use props for configuration, events for actions** - Props configure how a component behaves, events notify when things happen
2. **Keep communication patterns simple** - Don't over-engineer; start with props/events
3. **Avoid prop drilling** - Use provide/inject for deeply nested data
4. **Emit events after state changes** - Update state first, then notify parent
5. **Document communication contracts** - Clearly document what props, events, and provides a component uses
6. **Use template refs sparingly** - Prefer events over direct method calls
7. **Centralize global state** - Keep app-wide state in one place
8. **Name events descriptively** - Use action-oriented names (submitted, deleted, updated)

## See Also

- [Props](../core-concepts/props.md)
- [Events](../core-concepts/events.md)
- [Components](../core-concepts/components.md)
- [State Management](../core-concepts/state-management.md)
- [Template Refs](../core-concepts/template-refs.md)
