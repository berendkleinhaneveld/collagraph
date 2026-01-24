# Template Refs

## Overview

Template refs provide a way to get direct access to DOM elements and child component instances after they are rendered. This is useful when you need to imperatively interact with UI elements, such as setting focus, reading values, or calling methods on child components.

Refs are accessed via `self.refs`, a reactive dictionary that automatically updates when elements are added or removed from the DOM.

## Creating Refs

### Basic Ref Attribute

Add a `ref` attribute to any element or component in your template:

```html
<widget>
  <line-edit ref="inputField" placeholder="Enter text" />
  <button ref="submitButton" text="Submit" />
  <UserProfile ref="userProfile" />
</widget>

<script>
import collagraph as cg
from user_profile import UserProfile

class MyComponent(cg.Component):
    def mounted(self):
        # Refs are available after mounting
        print(f"Available refs: {list(self.refs.keys())}")
</script>
```

### Accessing Refs

Refs are accessed via the `self.refs` dictionary:

```python
class MyComponent(cg.Component):
    def mounted(self):
        # Check if ref exists
        if "inputField" in self.refs:
            # Access the element
            input_widget = self.refs["inputField"]
            input_widget.setFocus()

        # Direct access (only if you're sure it exists)
        button = self.refs["submitButton"]
```

## Refs to Elements

When you add a `ref` to a regular element (not a component), `self.refs` contains the actual DOM element:

```html
<window title="Refs Example">
  <widget>
    <line-edit
      ref="nameInput"
      placeholder="Enter your name"
    />
    <line-edit
      ref="emailInput"
      placeholder="Enter your email"
    />
    <button
      text="Submit"
      @clicked="handle_submit"
    />
  </widget>
</window>

<script>
import collagraph as cg

class Form(cg.Component):
    def handle_submit(self):
        # Access input elements directly
        if "nameInput" in self.refs and "emailInput" in self.refs:
            name = self.refs["nameInput"].text()
            email = self.refs["emailInput"].text()

            print(f"Name: {name}")
            print(f"Email: {email}")

            # Clear the inputs
            self.refs["nameInput"].clear()
            self.refs["emailInput"].clear()
</script>
```

### Common Element Operations

```python
class ElementManipulation(cg.Component):
    def mounted(self):
        # Focus an input
        if "input" in self.refs:
            self.refs["input"].setFocus()

    def read_value(self):
        # Read input value
        if "input" in self.refs:
            value = self.refs["input"].text()
            return value

    def set_value(self, value):
        # Set input value
        if "input" in self.refs:
            self.refs["input"].setText(value)

    def clear_input(self):
        # Clear input
        if "input" in self.refs:
            self.refs["input"].clear()

    def change_style(self):
        # Modify element styling (PySide example)
        if "label" in self.refs:
            self.refs["label"].setStyleSheet("color: red; font-size: 18px;")

    def enable_button(self):
        # Enable/disable button
        if "button" in self.refs:
            self.refs["button"].setEnabled(True)
```

## Refs to Components

When you add a `ref` to a component, `self.refs` contains the component **instance**, not its root element:

```html
<!-- Parent component -->
<widget>
  <Counter ref="counterComponent" initial="0" />
  <button text="Reset Counter" @clicked="reset_counter" />
</widget>

<script>
import collagraph as cg
from counter import Counter

class Parent(cg.Component):
    def reset_counter(self):
        # Access child component instance
        if "counterComponent" in self.refs:
            counter = self.refs["counterComponent"]

            # Call methods on the child component
            counter.reset()

            # Access child component state
            print(f"Current count: {counter.state['count']}")

            # Access child component props
            print(f"Initial value: {counter.props['initial']}")
</script>
```

**Counter component (counter.cgx):**
```html
<widget>
  <label :text="f'Count: {count}'" />
  <button text="Increment" @clicked="increment" />
</widget>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = self.props.get("initial", 0)

    def increment(self):
        self.state["count"] += 1

    def reset(self):
        """Public method that can be called by parent"""
        self.state["count"] = self.props.get("initial", 0)
</script>
```

## Dynamic Refs

Refs can be dynamic, using the `:ref` syntax:

```html
<widget>
  <input
    v-for="idx, field in enumerate(fields)"
    :ref="f'input_{idx}'"
    :placeholder="field"
  />
  <button text="Focus First" @clicked="focus_first" />
</widget>

<script>
import collagraph as cg

class DynamicRefs(cg.Component):
    def init(self):
        self.state["fields"] = ["Name", "Email", "Phone"]

    def focus_first(self):
        # Access dynamically created ref
        if "input_0" in self.refs:
            self.refs["input_0"].setFocus()

    def get_all_values(self):
        """Get values from all dynamically created inputs"""
        values = []
        for idx in range(len(self.state["fields"])):
            ref_name = f"input_{idx}"
            if ref_name in self.refs:
                values.append(self.refs[ref_name].text())
        return values
</script>
```

### Changing Ref Names Dynamically

When a ref name changes, the old ref is automatically removed and the new one is added:

```html
<input :ref="current_ref_name" />

<script>
import collagraph as cg

class ChangingRef(cg.Component):
    def init(self):
        self.state["current_ref_name"] = "myInput"

    def change_ref_name(self):
        # Change the ref name
        self.state["current_ref_name"] = "renamedInput"

        # Old ref "myInput" is removed
        # New ref "renamedInput" is added
</script>
```

## Function Refs

Refs can also be functions that are called when the element is mounted/unmounted:

```html
<input :ref="handle_input_ref" />

<script>
import collagraph as cg

class FunctionRef(cg.Component):
    def init(self):
        self.input_element = None

    def handle_input_ref(self, element):
        """
        Called with the element when it's mounted,
        and with None when it's unmounted
        """
        if element is not None:
            # Element mounted
            print("Input mounted")
            self.input_element = element
            element.setFocus()
        else:
            # Element unmounted
            print("Input unmounted")
            self.input_element = None
</script>
```

Function refs are useful for:
- Performing setup when element is mounted
- Cleanup when element is unmounted
- Storing references outside the refs dictionary
- Conditional logic based on element presence

## Refs with Conditional Rendering

Refs are automatically added/removed when elements appear/disappear with `v-if`:

```html
<widget>
  <input v-if="show_input" ref="conditionalInput" />
  <button text="Toggle Input" @clicked="toggle_input" />
  <button text="Focus Input" @clicked="focus_input" />
</widget>

<script>
import collagraph as cg

class ConditionalRef(cg.Component):
    def init(self):
        self.state["show_input"] = False

    def toggle_input(self):
        self.state["show_input"] = not self.state["show_input"]

    def focus_input(self):
        # Check if ref exists before using
        if "conditionalInput" in self.refs:
            self.refs["conditionalInput"].setFocus()
        else:
            print("Input not currently shown")
</script>
```

## Accessing Refs in Templates

Refs can be accessed directly in template expressions:

```html
<widget>
  <input ref="myInput" placeholder="Type here" />

  <!-- Access ref in template -->
  <button
    :disabled="not myInput"
    text="Submit"
  />

  <!-- Or explicitly -->
  <button
    :disabled="not refs.get('myInput')"
    text="Submit"
  />
</widget>
```

This is possible because of Collagraph's automatic variable lookup which checks `self.refs`.

### Reactive Refs in Templates

Refs are reactive, so templates update when refs are added/removed:

```html
<widget>
  <input v-if="show" ref="input" />

  <!-- This reactively updates based on ref presence -->
  <label :text="'Input is visible' if input else 'Input is hidden'" />

  <!-- Or more explicitly -->
  <label :text="'Input is visible' if refs.get('input') else 'Input is hidden'" />
</widget>
```

## When to Use Refs

### Good Use Cases

**1. Focus Management**
```python
def mounted(self):
    if "inputField" in self.refs:
        self.refs["inputField"].setFocus()
```

**2. Reading Form Values**
```python
def submit_form(self):
    if "nameInput" in self.refs:
        name = self.refs["nameInput"].text()
        # Process form...
```

**3. Imperatively Controlling Playback**
```python
def play_video(self):
    if "videoPlayer" in self.refs:
        self.refs["videoPlayer"].play()

def pause_video(self):
    if "videoPlayer" in self.refs:
        self.refs["videoPlayer"].pause()
```

**4. Measuring Elements**
```python
def get_dimensions(self):
    if "container" in self.refs:
        width = self.refs["container"].width()
        height = self.refs["container"].height()
        return (width, height)
```

**5. Calling Child Component Methods**
```python
def refresh_data(self):
    if "dataTable" in self.refs:
        self.refs["dataTable"].refresh()
```

**6. Third-Party Library Integration**
```python
def mounted(self):
    if "canvas" in self.refs:
        # Initialize third-party library with DOM element
        self.chart = ChartLibrary(self.refs["canvas"])
```

### When NOT to Use Refs

**Avoid using refs for:**

1. **Data Passing** - Use props instead
2. **State Management** - Use component state instead
3. **Styling** - Use dynamic attributes instead

```python
# ❌ Bad: Using refs for styling
def change_color(self):
    if "label" in self.refs:
        self.refs["label"].setStyleSheet("color: red")

# ✅ Good: Use reactive state and attributes
def init(self):
    self.state["color"] = "red"

# Template: <label :style="f'color: {color}'" />
```

## Complete Example

Here's a comprehensive example using various ref patterns:

```html
<window title="Template Refs Demo" width="500" height="400">
  <widget>
    <!-- Form inputs with refs -->
    <widget :layout="{'type': 'Box', 'direction': 'LeftToRight'}">
      <label text="Name:" />
      <line-edit
        ref="nameInput"
        placeholder="Enter your name"
      />
    </widget>

    <widget :layout="{'type': 'Box', 'direction': 'LeftToRight'}">
      <label text="Email:" />
      <line-edit
        ref="emailInput"
        placeholder="Enter your email"
      />
    </widget>

    <!-- Buttons for interaction -->
    <widget :layout="{'type': 'Box', 'direction': 'LeftToRight'}">
      <button text="Focus Name" @clicked="focus_name" />
      <button text="Focus Email" @clicked="focus_email" />
      <button text="Clear All" @clicked="clear_all" />
    </widget>

    <button text="Read Values" @clicked="read_values" />

    <!-- Output label with ref -->
    <label
      ref="outputLabel"
      text="Output will appear here"
    />

    <!-- Conditional ref -->
    <text-edit
      v-if="show_notes"
      ref="notesField"
      placeholder="Additional notes"
    />

    <button
      :text="'Hide Notes' if show_notes else 'Show Notes'"
      @clicked="toggle_notes"
    />
  </widget>
</window>

<script>
import collagraph as cg

class TemplateRefsDemo(cg.Component):
    """
    Comprehensive template refs demonstration.
    """

    def init(self):
        self.state["show_notes"] = False

    def mounted(self):
        """Auto-focus name input when component mounts"""
        self.focus_name()

    def focus_name(self):
        """Set focus to the name input field"""
        if "nameInput" in self.refs:
            self.refs["nameInput"].setFocus()

    def focus_email(self):
        """Set focus to the email input field"""
        if "emailInput" in self.refs:
            self.refs["emailInput"].setFocus()

    def clear_all(self):
        """Clear all input fields"""
        if "nameInput" in self.refs:
            self.refs["nameInput"].clear()
        if "emailInput" in self.refs:
            self.refs["emailInput"].clear()
        if "notesField" in self.refs:
            self.refs["notesField"].clear()
        if "outputLabel" in self.refs:
            self.refs["outputLabel"].setText("Fields cleared")

    def read_values(self):
        """Read values from all input fields"""
        name = ""
        email = ""
        notes = ""

        if "nameInput" in self.refs:
            name = self.refs["nameInput"].text()
        if "emailInput" in self.refs:
            email = self.refs["emailInput"].text()
        if "notesField" in self.refs:
            notes = self.refs["notesField"].toPlainText()

        # Display in output label
        if "outputLabel" in self.refs:
            output = f"Name: {name}\nEmail: {email}"
            if notes:
                output += f"\nNotes: {notes}"
            self.refs["outputLabel"].setText(output)

    def toggle_notes(self):
        """Toggle the notes field visibility"""
        self.state["show_notes"] = not self.state["show_notes"]

        # If showing notes, focus the field
        if self.state["show_notes"]:
            # Need to wait for next render cycle
            # In practice, you might use a timer or the updated() hook
            pass
</script>
```

## Best Practices

### 1. Always Check if Ref Exists

Refs might not exist due to conditional rendering:

```python
# ✅ Good: Check before using
if "myRef" in self.refs:
    self.refs["myRef"].doSomething()

# ❌ Bad: Might raise KeyError
self.refs["myRef"].doSomething()
```

### 2. Access Refs in `mounted()` or Later

Refs aren't available until the component is mounted:

```python
def init(self):
    # ❌ Bad: Refs not available yet
    # self.refs["input"].setFocus()
    pass

def mounted(self):
    # ✅ Good: Refs available now
    if "input" in self.refs:
        self.refs["input"].setFocus()
```

### 3. Use Refs Sparingly

Prefer declarative patterns over imperative ref manipulation:

```python
# ❌ Less ideal: Imperative with refs
def update_label(self):
    if "label" in self.refs:
        self.refs["label"].setText(f"Count: {self.state['count']}")

# ✅ Better: Declarative with state
# Template: <label :text="f'Count: {count}'" />
```

### 4. Clean Up Ref-Related Resources

If you store refs or use them with external libraries:

```python
def mounted(self):
    if "canvas" in self.refs:
        self.chart = ExternalChart(self.refs["canvas"])

def before_unmount(self):
    # Clean up external resources
    if hasattr(self, 'chart'):
        self.chart.destroy()
```

### 5. Document Refs in Public Components

If your component expects parent components to call methods via refs:

```python
class DataTable(cg.Component):
    """
    Data table component.

    Public Methods (accessible via ref):
        - refresh(): Reload table data
        - sort(column): Sort table by column
        - export_csv(): Export table to CSV

    Example:
        <DataTable ref="table" />

        # In parent:
        self.refs["table"].refresh()
    """

    def refresh(self):
        """Public method: Reload data"""
        self.load_data()

    def sort(self, column):
        """Public method: Sort by column"""
        self.state["sort_column"] = column
        self.apply_sort()
```

### 6. Use Descriptive Ref Names

Choose clear, meaningful ref names:

```python
# ✅ Good: Clear and descriptive
<input ref="emailInput" />
<button ref="submitButton" />
<DataGrid ref="userDataGrid" />

# ❌ Less clear: Too generic
<input ref="input1" />
<button ref="btn" />
<DataGrid ref="grid" />
```

## See Also

- [Components](components.md)
- [Lifecycle Hooks](lifecycle.md)
