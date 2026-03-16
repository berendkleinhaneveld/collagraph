# Best Practices

This guide compiles best practices for building maintainable, performant, and scalable Collagraph applications.

## Component Design

### Single Responsibility Principle

Each component should have one clear purpose:

```python
# Good: Focused component
class UserAvatar(cg.Component):
    """Displays user avatar"""
    pass

class UserProfile(cg.Component):
    """Shows detailed user profile"""
    pass

# Bad: Does too much
class UserEverything(cg.Component):
    """Avatar, profile, settings, notifications..."""
    pass
```

### Keep Components Small

Aim for:
- **< 100 lines**: Simple components
- **100-300 lines**: Medium components
- **> 300 lines**: Consider splitting

```python
# If component is large, extract sub-components
class LargeForm(cg.Component):
    # Extract these into separate components:
    # - PersonalInfoSection
    # - AddressSection
    # - PaymentSection
    pass
```

### Use Props for Configuration

Make components reusable with props:

```python
# Good: Configurable
class Button(cg.Component):
    def init(self):
        self.state["text"] = self.props.get("text", "Click")
        self.state["variant"] = self.props.get("variant", "primary")
        self.state["size"] = self.props.get("size", "medium")

# Bad: Hard-coded
class SubmitButton(cg.Component):
    def init(self):
        self.state["text"] = "Submit"  # Not reusable
```

### Clear Component Interfaces

Document props and events:

```python
class DataTable(cg.Component):
    """
    Displays data in a table.

    Props:
        columns (list[dict]): Column definitions with 'key' and 'label'
        rows (list[dict]): Row data
        sortable (bool): Enable column sorting (default: True)
        page-size (int): Rows per page (default: 25)

    Events:
        row-clicked: Emitted when row is clicked. Passes row data.
        sorted: Emitted when sorting changes. Passes {column, direction}.
    """
```

## State Management

### Initialize All State in init()

```python
# Good: All state defined upfront
def init(self):
    self.state["count"] = 0
    self.state["items"] = []
    self.state["loading"] = False
    self.state["error"] = None

# Bad: State created later
def some_method(self):
    self.state["new_field"] = value  # Unexpected!
```

### Keep State Minimal

Derive values with computed properties:

```python
# Good: Minimal state, derived values
def init(self):
    self.state["todos"] = []

@property
def completed_count(self):
    return sum(1 for t in self.state["todos"] if t["completed"])

@property
def active_count(self):
    return len(self.state["todos"]) - self.completed_count

# Bad: Redundant state
def init(self):
    self.state["todos"] = []
    self.state["completed_count"] = 0  # Redundant
    self.state["active_count"] = 0      # Redundant
```

### Use Descriptive State Names

```python
# Good
self.state["is_loading"] = True
self.state["has_error"] = False
self.state["selected_user_id"] = 42

# Bad
self.state["flag"] = True
self.state["err"] = False
self.state["id"] = 42
```

### Group Related State

```python
# Good: Organized
def init(self):
    self.state["user"] = {
        "id": None,
        "name": "",
        "email": ""
    }
    self.state["ui"] = {
        "theme": "light",
        "sidebar_open": True
    }

# Less organized
def init(self):
    self.state["user_id"] = None
    self.state["user_name"] = ""
    self.state["theme"] = "light"
    self.state["sidebar_open"] = True
```

## Event Handling

### Descriptive Event Names

```python
# Good: Clear action
self.emit("user-created", user)
self.emit("form-submitted", data)
self.emit("item-deleted", item_id)

# Bad: Vague
self.emit("done", user)
self.emit("ok", data)
self.emit("clicked", item_id)
```

### Event Data Structure

```python
# Good: Structured data
self.emit("order-placed", {
    "order_id": order_id,
    "total": total,
    "items": items
})

# Also good: Multiple arguments for simple cases
self.emit("item-selected", item_id, item_name)

# Bad: Unclear
self.emit("event", 123, "abc", [1, 2, 3])
```

### Use Lambdas in v-for

```html
<!-- Good: Lambda captures item -->
<button
  v-for="item in items"
  @clicked="lambda: handle_delete(item['id'])"
/>

<!-- Bad: Won't work as expected -->
<button
  v-for="item in items"
  @clicked="handle_delete(item['id'])"
/>
```

## Template Organization

### Consistent Formatting

```html
<!-- Good: Consistent indentation -->
<widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
  <label :text="title" />
  <widget :layout="{'type': 'box', 'direction': 'left-to-right'}">
    <button text="Cancel" @clicked="cancel" />
    <button text="Save" @clicked="save" />
  </widget>
</widget>

<!-- Bad: Inconsistent -->
<widget>
<label :text="title" />
    <widget>
<button text="Cancel" />
      <button text="Save" />
    </widget>
</widget>
```

### Extract Complex Expressions

```html
<!-- Good: Computed property -->
<label :text="formatted_date" />

<script>
@property
def formatted_date(self):
    return format_date(self.state["created_at"], "MM/DD/YYYY")
</script>

<!-- Bad: Complex expression in template -->
<label :text="datetime.strptime(created_at, '%Y-%m-%d').strftime('%m/%d/%Y')" />
```

### Use v-if for Conditional Rendering

```html
<!-- Good: Clear structure -->
<widget v-if="loading">
  <spinner />
</widget>
<widget v-else-if="error">
  <error-message :error="error" />
</widget>
<widget v-else>
  <data-display :data="data" />
</widget>

<!-- Bad: Nested ternaries -->
<label :text="'Loading...' if loading else ('Error' if error else 'Done')" />
```

## Performance

### Provide Keys in v-for

```html
<!-- Good: Unique key -->
<widget
  v-for="todo in todos"
  :key="todo['id']"
>
  <!-- content -->
</widget>

<!-- Bad: No key (slower updates) -->
<widget v-for="todo in todos">
  <!-- content -->
</widget>
```

### Avoid Expensive Computed Properties

```python
# Good: Cache expensive calculations
def init(self):
    self.state["data"] = []
    self._cached_result = None
    self._cache_key = None

@property
def expensive_calculation(self):
    cache_key = len(self.state["data"])
    if self._cache_key != cache_key:
        self._cached_result = self._compute()
        self._cache_key = cache_key
    return self._cached_result

# Bad: Recalculates every time
@property
def expensive_calculation(self):
    # Expensive operation runs on every access
    return self._compute()
```

### Debounce Expensive Operations

```python
import threading

class SearchComponent(cg.Component):
    def init(self):
        self.search_timer = None

    def handle_input(self, text):
        self.state["query"] = text

        # Debounce search
        if self.search_timer:
            self.search_timer.cancel()

        self.search_timer = threading.Timer(0.3, lambda: self.search(text))
        self.search_timer.start()
```

## Code Organization

### Feature-Based Structure

```
features/
├── users/
│   ├── components/
│   ├── services/
│   └── state/
└── products/
    ├── components/
    ├── services/
    └── state/
```

### Consistent Naming

```
# Components: PascalCase
UserProfile, DataTable, LoginForm

# Files: snake_case
user_profile.cgx, data_table.cgx, login_form.cgx

# Methods: snake_case
def handle_click(self)
def fetch_users(self)

# Properties: snake_case
@property
def full_name(self)
```

### Separate Business Logic

```python
# services/user_service.py
class UserService:
    def get_users(self):
        # Business logic here
        pass

# components/user_list.cgx
from services.user_service import UserService

class UserList(cg.Component):
    def init(self):
        self.user_service = UserService()

    def load_users(self):
        users = self.user_service.get_users()
        self.state["users"] = users
```

## Error Handling

### Handle Errors Gracefully

```python
def load_data(self):
    self.state["loading"] = True
    self.state["error"] = None

    try:
        data = fetch_data()
        self.state["data"] = data
    except Exception as e:
        self.state["error"] = str(e)
        logger.error(f"Failed to load data: {e}", exc_info=True)
    finally:
        self.state["loading"] = False
```

### Validate Props

```python
def init(self):
    # Validate required props
    if "user_id" not in self.props:
        raise ValueError("user_id prop is required")

    # Validate types
    user_id = self.props["user_id"]
    if not isinstance(user_id, int):
        raise TypeError(f"user_id must be int, got {type(user_id)}")
```

### Provide Defaults

```python
def init(self):
    # Always provide sensible defaults
    self.state["title"] = self.props.get("title", "Untitled")
    self.state["items"] = self.props.get("items", [])
    self.state["enabled"] = self.props.get("enabled", True)
```

## Testing

### Write Tests for Components

```python
def test_counter_increment(load_component, render_component):
    Counter, _ = load_component("""...""")
    dom = render_component(Counter)

    # Test initial state
    assert dom["children"][0]["attrs"]["text"] == "Count: 0"

    # Test increment
    button = dom["children"][1]
    for handler in button["handlers"]["clicked"]:
        handler()

    assert dom["children"][0]["attrs"]["text"] == "Count: 1"
```

### Test Edge Cases

```python
def test_empty_list(render_component):
    # Test with empty data
    dom = render_component(List, props={"items": []})
    assert len(dom["children"]) == 0

def test_null_values(render_component):
    # Test with null
    dom = render_component(Component, props={"user": None})
    # Should handle gracefully
```

## Documentation

### Document Components

```python
class DataGrid(cg.Component):
    """
    Displays data in a sortable, paginated grid.

    Props:
        columns (list[dict]): Column definitions
        rows (list[dict]): Data rows
        sortable (bool): Enable sorting (default: True)
        page_size (int): Rows per page (default: 25)

    Events:
        row-clicked: When user clicks a row
        sorted: When sort order changes

    Example:
        <DataGrid
          :columns="columns"
          :rows="users"
          :sortable="True"
          @row-clicked="handle_row_click"
        />
    """
```

### Add Code Comments

```python
def complex_calculation(self):
    # First, filter active items
    active = [i for i in self.state["items"] if i["active"]]

    # Then group by category
    grouped = defaultdict(list)
    for item in active:
        grouped[item["category"]].append(item)

    # Finally, compute totals
    return {cat: sum(i["value"] for i in items)
            for cat, items in grouped.items()}
```

## Security

### Validate User Input

```python
def handle_submit(self, form_data):
    # Validate before using
    email = form_data.get("email", "").strip()

    if not email:
        raise ValueError("Email is required")

    if not is_valid_email(email):
        raise ValueError("Invalid email format")

    # Safe to use
    self.save_user(email)
```

### Sanitize Data

```python
def display_user_content(self, content):
    # Escape special characters if displaying user content
    import html
    safe_content = html.escape(content)
    self.state["display_text"] = safe_content
```

## Avoiding Common Pitfalls

### Don't Modify Props

```python
# Wrong
def init(self):
    self.props["value"] = 10  # Error!

# Right
def init(self):
    self.state["value"] = self.props.get("value", 10)
```

### Don't Forget Keys in v-for

```html
<!-- Wrong: No key -->
<widget v-for="item in items">

<!-- Right: Unique key -->
<widget v-for="item in items" :key="item['id']">
```

### Clean Up Resources

```python
def mounted(self):
    self.timer = start_timer(self.tick)
    self.subscription = subscribe(self.handler)

def before_unmount(self):
    # Always clean up!
    cancel_timer(self.timer)
    self.subscription.unsubscribe()
```

### Avoid Infinite Loops

```python
# Wrong: Infinite loop
def updated(self):
    self.state["count"] += 1  # Triggers updated() again!

# Right: Guard condition
def updated(self):
    if self.state["needs_update"]:
        self.state["needs_update"] = False
        self.perform_update()
```

## See Also

- [Code Organization](code-organization.md)
- [Components](../core-concepts/components.md)
- [State Management](../core-concepts/state-management.md)
- [Testing](testing.md)
