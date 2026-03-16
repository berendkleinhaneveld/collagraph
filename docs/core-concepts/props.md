# Props

## Overview

Props (short for "properties") allow parent components to pass data to child components. They are the primary mechanism for component communication in Collagraph, enabling a unidirectional data flow from parent to child.

Props are **read-only** from the child component's perspective, enforcing a clear separation of concerns and making data flow predictable.

## Passing Props

### Basic Prop Passing

In the parent component's template, pass props as attributes:

```html
<!-- Static props -->
<UserCard name="Alice" role="Developer" />

<!-- Dynamic props (using : prefix) -->
<UserCard :name="username" :role="user_role" />
```

### Dynamic Props

Use the `:` prefix to bind props to reactive data:

```html
<widget>
  <Counter :initial-count="start_value" />
  <UserProfile :user="current_user" />
  <StatusBadge :is-active="is_online" />
</widget>
```

```python
class Parent(cg.Component):
    def init(self):
        self.state["start_value"] = 10
        self.state["current_user"] = {"name": "Alice", "email": "alice@example.com"}
        self.state["is_online"] = True
```

### Prop Naming Conventions

Props in templates use kebab-case (`initial-count`) and are automatically converted to snake_case (`initial_count`) when accessed in Python:

```html
<!-- Template: kebab-case -->
<MyComponent my-prop-name="value" />
```

```python
# Python: snake_case
class MyComponent(cg.Component):
    def init(self):
        value = self.props.get("my_prop_name")
```

## Accessing Props

### Using `self.props`

Props are accessed via the `self.props` dictionary in the component:

```python
class ChildComponent(cg.Component):
    def init(self):
        # Access props with .get() for safety
        name = self.props.get("name", "Guest")
        age = self.props.get("age", 0)

        # Or direct access if you're sure it exists
        email = self.props["email"]
```

### In Templates

Props can be accessed directly in templates (through automatic lookup):

```html
<label :text="name" />
<label :text="f'Age: {age}'" />
```

Or explicitly:

```html
<label :text="props['name']" />
<label :text="props.get('age', 0)" />
```

## Default Values

Always provide default values when accessing props to make your components more robust:

```python
class UserCard(cg.Component):
    def init(self):
        # Provide sensible defaults
        self.state["name"] = self.props.get("name", "Anonymous")
        self.state["email"] = self.props.get("email", "no-email@example.com")
        self.state["role"] = self.props.get("role", "User")
        self.state["is_active"] = self.props.get("is_active", True)
```

### Using Props Directly vs Copying to State

You can use props directly in templates without copying to state:

```html
<!-- Direct prop usage -->
<label :text="name" />
```

Or copy to state if you need to transform or modify the value:

```python
def init(self):
    # Copy to state if you need a mutable version
    self.state["title"] = self.props.get("title", "Untitled").upper()

    # Or if you need to transform the prop
    self.state["count"] = max(0, self.props.get("initial_count", 0))
```

## Prop Types

While Collagraph doesn't enforce prop types at runtime, you can document expected types and handle them appropriately:

```python
class DataTable(cg.Component):
    """
    Data table component.

    Props:
        columns (list[dict]): List of column definitions
        rows (list[dict]): List of row data
        sortable (bool): Whether columns are sortable
        page_size (int): Number of rows per page
        on_row_click (callable): Callback when row is clicked
    """

    def init(self):
        # Access props with expected types
        columns = self.props.get("columns", [])
        rows = self.props.get("rows", [])
        sortable = self.props.get("sortable", False)
        page_size = self.props.get("page_size", 10)

        # Validate types if needed
        if not isinstance(columns, list):
            raise TypeError("columns must be a list")

        self.state["columns"] = columns
        self.state["rows"] = rows
```

## Passing Different Data Types

Props can be any Python type:

### Strings

```html
<MyComponent message="Hello" />
<MyComponent :message="dynamic_message" />
```

### Numbers

```html
<!-- Static number (as string, will need parsing) -->
<Counter count="10" />

<!-- Dynamic number (actual number type) -->
<Counter :count="10" />
<Counter :count="initial_value" />
```

### Booleans

```html
<!-- Static boolean -->
<Toggle enabled="True" />

<!-- Dynamic boolean -->
<Toggle :enabled="is_active" />
<Toggle :enabled="count > 0" />
```

### Lists and Arrays

```html
<ItemList :items="['Apple', 'Banana', 'Cherry']" />
<ItemList :items="fruit_list" />
```

### Dictionaries/Objects

```html
<UserProfile :user="{'name': 'Alice', 'age': 30}" />
<UserProfile :user="current_user" />
```

### Functions/Callbacks

```html
<Button :on-click="handle_click" />
<DataTable :row-renderer="render_custom_row" />
```

```python
class Parent(cg.Component):
    def handle_click(self):
        print("Button was clicked!")

    def render_custom_row(self, row_data):
        return f"Custom: {row_data['name']}"
```

## One-Way Data Flow

Props follow a **one-way data flow** from parent to child:

```
Parent Component
    |
    | (props)
    ↓
Child Component
```

### Props Are Read-Only

Child components **cannot** modify props:

```python
class Child(cg.Component):
    def init(self):
        # This will raise an error!
        # self.props["name"] = "New Name"  # ❌ ReadonlyError

        # Instead, copy to state if you need to modify
        self.state["name"] = self.props.get("name", "")  # ✅

    def update_name(self, new_name):
        # Modify state, not props
        self.state["name"] = new_name
```

### Communication Back to Parent

To send data back to the parent, use events:

```python
# Child component
class Child(cg.Component):
    def handle_change(self, new_value):
        # Emit event to parent
        self.emit("value-changed", new_value)
```

```html
<!-- Parent template -->
<Child :value="current_value" @value-changed="handle_value_change" />
```

```python
# Parent component
class Parent(cg.Component):
    def handle_value_change(self, new_value):
        self.state["current_value"] = new_value
```

## Reactive Props

When a parent's state changes, props passed to children automatically update:

```python
class Parent(cg.Component):
    def init(self):
        self.state["counter"] = 0

    def increment(self):
        # When this changes, child's prop automatically updates
        self.state["counter"] += 1
```

```html
<widget>
  <button text="Increment" @clicked="increment" />
  <!-- Child receives updated prop automatically -->
  <Display :value="counter" />
</widget>
```

### Lifecycle and Props

When props update, the `updated()` lifecycle hook is called:

```python
class Display(cg.Component):
    def updated(self):
        # Called when props (or state) change
        print(f"Updated! Current value: {self.props.get('value')}")
```

## v-bind Directive

Use `v-bind` to pass all properties from an object as individual props:

```html
<!-- Instead of this -->
<UserCard
  :name="user['name']"
  :email="user['email']"
  :role="user['role']"
/>

<!-- Use v-bind -->
<UserCard v-bind="user" />
```

You can also combine `v-bind` with explicit props:

```html
<!-- Spread defaults, then override specific props -->
<Button
  v-bind="default_button_props"
  :text="custom_label"
  :enabled="is_active"
/>
```

## Props in v-for

When using `v-for`, you can bind props from loop variables:

```html
<UserCard
  v-for="user in users"
  :key="user['id']"
  v-bind="user"
  @click="lambda: select_user(user)"
/>
```

## Common Patterns

### Configuration Props

```python
class DataGrid(cg.Component):
    """
    Configurable data grid component.
    """

    def init(self):
        # Configuration via props
        self.state["columns"] = self.props.get("columns", [])
        self.state["sortable"] = self.props.get("sortable", True)
        self.state["paginated"] = self.props.get("paginated", False)
        self.state["page_size"] = self.props.get("page_size", 25)
        self.state["striped"] = self.props.get("striped", True)
```

### Callback Props

```python
class FileUploader(cg.Component):
    def init(self):
        self.on_upload_complete = self.props.get("on_upload_complete")
        self.on_error = self.props.get("on_error")

    def upload_file(self, file):
        try:
            # Upload logic...
            if self.on_upload_complete:
                self.on_upload_complete(file)
        except Exception as e:
            if self.on_error:
                self.on_error(e)
```

### Render Props

```python
class DataProvider(cg.Component):
    """
    Component that provides data to a render function.
    """

    def init(self):
        self.state["data"] = []
        self.state["loading"] = True

        # Get render function from props
        self.render_fn = self.props.get("render")

    def render_content(self):
        if self.render_fn:
            return self.render_fn({
                "data": self.state["data"],
                "loading": self.state["loading"]
            })
        return None
```

## Validation and Type Checking

While not enforced by Collagraph, you can add your own validation:

```python
class ValidatedComponent(cg.Component):
    def init(self):
        # Validate required props
        if "user_id" not in self.props:
            raise ValueError("user_id prop is required")

        # Validate types
        age = self.props.get("age")
        if age is not None and not isinstance(age, int):
            raise TypeError("age must be an integer")

        # Validate ranges
        if age is not None and (age < 0 or age > 150):
            raise ValueError("age must be between 0 and 150")

        self.state["user_id"] = self.props["user_id"]
        self.state["age"] = age
```

## Best Practices

### 1. Provide Defaults

Always provide sensible defaults for optional props:

```python
def init(self):
    self.state["title"] = self.props.get("title", "Untitled")
    self.state["enabled"] = self.props.get("enabled", True)
```

### 2. Document Props

Use docstrings to document expected props:

```python
class MyComponent(cg.Component):
    """
    Component description.

    Props:
        title (str): The component title
        enabled (bool): Whether the component is enabled
        items (list): List of items to display
        on_submit (callable): Callback when form is submitted
    """
```

### 3. Use Descriptive Prop Names

Choose clear, descriptive names:

```python
# Good
<UserCard user-name="Alice" is-active="True" />

# Less clear
<UserCard name="Alice" active="True" />
```

### 4. Don't Mutate Props

Never try to modify props. Copy to state if needed:

```python
def init(self):
    # ❌ Don't do this
    # self.props["value"] = new_value

    # ✅ Do this instead
    self.state["value"] = self.props.get("value", "")
```

### 5. Keep Props Simple

Prefer multiple simple props over complex nested structures:

```python
# Good: Simple, clear props
<UserCard name="Alice" email="alice@example.com" role="Admin" />

# Less ideal: Complex nested object
<UserCard :config="{'user': {'personal': {'name': 'Alice'}}}" />
```

### 6. Use Props for Configuration, State for Data

Props should configure how a component behaves, while state manages dynamic data:

```python
class SearchBox(cg.Component):
    def init(self):
        # Props: configuration
        placeholder = self.props.get("placeholder", "Search...")
        min_chars = self.props.get("min_chars", 3)

        # State: dynamic data
        self.state["query"] = ""
        self.state["results"] = []
```

## See Also

- [Components](components.md)
- [State Management](state-management.md)
