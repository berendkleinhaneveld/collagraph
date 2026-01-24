# PySide Layouts

Layouts control how widgets are arranged within containers. The PySide renderer supports Qt's powerful layout system through a declarative API.

## Overview

Layouts are specified using the `layout` attribute on container widgets. When you add children to a widget without specifying a layout, a vertical box layout is created automatically.

## Box Layout

Box layouts arrange widgets in a row (horizontal) or column (vertical).

### Vertical Layout (Default)

```python
{
    "type": "widget",
    # No layout specified - defaults to vertical
    "children": [
        {"type": "label", "text": "First"},
        {"type": "label", "text": "Second"},
        {"type": "label", "text": "Third"}
    ]
}
```

```xml
<widget>
  <label text="First" />
  <label text="Second" />
  <label text="Third" />
</widget>
```

### Horizontal Layout

```python
{
    "type": "widget",
    "layout": {"type": "Box", "direction": "LeftToRight"},
    "children": [
        {"type": "button", "text": "Left"},
        {"type": "button", "text": "Middle"},
        {"type": "button", "text": "Right"}
    ]
}
```

```xml
<widget :layout="{'type': 'Box', 'direction': 'LeftToRight'}">
  <button text="Left" />
  <button text="Middle" />
  <button text="Right" />
</widget>
```

### Available Directions

- `"TopToBottom"` - Vertical (default)
- `"LeftToRight"` - Horizontal
- `"RightToLeft"` - Horizontal, right-to-left
- `"BottomToTop"` - Vertical, bottom-to-top

### Spacing and Margins

```python
{
    "type": "widget",
    "layout": {
        "type": "Box",
        "direction": "LeftToRight",
        "spacing": 10,  # Space between widgets
        "contents-margins": (10, 10, 10, 10)  # (left, top, right, bottom)
    },
    "children": [...]
}
```

## Grid Layout

Grid layouts arrange widgets in rows and columns.

### Basic Grid

```python
{
    "type": "widget",
    "layout": {"type": "Grid"},
    "children": [
        {"type": "label", "text": "Row 1, Col 1", "grid-index": (0, 0)},
        {"type": "label", "text": "Row 1, Col 2", "grid-index": (0, 1)},
        {"type": "label", "text": "Row 2, Col 1", "grid-index": (1, 0)},
        {"type": "label", "text": "Row 2, Col 2", "grid-index": (1, 1)}
    ]
}
```

```xml
<widget :layout="{'type': 'Grid'}">
  <label text="Row 1, Col 1" :grid_index="(0, 0)" />
  <label text="Row 1, Col 2" :grid_index="(0, 1)" />
  <label text="Row 2, Col 1" :grid_index="(1, 0)" />
  <label text="Row 2, Col 2" :grid_index="(1, 1)" />
</widget>
```

### Spanning Rows and Columns

The `grid-index` attribute accepts four values: `(row, column, rowSpan, columnSpan)`

```python
{
    "type": "widget",
    "layout": {"type": "Grid"},
    "children": [
        # This widget spans 2 rows and 1 column
        {"type": "label", "text": "Spans 2 rows", "grid-index": (0, 0, 2, 1)},
        # This widget spans 1 row and 2 columns
        {"type": "label", "text": "Spans 2 cols", "grid-index": (0, 1, 1, 2)},
        {"type": "label", "text": "Normal", "grid-index": (1, 1)}
    ]
}
```

### Column and Row Stretch

Control how extra space is distributed:

```python
{
    "type": "widget",
    "layout": {
        "type": "Grid",
        # Column 1 gets 10 units, column 2 gets 20 units of stretch
        "column-stretch": [(1, 10), (2, 20)],
        # Row 0 gets 5 units of stretch
        "row-stretch": [(0, 5)]
    },
    "children": [...]
}
```

```xml
<widget :layout="{'type': 'Grid', 'column_stretch': [(1, 10), (2, 20)]}">
  <!-- widgets -->
</widget>
```

## Form Layout

Form layouts create two-column forms with labels on the left and input widgets on the right.

### Basic Form

```python
{
    "type": "widget",
    "layout": {"type": "Form"},
    "children": [
        {"type": "line-edit", "form-label": "Name:", "form-index": 0},
        {"type": "line-edit", "form-label": "Email:", "form-index": 1},
        {"type": "spin-box", "form-label": "Age:", "form-index": 2}
    ]
}
```

```xml
<widget :layout="{'type': 'Form'}">
  <line-edit form_label="Name:" :form_index="0" />
  <line-edit form_label="Email:" :form_index="1" />
  <spin-box form_label="Age:" :form_index="2" />
</widget>
```

### Form Attributes

- `form-label` - Label text for the field
- `form-index` - Position in the form (optional, defaults to append order)

### Dynamic Forms

```python
class FormExample(cg.Component):
    def init(self):
        self.state["fields"] = [
            ("Name", "line-edit"),
            ("Email", "line-edit"),
            ("Age", "spin-box")
        ]

    def render(self):
        return {
            "type": "widget",
            "layout": {"type": "Form"},
            "children": [
                {
                    "type": widget_type,
                    "form-label": f"{label}:",
                    "form-index": i
                }
                for i, (label, widget_type) in enumerate(self.state["fields"])
            ]
        }
```

## Stacked Layout

Stacked layouts show only one child widget at a time, like a deck of cards.

```python
{
    "type": "widget",
    "layout": {
        "type": "Stacked",
        "current-index": self.state["page"]  # Which page to show
    },
    "children": [
        {"type": "label", "text": "Page 1"},
        {"type": "label", "text": "Page 2"},
        {"type": "label", "text": "Page 3"}
    ]
}
```

```xml
<widget :layout="{'type': 'Stacked', 'current_index': page}">
  <label text="Page 1" />
  <label text="Page 2" />
  <label text="Page 3" />
</widget>
```

## Nested Layouts

Layouts can be nested to create complex UIs:

```python
{
    "type": "widget",
    # Outer vertical layout
    "children": [
        {
            "type": "widget",
            # Nested horizontal layout for buttons
            "layout": {"type": "Box", "direction": "LeftToRight"},
            "children": [
                {"type": "button", "text": "Button 1"},
                {"type": "button", "text": "Button 2"}
            ]
        },
        {
            "type": "widget",
            # Nested grid layout
            "layout": {"type": "Grid"},
            "children": [
                {"type": "label", "text": "A", "grid-index": (0, 0)},
                {"type": "label", "text": "B", "grid-index": (0, 1)}
            ]
        }
    ]
}
```

## Custom Layouts

You can register custom Qt layout classes:

```python
from PySide6.QtWidgets import QLayout
import collagraph as cg

class FlowLayout(QLayout):
    # Custom layout implementation
    pass

# Register the layout
cg.PySideRenderer.register_layout("flow", FlowLayout)

# Use in components
{
    "type": "widget",
    "layout": {"type": "flow"},
    "children": [...]
}
```

## Complete Example

```python
import collagraph as cg

class LayoutExample(cg.Component):
    def init(self):
        self.state["name"] = ""
        self.state["email"] = ""
        self.state["age"] = 0

    def render(self):
        return {
            "type": "window",
            "title": "Layout Example",
            "children": [
                {
                    "type": "widget",
                    "children": [
                        # Form section
                        {
                            "type": "group-box",
                            "title": "User Information",
                            "layout": {"type": "Form"},
                            "children": [
                                {
                                    "type": "line-edit",
                                    "form-label": "Name:",
                                    "text": self.state["name"],
                                    "@text-changed": lambda t: self.state.update({"name": t})
                                },
                                {
                                    "type": "line-edit",
                                    "form-label": "Email:",
                                    "text": self.state["email"],
                                    "@text-changed": lambda t: self.state.update({"email": t})
                                },
                                {
                                    "type": "spin-box",
                                    "form-label": "Age:",
                                    "value": self.state["age"],
                                    "@value-changed": lambda v: self.state.update({"age": v})
                                }
                            ]
                        },
                        # Button section
                        {
                            "type": "widget",
                            "layout": {"type": "Box", "direction": "LeftToRight"},
                            "children": [
                                {"type": "button", "text": "Save", "@clicked": self.save},
                                {"type": "button", "text": "Cancel", "@clicked": self.cancel}
                            ]
                        }
                    ]
                }
            ]
        }

    def save(self):
        print(f"Saving: {self.state}")

    def cancel(self):
        self.state.update({"name": "", "email": "", "age": 0})
```

## See Also

- [PySide Widgets](pyside-widgets.md)
- [PySide Renderer](pyside.md)
