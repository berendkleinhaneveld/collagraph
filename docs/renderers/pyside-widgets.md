# PySide Available Widgets

This page documents all available widgets in the PySide renderer, their attributes, and common events.

## Basic Widgets

### label

Display text or images.

**Attributes:**
- `text` - The text to display
- `word-wrap` - Enable word wrapping (boolean)
- `alignment` - Text alignment (e.g., `Qt.AlignCenter`)

**Example:**
```python
{"type": "label", "text": "Hello World"}
```

```xml
<label text="Hello World" />
<label :text="f'Count: {count}'" />
```

### button / push-button

Clickable button with text or icon.

**Attributes:**
- `text` - Button label
- `enabled` - Whether the button is enabled (boolean)
- `checkable` - Make button toggleable (boolean)
- `checked` - Checked state for checkable buttons (boolean)
- `icon` - Button icon (QIcon)

**Events:**
- `@clicked` - Emitted when button is clicked
- `@toggled` - Emitted when checkable button state changes

**Example:**
```python
{
    "type": "button",
    "text": "Click me",
    "@clicked": self.handle_click
}
```

```xml
<button text="Submit" @clicked="submit" />
<button text="Toggle" checkable :checked="is_active" @toggled="toggle" />
```

### line-edit

Single-line text input field.

**Attributes:**
- `text` - Current text value
- `placeholder-text` - Placeholder text shown when empty
- `max-length` - Maximum number of characters
- `read-only` - Make field read-only (boolean)
- `echo-mode` - Password mode (e.g., `QLineEdit.Password`)

**Events:**
- `@text-changed` - Emitted when text changes
- `@editing-finished` - Emitted when editing is complete (Enter or focus lost)
- `@return-pressed` - Emitted when Enter is pressed

**Example:**
```python
{
    "type": "line-edit",
    "text": self.state["name"],
    "placeholder-text": "Enter your name",
    "@text-changed": lambda text: self.state.update({"name": text})
}
```

```xml
<line-edit
    :text="name"
    placeholder-text="Enter your name"
    @text-changed="name_changed"
/>
```

### text-edit

Multi-line text editor with rich text support.

**Attributes:**
- `text` - Plain text content
- `html` - HTML formatted content
- `read-only` - Make editor read-only (boolean)
- `placeholder-text` - Placeholder text

**Events:**
- `@text-changed` - Emitted when text changes

**Example:**
```python
{"type": "text-edit", "text": self.state["notes"]}
```

```xml
<text-edit :text="notes" @text-changed="notes_changed" />
```

### checkbox

Boolean checkbox with label.

**Attributes:**
- `text` - Label text
- `checked` - Checked state (boolean)
- `tristate` - Enable three-state mode (boolean)

**Events:**
- `@state-changed` - Emitted when state changes (passes int: 0, 1, or 2)
- `@toggled` - Emitted when toggled (passes boolean)

**Example:**
```python
{
    "type": "checkbox",
    "text": "Enable feature",
    "checked": self.state["enabled"],
    "@toggled": lambda checked: self.state.update({"enabled": checked})
}
```

```xml
<checkbox
    text="Enable feature"
    :checked="enabled"
    @toggled="toggle_feature"
/>
```

### radio-button

Radio button for mutually exclusive selections.

**Attributes:**
- `text` - Label text
- `checked` - Whether this radio is selected (boolean)

**Events:**
- `@toggled` - Emitted when selection changes

**Example:**
```python
{
    "type": "widget",
    "children": [
        {"type": "radio-button", "text": "Option 1", "checked": self.state["option"] == 1, "@toggled": lambda: self.select_option(1)},
        {"type": "radio-button", "text": "Option 2", "checked": self.state["option"] == 2, "@toggled": lambda: self.select_option(2)}
    ]
}
```

### combobox

Dropdown selection widget.

**Attributes:**
- `items` - List of items to display
- `current-index` - Selected item index
- `current-text` - Selected item text
- `editable` - Allow custom text entry (boolean)

**Events:**
- `@current-index-changed` - Emitted when selection changes (passes index)
- `@current-text-changed` - Emitted when selected text changes

**Example:**
```python
{
    "type": "combobox",
    "items": ["Red", "Green", "Blue"],
    "current-index": self.state["color_index"],
    "@current-index-changed": lambda idx: self.state.update({"color_index": idx})
}
```

```xml
<qcombobox
    :items="['Red', 'Green', 'Blue']"
    :current_index="color_index"
    @current_index_changed="color_changed"
/>
```

### spin-box

Numeric input with increment/decrement buttons.

**Attributes:**
- `value` - Current value
- `minimum` - Minimum allowed value
- `maximum` - Maximum allowed value
- `single-step` - Increment/decrement step size
- `prefix` - Text prefix (e.g., "$")
- `suffix` - Text suffix (e.g., "kg")

**Events:**
- `@value-changed` - Emitted when value changes

**Example:**
```python
{
    "type": "spin-box",
    "minimum": 0,
    "maximum": 100,
    "value": self.state["quantity"],
    "@value-changed": lambda val: self.state.update({"quantity": val})
}
```

```xml
<spinbox
    :minimum="0"
    :maximum="100"
    :value="quantity"
    @value_changed="quantity_changed"
/>
```

### slider

Slider for selecting numeric values.

**Attributes:**
- `value` - Current value
- `minimum` - Minimum value
- `maximum` - Maximum value
- `orientation` - Horizontal or Vertical (e.g., `Qt.Horizontal`)
- `tick-position` - Where to show tick marks
- `tracking` - Emit value-changed during dragging (boolean)

**Events:**
- `@value-changed` - Emitted when value changes
- `@slider-moved` - Emitted during dragging

**Example:**
```python
{
    "type": "slider",
    "orientation": Qt.Horizontal,
    "minimum": 0,
    "maximum": 100,
    "value": self.state["volume"],
    "@value-changed": lambda val: self.state.update({"volume": val})
}
```

```xml
<slider
    :orientation="QtCore.Qt.Orientation.Horizontal"
    :minimum="0"
    :maximum="100"
    :value="volume"
    @value_changed="volume_changed"
/>
```

### progress-bar

Progress indicator for long operations.

**Attributes:**
- `value` - Current progress value
- `minimum` - Minimum value
- `maximum` - Maximum value
- `text-visible` - Show percentage text (boolean)
- `format` - Text format string (e.g., "%p%")

**Example:**
```python
{"type": "progress-bar", "minimum": 0, "maximum": 100, "value": self.state["progress"]}
```

## Container Widgets

### widget

Generic container widget. Automatically gets a vertical box layout when children are added.

**Attributes:**
- `layout` - Specify layout type and configuration (dict)
- `size` - Widget size as tuple (width, height)
- `minimum-size` - Minimum size
- `maximum-size` - Maximum size

**Example:**
```python
{
    "type": "widget",
    "children": [
        {"type": "label", "text": "Hello"},
        {"type": "button", "text": "Click"}
    ]
}
```

```xml
<widget>
  <label text="Hello" />
  <button text="Click" @clicked="handle_click" />
</widget>
```

### group-box

Container with a title and border.

**Attributes:**
- `title` - Group box title
- `checkable` - Make title a checkbox (boolean)
- `checked` - Checked state if checkable
- `layout` - Layout configuration

**Example:**
```python
{
    "type": "group-box",
    "title": "Settings",
    "children": [
        {"type": "checkbox", "text": "Option 1"},
        {"type": "checkbox", "text": "Option 2"}
    ]
}
```

```xml
<groupbox title="Settings">
  <checkbox text="Option 1" />
  <checkbox text="Option 2" />
</groupbox>
```

### scroll-area

Scrollable container for large content.

**Attributes:**
- `widget-resizable` - Allow content to resize (boolean)
- `horizontal-scrollbar-policy` - Horizontal scrollbar policy
- `vertical-scrollbar-policy` - Vertical scrollbar policy

**Example:**
```python
{
    "type": "scroll-area",
    "widget-resizable": True,
    "children": [
        {"type": "label", "text": "Very long content..."}
    ]
}
```

### tab-widget

Tabbed interface for multiple pages.

**Attributes:**
- `current-index` - Currently selected tab index
- `tab-position` - Position of tabs (North, South, East, West)

**Events:**
- `@current-changed` - Emitted when active tab changes

**Child Attributes:**
- `tab-index` - Tab position (optional, defaults to append)
- `tab-label` - Tab title text

**Example:**
```python
{
    "type": "tab-widget",
    "children": [
        {
            "type": "widget",
            "tab-label": "Tab 1",
            "tab-index": 0,
            "children": [{"type": "label", "text": "Content 1"}]
        },
        {
            "type": "widget",
            "tab-label": "Tab 2",
            "tab-index": 1,
            "children": [{"type": "label", "text": "Content 2"}]
        }
    ]
}
```

```xml
<tabwidget>
  <widget tab_label="Tab 1" tab_index="0">
    <label text="Content 1" />
  </widget>
  <widget tab_label="Tab 2" tab_index="1">
    <label text="Content 2" />
  </widget>
</tabwidget>
```

### splitter

Resizable split panes.

**Attributes:**
- `orientation` - Horizontal or Vertical split
- `sizes` - List of pane sizes

**Example:**
```python
{
    "type": "QSplitter",
    "orientation": Qt.Horizontal,
    "children": [
        {"type": "text-edit", "text": "Left pane"},
        {"type": "text-edit", "text": "Right pane"}
    ]
}
```

## Layout Configuration

Widgets support the `layout` attribute to specify their layout:

```python
{
    "type": "widget",
    "layout": {"type": "Box", "direction": "LeftToRight"},
    "children": [...]
}
```

### Available Layouts

- `Box` - Vertical or horizontal box layout
- `Grid` - Grid layout with rows and columns
- `Form` - Two-column form layout
- `Stacked` - Stacked layout (one visible at a time)

See [PySide Layouts](pyside-layouts.md) for detailed layout documentation.

## Advanced Widgets

### tree-view

Hierarchical tree view with model/view architecture.

**Attributes:**
- `selection-mode` - Selection mode (e.g., `QTreeView.ExtendedSelection`)
- `header-hidden` - Hide the header (boolean)
- `root-is-decorated` - Show expand/collapse indicators (boolean)

**Children:**
- `item-model` or `qstandarditemmodel` - Data model
- `itemselectionmodel` - Selection model

**Events:**
- Via selection model: `@selection-changed`

See [PySide Advanced](pyside-advanced.md) for detailed examples.

### tree-widget

Simpler tree widget without model/view separation.

**Attributes:**
- `column-count` - Number of columns
- `header-labels` - List of header labels

**Children:**
- `tree-widget-item` - Tree items

### list-view

List display with model/view architecture. Similar to tree-view but for flat lists.

### dialog-button-box

Standard dialog button container.

**Attributes:**
- `buttons` - Tuple of button names (e.g., `("Ok", "Cancel")`)

**Events:**
- `@accepted` - OK button clicked
- `@rejected` - Cancel button clicked

**Example:**
```python
{
    "type": "dialogbuttonbox",
    "buttons": ("Ok", "Cancel"),
    "@accepted": self.accept,
    "@rejected": self.reject
}
```

```xml
<dialogbuttonbox
    :buttons="('Ok', 'Cancel')"
    @accepted="accept"
    @rejected="reject"
/>
```

## Dialogs and Windows

### window / main-window

Top-level application window.

**Attributes:**
- `title` or `window-title` - Window title
- `size` - Window size tuple (width, height)
- `minimum-size` - Minimum window size
- `maximum-size` - Maximum window size

**Main Window Children:**
- `menubar` - Menu bar
- `toolbar` - Tool bars
- `statusbar` - Status bar
- `dock` - Dock widgets
- `widget` - Central widget

**Example:**
```python
{
    "type": "window",
    "title": "My Application",
    "children": [
        {"type": "widget", "children": [...]}
    ]
}
```

```xml
<window title="My Application">
  <menubar>
    <menu title="File">
      <action text="Open" @triggered="open_file" />
      <action text="Save" @triggered="save_file" />
    </menu>
  </menubar>
  <widget>
    <!-- Central widget content -->
  </widget>
</window>
```

### qdialog / dialog

Modal or modeless dialog window.

**Attributes:**
- `modal` - Make dialog modal (boolean)
- `window-modality` - Modality type (ApplicationModal or WindowModal)

**Events:**
- `@accepted` - Dialog accepted
- `@rejected` - Dialog rejected
- `@finished` - Dialog closed

**Methods (via self.element):**
- `accept()` - Accept and close dialog
- `reject()` - Reject and close dialog

See [PySide Dialogs](pyside-dialogs.md) for detailed examples.

## Menu and Toolbar Widgets

### menubar

Menu bar for main windows.

**Children:**
- `menu` - Menus

### menu

Drop-down menu.

**Attributes:**
- `title` - Menu title

**Children:**
- `action` - Menu actions
- `menu` - Submenus

### action

Menu action or toolbar button.

**Attributes:**
- `text` - Action text
- `separator` - Make this a separator (boolean)
- `checkable` - Make action checkable (boolean)
- `checked` - Checked state
- `shortcut` - Keyboard shortcut

**Events:**
- `@triggered` - Action triggered

### toolbar

Tool bar for main windows.

**Attributes:**
- `window-title` - Toolbar name
- `area` - Toolbar area (TopToolBarArea, BottomToolBarArea, etc.)
- `movable` - Allow moving toolbar (boolean)

**Children:**
- `action` - Toolbar actions

### statusbar

Status bar for main windows.

**Methods:**
- Use `self.element.showMessage("text")` to show messages

## Item Models

### itemmodel / qstandarditemmodel

Data model for tree-view, list-view, etc.

**Children:**
- `standarditem` - Model items

### standarditem

Item for standard item models.

**Attributes:**
- `text` - Item text
- `checkable` - Make item checkable (boolean)
- `checked` - Checked state

**Children:**
- `standarditem` - Child items

### itemselectionmodel

Selection model for views.

**Events:**
- `@selection-changed` - Selection changed (passes selected, deselected)

**Example:**
```xml
<treeview>
  <qstandarditemmodel>
    <standarditem text="Root 1">
      <standarditem text="Child 1.1" />
      <standarditem text="Child 1.2" />
    </standarditem>
    <standarditem text="Root 2" />
  </qstandarditemmodel>
  <itemselectionmodel @selection-changed="selection_changed" />
</treeview>
```

## See Also

- [PySide Renderer](pyside.md)
- [PySide Layouts](pyside-layouts.md)
- [PySide Dialogs](pyside-dialogs.md)
- [PySide Advanced](pyside-advanced.md)
