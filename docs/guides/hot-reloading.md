# Hot Reloading

This guide covers hot reloading in Collagraph - a powerful development feature that automatically updates your application when you change code, without losing application state.

## Overview

Hot reloading watches your component files and automatically reloads them when changes are detected. This enables a fast development workflow:

1. Edit a component file
2. Save the file
3. See changes instantly in the running application
4. Application state is preserved (where possible)

## Enabling Hot Reloading

### Using the CLI

The easiest way to enable hot reloading is with the Collagraph CLI:

```bash
# Note: Hot reloading is enabled by default when using the CLI
python -m collagraph app.cgx
```

or with uv:

```bash
uv run collagraph app.cgx
```

The CLI automatically watches for file changes and reloads components.

### Manual Setup (Programmatic)

For custom applications, you can implement hot reloading manually:

```python
from PySide6 import QtWidgets
import collagraph as cg
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib
import sys

class HotReloadHandler(FileSystemEventHandler):
    """Handle file changes for hot reloading"""

    def __init__(self, gui, component_class, container):
        self.gui = gui
        self.component_class = component_class
        self.container = container
        self.module_name = component_class.__module__

    def on_modified(self, event):
        """Called when a file is modified"""
        if not event.is_directory and event.src_path.endswith('.cgx'):
            print(f"Reloading {event.src_path}...")

            # Reload the module
            if self.module_name in sys.modules:
                importlib.reload(sys.modules[self.module_name])

                # Re-render component
                self.gui.render(self.component_class, self.container)


# Setup hot reloading
app = QtWidgets.QApplication()
gui = cg.Collagraph(renderer=cg.PySideRenderer())
container = app

from app import App

gui.render(App, container)

# Start file watcher
event_handler = HotReloadHandler(gui, App, container)
observer = Observer()
observer.schedule(event_handler, path=".", recursive=True)
observer.start()

app.exec()

# Cleanup
observer.stop()
observer.join()
```

Install watchdog for file watching:

```bash
pip install watchdog
```

## How Hot Reloading Works

### File Watching

Hot reloading uses file system watchers to detect changes to `.cgx` files:

1. **File watcher** monitors the directory for changes
2. **Detect change** when a `.cgx` file is modified
3. **Reload module** reimport the Python module
4. **Re-render** render the component with updated code
5. **Preserve state** maintain existing state where possible

### Module Reloading

When a file changes:

```python
# Before reload
from counter import Counter  # Original version

# File is modified

# After reload
import importlib
import sys

# Reload the module
if 'counter' in sys.modules:
    importlib.reload(sys.modules['counter'])

# Counter now has the updated code
```

### Component Re-rendering

The component is re-rendered with the updated code:

```python
# Previous component instance is unmounted
# New component instance is created with updated code
# State can be preserved if implemented
```

## State Preservation

### Default Behavior

By default, hot reloading **does not** preserve component state - the component is fully re-initialized. This means:

- `init()` is called again
- State starts from scratch
- Props are re-applied

**Example - State is lost:**

```html
<!-- counter.cgx -->
<widget>
  <label :text="f'Count: {count}'" />
  <button text="+" @clicked="increment" />
</widget>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0  # Resets to 0 on reload

    def increment(self):
        self.state["count"] += 1
</script>
```

If you increment to 5 and then modify the file, count resets to 0.

### Preserving State (Advanced)

To preserve state across reloads, you can use a global state store:

```python
# state_store.py
from observ import reactive

# Global state that persists across reloads
persistent_state = reactive({
    "counter": 0
})
```

```html
<!-- counter.cgx -->
<widget>
  <label :text="f'Count: {count}'" />
  <button text="+" @clicked="increment" />
</widget>

<script>
import collagraph as cg
from state_store import persistent_state

class Counter(cg.Component):
    def init(self):
        # Use persistent state instead of local state
        self.state["count"] = persistent_state["counter"]

    def increment(self):
        self.state["count"] += 1
        persistent_state["counter"] = self.state["count"]
</script>
```

Now the count persists across hot reloads!

## Development Workflow

### Typical Development Cycle

1. **Start application** with hot reloading:
   ```bash
   uv run collagraph app.cgx
   ```

2. **Make changes** to components in your editor

3. **Save file** - changes automatically reload

4. **See updates** instantly in the running app

5. **Iterate** quickly without manual restarts

### Best Practices for Hot Reloading

**1. Save frequently** - Changes only take effect when you save

**2. Watch console** - Look for reload messages and errors:
```
Reloading /path/to/component.cgx...
✓ Reload successful
```

**3. Keep components small** - Smaller components reload faster

**4. Use global state** - For state you want to preserve

**5. Test edge cases** - Sometimes hot reload behaves differently than cold start

## Limitations

### What Works

✅ **Component template changes** - Modify HTML structure
✅ **Component logic changes** - Update methods, computed properties
✅ **Style changes** - Update style-sheet attributes
✅ **New components** - Add new component files
✅ **Import changes** - Add/remove imports

### What Doesn't Work

❌ **State preservation** - Local state resets (unless using global state)
❌ **Active event handlers** - Need to be re-registered
❌ **Third-party library changes** - External modules aren't reloaded
❌ **Configuration changes** - App-level config requires restart

### Edge Cases

**Syntax Errors:**
```python
# If you save invalid Python code:
def increment(self)
    # Missing colon and body
```

The reload will fail and show an error. Fix the syntax and save again.

**Import Errors:**
```python
# If you import something that doesn't exist:
from nonexistent_module import Foo
```

The reload fails. Fix the import and save again.

**Circular Dependencies:**

Hot reloading may fail with circular imports. Restructure to avoid them.

## Debugging Hot Reload Issues

### Reload Not Triggering

**Problem:** Saving file doesn't trigger reload

**Solutions:**
- Check file is in watched directory
- Ensure file has `.cgx` extension
- Look for file watcher errors in console
- Try restarting the application

### Reload Fails

**Problem:** Reload triggers but fails with error

**Solutions:**
- Check console for syntax errors
- Verify all imports are valid
- Fix any Python errors
- Ensure component class exists

### Changes Not Visible

**Problem:** Reload succeeds but changes not visible

**Solutions:**
- Check the right component is being edited
- Clear browser cache (if using web renderer)
- Ensure component is actually rendered
- Check if change is in dead code

### State Lost

**Problem:** Component state resets on reload

**Solutions:**
- This is expected behavior
- Use global state for persistence
- Document initial state clearly

## Example: Hot Reload Workflow

Let's walk through a typical hot reload development session:

**1. Start with basic counter:**

```html
<!-- counter.cgx -->
<widget>
  <label :text="f'Count: {count}'" />
  <button text="Increment" @clicked="increment" />
</widget>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1
</script>
```

**2. Run with hot reload:**

```bash
uv run collagraph counter.cgx
```

**3. Click button a few times → count is 5**

**4. Add a decrement button:**

```html
<!-- Add this line -->
<button text="Decrement" @clicked="decrement" />
```

```python
# Add this method
def decrement(self):
    self.state["count"] -= 1
```

**5. Save file → Component reloads → Count resets to 0**

**6. Add persistent state:**

```python
# state_store.py
from observ import reactive
persistent = reactive({"count": 0})
```

```html
<!-- counter.cgx - updated -->
<script>
import collagraph as cg
from state_store import persistent

class Counter(cg.Component):
    def init(self):
        self.state["count"] = persistent["count"]

    def increment(self):
        self.state["count"] += 1
        persistent["count"] = self.state["count"]

    def decrement(self):
        self.state["count"] -= 1
        persistent["count"] = self.state["count"]
</script>
```

**7. Save → Reload → Count preserved at 5!**

**8. Continue iterating with preserved state**

## Production Considerations

### Disable Hot Reloading in Production

Hot reloading should only be used in development:

```python
import os

# Determine if in development
IS_DEV = os.getenv("ENV") == "development"

if IS_DEV:
    # Enable hot reloading
    setup_hot_reload()
else:
    # Production - no hot reload
    run_app()
```

### Performance Impact

Hot reloading has minimal performance impact:
- File watching uses minimal CPU
- Reloads only happen on file changes
- No impact on production (when disabled)

## Advanced: Custom Hot Reload

### Selective Reloading

Reload only specific components:

```python
class SelectiveReloadHandler(FileSystemEventHandler):
    def __init__(self, reload_map):
        self.reload_map = reload_map  # {file_path: component_class}

    def on_modified(self, event):
        if event.src_path in self.reload_map:
            component = self.reload_map[event.src_path]
            reload_component(component)
```

### State Migration

Implement custom state migration:

```python
class StatefulComponent(cg.Component):
    # Class variable to store state across reloads
    _preserved_state = {}

    def init(self):
        # Restore state if available
        if self.__class__._preserved_state:
            self.state.update(self.__class__._preserved_state)
        else:
            # Initialize fresh
            self.state["count"] = 0

    def before_unmount(self):
        # Save state before reload
        self.__class__._preserved_state = dict(self.state)
```

## See Also

- [CLI](../api-reference/cli.md)
- [Components](../core-concepts/components.md)
- [State Management](../core-concepts/state-management.md)
- [Debugging](debugging.md)
