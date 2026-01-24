# Lifecycle Hooks

## Overview

Lifecycle hooks are special methods that are called at specific points in a component's lifecycle. They allow you to run code when a component is created, mounted, updated, or destroyed. Understanding lifecycle hooks is crucial for managing side effects, fetching data, and cleaning up resources.

## Component Lifecycle Phases

A Collagraph component goes through several phases:

1. **Creation**: Component instance is created
2. **Initialization**: `init()` is called, state is initialized
3. **Mounting**: Component is added to the DOM tree
4. **Mounted**: `mounted()` is called after mounting completes
5. **Updates**: Component re-renders when state or props change
6. **Updated**: `updated()` is called after each update
7. **Unmounting**: Component is being removed from DOM
8. **Before Unmount**: `before_unmount()` is called for cleanup

```
Creation → Initialization → Mounting → Mounted
                                          ↓
                                      ┌─────────┐
                                      │ Active  │
                                      │ Updates │
                                      └─────────┘
                                          ↓
                              Before Unmount → Unmounted
```

## Available Lifecycle Hooks

### `init()`

**When**: Called when the component instance is created, before mounting.

**Purpose**: Initialize component state, set up instance properties, and prepare data.

**Important**: This is called **after** the base `Component.__init__()`, so `self.props`, `self.state`, and other properties are available.

```python
class MyComponent(cg.Component):
    def init(self):
        """Initialize component state and instance variables"""
        # Initialize state
        self.state["count"] = self.props.get("initial_count", 0)
        self.state["items"] = []
        self.state["loading"] = False

        # Set up instance variables (not reactive)
        self.timer_id = None
        self.cache = {}
```

**Use cases:**
- Initialize state from props
- Set up non-reactive instance variables
- Prepare initial data
- Set up default values

**Do NOT:**
- Access DOM elements (component isn't mounted yet)
- Access template refs (not available yet)
- Make assumptions about child components (they may not exist yet)

### `mounted()`

**When**: Called after the component has been mounted to the DOM.

**Purpose**: Perform operations that require DOM access, set up subscriptions, fetch initial data.

**Order**: Child components' `mounted()` is called before parent's `mounted()`.

```python
class DataFetcher(cg.Component):
    def init(self):
        self.state["data"] = []
        self.state["loading"] = True

    def mounted(self):
        """Called after component is mounted to DOM"""
        # Access DOM elements via refs
        if "inputField" in self.refs:
            self.refs["inputField"].setFocus()

        # Fetch initial data
        self.fetch_data()

        # Set up subscriptions
        self.subscription = subscribe_to_updates(self.handle_update)

        # Start timers
        self.timer_id = start_timer(1000, self.update_time)

    def fetch_data(self):
        # Fetch data from API
        data = api.get_data()
        self.state["data"] = data
        self.state["loading"] = False
```

**Use cases:**
- Access and manipulate DOM elements
- Access template refs
- Fetch data from APIs
- Set up event listeners
- Start timers or animations
- Initialize third-party libraries that need DOM access

**Order of execution:**
```
GrandChild.mounted() → Child.mounted() → Parent.mounted()
```

### `updated()`

**When**: Called after the component has re-rendered due to state or prop changes.

**Purpose**: React to changes, perform side effects after updates.

**Order**: Child components' `updated()` is called before parent's `updated()`.

**Important**: `updated()` is called after **every** update, so be careful with side effects that might trigger infinite loops.

```python
class ScrollToBottom(cg.Component):
    def init(self):
        self.state["messages"] = []

    def updated(self):
        """Called after component updates"""
        # Scroll to bottom when new messages are added
        if "messageContainer" in self.refs:
            container = self.refs["messageContainer"]
            container.scrollToBottom()

    def add_message(self, message):
        self.state["messages"].append(message)
        # This will trigger updated() to be called
```

**Use cases:**
- React to state or prop changes
- Update third-party libraries
- Adjust scroll positions
- Trigger animations
- Log analytics events

**Caution: Avoid Infinite Loops**

Don't modify state in `updated()` without guards:

```python
# ❌ BAD: Infinite loop!
def updated(self):
    self.state["update_count"] += 1  # This triggers updated() again!

# ✅ GOOD: Use guards
def updated(self):
    # Only update if condition is met
    if self.state["needs_recalculation"]:
        self.state["needs_recalculation"] = False
        self.recalculate()
```

### `before_unmount()`

**When**: Called right before the component is unmounted and destroyed.

**Purpose**: Clean up side effects, subscriptions, timers, and external resources.

**Important**: There are no strict guarantees about the order in which components are unmounted. A parent's `before_unmount()` might be called before or after its children's.

```python
class MyComponent(cg.Component):
    def init(self):
        self.subscription = None
        self.timer_id = None

    def mounted(self):
        # Set up resources that need cleanup
        self.subscription = subscribe_to_events(self.handle_event)
        self.timer_id = start_timer(1000, self.tick)

    def before_unmount(self):
        """Clean up before component is destroyed"""
        # Cancel subscriptions
        if self.subscription:
            self.subscription.unsubscribe()

        # Cancel timers
        if self.timer_id:
            cancel_timer(self.timer_id)

        # Close connections
        if hasattr(self, 'connection'):
            self.connection.close()

        # Remove event listeners
        document.removeEventListener('click', self.handle_click)
```

**Use cases:**
- Cancel timers and intervals
- Unsubscribe from observables or event streams
- Close network connections
- Remove global event listeners
- Clean up third-party library instances
- Release allocated resources

## Lifecycle Hook Examples

### Data Fetching

```python
class UserProfile(cg.Component):
    def init(self):
        self.state["user"] = None
        self.state["loading"] = True
        self.state["error"] = None

    def mounted(self):
        """Fetch user data after component mounts"""
        self.fetch_user()

    def fetch_user(self):
        user_id = self.props.get("user_id")
        if not user_id:
            return

        try:
            user = api.get_user(user_id)
            self.state["user"] = user
            self.state["loading"] = False
        except Exception as e:
            self.state["error"] = str(e)
            self.state["loading"] = False
```

### Real-time Updates

```python
from observ import watch

class LiveDataComponent(cg.Component):
    def init(self):
        self.state["data"] = []
        self.watchers = {}

    def mounted(self):
        """Set up watchers after mounting"""
        # Watch for prop changes
        self.watchers["filter"] = watch(
            lambda: self.props.get("filter"),
            self.on_filter_changed,
            immediate=True
        )

    def on_filter_changed(self, new_filter):
        """React to filter prop changes"""
        self.fetch_data(new_filter)

    def before_unmount(self):
        """Clean up watchers"""
        for watcher in self.watchers.values():
            watcher.stop()
```

### Timer Management

```python
class CountdownTimer(cg.Component):
    def init(self):
        self.state["seconds"] = self.props.get("initial_seconds", 60)
        self.timer_id = None

    def mounted(self):
        """Start timer when component mounts"""
        self.start_timer()

    def start_timer(self):
        import threading
        self.timer_id = threading.Timer(1.0, self.tick)
        self.timer_id.start()

    def tick(self):
        if self.state["seconds"] > 0:
            self.state["seconds"] -= 1
            self.start_timer()  # Schedule next tick
        else:
            self.emit("timer-complete")

    def before_unmount(self):
        """Cancel timer before unmounting"""
        if self.timer_id:
            self.timer_id.cancel()
```

### Focus Management

```python
class AutoFocusInput(cg.Component):
    def mounted(self):
        """Set focus to input field after mounting"""
        if "inputField" in self.refs:
            self.refs["inputField"].setFocus()
```

### Scroll Position Tracking

```python
class ScrollTracker(cg.Component):
    def init(self):
        self.state["scroll_position"] = 0

    def mounted(self):
        """Set up scroll listener"""
        if "scrollArea" in self.refs:
            scroll_area = self.refs["scrollArea"]
            # Note: This is pseudo-code, actual implementation depends on renderer
            scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)

    def on_scroll(self, position):
        self.state["scroll_position"] = position

    def before_unmount(self):
        """Remove scroll listener"""
        if "scrollArea" in self.refs:
            scroll_area = self.refs["scrollArea"]
            scroll_area.verticalScrollBar().valueChanged.disconnect(self.on_scroll)
```

## Lifecycle Hook Execution Order

### Mounting Order

When a component tree is mounted:

```python
# Component hierarchy:
# Parent
# └── Child
#     └── GrandChild

# Execution order:
# 1. Parent.init()
# 2.   Child.init()
# 3.     GrandChild.init()
# 4.     GrandChild.mounted()
# 5.   Child.mounted()
# 6. Parent.mounted()
```

Child components are fully mounted before their parents.

### Update Order

When a parent's state changes affecting children:

```python
# Execution order:
# 1.     GrandChild.updated()
# 2.   Child.updated()
# 3. Parent.updated()
```

Child components are updated before their parents.

### Unmount Order

When components are unmounted:

```python
# No strict order guarantee, but typically:
# 1. Parent.before_unmount()
# 2. Child.before_unmount()
# 3. GrandChild.before_unmount()
```

## Async Operations and Lifecycle

While Collagraph lifecycle hooks are synchronous, you can perform async operations:

```python
import asyncio
import threading

class AsyncDataComponent(cg.Component):
    def init(self):
        self.state["data"] = []
        self.state["loading"] = False

    def mounted(self):
        """Trigger async data loading"""
        self.load_data_async()

    def load_data_async(self):
        """Load data in background thread"""
        def fetch():
            self.state["loading"] = True
            try:
                data = expensive_api_call()
                # Update state on completion
                self.state["data"] = data
            finally:
                self.state["loading"] = False

        thread = threading.Thread(target=fetch)
        thread.start()
```

## Best Practices

### 1. Initialize State in `init()`

Always initialize all state properties in `init()`:

```python
def init(self):
    # Initialize all state upfront
    self.state["data"] = []
    self.state["loading"] = False
    self.state["error"] = None
```

### 2. Access DOM in `mounted()` or Later

Don't try to access refs or DOM elements in `init()`:

```python
def init(self):
    # ❌ Wrong: refs not available yet
    # self.refs["input"].setFocus()
    pass

def mounted(self):
    # ✅ Correct: refs available now
    if "input" in self.refs:
        self.refs["input"].setFocus()
```

### 3. Always Clean Up in `before_unmount()`

If you create resources in `mounted()`, clean them up in `before_unmount()`:

```python
def mounted(self):
    self.subscription = subscribe(self.handler)
    self.timer_id = start_timer(1000, self.tick)

def before_unmount(self):
    # Always clean up
    if self.subscription:
        self.subscription.unsubscribe()
    if self.timer_id:
        cancel_timer(self.timer_id)
```

### 4. Be Careful with `updated()`

Avoid infinite loops by guarding state modifications:

```python
def updated(self):
    # ✅ Safe: only updates when needed
    if self.state["needs_refresh"]:
        self.state["needs_refresh"] = False
        self.refresh_data()
```

### 5. Keep Lifecycle Hooks Simple

Delegate complex logic to separate methods:

```python
def mounted(self):
    # Good: delegates to focused methods
    self.setup_subscriptions()
    self.fetch_initial_data()
    self.configure_ui()

def setup_subscriptions(self):
    # Detailed subscription logic
    pass

def fetch_initial_data(self):
    # Data fetching logic
    pass

def configure_ui(self):
    # UI configuration logic
    pass
```

### 6. Document Side Effects

Document what side effects occur in lifecycle hooks:

```python
class WebSocketComponent(cg.Component):
    """
    Component that maintains a WebSocket connection.

    Lifecycle:
        - mounted(): Opens WebSocket connection
        - before_unmount(): Closes WebSocket connection
    """

    def mounted(self):
        """Open WebSocket connection on mount"""
        self.ws = WebSocket(self.props.get("url"))
        self.ws.connect()

    def before_unmount(self):
        """Close WebSocket connection before unmount"""
        if self.ws:
            self.ws.close()
```

### 7. Handle Props Changes

If you need to react to prop changes, use watchers or check in `updated()`:

```python
from observ import watch

class DynamicComponent(cg.Component):
    def init(self):
        self.watchers = {}

    def mounted(self):
        # Watch for prop changes
        self.watchers["user_id"] = watch(
            lambda: self.props.get("user_id"),
            self.on_user_id_changed,
            immediate=True
        )

    def on_user_id_changed(self, new_id):
        """Fetch new user data when user_id prop changes"""
        self.fetch_user(new_id)

    def before_unmount(self):
        # Clean up watchers
        for watcher in self.watchers.values():
            watcher.stop()
```

## See Also

- [Components](components.md)
- [Reactivity System](reactivity.md)
