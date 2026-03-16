# Integrating with PySide Applications

This guide shows how to integrate Collagraph into existing PySide/Qt applications and mix Collagraph components with traditional Qt code.

## Overview

Collagraph can be used in three ways with PySide:

1. **Pure Collagraph** - Build entire app with Collagraph
2. **Hybrid** - Mix Collagraph components with Qt widgets
3. **Embedded** - Embed Collagraph in existing Qt app

This guide focuses on scenarios 2 and 3.

## Basic Integration

### Rendering Collagraph Component in Qt Window

```python
from PySide6 import QtWidgets
import collagraph as cg

# Create Qt application
app = QtWidgets.QApplication()

# Create main window
window = QtWidgets.QMainWindow()
window.setWindowTitle("Collagraph + Qt")
window.resize(800, 600)

# Create central widget
central_widget = QtWidgets.QWidget()
window.setCentralWidget(central_widget)

# Create layout
layout = QtWidgets.QVBoxLayout(central_widget)

# Render Collagraph component into layout
gui = cg.Collagraph(renderer=cg.PySideRenderer())

from my_component import MyComponent
component_widget = gui.render(MyComponent, layout)

# Show window
window.show()
app.exec()
```

### Embedding in Existing Application

```python
class ExistingApp(QtWidgets.QMainWindow):
    """Existing Qt application"""

    def __init__(self):
        super().__init__()

        # Existing Qt UI setup
        self.setup_menu_bar()
        self.setup_toolbar()

        # Create central widget with layout
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        # Add traditional Qt widgets
        layout.addWidget(QtWidgets.QLabel("Traditional Qt Label"))

        # Add Collagraph component
        self.add_collagraph_component(layout)

        # Add more Qt widgets
        layout.addWidget(QtWidgets.QPushButton("Traditional Qt Button"))

    def add_collagraph_component(self, layout):
        """Add Collagraph component to layout"""
        gui = cg.Collagraph(renderer=cg.PySideRenderer())

        from components.dashboard import Dashboard
        self.dashboard = gui.render(Dashboard, layout, props={
            "user_id": self.current_user_id
        })
```

## Accessing Qt Widgets from Collagraph

### Using Template Refs

Access the underlying Qt widget:

```html
<widget>
  <lineedit ref="myInput" placeholder-text="Enter text" />
  <button text="Focus Input" @clicked="focus_input" />
</widget>

<script>
import collagraph as cg

class MyComponent(cg.Component):
    def focus_input(self):
        """Focus the Qt widget directly"""
        if "myInput" in self.refs:
            qt_widget = self.refs["myInput"]

            # Call Qt methods
            qt_widget.setFocus()
            qt_widget.selectAll()
</script>
```

### Accessing Component Root Element

```python
class MyComponent(cg.Component):
    def mounted(self):
        """Access root Qt widget"""
        # self.element is the root Qt widget
        root_widget = self.element

        # Modify Qt properties
        root_widget.setStyleSheet("background-color: #f0f0f0;")
        root_widget.setMinimumSize(400, 300)
```

### Direct Qt API Usage

```html
<treewidget ref="tree" object-name="my-tree">
  <treewidgetitem
    v-for="item in items"
    :content="{0: item['name']}"
  />
</treewidget>

<script>
import collagraph as cg
from PySide6 import QtWidgets

class TreeComponent(cg.Component):
    def mounted(self):
        """Configure tree widget using Qt API"""
        if "tree" in self.refs:
            tree = self.refs["tree"]

            # Use Qt API
            tree.setColumnCount(1)
            tree.setHeaderLabels(["Name"])
            tree.setAlternatingRowColors(True)
            tree.setSortingEnabled(True)

            # Connect Qt signals
            tree.itemClicked.connect(self.on_item_clicked)

    def on_item_clicked(self, item, column):
        """Handle Qt signal"""
        print(f"Clicked: {item.text(column)}")
</script>
```

## Mixing Collagraph and Qt Code

### Qt Widget in Collagraph Component

Create custom Qt widget and use it in Collagraph:

**custom_widget.py:**
```python
from PySide6 import QtWidgets, QtCore

class CustomColorPicker(QtWidgets.QWidget):
    """Custom Qt widget"""

    color_changed = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QHBoxLayout(self)

        self.color_display = QtWidgets.QLabel()
        self.color_display.setFixedSize(50, 50)
        self.color_display.setStyleSheet("background-color: red;")

        self.button = QtWidgets.QPushButton("Pick Color")
        self.button.clicked.connect(self.pick_color)

        layout.addWidget(self.color_display)
        layout.addWidget(self.button)

        self.current_color = "red"

    def pick_color(self):
        from PySide6.QtWidgets import QColorDialog

        color = QColorDialog.getColor()
        if color.isValid():
            color_name = color.name()
            self.current_color = color_name
            self.color_display.setStyleSheet(f"background-color: {color_name};")
            self.color_changed.emit(color_name)
```

**Use in Collagraph:**
```html
<widget>
  <label :text="f'Selected color: {color}'" />
  <!-- Note: Can't use custom Qt widgets directly in template -->
  <!-- Must add programmatically -->
</widget>

<script>
import collagraph as cg
from custom_widget import CustomColorPicker

class MyComponent(cg.Component):
    def init(self):
        self.state["color"] = "red"
        self.color_picker = None

    def mounted(self):
        """Add custom Qt widget after mounting"""
        if self.element:
            # Create custom widget
            self.color_picker = CustomColorPicker()
            self.color_picker.color_changed.connect(self.on_color_changed)

            # Add to layout
            layout = self.element.layout()
            if layout:
                layout.addWidget(self.color_picker)

    def on_color_changed(self, color):
        """Handle custom widget signal"""
        self.state["color"] = color

    def before_unmount(self):
        """Clean up"""
        if self.color_picker:
            self.color_picker.deleteLater()
</script>
```

### Collagraph Component as Qt Widget

Wrap Collagraph component for use in Qt code:

```python
from PySide6 import QtWidgets
import collagraph as cg

class CollagraphWidget(QtWidgets.QWidget):
    """Wrapper to use Collagraph component as Qt widget"""

    def __init__(self, component_class, props=None, parent=None):
        super().__init__(parent)

        # Create layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Render Collagraph component
        self.gui = cg.Collagraph(renderer=cg.PySideRenderer())
        self.component = self.gui.render(
            component_class,
            layout,
            props=props or {}
        )

# Use it in traditional Qt code
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Use Collagraph component as regular Qt widget
        from components.user_list import UserList

        self.user_list_widget = CollagraphWidget(
            UserList,
            props={"filter": "active"}
        )

        self.setCentralWidget(self.user_list_widget)
```

## Event Handling Between Systems

### Collagraph to Qt

Emit events from Collagraph, handle in Qt:

**Collagraph component:**
```html
<widget>
  <button text="Save" @clicked="handle_save" />
</widget>

<script>
import collagraph as cg

class SaveButton(cg.Component):
    def handle_save(self):
        # Emit event
        self.emit("save-requested", {"data": "value"})
</script>
```

**Qt parent:**
```python
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Render Collagraph component
        gui = cg.Collagraph(renderer=cg.PySideRenderer())

        from components.save_button import SaveButton

        # Get component instance to listen to events
        self.save_component = SaveButton()

        # Connect to Collagraph event
        # Note: This requires exposing component instance
        # Better to use provide/inject or global state
```

**Better approach - use callbacks:**
```python
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        gui = cg.Collagraph(renderer=cg.PySideRenderer())

        from components.save_button import SaveButton

        # Pass Qt callback as prop
        widget = gui.render(SaveButton, central_layout, props={
            "on_save": self.handle_save
        })

    def handle_save(self, data):
        """Handle save from Collagraph"""
        print(f"Save requested: {data}")
        # Handle in Qt
```

### Qt to Collagraph

Pass data from Qt to Collagraph via props:

```python
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Traditional Qt controls
        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems(["All", "Active", "Inactive"])
        self.filter_combo.currentTextChanged.connect(self.update_filter)

        # Collagraph component
        from components.data_table import DataTable

        self.gui = cg.Collagraph(renderer=cg.PySideRenderer())
        self.table_state = {"filter": "All"}

        self.table = self.gui.render(
            DataTable,
            layout,
            props=self.table_state
        )

    def update_filter(self, filter_text):
        """Update filter from Qt combo box"""
        # Update props and re-render
        self.table_state["filter"] = filter_text
        # Re-render component with new props
        self.gui.render(DataTable, layout, props=self.table_state)
```

## Sharing State Between Qt and Collagraph

### Using Reactive State

```python
from observ import reactive
from PySide6 import QtCore

# Create shared reactive state
shared_state = reactive({
    "user": None,
    "selection": []
})

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Provide shared state to Collagraph
        gui = cg.Collagraph(renderer=cg.PySideRenderer())

        from components.user_panel import UserPanel

        gui.render(UserPanel, layout, state=shared_state)

        # Qt widget can also access/modify shared state
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.itemSelectionChanged.connect(
            self.on_selection_changed
        )

    def on_selection_changed(self):
        """Update shared state from Qt widget"""
        selected_items = [
            item.text()
            for item in self.list_widget.selectedItems()
        ]
        shared_state["selection"] = selected_items
```

## Using Qt Dialogs

### Showing Qt Dialog from Collagraph

```html
<widget>
  <button text="Open Dialog" @clicked="show_dialog" />
  <label :text="f'Selected: {selected}'" />
</widget>

<script>
import collagraph as cg
from PySide6 import QtWidgets

class MyComponent(cg.Component):
    def init(self):
        self.state["selected"] = ""

    def show_dialog(self):
        """Show Qt file dialog"""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.element,
            "Select File",
            "",
            "All Files (*.*)"
        )

        if file_name:
            self.state["selected"] = file_name
</script>
```

### Using Collagraph Dialog in Qt

```python
# Create dialog with Collagraph content
class CollagraphDialog(QtWidgets.QDialog):
    def __init__(self, component_class, props=None, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)

        # Render Collagraph component
        gui = cg.Collagraph(renderer=cg.PySideRenderer())
        self.component = gui.render(
            component_class,
            layout,
            props=props or {}
        )

        # Add buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

# Use it
from components.settings_form import SettingsForm

dialog = CollagraphDialog(SettingsForm, props={"user": current_user})
if dialog.exec():
    # User clicked OK
    pass
```

## Styling and Theming

### Apply Qt Stylesheet to Collagraph

```python
app = QtWidgets.QApplication()

# Apply stylesheet to entire app (including Collagraph)
app.setStyleSheet("""
    QWidget {
        font-size: 12pt;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 8px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")

# Render Collagraph component - inherits styles
gui = cg.Collagraph(renderer=cg.PySideRenderer())
gui.render(MyComponent, container)
```

### Per-Component Styling

```html
<widget :style-sheet="'background-color: #f5f5f5; padding: 10px;'">
  <button
    text="Styled Button"
    :style-sheet="'background-color: blue; color: white;'"
  />
</widget>
```

## Best Practices

### 1. Use Template Refs for Qt Access

```python
# Good: Use refs
def mounted(self):
    if "myWidget" in self.refs:
        qt_widget = self.refs["myWidget"]
        qt_widget.setFocus()

# Less ideal: Search for widget
def mounted(self):
    widget = self.element.findChild(QtWidgets.QLineEdit)
```

### 2. Clean Up Qt Resources

```python
def mounted(self):
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.update)
    self.timer.start(1000)

def before_unmount(self):
    # Always clean up
    if self.timer:
        self.timer.stop()
        self.timer.deleteLater()
```

### 3. Use Signals for Communication

```python
# Good: Use Qt signals
class MyWidget(QtWidgets.QWidget):
    data_changed = QtCore.Signal(dict)

    def update_data(self, data):
        self.data_changed.emit(data)

# In Collagraph
def mounted(self):
    if "customWidget" in self.refs:
        widget = self.refs["customWidget"]
        widget.data_changed.connect(self.handle_data_changed)
```

### 4. Provide Context to Components

```python
# Good: Provide Qt resources
class App(cg.Component):
    def init(self):
        # Provide Qt application for descendants
        self.provide("qt_app", QtWidgets.QApplication.instance())
        self.provide("main_window", self.get_main_window())

class ChildComponent(cg.Component):
    def init(self):
        # Access Qt resources
        self.qt_app = self.inject("qt_app")
        self.main_window = self.inject("main_window")
```

## Complete Integration Example

```python
# main.py
from PySide6 import QtWidgets, QtCore
import collagraph as cg
from observ import reactive

# Shared state between Qt and Collagraph
app_state = reactive({
    "user": None,
    "theme": "light",
    "data": []
})

class HybridApplication(QtWidgets.QMainWindow):
    """Application mixing Qt and Collagraph"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hybrid Qt + Collagraph App")
        self.resize(1200, 800)

        # Setup UI
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_central_widget()
        self.setup_status_bar()

    def setup_menu_bar(self):
        """Traditional Qt menu bar"""
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("New", self.new_file)
        file_menu.addAction("Open", self.open_file)
        file_menu.addAction("Exit", self.close)

    def setup_toolbar(self):
        """Traditional Qt toolbar"""
        toolbar = self.addToolBar("Main")
        toolbar.addAction("Refresh", self.refresh_data)

    def setup_central_widget(self):
        """Central widget with Collagraph component"""
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        splitter = QtWidgets.QSplitter()
        central_layout = QtWidgets.QVBoxLayout(central)
        central_layout.addWidget(splitter)

        # Left: Traditional Qt widget
        self.setup_qt_sidebar(splitter)

        # Right: Collagraph component
        self.setup_collagraph_content(splitter)

    def setup_qt_sidebar(self, splitter):
        """Traditional Qt sidebar"""
        sidebar = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(sidebar)

        layout.addWidget(QtWidgets.QLabel("Qt Sidebar"))

        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems(["All", "Active", "Completed"])
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        layout.addWidget(self.filter_combo)

        layout.addStretch()
        splitter.addWidget(sidebar)

    def setup_collagraph_content(self, splitter):
        """Collagraph content area"""
        content = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(content)

        # Render Collagraph component
        gui = cg.Collagraph(renderer=cg.PySideRenderer())

        from components.dashboard import Dashboard

        self.dashboard = Dashboard()
        gui.render(Dashboard, layout, state=app_state)

        splitter.addWidget(content)

    def setup_status_bar(self):
        """Traditional Qt status bar"""
        self.statusBar().showMessage("Ready")

    def new_file(self):
        """Qt menu action"""
        app_state["data"] = []
        self.statusBar().showMessage("New file created")

    def open_file(self):
        """Qt menu action"""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self)
        if file_name:
            # Load data and update shared state
            app_state["data"] = load_data(file_name)
            self.statusBar().showMessage(f"Opened: {file_name}")

    def refresh_data(self):
        """Toolbar action affecting Collagraph component"""
        # Update shared state - Collagraph component reacts
        app_state["data"] = fetch_fresh_data()
        self.statusBar().showMessage("Data refreshed")

    def on_filter_changed(self, filter_text):
        """Qt combo box affects Collagraph"""
        app_state["filter"] = filter_text.lower()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = HybridApplication()
    window.show()
    app.exec()
```

## See Also

- [PySide Renderer](../renderers/pyside.md)
- [Template Refs](../core-concepts/template-refs.md)
- [Components](../core-concepts/components.md)
- [State Management](../core-concepts/state-management.md)
