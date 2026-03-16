# PySide Dialogs & Windows

Dialogs and windows are the top-level containers in your application. This guide covers creating and managing windows, modal dialogs, and various dialog types.

## Windows

### Basic Window

A window is a top-level container for your application UI:

```python
import collagraph as cg

class MyApp(cg.Component):
    def render(self):
        return {
            "type": "window",
            "title": "My Application",
            "size": (800, 600),
            "children": [
                {"type": "label", "text": "Hello World"}
            ]
        }

app = cg.Collagraph(MyApp, cg.PySideRenderer)
app.run()
```

```xml
<window title="My Application" :size="(800, 600)">
  <widget>
    <label text="Hello World" />
  </widget>
</window>
```

### Window Attributes

- `title` or `window-title` - Window title text
- `size` - Initial size as tuple (width, height)
- `minimum-size` - Minimum window size
- `maximum-size` - Maximum window size
- `window-icon` - Window icon (QIcon)
- `window-flags` - Window flags for customization

### Main Window

Main windows support menus, toolbars, status bars, and dock widgets:

```python
{
    "type": "window",
    "title": "Main Application",
    "children": [
        {
            "type": "menubar",
            "children": [
                {
                    "type": "menu",
                    "title": "File",
                    "children": [
                        {"type": "action", "text": "Open", "@triggered": self.open_file},
                        {"type": "action", "text": "Save", "@triggered": self.save_file},
                        {"type": "action", "separator": True},
                        {"type": "action", "text": "Exit", "@triggered": self.exit_app}
                    ]
                }
            ]
        },
        {
            "type": "toolbar",
            "window-title": "Main Toolbar",
            "children": [
                {"type": "action", "text": "New", "@triggered": self.new_file},
                {"type": "action", "text": "Open", "@triggered": self.open_file}
            ]
        },
        {
            "type": "widget",
            # Central widget
            "children": [...]
        },
        {
            "type": "statusbar"
        }
    ]
}
```

```xml
<window title="Main Application">
  <menubar>
    <menu title="File">
      <action text="Open" @triggered="open_file" />
      <action text="Save" @triggered="save_file" />
      <action separator />
      <action text="Exit" @triggered="exit_app" />
    </menu>
  </menubar>

  <toolbar window-title="Main Toolbar">
    <action text="New" @triggered="new_file" />
    <action text="Open" @triggered="open_file" />
  </toolbar>

  <widget>
    <!-- Central widget content -->
  </widget>

  <statusbar />
</window>
```

## Dialogs

### Modal vs Modeless Dialogs

**Modal dialogs** block interaction with other windows until closed:

```python
{
    "type": "qdialog",
    "modal": True,  # Blocks other windows
    "window-modality": Qt.ApplicationModal,  # Block entire app
    "children": [...]
}
```

**Modeless dialogs** allow interaction with other windows:

```python
{
    "type": "qdialog",
    # modal not set or False
    "children": [...]
}
```

### Window Modality Types

- `Qt.ApplicationModal` - Blocks all windows in the application
- `Qt.WindowModal` - Blocks only the parent window
- `Qt.NonModal` - Non-blocking dialog

### Custom Dialog Example

```python
import collagraph as cg
from PySide6.QtCore import Qt

class ListDialog(cg.Component):
    def init(self):
        self.state["selected"] = -1
        self.state["items"] = self.props.get("items", [])

    def render(self):
        return {
            "type": "qdialog",
            "modal": True,
            "window-modality": Qt.WindowModal,
            "@accepted": self.accepted,
            "@rejected": self.rejected,
            "children": [
                {"type": "label", "text": "Select an item:"},
                {
                    "type": "treeview",
                    "children": [
                        {
                            "type": "qstandarditemmodel",
                            "children": [
                                {"type": "standarditem", "text": str(item)}
                                for item in self.state["items"]
                            ]
                        },
                        {
                            "type": "qitemselectionmodel",
                            "@selection-changed": self.selection_changed
                        }
                    ]
                },
                {
                    "type": "dialogbuttonbox",
                    "buttons": ("Ok", "Cancel"),
                    "@accepted": lambda: self.element.accept(),
                    "@rejected": lambda: self.element.reject()
                }
            ]
        }

    def selection_changed(self, new, old):
        indexes = new.indexes()
        if indexes:
            self.state["selected"] = indexes[0].row()

    def accepted(self):
        # Emit the selected value
        self.emit("accepted", self.state["selected"])
        self.emit("finished")

    def rejected(self):
        self.emit("rejected")
        self.emit("finished")
```

```xml
<qdialog
    modal
    :window-modality="Qt.WindowModal"
    @accepted="accepted"
    @rejected="rejected"
>
  <label text="Select an item:" />
  <treeview>
    <qstandarditemmodel>
      <standarditem v-for="item in items" :text="str(item)" />
    </qstandarditemmodel>
    <qitemselectionmodel @selection-changed="selection_changed" />
  </treeview>
  <dialogbuttonbox
    :buttons="('Ok', 'Cancel')"
    @accepted="lambda: element.accept()"
    @rejected="lambda: element.reject()"
  />
</qdialog>
```

### Using the Dialog

```python
class MainApp(cg.Component):
    def init(self):
        self.state["show_dialog"] = False
        self.state["selected_item"] = None

    def render(self):
        children = [
            {
                "type": "button",
                "text": "Show Dialog",
                "@clicked": self.show_dialog
            }
        ]

        if self.state["show_dialog"]:
            children.append({
                "type": ListDialog,
                "items": [1, 2, 3, 4, 5],
                "@accepted": self.dialog_accepted,
                "@rejected": self.dialog_rejected,
                "@finished": self.dialog_finished
            })

        return {"type": "widget", "children": children}

    def show_dialog(self):
        self.state["show_dialog"] = True

    def dialog_accepted(self, selected):
        self.state["selected_item"] = selected
        print(f"Selected: {selected}")

    def dialog_rejected(self):
        print("Dialog cancelled")

    def dialog_finished(self):
        self.state["show_dialog"] = False
```

## Dialog Events

Dialogs emit several events:

- `@accepted` - User accepted the dialog (clicked OK, etc.)
- `@rejected` - User rejected the dialog (clicked Cancel, etc.)
- `@finished` - Dialog closed (either accepted or rejected)

## Dialog Methods

Access dialog methods via `self.element`:

```python
def accept_dialog(self):
    self.element.accept()  # Close dialog with accepted status

def reject_dialog(self):
    self.element.reject()  # Close dialog with rejected status

def close_dialog(self):
    self.element.close()  # Close dialog
```

## Dialog Button Box

The `dialogbuttonbox` widget provides standard dialog buttons:

```python
{
    "type": "dialogbuttonbox",
    "buttons": ("Ok", "Cancel"),  # Standard button set
    "@accepted": self.on_accept,
    "@rejected": self.on_reject
}
```

### Standard Buttons

You can use these standard button names:
- `"Ok"`, `"Cancel"`, `"Yes"`, `"No"`
- `"Save"`, `"Discard"`, `"Apply"`
- `"Close"`, `"Reset"`, `"Help"`

### Custom Buttons

```python
{
    "type": "dialogbuttonbox",
    "children": [
        {
            "type": "button",
            "text": "Custom Action",
            "role": "AcceptRole",
            "@clicked": self.custom_action
        }
    ]
}
```

## Built-in Qt Dialogs

### File Dialog

```python
def open_file(self):
    from PySide6.QtWidgets import QFileDialog

    filename, _ = QFileDialog.getOpenFileName(
        self.element,
        "Open File",
        "",
        "Text Files (*.txt);;All Files (*)"
    )
    if filename:
        print(f"Selected: {filename}")

def save_file(self):
    from PySide6.QtWidgets import QFileDialog

    filename, _ = QFileDialog.getSaveFileName(
        self.element,
        "Save File",
        "",
        "Text Files (*.txt)"
    )
    if filename:
        print(f"Saving to: {filename}")

def select_directory(self):
    from PySide6.QtWidgets import QFileDialog

    directory = QFileDialog.getExistingDirectory(
        self.element,
        "Select Directory"
    )
    if directory:
        print(f"Selected: {directory}")
```

### Message Box

```python
def show_info(self):
    from PySide6.QtWidgets import QMessageBox

    QMessageBox.information(
        self.element,
        "Information",
        "This is an information message"
    )

def show_warning(self):
    from PySide6.QtWidgets import QMessageBox

    QMessageBox.warning(
        self.element,
        "Warning",
        "This is a warning message"
    )

def show_error(self):
    from PySide6.QtWidgets import QMessageBox

    QMessageBox.critical(
        self.element,
        "Error",
        "An error occurred"
    )

def ask_question(self):
    from PySide6.QtWidgets import QMessageBox

    reply = QMessageBox.question(
        self.element,
        "Confirm",
        "Are you sure?",
        QMessageBox.Yes | QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        print("User clicked Yes")
    else:
        print("User clicked No")
```

### Input Dialog

```python
def get_text(self):
    from PySide6.QtWidgets import QInputDialog

    text, ok = QInputDialog.getText(
        self.element,
        "Input",
        "Enter your name:"
    )
    if ok and text:
        print(f"Name: {text}")

def get_number(self):
    from PySide6.QtWidgets import QInputDialog

    num, ok = QInputDialog.getInt(
        self.element,
        "Input",
        "Enter a number:",
        value=0,
        min=0,
        max=100
    )
    if ok:
        print(f"Number: {num}")

def get_choice(self):
    from PySide6.QtWidgets import QInputDialog

    items = ["Red", "Green", "Blue"]
    item, ok = QInputDialog.getItem(
        self.element,
        "Select",
        "Choose a color:",
        items,
        current=0,
        editable=False
    )
    if ok and item:
        print(f"Selected: {item}")
```

## Complete Dialog Example

```xml
<!-- dialog_example.cgx -->
<window title="Dialog Example">
  <widget>
    <button text="Show Custom Dialog" @clicked="show_custom" />
    <button text="Show File Dialog" @clicked="show_file" />
    <button text="Show Message Box" @clicked="show_message" />
    <label :text="f'Result: {result}'" />
  </widget>
</window>

<script>
import collagraph as cg
from PySide6.QtWidgets import QFileDialog, QMessageBox

class DialogExample(cg.Component):
    def init(self):
        self.state["show_dialog"] = False
        self.state["result"] = "None"

    def show_custom(self):
        self.state["show_dialog"] = True

    def show_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.element,
            "Select File"
        )
        if filename:
            self.state["result"] = filename

    def show_message(self):
        reply = QMessageBox.question(
            self.element,
            "Confirm",
            "Do you like dialogs?",
            QMessageBox.Yes | QMessageBox.No
        )
        self.state["result"] = "Yes" if reply == QMessageBox.Yes else "No"

    def dialog_accepted(self, value):
        self.state["result"] = f"Selected: {value}"

    def dialog_finished(self):
        self.state["show_dialog"] = False
</script>
```

## See Also

- [PySide Widgets](pyside-widgets.md)
- [PySide Renderer](pyside.md)
