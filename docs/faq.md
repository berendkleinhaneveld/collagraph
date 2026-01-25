# Frequently Asked Questions

Common questions and answers about Collagraph.

## General

### What is Collagraph?
Collagraph is a Python framework for building reactive user interfaces, inspired by Vue.js. It allows you to write declarative UI code using Vue-like template syntax, component classes, or render functions. The framework provides automatic reactivity through the `observ` library, meaning your UI updates automatically when state changes.

### How is it different from other Python UI frameworks?
Collagraph stands out from traditional Python UI frameworks in several ways:

- **Declarative Syntax**: Write UI code in a Vue-like template syntax rather than imperative code. This makes your UI logic more readable and maintainable.
- **Automatic Reactivity**: State changes automatically trigger UI updates. No need to manually call update methods or manage event listeners.
- **Single-File Components**: Keep your template and logic together in `.cgx` files, similar to Vue's `.vue` files.
- **Renderer Abstraction**: The same component code can work with different renderers (PySide6, PyGfx, or custom renderers).
- **Vue-Inspired Features**: Familiar concepts like directives (`v-if`, `v-for`, `v-bind`, `v-on`), computed properties, watchers, and lifecycle hooks.
- **Python-Native**: Despite the Vue-like syntax, everything is pure Python under the hood with Python expressions in templates.

Unlike frameworks like PyQt/PySide where you write imperative code, or frameworks like Kivy/Toga with their own DSLs, Collagraph combines the best of both worlds: declarative syntax with Python's full power.

### Can I use it for production applications?
Yes, Collagraph can be used for production applications, but consider the following:

**Stability**: The framework is actively developed and used in real projects. However, as evidenced by frequent releases and improvements, the API may still evolve. Pin your version dependencies carefully.

**Production Use Cases**:
- Internal tools and utilities
- Desktop applications with PySide6
- 3D visualization tools with PyGfx
- Prototyping and MVPs

**Considerations**:
- The framework is maintained by a small team, so community support is more limited than larger frameworks
- Test your application thoroughly, especially around reactivity and state management
- Review release notes when upgrading, as there may be breaking changes
- Consider contributing back if you find issues or need features

If you're building mission-critical software with long-term support requirements, evaluate whether the benefits of Collagraph's reactive paradigm outweigh the risks of a younger framework.

## Technical

### How does reactivity work?
Collagraph uses the `observ` library to provide automatic reactivity:

1. **Observable State**: When you assign values to `self.state`, they become observable through the `observ` library
2. **Dependency Tracking**: During rendering, Collagraph tracks which state values each part of the UI depends on
3. **Automatic Updates**: When state changes, Collagraph detects the change and schedules a re-render
4. **Fine-Grained Updates**: Only the parts of the UI that depend on changed state are updated

```python
class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0  # Observable state

    def increment(self):
        self.state["count"] += 1  # Change triggers re-render
```

The reactivity system is "deep" by default, meaning changes to nested objects and arrays are also tracked:

```python
self.state["user"]["name"] = "Alice"  # Nested change detected
self.state["items"].append("new")      # List mutation detected
```

Under the hood, this is powered by the `observ` library's proxy-based reactivity system, similar to Vue 3's reactivity. For more details, see the [Reactivity System](core-concepts/reactivity.md) documentation.

### Can I mix Collagraph with regular PySide code?
Yes! Collagraph components integrate seamlessly with regular PySide6 code:

**Using PySide widgets in Collagraph**:
```python
# You can mount Collagraph components into existing PySide widgets
app = QtWidgets.QApplication()
main_window = QtWidgets.QMainWindow()  # Regular PySide
container = QtWidgets.QWidget()

gui = cg.Collagraph(renderer=cg.PySideRenderer())
gui.render(MyComponent, container)  # Mount into PySide widget
main_window.setCentralWidget(container)
```

**Accessing the underlying Qt widget**:
```python
# In your component, you can access template refs to get Qt widgets
def init(self):
    pass

def mounted(self):
    # Access the actual Qt widget
    qt_widget = self.refs["myButton"]
    qt_widget.setStyleSheet("background-color: blue;")
```

**Custom widget registration**:
You can register custom PySide widgets to use them in templates:
```python
renderer = cg.PySideRenderer()
renderer.register_widget("custom-widget", MyCustomQtWidget)
```

This makes it easy to gradually adopt Collagraph in existing PySide applications or use specialized Qt widgets when needed.

### Does it support async/await?
Collagraph has limited async/await support. The framework itself is synchronous, as it's built on top of Qt's synchronous event loop (for PySide) or similar synchronous rendering systems.

**What works**:
- You can define `async` methods in your components
- You can use `asyncio` for background tasks
- Qt's async support (through libraries like qasync) can be integrated

**What requires extra work**:
- Event handlers are called synchronously by default
- You need to manually integrate async event loops
- Lifecycle hooks are synchronous

**Example with background tasks**:
```python
import asyncio

class DataLoader(cg.Component):
    def init(self):
        self.state["data"] = None
        self.state["loading"] = False

    def load_data(self):
        self.state["loading"] = True
        # Run async task
        asyncio.create_task(self._fetch_data())

    async def _fetch_data(self):
        data = await some_async_api_call()
        self.state["data"] = data
        self.state["loading"] = False
```

For better async integration with Qt, consider using libraries like [qasync](https://github.com/CabbageDevelopment/qasync).

### What Python versions are supported?
Python 3.10 or higher is required. The framework takes advantage of modern Python features like pattern matching and improved type hints.

## See Also

- [Troubleshooting](troubleshooting.md)
- [Getting Started](getting-started/installation.md)
