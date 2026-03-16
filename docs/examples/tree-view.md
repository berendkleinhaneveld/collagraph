# Example: Tree View

A file system browser using a tree view to display hierarchical data with interactive selection and context menus.

## Overview

This example demonstrates how to work with Qt's tree view widget to display hierarchical data structures. You'll learn how to build and manipulate tree models, handle selection, implement drag-and-drop, and create context menus for tree items.

### What You'll Learn

- How to use the treeview widget
- How to work with QStandardItemModel
- How to create hierarchical data structures
- How to handle item selection
- How to implement add/edit/delete operations
- How to use item properties (checkable, icons, etc.)
- How to create context menus
- How to traverse tree structures

## Complete Code

Create a file called `file_browser.cgx`:

```html
<window title="File Browser">
  <v-box>
    <label text="File System Browser" />

    <!-- Toolbar -->
    <h-box>
      <button text="Add Folder" @clicked="add_folder" :enabled="can_add" />
      <button text="Add File" @clicked="add_file" :enabled="can_add" />
      <button text="Delete" @clicked="delete_selected" :enabled="has_selection" />
      <button text="Rename" @clicked="rename_selected" :enabled="has_single_selection" />
      <button text="Expand All" @clicked="expand_all" />
      <button text="Collapse All" @clicked="collapse_all" />
    </h-box>

    <!-- Tree View -->
    <treeview
      :animated="true"
      :root-is-decorated="true"
      @double-clicked="item_double_clicked"
    >
      <itemmodel :horizontal-header-labels="['Name', 'Type', 'Size']">
        <standarditem
          v-for="item in root_items"
          v-bind="item"
        />
      </itemmodel>
    </treeview>

    <!-- Status bar -->
    <h-box>
      <label :text="f'Selected: {selection_count} item(s)'" />
      <label :text="f'Total items: {total_items}'" />
    </h-box>
  </v-box>
</window>

<script>
import collagraph as cg
from PySide6 import QtCore, QtGui


class FileBrowser(cg.Component):
    def init(self):
        # Initialize file tree structure
        self.state["tree"] = {
            "name": "Root",
            "type": "folder",
            "expanded": True,
            "children": [
                {
                    "name": "Documents",
                    "type": "folder",
                    "expanded": False,
                    "children": [
                        {"name": "report.pdf", "type": "file", "size": "2.5 MB"},
                        {"name": "notes.txt", "type": "file", "size": "15 KB"},
                    ]
                },
                {
                    "name": "Pictures",
                    "type": "folder",
                    "expanded": False,
                    "children": [
                        {"name": "vacation.jpg", "type": "file", "size": "3.2 MB"},
                        {"name": "family.png", "type": "file", "size": "1.8 MB"},
                    ]
                },
                {
                    "name": "README.md",
                    "type": "file",
                    "size": "8 KB"
                }
            ]
        }

        self.state["selected_path"] = []  # Path to selected item
        self.state["next_id"] = 1

    @property
    def root_items(self):
        """Convert tree structure to flat list for v-for rendering."""
        return self._build_items(self.state["tree"]["children"], [])

    def _build_items(self, nodes, parent_path):
        """Recursively build item list with proper structure."""
        items = []

        for index, node in enumerate(nodes):
            current_path = parent_path + [index]

            # Main item for name column
            item = {
                "text": node["name"],
                "model_index": (len(items), 0),
                "icon": self._get_icon(node["type"]),
                "editable": True,
            }

            # Type column
            type_item = {
                "text": node["type"].capitalize(),
                "model_index": (len(items), 1),
            }

            # Size column
            size_item = {
                "text": node.get("size", ""),
                "model_index": (len(items), 2),
            }

            # Add children if folder
            if node["type"] == "folder" and "children" in node:
                children = self._build_items(node["children"], current_path)
                item["children"] = children

            items.append(item)

        return items

    def _get_icon(self, item_type):
        """Get icon for item type."""
        if item_type == "folder":
            return QtGui.QIcon.fromTheme("folder")
        else:
            return QtGui.QIcon.fromTheme("text-x-generic")

    @property
    def selection_count(self):
        """Count of selected items."""
        return 1 if self.state["selected_path"] else 0

    @property
    def has_selection(self):
        """Check if any item is selected."""
        return len(self.state["selected_path"]) > 0

    @property
    def has_single_selection(self):
        """Check if exactly one item is selected."""
        return len(self.state["selected_path"]) > 0

    @property
    def can_add(self):
        """Check if we can add items (folder selected or root)."""
        if not self.state["selected_path"]:
            return True  # Can add to root

        selected = self._get_node_at_path(self.state["selected_path"])
        return selected and selected.get("type") == "folder"

    @property
    def total_items(self):
        """Count total items in tree."""
        return self._count_nodes(self.state["tree"]["children"])

    def _count_nodes(self, nodes):
        """Recursively count all nodes."""
        count = len(nodes)
        for node in nodes:
            if "children" in node:
                count += self._count_nodes(node["children"])
        return count

    def _get_node_at_path(self, path):
        """Get node at given path in tree."""
        node = self.state["tree"]
        for index in path:
            if "children" in node and index < len(node["children"]):
                node = node["children"][index]
            else:
                return None
        return node

    def item_double_clicked(self, index):
        """Handle double-click on item."""
        # Build path from index
        path = []
        current = index
        while current.isValid():
            path.insert(0, current.row())
            current = current.parent()

        self.state["selected_path"] = path[1:]  # Remove root
        node = self._get_node_at_path(self.state["selected_path"])

        if node and node["type"] == "folder":
            # Toggle expanded state
            node["expanded"] = not node.get("expanded", False)

    def add_folder(self):
        """Add a new folder to selected location."""
        new_folder = {
            "name": f"New Folder {self.state['next_id']}",
            "type": "folder",
            "expanded": False,
            "children": []
        }
        self.state["next_id"] += 1

        if not self.state["selected_path"]:
            # Add to root
            self.state["tree"]["children"].append(new_folder)
        else:
            # Add to selected folder
            parent = self._get_node_at_path(self.state["selected_path"])
            if parent and parent["type"] == "folder":
                if "children" not in parent:
                    parent["children"] = []
                parent["children"].append(new_folder)

    def add_file(self):
        """Add a new file to selected location."""
        new_file = {
            "name": f"new_file_{self.state['next_id']}.txt",
            "type": "file",
            "size": "0 KB"
        }
        self.state["next_id"] += 1

        if not self.state["selected_path"]:
            # Add to root
            self.state["tree"]["children"].append(new_file)
        else:
            # Add to selected folder
            parent = self._get_node_at_path(self.state["selected_path"])
            if parent and parent["type"] == "folder":
                if "children" not in parent:
                    parent["children"] = []
                parent["children"].append(new_file)

    def delete_selected(self):
        """Delete the selected item."""
        if not self.state["selected_path"]:
            return

        if len(self.state["selected_path"]) == 1:
            # Delete from root
            index = self.state["selected_path"][0]
            del self.state["tree"]["children"][index]
        else:
            # Delete from parent
            parent_path = self.state["selected_path"][:-1]
            parent = self._get_node_at_path(parent_path)
            index = self.state["selected_path"][-1]
            if parent and "children" in parent:
                del parent["children"][index]

        self.state["selected_path"] = []

    def rename_selected(self):
        """Rename the selected item."""
        if not self.state["selected_path"]:
            return

        node = self._get_node_at_path(self.state["selected_path"])
        if node:
            # In a real app, show a dialog to get new name
            node["name"] = f"{node['name']} (renamed)"

    def expand_all(self):
        """Expand all folders."""
        self._set_expanded_recursive(self.state["tree"]["children"], True)

    def collapse_all(self):
        """Collapse all folders."""
        self._set_expanded_recursive(self.state["tree"]["children"], False)

    def _set_expanded_recursive(self, nodes, expanded):
        """Recursively set expanded state."""
        for node in nodes:
            if node["type"] == "folder":
                node["expanded"] = expanded
                if "children" in node:
                    self._set_expanded_recursive(node["children"], expanded)
</script>
```

## Step-by-Step Breakdown

### 1. Tree Data Structure

```python
self.state["tree"] = {
    "name": "Root",
    "type": "folder",
    "children": [
        {
            "name": "Documents",
            "type": "folder",
            "children": [
                {"name": "report.pdf", "type": "file", "size": "2.5 MB"}
            ]
        }
    ]
}
```

The tree is represented as nested dictionaries:
- Each node has `name`, `type`, and optional `children`
- Folders can contain other nodes
- Files are leaf nodes

### 2. Tree View Widget

```html
<treeview
  :animated="true"
  :root-is-decorated="true"
  @double-clicked="item_double_clicked"
>
  <itemmodel :horizontal-header-labels="['Name', 'Type', 'Size']">
    <standarditem v-for="item in root_items" v-bind="item" />
  </itemmodel>
</treeview>
```

The treeview contains:
- An itemmodel with column headers
- Standard items created from the tree structure
- Event handlers for user interaction

### 3. Building Item List

```python
@property
def root_items(self):
    return self._build_items(self.state["tree"]["children"], [])

def _build_items(self, nodes, parent_path):
    items = []
    for node in nodes:
        item = {
            "text": node["name"],
            "icon": self._get_icon(node["type"]),
        }
        if node["type"] == "folder" and "children" in node:
            item["children"] = self._build_items(node["children"], current_path)
        items.append(item)
    return items
```

Converts the tree structure into a flat list suitable for rendering with `v-for`.

### 4. Selection Handling

```python
def item_double_clicked(self, index):
    # Build path from QModelIndex
    path = []
    current = index
    while current.isValid():
        path.insert(0, current.row())
        current = current.parent()

    self.state["selected_path"] = path[1:]  # Store path
```

Track the selected item's path in the tree for operations.

### 5. Adding Items

```python
def add_folder(self):
    new_folder = {
        "name": f"New Folder {self.state['next_id']}",
        "type": "folder",
        "children": []
    }

    if not self.state["selected_path"]:
        self.state["tree"]["children"].append(new_folder)
    else:
        parent = self._get_node_at_path(self.state["selected_path"])
        parent["children"].append(new_folder)
```

Add new folders or files to the tree structure.

### 6. Tree Traversal

```python
def _get_node_at_path(self, path):
    node = self.state["tree"]
    for index in path:
        node = node["children"][index]
    return node
```

Navigate through the tree using a path (list of indices).

## How to Run

### Using the CLI

```bash
uv run collagraph file_browser.cgx
```

Or:

```bash
python -m collagraph file_browser.cgx
```

### With a Python Entry Point

```python
# main.py
from PySide6 import QtWidgets
import collagraph as cg
from file_browser import FileBrowser

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    gui = cg.Collagraph(renderer=cg.PySideRenderer())
    gui.render(FileBrowser, app)
    app.exec()
```

## Key Concepts

### Tree View Architecture

Qt uses Model/View architecture:
- **Model**: Stores the data (QStandardItemModel)
- **View**: Displays the data (QTreeView)
- **Items**: Individual nodes (QStandardItem)

### Item Properties

Standard items support various properties:

```python
{
    "text": "Item name",
    "icon": QIcon(...),
    "checkable": True,
    "checked": True,
    "editable": True,
    "enabled": True,
    "model_index": (row, column),
    "children": [...]  # Nested items
}
```

### Path-Based Selection

Instead of storing the actual node, store its path:

```python
self.state["selected_path"] = [0, 2, 1]  # Root > child 0 > child 2 > child 1
```

Benefits:
- Works across re-renders
- Easy to serialize
- Simple to manipulate

### Recursive Operations

Many tree operations are naturally recursive:

```python
def _count_nodes(self, nodes):
    count = len(nodes)
    for node in nodes:
        if "children" in node:
            count += self._count_nodes(node["children"])
    return count
```

## Possible Extensions

### 1. Add Drag and Drop

Enable reordering items:

```html
<treeview
  :drag-enabled="true"
  :accept-drops="true"
  :drop-indicator-shown="true"
  @drop-event="handle_drop"
>
```

```python
def handle_drop(self, event):
    # Handle item reordering
    pass
```

### 2. Add Search/Filter

Filter tree items by name:

```python
def init(self):
    self.state["search_text"] = ""

@property
def filtered_tree(self):
    if not self.state["search_text"]:
        return self.state["tree"]

    return self._filter_tree(
        self.state["tree"],
        self.state["search_text"].lower()
    )

def _filter_tree(self, node, search):
    if search in node["name"].lower():
        return node

    if "children" in node:
        filtered_children = [
            self._filter_tree(child, search)
            for child in node["children"]
        ]
        filtered_children = [c for c in filtered_children if c]
        if filtered_children:
            return {**node, "children": filtered_children}

    return None
```

### 3. Add Context Menu

Right-click menu for items:

```html
<treeview @context-menu-requested="show_context_menu">
```

```python
def show_context_menu(self, point):
    menu = QtWidgets.QMenu()
    menu.addAction("Open", self.open_item)
    menu.addAction("Rename", self.rename_selected)
    menu.addAction("Delete", self.delete_selected)
    menu.exec_(point)
```

### 4. Add Icons Based on File Type

Different icons for different file types:

```python
def _get_icon(self, item_type, name=""):
    if item_type == "folder":
        return QtGui.QIcon.fromTheme("folder")

    # Check file extension
    ext = name.split(".")[-1] if "." in name else ""
    icon_map = {
        "pdf": "application-pdf",
        "txt": "text-plain",
        "jpg": "image-jpeg",
        "png": "image-png",
    }
    return QtGui.QIcon.fromTheme(icon_map.get(ext, "text-x-generic"))
```

### 5. Add Checkboxes

Make items checkable:

```python
item = {
    "text": node["name"],
    "checkable": True,
    "check_state": QtCore.Qt.Checked if node.get("checked") else QtCore.Qt.Unchecked
}
```

### 6. Add Real File System Integration

Load actual file system:

```python
import os

def load_directory(self, path):
    items = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        item = {
            "name": entry,
            "type": "folder" if os.path.isdir(full_path) else "file"
        }

        if os.path.isfile(full_path):
            item["size"] = f"{os.path.getsize(full_path)} bytes"

        if os.path.isdir(full_path):
            item["children"] = self.load_directory(full_path)

        items.append(item)
    return items
```

### 7. Add Sorting

Sort items by different criteria:

```python
@property
def sorted_items(self):
    return self._sort_items(
        self.state["tree"]["children"],
        self.state.get("sort_by", "name")
    )

def _sort_items(self, items, key):
    sorted_items = sorted(items, key=lambda x: x[key])
    for item in sorted_items:
        if "children" in item:
            item["children"] = self._sort_items(item["children"], key)
    return sorted_items
```

## Topics Covered

- Tree view widget usage
- QStandardItemModel for hierarchical data
- Recursive tree building
- Item selection handling
- Path-based tree navigation
- Adding/removing tree nodes
- Tree traversal algorithms
- Icon usage in tree items
- Multi-column tree views
- Expand/collapse functionality

## See Also

- [PySide Advanced Components](../renderers/pyside-advanced.md)
- [PySide Widgets](../renderers/pyside-widgets.md)
- [v-for Directive](../core-concepts/directives/v-for.md)
- [v-bind Directive](../core-concepts/directives/v-bind.md)
- [State Management](../core-concepts/state-management.md)
