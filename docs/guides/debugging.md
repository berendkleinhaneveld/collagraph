# Debugging

This guide covers debugging techniques for Collagraph applications, from simple print statements to advanced debugging tools.

## Common Errors and Solutions

### ImportError: Cannot import component

**Error:**
```
ImportError: cannot import name 'MyComponent' from 'my_component'
```

**Causes:**
- Component file doesn't exist
- Component class name doesn't match
- File not in Python path

**Solutions:**
```python
# Check file exists
# my_component.cgx

# Check class name matches
class MyComponent(cg.Component):  # Must match import
    pass

# Check import path
from my_component import MyComponent  # File: my_component.cgx
```

### AttributeError: Component has no attribute 'state'

**Error:**
```
AttributeError: 'MyComponent' object has no attribute 'state'
```

**Cause:**
- Trying to access `self.state` in `__init__()` instead of `init()`

**Solution:**
```python
# Wrong
class MyComponent(cg.Component):
    def __init__(self):
        super().__init__()
        self.state["value"] = 0  # State not ready yet!

# Correct
class MyComponent(cg.Component):
    def init(self):
        self.state["value"] = 0  # Use init() hook
```

### ReadonlyError: Cannot modify props

**Error:**
```
ReadonlyError: Cannot modify readonly dict
```

**Cause:**
- Trying to modify `self.props`

**Solution:**
```python
# Wrong
def init(self):
    self.props["value"] = 10  # Props are read-only!

# Correct
def init(self):
    # Copy to state if you need to modify
    self.state["value"] = self.props.get("value", 0)
```

### Template Syntax Errors

**Error:**
```
SyntaxError: invalid syntax in template
```

**Causes:**
- Missing closing tags
- Invalid Python expressions
- Incorrect attribute syntax

**Solutions:**
```html
<!-- Wrong: Missing closing tag -->
<widget>
  <label text="Hello" />

<!-- Correct -->
<widget>
  <label text="Hello" />
</widget>

<!-- Wrong: Invalid expression -->
<label :text="count + " />

<!-- Correct -->
<label :text="f'Count: {count}'" />
```

## Using Print/Logging

### Basic Print Debugging

```python
class MyComponent(cg.Component):
    def init(self):
        print("Component initialized")
        print(f"Props: {self.props}")
        self.state["count"] = 0

    def increment(self):
        print(f"Before: {self.state['count']}")
        self.state["count"] += 1
        print(f"After: {self.state['count']}")
```

### Logging Module

```python
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MyComponent(cg.Component):
    def init(self):
        logger.debug(f"Initializing {self.__class__.__name__}")
        self.state["data"] = []

    def load_data(self):
        logger.info("Loading data...")
        try:
            data = fetch_data()
            self.state["data"] = data
            logger.info(f"Loaded {len(data)} items")
        except Exception as e:
            logger.error(f"Failed to load data: {e}", exc_info=True)
```

### Logging Helper Mixin

```python
import logging

class LoggingMixin:
    """Mixin for logging component lifecycle"""

    @property
    def logger(self):
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger

    def init(self):
        self.logger.debug(f"init() - props: {self.props}")
        super().init() if hasattr(super(), 'init') else None

    def mounted(self):
        self.logger.debug("mounted()")
        super().mounted() if hasattr(super(), 'mounted') else None

    def updated(self):
        self.logger.debug("updated()")
        super().updated() if hasattr(super(), 'updated') else None

    def before_unmount(self):
        self.logger.debug("before_unmount()")
        super().before_unmount() if hasattr(super(), 'before_unmount') else None


class MyComponent(LoggingMixin, cg.Component):
    def init(self):
        super().init()
        self.logger.info("Component ready")
        self.state["value"] = 0
```

## Python Debugger (pdb)

### Using pdb

```python
import pdb

class MyComponent(cg.Component):
    def handle_click(self):
        # Set breakpoint
        pdb.set_trace()

        # Code execution stops here
        # Use pdb commands:
        # n - next line
        # s - step into
        # c - continue
        # p variable - print variable
        # l - list code
        # q - quit

        self.state["count"] += 1
```

### Breakpoint() (Python 3.7+)

```python
class MyComponent(cg.Component):
    def complex_calculation(self):
        data = self.state["data"]

        # Modern way to set breakpoint
        breakpoint()

        result = process_data(data)
        return result
```

### Conditional Breakpoints

```python
class MyComponent(cg.Component):
    def process_item(self, item):
        # Only break for specific items
        if item["id"] == 42:
            breakpoint()

        # Process item
        self.state["items"].append(item)
```

## Inspecting Component State

### State Inspection Utilities

```python
class MyComponent(cg.Component):
    def debug_state(self):
        """Print current component state"""
        print("=== Component State ===")
        print(f"Class: {self.__class__.__name__}")
        print(f"Props: {self.props}")
        print(f"State: {self.state}")
        print(f"Refs: {list(self.refs.keys())}")
        print(f"Parent: {self.parent.__class__.__name__ if self.parent else None}")

    def handle_debug_click(self):
        self.debug_state()
```

### Pretty Print State

```python
import json
from observ import to_raw

class MyComponent(cg.Component):
    def print_state(self):
        """Pretty print state as JSON"""
        # Use to_raw() to get a plain dict without reactive proxies
        print(json.dumps(to_raw(self.state), indent=2, default=str))
```

### State Change Tracking

```python
from observ import watch

class MyComponent(cg.Component):
    def init(self):
        self.state["count"] = 0

        # Track state changes
        self.watchers = {}

    def mounted(self):
        # Watch count changes
        self.watchers["count_debug"] = watch(
            lambda: self.state["count"],
            lambda new, old=None: print(f"count: {old} → {new}")
        )

    def before_unmount(self):
        for watcher in self.watchers.values():
            watcher.stop()
```

## Tracking Re-renders

### Render Counter

```python
class MyComponent(cg.Component):
    # Class variable to track renders
    render_count = 0

    def init(self):
        MyComponent.render_count = 0
        self.state["value"] = 0

    def updated(self):
        MyComponent.render_count += 1
        print(f"Render #{MyComponent.render_count}")
```

### Update Tracking

```python
import time
from observ import to_raw

class MyComponent(cg.Component):
    def init(self):
        self.state["data"] = []
        self.update_log = []

    def updated(self):
        """Log what triggered update"""
        import traceback

        # Capture stack trace
        stack = traceback.format_stack()

        self.update_log.append({
            "timestamp": time.time(),
            # Use to_raw() to snapshot state as plain dict
            "state": to_raw(self.state),
            "stack": stack
        })

        # Print latest update
        print(f"Update triggered. State: {self.state}")
```

## Performance Debugging

### Timing Component Operations

```python
import time

class TimedComponent(cg.Component):
    def init(self):
        self.timings = {}

    def time_it(self, name):
        """Context manager for timing operations"""
        class Timer:
            def __init__(self, component, name):
                self.component = component
                self.name = name

            def __enter__(self):
                self.start = time.time()
                return self

            def __exit__(self, *args):
                duration = time.time() - self.start
                self.component.timings[self.name] = duration
                print(f"{self.name}: {duration:.4f}s")

        return Timer(self, name)

    def expensive_operation(self):
        with self.time_it("data_processing"):
            # Simulate expensive operation
            data = self.process_data()
            self.state["data"] = data
```

### Profiling

```python
import cProfile
import pstats

class MyComponent(cg.Component):
    def profile_method(self):
        """Profile this method's performance"""
        profiler = cProfile.Profile()
        profiler.enable()

        # Code to profile
        self.complex_calculation()

        profiler.disable()

        # Print stats
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10
```

## Debugging with DictRenderer

### Inspecting Component Structure

```python
import collagraph as cg
from collagraph.renderers.dict_renderer import format_dict

# Render to dict for inspection
gui = cg.Collagraph(cg.DictRenderer(), event_loop_type=cg.EventLoopType.SYNC)
container = {"type": "root"}

from my_component import MyComponent
gui.render(MyComponent, container)

# Pretty print structure
print(format_dict(container))
```

Output:
```
<root>
  <widget>
    <label text="Hello" />
    <button text="Click" />
  </widget>
</root>
```

### Debugging Event Handlers

```python
# Get component DOM
dom = container["children"][0]

# Check handlers exist
print(f"Handlers: {dom.get('handlers', {}).keys()}")

# Test handler directly
if "clicked" in dom["handlers"]:
    for handler in dom["handlers"]["clicked"]:
        handler()  # Call handler directly
```

## Using Template Refs for Debugging

```html
<widget>
  <lineedit ref="debugInput" />
  <button text="Debug" @clicked="debug_input" />
</widget>

<script>
import collagraph as cg

class MyComponent(cg.Component):
    def debug_input(self):
        """Debug input widget"""
        if "debugInput" in self.refs:
            widget = self.refs["debugInput"]

            # Inspect Qt widget
            print(f"Widget type: {type(widget)}")
            print(f"Text: {widget.text()}")
            print(f"Enabled: {widget.isEnabled()}")
            print(f"Visible: {widget.isVisible()}")

            # Get all properties
            print("\nAll properties:")
            for prop in dir(widget):
                if not prop.startswith('_'):
                    try:
                        value = getattr(widget, prop)
                        if not callable(value):
                            print(f"  {prop}: {value}")
                    except:
                        pass
</script>
```

## Debugging Event Flow

### Event Tracing

```python
class MyComponent(cg.Component):
    def init(self):
        self.state["event_log"] = []

    def log_event(self, event_name, data=None):
        """Log event for debugging"""
        self.state["event_log"].append({
            "event": event_name,
            "data": data,
            "timestamp": time.time()
        })
        print(f"Event: {event_name} - {data}")

    def handle_click(self):
        self.log_event("button_clicked")
        self.state["count"] += 1
        self.log_event("count_updated", self.state["count"])

    def print_event_log(self):
        """Print all logged events"""
        print("=== Event Log ===")
        for event in self.state["event_log"]:
            print(f"{event['timestamp']}: {event['event']} - {event['data']}")
```

## Debugging Tips

### 1. Start Simple

```python
# Add simple print first
def handle_click(self):
    print("Button clicked!")
    self.state["count"] += 1
```

### 2. Check State Regularly

```python
def increment(self):
    print(f"State before: {self.state['count']}")
    self.state["count"] += 1
    print(f"State after: {self.state['count']}")
```

### 3. Use Assertions

```python
def calculate(self):
    result = self.compute_value()

    # Assert expectations
    assert result >= 0, f"Expected positive result, got {result}"
    assert isinstance(result, int), f"Expected int, got {type(result)}"

    self.state["result"] = result
```

### 4. Isolate Problems

```python
# Comment out code to isolate issue
def complex_method(self):
    self.step1()  # Works
    # self.step2()  # Comment out
    # self.step3()  # Comment out

    # Uncomment one at a time to find problem
```

### 5. Check Props

```python
def init(self):
    # Validate props
    required_props = ["user_id", "name"]
    for prop in required_props:
        if prop not in self.props:
            raise ValueError(f"Missing required prop: {prop}")

    # Log props
    print(f"Received props: {dict(self.props)}")
```

## Common Debugging Scenarios

### Component Not Rendering

**Check:**
1. Component imported correctly?
2. Component class defined?
3. Template syntax valid?
4. Component added to parent template?

```python
# Debug rendering
print(f"Component class: {MyComponent}")
print(f"Has render: {hasattr(MyComponent, 'render')}")

# Check DOM output
gui.render(MyComponent, container)
print(f"DOM: {container}")
```

### Event Handler Not Firing

**Check:**
1. Handler method exists?
2. Handler attached in template?
3. Event name correct?
4. Element enabled?

```python
# Check in DictRenderer
dom = container["children"][0]
print(f"Handlers: {dom.get('handlers', {})}")

# Test handler directly
for handler in dom["handlers"]["clicked"]:
    handler()
```

### State Not Updating

**Check:**
1. State initialized in `init()`?
2. State modified correctly?
3. Using reactive assignment?

```python
# Debug state updates
def update_value(self, new_value):
    print(f"Old value: {self.state.get('value')}")

    # Update state
    self.state["value"] = new_value

    print(f"New value: {self.state.get('value')}")
```

## VS Code Debugging

### Launch Configuration

**.vscode/launch.json:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Collagraph App",
            "type": "python",
            "request": "launch",
            "module": "collagraph",
            "args": ["app.cgx"],
            "console": "integratedTerminal"
        }
    ]
}
```

Set breakpoints in VS Code and use F5 to start debugging.

## Best Practices

1. **Start with print statements** - Simple and effective
2. **Use logging for production** - Better than print in real apps
3. **Test in isolation** - Use DictRenderer for unit tests
4. **Check props and state** - Most bugs are data-related
5. **Use breakpoints strategically** - Don't overuse
6. **Keep event logs** - Track what happened
7. **Profile performance** - Measure, don't guess
8. **Read error messages** - They usually tell you what's wrong
9. **Use version control** - Git diff shows what changed
10. **Ask for help** - Don't spend hours stuck

## See Also

- [Testing](testing.md)
- [Hot Reloading](hot-reloading.md)
- [Dict Renderer](../renderers/dict.md)
- [Components](../core-concepts/components.md)
