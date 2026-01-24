# Troubleshooting

Common problems and their solutions when working with Collagraph.

## Installation Issues

### ImportError: No module named 'collagraph'
Make sure Collagraph is installed:
```bash
pip install collagraph
```

Or if using `uv`:
```bash
uv pip install collagraph
```

### PySide6 not found
Install PySide6 along with Collagraph:
```bash
pip install collagraph[pyside]
```

Or with `uv`:
```bash
uv pip install "collagraph[pyside]"
```

### PyGfx not found
For 3D rendering with PyGfx:
```bash
pip install collagraph[pygfx]
```

### Syntax highlighting not working for .cgx files
Install the appropriate editor extension:

**VSCode**: Search for "CGX" in the extensions marketplace and install [CGX syntax highlight for VSCode](https://github.com/fork-tongue/cgx-syntax-highlight-vscode)

**Sublime Text**: Install via Package Control by searching for "CGX Syntax Highlight" or install from [CGX syntax highlight for Sublime Text](https://github.com/fork-tongue/cgx-syntax-highlight-sublime)

## Runtime Issues

### Component not updating when state changes

This is the most common issue. Here are the typical causes and solutions:

**Problem**: You're modifying non-reactive data
```python
# Wrong: Regular instance variable is not reactive
def init(self):
    self.count = 0

def increment(self):
    self.count += 1  # Won't trigger re-render
```

**Solution**: Use `self.state` for reactive data
```python
# Correct: Use self.state for reactive values
def init(self):
    self.state["count"] = 0

def increment(self):
    self.state["count"] += 1  # Triggers re-render
```

**Problem**: Replacing the entire state dictionary
```python
# Wrong: This breaks reactivity
def reset(self):
    self.state = {}  # Don't replace the state object
```

**Solution**: Modify state properties individually
```python
# Correct: Modify individual properties
def reset(self):
    self.state.clear()
    self.state["count"] = 0
    # Or update in place
    for key in list(self.state.keys()):
        del self.state[key]
```

**Problem**: Mutating objects outside the reactive system
```python
# Potentially problematic
def init(self):
    self.data = {"value": 0}
    self.state["ref"] = self.data

def update(self):
    self.data["value"] = 1  # May not trigger update
```

**Solution**: Always mutate through the reactive state
```python
def init(self):
    self.state["data"] = {"value": 0}

def update(self):
    self.state["data"]["value"] = 1  # Correctly triggers update
```

### Events not firing

**Problem**: Wrong event name in template
```html
<!-- Wrong: 'onclick' is not a valid Qt signal name -->
<button text="Click" @onclick="handle_click" />
```

**Solution**: Use the correct PySide signal name
```html
<!-- Correct: Use 'clicked' for buttons -->
<button text="Click" @clicked="handle_click" />
```

Common Qt signal names:
- `clicked` - for buttons
- `toggled` - for checkboxes
- `textChanged` - for line edits
- `currentIndexChanged` - for combo boxes
- `returnPressed` - for line edits when Enter is pressed

**Problem**: Method doesn't exist or has wrong name
```python
# Template references handle_click
@clicked="handle_click"

# But method is named differently
def handleClick(self):  # Wrong name
    pass
```

**Solution**: Ensure method names match exactly
```python
def handle_click(self):  # Correct
    pass
```

**Problem**: Lambda syntax error
```html
<!-- Wrong: Missing lambda keyword -->
<button @clicked="toggle_item(idx)" />
```

**Solution**: Use lambda for parameterized calls
```html
<!-- Correct: Use lambda to pass parameters -->
<button @clicked="lambda: toggle_item(idx)" />
```

### .cgx files not importing

**Problem**: Importing .cgx before importing collagraph
```python
# Wrong: Import order matters
from counter import Counter
import collagraph as cg
```

**Solution**: Import collagraph first
```python
# Correct: Import collagraph first to register .cgx import hook
import collagraph as cg
from counter import Counter
```

**Problem**: .cgx file not in Python path
```
project/
├── main.py
└── subdir/
    └── counter.cgx
```

**Solution**: Ensure the .cgx file location is importable or adjust Python path
```python
# Option 1: Add __init__.py to make it a package
# Option 2: Adjust sys.path
import sys
sys.path.append("subdir")

# Option 3: Use relative paths if in a package
from .subdir.counter import Counter
```

**Problem**: Syntax error in .cgx file
```html
<!-- Invalid template syntax or Python syntax in script -->
<widget>
  <button text="Click" @clicked=handle_click" />  <!-- Missing opening quote -->
</widget>
```

**Solution**: Check for syntax errors. Common issues:
- Missing quotes in attributes
- Unclosed tags
- Invalid Python syntax in `<script>` section
- Missing `<script>` closing tag

### Template syntax errors

**Problem**: Using Python f-strings incorrectly
```html
<!-- Wrong: Can't use f-string in attribute value directly -->
<label text=f"Count: {count}" />
```

**Solution**: Use `:text` binding with f-string
```html
<!-- Correct: Use v-bind (:) for dynamic values -->
<label :text="f'Count: {count}'" />
```

**Problem**: Accessing props incorrectly
```html
<!-- Wrong: props is a dict, not attributes -->
<label :text="props.name" />
```

**Solution**: Access props as dictionary
```html
<!-- Correct: Use dictionary access -->
<label :text="props['name']" />
<!-- Or use .get() for optional props -->
<label :text="props.get('name', 'Default')" />
```

## Performance Issues

### Slow rendering

**Problem**: Too many components re-rendering
```python
# Every state change re-renders entire tree
def init(self):
    self.state["global_data"] = huge_list
```

**Solution**: Split into smaller components
```python
# Break down into smaller components that only re-render what changed
class ListItem(cg.Component):
    # Only re-renders when its props change
    pass

class ListView(cg.Component):
    # Uses ListItem for each item
    pass
```

**Problem**: Expensive computations in render
```html
<label :text="f'Result: {expensive_calculation()}'" />
```

**Solution**: Use computed properties
```python
from observ import computed

def init(self):
    self.state["input_data"] = []
    # Computed property caches result
    self.result = computed(lambda: expensive_calculation(self.state["input_data"]))
```

**Problem**: Large lists without keys
```html
<!-- No key attribute for list items -->
<div v-for="item in items">
  <label :text="item['name']" />
</div>
```

**Solution**: Use keys for efficient reconciliation
```html
<!-- With key for efficient updates -->
<div v-for="item in items" :key="item['id']">
  <label :text="item['name']" />
</div>
```

### High memory usage

**Problem**: Not cleaning up watchers or computed properties
```python
def on_mounted(self):
    # Creating watchers without cleanup
    watch(lambda: self.state["data"], self.handle_change)
```

**Solution**: Clean up in unmount hook
```python
def on_mounted(self):
    self._watcher = watch(lambda: self.state["data"], self.handle_change)

def on_unmounted(self):
    # Clean up watcher
    if hasattr(self, "_watcher"):
        self._watcher()  # Call the cleanup function
```

**Problem**: Storing large objects in reactive state unnecessarily
```python
def init(self):
    # Large non-UI data stored reactively
    self.state["huge_dataset"] = load_huge_data()
```

**Solution**: Only make UI-relevant data reactive
```python
def init(self):
    # Store large data as regular instance variable
    self.huge_dataset = load_huge_data()
    # Only reactive state for UI
    self.state["filtered_count"] = len(self.huge_dataset)
```

### Signals firing unexpectedly in PySide

**Problem**: Signal loops causing infinite updates

This has been addressed in recent versions (0.8.8+) with automatic signal blocking, but if you're on an older version or experiencing issues:

**Solution**: Upgrade to the latest version
```bash
pip install --upgrade collagraph
```

The PySide renderer now automatically blocks signals when setting attributes directly to prevent unwanted signal triggers.

## Debugging Tips

### Enable verbose logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check component state
```python
def on_mounted(self):
    print(f"Component state: {dict(self.state)}")
    print(f"Component props: {self.props}")
```

### Verify template refs
```python
def on_mounted(self):
    print(f"Available refs: {list(self.refs.keys())}")
```

### Use the render method directly
Instead of using .cgx files, try using the render method to isolate issues:
```python
class MyComponent(cg.Component):
    def render(self):
        return {
            "type": "label",
            "text": f"Count: {self.state['count']}"
        }
```

## See Also

- [FAQ](faq.md)
- [Debugging Guide](guides/debugging.md)
