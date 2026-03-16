# Watchers

## Overview

Watchers allow you to perform side effects in response to reactive state changes. Unlike computed properties (which derive new values), watchers are for performing actions like data fetching, API calls, logging, or updating external systems when reactive data changes.

Watchers are powered by the [observ](https://github.com/fork-tongue/observ) library and provide flexible options for tracking and reacting to changes.

## Creating Watchers

### Using `watch()`

The most common way to create watchers is with the `watch()` function:

```python
from observ import watch
import collagraph as cg

class SearchComponent(cg.Component):
    def init(self):
        self.state["search_query"] = ""
        self.state["results"] = []
        self.watchers = {}

    def mounted(self):
        # Watch search query and fetch results when it changes
        self.watchers["search"] = watch(
            lambda: self.state["search_query"],
            self.perform_search
        )

    def perform_search(self, new_query):
        """Called when search_query changes"""
        if len(new_query) >= 3:
            results = api.search(new_query)
            self.state["results"] = results
        else:
            self.state["results"] = []

    def before_unmount(self):
        # Clean up watchers
        for watcher in self.watchers.values():
            watcher.stop()
```

### Basic Watch Syntax

```python
from observ import watch

# watch(source, callback, options)
watcher = watch(
    lambda: self.state["value"],  # What to watch
    self.on_value_changed          # What to do when it changes
)
```

## Watch Callbacks

### Single Argument Callback

The callback receives the new value:

```python
def mounted(self):
    self.watchers["counter"] = watch(
        lambda: self.state["count"],
        self.on_count_changed
    )

def on_count_changed(self, new_count):
    """Called with new value when count changes"""
    print(f"Count changed to: {new_count}")
```

### Two Argument Callback

To receive both new and old values, the callback can accept two arguments:

```python
def mounted(self):
    self.watchers["status"] = watch(
        lambda: self.state["status"],
        self.on_status_changed
    )

def on_status_changed(self, new_status, old_status=None):
    """Called with new and old values"""
    print(f"Status changed from {old_status} to {new_status}")

    # Perform different actions based on transition
    if old_status == "pending" and new_status == "complete":
        self.notify_completion()
```

### Inline Callbacks

You can use lambda functions for simple watchers:

```python
def mounted(self):
    # Simple inline callback
    self.watchers["theme"] = watch(
        lambda: self.state["theme"],
        lambda theme: print(f"Theme changed to: {theme}")
    )
```

## Watch Options

### Immediate Execution

By default, watchers don't run immediately. Use `immediate=True` to run the callback once on creation:

```python
def mounted(self):
    # Run callback immediately with current value
    self.watchers["user_id"] = watch(
        lambda: self.props.get("user_id"),
        self.fetch_user_data,
        immediate=True  # Fetch data right away
    )

def fetch_user_data(self, user_id):
    """Fetches user data from API"""
    if user_id:
        user = api.get_user(user_id)
        self.state["user"] = user
```

This is useful for:
- Fetching initial data based on props
- Setting up initial state based on reactive values
- Running initialization logic that depends on reactive data

## Using `watch_effect()`

`watch_effect()` automatically tracks all reactive dependencies used within its callback:

```python
from observ import watch_effect

class AutomaticDependencies(cg.Component):
    def init(self):
        self.state["first_name"] = "Alice"
        self.state["last_name"] = "Smith"
        self.watchers = {}

    def mounted(self):
        # Automatically watches first_name AND last_name
        self.watchers["name"] = watch_effect(
            lambda: print(f"Full name: {self.state['first_name']} {self.state['last_name']}")
        )

    def before_unmount(self):
        for watcher in self.watchers.values():
            watcher.stop()
```

`watch_effect()` is useful when:
- You have multiple dependencies
- Dependencies might change
- You want automatic dependency tracking

## Common Use Cases

### Data Fetching

```python
class UserProfile(cg.Component):
    def init(self):
        self.state["user_id"] = None
        self.state["user_data"] = None
        self.state["loading"] = False
        self.watchers = {}

    def mounted(self):
        # Watch user_id and fetch data when it changes
        self.watchers["user"] = watch(
            lambda: self.props.get("user_id"),
            self.fetch_user,
            immediate=True
        )

    def fetch_user(self, user_id):
        """Fetch user data when ID changes"""
        if not user_id:
            self.state["user_data"] = None
            return

        self.state["loading"] = True
        try:
            user = api.get_user(user_id)
            self.state["user_data"] = user
        except Exception as e:
            print(f"Error fetching user: {e}")
        finally:
            self.state["loading"] = False

    def before_unmount(self):
        for watcher in self.watchers.values():
            watcher.stop()
```

### Saving to Local Storage

```python
class PersistentSettings(cg.Component):
    def init(self):
        self.state["settings"] = {
            "theme": "light",
            "language": "en",
            "notifications": True
        }
        self.watchers = {}

    def mounted(self):
        # Save settings to localStorage when they change
        self.watchers["settings"] = watch(
            lambda: self.state["settings"],
            self.save_settings
        )

    def save_settings(self, settings):
        """Save settings to persistent storage"""
        import json
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def before_unmount(self):
        for watcher in self.watchers.values():
            watcher.stop()
```

### Validation

```python
class FormValidation(cg.Component):
    def init(self):
        self.state["email"] = ""
        self.state["email_error"] = ""
        self.watchers = {}

    def mounted(self):
        # Validate email when it changes
        self.watchers["email"] = watch(
            lambda: self.state["email"],
            self.validate_email
        )

    def validate_email(self, email):
        """Validate email format"""
        import re

        if not email:
            self.state["email_error"] = ""
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.state["email_error"] = "Invalid email format"
        else:
            self.state["email_error"] = ""

    def before_unmount(self):
        for watcher in self.watchers.values():
            watcher.stop()
```

### Debounced Search

```python
import threading

class DebouncedSearch(cg.Component):
    def init(self):
        self.state["search_query"] = ""
        self.state["results"] = []
        self.watchers = {}
        self.search_timer = None

    def mounted(self):
        # Watch search query
        self.watchers["search"] = watch(
            lambda: self.state["search_query"],
            self.schedule_search
        )

    def schedule_search(self, query):
        """Debounce search - wait 300ms after user stops typing"""
        # Cancel previous timer
        if self.search_timer:
            self.search_timer.cancel()

        # Schedule new search
        self.search_timer = threading.Timer(0.3, lambda: self.perform_search(query))
        self.search_timer.start()

    def perform_search(self, query):
        """Actually perform the search"""
        if len(query) >= 3:
            results = api.search(query)
            self.state["results"] = results

    def before_unmount(self):
        # Clean up
        if self.search_timer:
            self.search_timer.cancel()
        for watcher in self.watchers.values():
            watcher.stop()
```

### Logging and Analytics

```python
class AnalyticsTracker(cg.Component):
    def init(self):
        self.state["current_page"] = "home"
        self.state["user_actions"] = []
        self.watchers = {}

    def mounted(self):
        # Track page changes
        self.watchers["page"] = watch(
            lambda: self.state["current_page"],
            self.track_page_view
        )

        # Track user actions
        self.watchers["actions"] = watch(
            lambda: len(self.state["user_actions"]),
            self.log_action_count
        )

    def track_page_view(self, page):
        """Send page view to analytics"""
        analytics.track("page_view", {"page": page})

    def log_action_count(self, count):
        """Log when user performs actions"""
        print(f"User has performed {count} actions")

    def before_unmount(self):
        for watcher in self.watchers.values():
            watcher.stop()
```

### Syncing State

```python
class SyncedComponents(cg.Component):
    def init(self):
        self.state["local_value"] = 0
        self.watchers = {}

    def mounted(self):
        # Sync local state with prop changes
        self.watchers["prop_sync"] = watch(
            lambda: self.props.get("external_value"),
            self.sync_from_prop,
            immediate=True
        )

        # Emit changes to parent
        self.watchers["emit_sync"] = watch(
            lambda: self.state["local_value"],
            self.sync_to_parent
        )

    def sync_from_prop(self, external_value):
        """Update local state when prop changes"""
        if external_value != self.state["local_value"]:
            self.state["local_value"] = external_value

    def sync_to_parent(self, local_value):
        """Emit local changes to parent"""
        self.emit("value-changed", local_value)

    def before_unmount(self):
        for watcher in self.watchers.values():
            watcher.stop()
```

## Multiple Dependencies

Watch multiple values by returning them as a tuple:

```python
def mounted(self):
    # Watch multiple values
    self.watchers["multi"] = watch(
        lambda: (self.state["width"], self.state["height"]),
        self.on_dimensions_changed
    )

def on_dimensions_changed(self, dimensions):
    """Called when either width or height changes"""
    width, height = dimensions
    area = width * height
    self.state["area"] = area
    print(f"Dimensions: {width}x{height}, Area: {area}")
```

## Watchers vs Computed Properties

### Use Computed Properties When:

- You need to derive a value from other values
- The result should be cached
- You want automatic dependency tracking
- The operation is synchronous and pure

```python
# ✅ Computed property: Derive value
@property
def full_name(self):
    return f"{self.state['first']} {self.state['last']}"
```

### Use Watchers When:

- You need to perform side effects (API calls, logging, etc.)
- You need to perform asynchronous operations
- You need to update external systems
- You need to debounce or throttle operations

```python
# ✅ Watcher: Side effect
def mounted(self):
    self.watchers["name"] = watch(
        lambda: self.state["name"],
        self.save_to_database  # Side effect!
    )
```

### Example Comparison

```python
class UserComponent(cg.Component):
    def init(self):
        self.state["first_name"] = "Alice"
        self.state["last_name"] = "Smith"
        self.watchers = {}

    # ✅ Computed: Derive display value (no side effects)
    @property
    def full_name(self):
        return f"{self.state['first_name']} {self.state['last_name']}"

    # ✅ Watcher: Perform side effect when name changes
    def mounted(self):
        self.watchers["name"] = watch(
            lambda: (self.state["first_name"], self.state["last_name"]),
            self.log_name_change
        )

    def log_name_change(self, names):
        """Side effect: log to analytics"""
        first, last = names
        analytics.track("name_changed", {
            "first_name": first,
            "last_name": last
        })

    def before_unmount(self):
        for watcher in self.watchers.values():
            watcher.stop()
```

## Cleanup

Always stop watchers in `before_unmount()` to prevent memory leaks:

```python
class ProperCleanup(cg.Component):
    def init(self):
        self.state["value"] = 0
        self.watchers = {}

    def mounted(self):
        # Create watchers
        self.watchers["value"] = watch(
            lambda: self.state["value"],
            self.on_value_changed
        )

    def on_value_changed(self, value):
        print(f"Value: {value}")

    def before_unmount(self):
        # IMPORTANT: Stop all watchers
        for watcher in self.watchers.values():
            watcher.stop()

        # Clear the dictionary
        self.watchers.clear()
```

## Best Practices

### 1. Store Watchers for Cleanup

Always store watcher references so you can stop them:

```python
def init(self):
    self.watchers = {}  # Store all watchers here

def mounted(self):
    self.watchers["my_watcher"] = watch(...)

def before_unmount(self):
    for watcher in self.watchers.values():
        watcher.stop()
```

### 2. Use `immediate=True` for Initial Data

When fetching data based on props or state:

```python
def mounted(self):
    # Fetch data immediately and on changes
    self.watchers["data"] = watch(
        lambda: self.props.get("id"),
        self.fetch_data,
        immediate=True  # Don't wait for first change
    )
```

### 3. Handle Edge Cases

Check for None/empty values in callbacks:

```python
def fetch_user(self, user_id):
    # Handle None or empty ID
    if not user_id:
        self.state["user"] = None
        return

    # Proceed with fetch
    user = api.get_user(user_id)
    self.state["user"] = user
```

### 4. Avoid Infinite Loops

Don't modify the watched value inside the watcher callback:

```python
# ❌ BAD: Infinite loop!
def mounted(self):
    self.watchers["bad"] = watch(
        lambda: self.state["count"],
        lambda count: self.state.__setitem__("count", count + 1)  # Triggers watcher again!
    )

# ✅ GOOD: Modify different state
def mounted(self):
    self.watchers["good"] = watch(
        lambda: self.state["count"],
        lambda count: self.state.__setitem__("double", count * 2)  # Different state
    )
```

### 5. Use Watchers for Side Effects Only

Keep watchers focused on side effects, not derivations:

```python
# ❌ Bad: Use computed property instead
def mounted(self):
    self.watchers["bad"] = watch(
        lambda: self.state["items"],
        lambda items: self.state.__setitem__("count", len(items))
    )

# ✅ Good: Use computed property
@property
def count(self):
    return len(self.state["items"])

# ✅ Good: Use watcher for side effects
def mounted(self):
    self.watchers["good"] = watch(
        lambda: self.state["items"],
        lambda items: self.send_to_analytics("items_changed", len(items))
    )
```

### 6. Document Complex Watchers

Add comments explaining what the watcher does:

```python
def mounted(self):
    # Watch for changes to user preferences and persist to disk
    # Debounced to avoid excessive writes
    self.watchers["preferences"] = watch(
        lambda: self.state["user_preferences"],
        self.save_preferences_debounced
    )
```

## See Also

- [Reactivity System](reactivity.md)
- [Computed Properties](computed.md)
