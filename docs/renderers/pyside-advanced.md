# PySide Advanced Components

This guide covers advanced Qt widgets and features including tree views, item models, menus, toolbars, and dock widgets.

## Tree Views

Tree views display hierarchical data using Qt's Model/View architecture.

### Basic Tree View

```python
import collagraph as cg

class TreeExample(cg.Component):
    def init(self):
        self.state["items"] = [
            {
                "text": "Root 1",
                "children": [
                    {"text": "Child 1.1"},
                    {"text": "Child 1.2"}
                ]
            },
            {
                "text": "Root 2",
                "children": [
                    {"text": "Child 2.1"}
                ]
            }
        ]
        self.state["selected"] = []

    def render(self):
        return {
            "type": "treeview",
            "selection-mode": QtWidgets.QTreeView.ExtendedSelection,
            "children": [
                {
                    "type": Model,
                    "items": self.state["items"],
                    "@item-changed": self.item_changed
                },
                {
                    "type": "itemselectionmodel",
                    "object-name": "selection-model",
                    "@selection-changed": self.selection_changed
                }
            ]
        }

    def item_changed(self, item):
        # Handle item changes
        print(f"Item changed: {item.text()}")

    def selection_changed(self, selected, deselected):
        # Update selected items
        selection_model = self.element.findChild(
            QtCore.QItemSelectionModel,
            "selection-model"
        )
        if selection_model:
            self.state["selected"] = [
                index.row() for index in selection_model.selectedRows()
            ]
```

```xml
<treeview :selection-mode="QtWidgets.QTreeView.ExtendedSelection">
  <Model
    :items="items"
    @item-changed="item_changed"
  />
  <itemselectionmodel
    object-name="selection-model"
    @selection-changed="selection_changed"
  />
</treeview>
```

### Tree View Attributes

- `selection-mode` - Selection mode (SingleSelection, MultiSelection, ExtendedSelection)
- `header-hidden` - Hide column headers (boolean)
- `root-is-decorated` - Show expand/collapse indicators (boolean)
- `uniform-row-heights` - Optimize for uniform heights (boolean)
- `animated` - Animate expand/collapse (boolean)

### Creating a Tree Model Component

```python
import collagraph as cg
from PySide6.QtGui import QStandardItemModel, QStandardItem

class TreeModel(cg.Component):
    def init(self):
        self.state["columns"] = self.props.get("columns", ["text"])
        self.state["items"] = self.props.get("items", [])

    def render(self):
        return {
            "type": "qstandarditemmodel",
            "children": self.render_items(self.state["items"])
        }

    def render_items(self, items):
        result = []
        for item_data in items:
            item_dict = {
                "type": "standarditem",
                "text": item_data.get("text", "")
            }

            # Add children recursively
            if "children" in item_data and item_data["children"]:
                item_dict["children"] = self.render_items(item_data["children"])

            result.append(item_dict)
        return result
```

## Item Models

Item models provide data to views. The most common is `QStandardItemModel`.

### Standard Item Model

```python
{
    "type": "qstandarditemmodel",
    "children": [
        {
            "type": "standarditem",
            "text": "Item 1",
            "checkable": True,
            "checked": True
        },
        {
            "type": "standarditem",
            "text": "Item 2",
            "children": [
                {"type": "standarditem", "text": "Subitem 2.1"}
            ]
        }
    ]
}
```

```xml
<qstandarditemmodel>
  <standarditem text="Item 1" checkable :checked="true" />
  <standarditem text="Item 2">
    <standarditem text="Subitem 2.1" />
  </standarditem>
</qstandarditemmodel>
```

### Standard Item Attributes

- `text` - Item text
- `checkable` - Make item checkable (boolean)
- `checked` - Checked state (boolean)
- `editable` - Allow editing (boolean)
- `enabled` - Item enabled state (boolean)
- `icon` - Item icon (QIcon)

## Tree Widget (Simplified Tree)

For simpler use cases, `QTreeWidget` doesn't require a separate model:

```python
{
    "type": "treewidget",
    "column-count": 2,
    "header-labels": ["Name", "Value"],
    "children": [
        {
            "type": "treewidgetitem",
            "text": ["Root", "100"],
            "children": [
                {"type": "treewidgetitem", "text": ["Child", "50"]}
            ]
        }
    ]
}
```

```xml
<treewidget
    :column-count="2"
    :header-labels="['Name', 'Value']"
>
  <treewidgetitem :text="['Root', '100']">
    <treewidgetitem :text="['Child', '50']" />
  </treewidgetitem>
</treewidget>
```

## Menus and Actions

### Menu Bar

```python
{
    "type": "menubar",
    "children": [
        {
            "type": "menu",
            "title": "File",
            "children": [
                {
                    "type": "action",
                    "text": "New",
                    "shortcut": "Ctrl+N",
                    "@triggered": self.new_file
                },
                {
                    "type": "action",
                    "text": "Open",
                    "shortcut": "Ctrl+O",
                    "@triggered": self.open_file
                },
                {"type": "action", "separator": True},
                {
                    "type": "action",
                    "text": "Exit",
                    "@triggered": self.exit_app
                }
            ]
        },
        {
            "type": "menu",
            "title": "Edit",
            "children": [
                {
                    "type": "action",
                    "text": "Undo",
                    "shortcut": "Ctrl+Z",
                    "enabled": self.can_undo(),
                    "@triggered": self.undo
                },
                {
                    "type": "action",
                    "text": "Redo",
                    "shortcut": "Ctrl+Y",
                    "enabled": self.can_redo(),
                    "@triggered": self.redo
                }
            ]
        }
    ]
}
```

```xml
<menubar>
  <menu title="File">
    <action text="New" shortcut="Ctrl+N" @triggered="new_file" />
    <action text="Open" shortcut="Ctrl+O" @triggered="open_file" />
    <action separator />
    <action text="Exit" @triggered="exit_app" />
  </menu>
  <menu title="Edit">
    <action text="Undo" shortcut="Ctrl+Z" :enabled="can_undo" @triggered="undo" />
    <action text="Redo" shortcut="Ctrl+Y" :enabled="can_redo" @triggered="redo" />
  </menu>
</menubar>
```

### Action Attributes

- `text` - Action text
- `icon` - Action icon (QIcon)
- `shortcut` - Keyboard shortcut (e.g., "Ctrl+S")
- `checkable` - Make action checkable (boolean)
- `checked` - Checked state (boolean)
- `enabled` - Whether action is enabled (boolean)
- `separator` - Make this a separator (boolean)
- `menu` - Submenu (for actions in menus)

### Context Menu

```python
class ContextMenuExample(cg.Component):
    def init(self):
        self.state["context_menu_pos"] = None

    def render(self):
        children = [
            {
                "type": "label",
                "text": "Right-click me",
                "@context-menu": self.show_context_menu
            }
        ]

        if self.state["context_menu_pos"]:
            children.append({
                "type": "menu",
                "children": [
                    {"type": "action", "text": "Copy", "@triggered": self.copy},
                    {"type": "action", "text": "Paste", "@triggered": self.paste}
                ]
            })

        return {"type": "widget", "children": children}

    def show_context_menu(self, pos):
        self.state["context_menu_pos"] = pos
```

## Toolbars

Toolbars contain actions and can be docked around the main window.

```python
{
    "type": "toolbar",
    "window-title": "Main Toolbar",
    "area": QtCore.Qt.TopToolBarArea,
    "movable": True,
    "children": [
        {
            "type": "action",
            "text": "New",
            "icon": QtGui.QIcon("new.png"),
            "@triggered": self.new_file
        },
        {
            "type": "action",
            "text": "Open",
            "icon": QtGui.QIcon("open.png"),
            "@triggered": self.open_file
        },
        {"type": "action", "separator": True},
        {
            "type": "action",
            "text": "Save",
            "icon": QtGui.QIcon("save.png"),
            "@triggered": self.save_file
        }
    ]
}
```

```xml
<toolbar
    window-title="Main Toolbar"
    :area="QtCore.Qt.TopToolBarArea"
    movable
>
  <action text="New" :icon="new_icon" @triggered="new_file" />
  <action text="Open" :icon="open_icon" @triggered="open_file" />
  <action separator />
  <action text="Save" :icon="save_icon" @triggered="save_file" />
</toolbar>
```

### Toolbar Attributes

- `window-title` - Toolbar name
- `area` - Initial area (TopToolBarArea, BottomToolBarArea, LeftToolBarArea, RightToolBarArea)
- `movable` - Allow moving/docking (boolean)
- `floatable` - Allow floating (boolean)
- `icon-size` - Icon size (QSize)

## Status Bar

Status bars show status information at the bottom of windows.

```python
class StatusBarExample(cg.Component):
    def init(self):
        self.state["status"] = "Ready"

    def mounted(self):
        # Access status bar after mount
        if hasattr(self.element, 'statusBar'):
            self.status_bar = self.element.statusBar()

    def render(self):
        return {
            "type": "window",
            "children": [
                {"type": "widget", "children": [...]},
                {"type": "statusbar"}
            ]
        }

    def update_status(self, message):
        self.state["status"] = message
        if hasattr(self, 'status_bar'):
            self.status_bar.showMessage(message, 3000)  # Show for 3 seconds
```

## Dock Widgets

Dock widgets are panels that can be docked around the main window.

```python
{
    "type": "window",
    "children": [
        {
            "type": "dock",
            "window-title": "Properties",
            "area": QtCore.Qt.RightDockWidgetArea,
            "features": QtWidgets.QDockWidget.DockWidgetMovable |
                       QtWidgets.QDockWidget.DockWidgetFloatable,
            "children": [
                {
                    "type": "widget",
                    "children": [
                        {"type": "label", "text": "Properties panel"}
                    ]
                }
            ]
        },
        {
            "type": "widget",
            # Central widget
            "children": [...]
        }
    ]
}
```

```xml
<window title="Docked Application">
  <dock
    window-title="Properties"
    :area="QtCore.Qt.RightDockWidgetArea"
  >
    <widget>
      <label text="Properties panel" />
    </widget>
  </dock>

  <widget>
    <!-- Central widget -->
  </widget>
</window>
```

### Dock Widget Attributes

- `window-title` - Dock widget title
- `area` - Initial dock area (LeftDockWidgetArea, RightDockWidgetArea, TopDockWidgetArea, BottomDockWidgetArea)
- `features` - Allowed features (DockWidgetMovable, DockWidgetFloatable, DockWidgetClosable)
- `floating` - Start as floating window (boolean)

## Complete Advanced Example

```python
import collagraph as cg
from PySide6 import QtCore, QtWidgets

class AdvancedApp(cg.Component):
    def init(self):
        self.state["items"] = [
            {"text": "Project", "children": [
                {"text": "src"},
                {"text": "docs"}
            ]}
        ]
        self.state["selected"] = []
        self.state["show_properties"] = True

    def render(self):
        children = [
            {
                "type": "menubar",
                "children": [
                    {
                        "type": "menu",
                        "title": "View",
                        "children": [
                            {
                                "type": "action",
                                "text": "Properties",
                                "checkable": True,
                                "checked": self.state["show_properties"],
                                "@toggled": lambda c: self.state.update({"show_properties": c})
                            }
                        ]
                    }
                ]
            },
            {
                "type": "toolbar",
                "window-title": "Main",
                "children": [
                    {"type": "action", "text": "Add", "@triggered": self.add_item}
                ]
            }
        ]

        if self.state["show_properties"]:
            children.append({
                "type": "dock",
                "window-title": "Properties",
                "area": QtCore.Qt.RightDockWidgetArea,
                "children": [
                    {
                        "type": "widget",
                        "children": [
                            {"type": "label", "text": f"Selected: {len(self.state['selected'])}"}
                        ]
                    }
                ]
            })

        children.append({
            "type": "widget",
            "children": [
                {
                    "type": "treeview",
                    "children": [
                        {
                            "type": TreeModel,
                            "items": self.state["items"]
                        },
                        {
                            "type": "itemselectionmodel",
                            "@selection-changed": self.selection_changed
                        }
                    ]
                }
            ]
        })

        children.append({"type": "statusbar"})

        return {
            "type": "window",
            "title": "Advanced Application",
            "children": children
        }

    def add_item(self):
        self.state["items"].append({"text": "New Item"})

    def selection_changed(self, selected, deselected):
        # Update selection
        pass
```

## See Also

- [PySide Widgets](pyside-widgets.md)
- [PySide Renderer](pyside.md)
