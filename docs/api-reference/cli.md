# CLI

## Overview

The Collagraph CLI provides a convenient way to run `.cgx` component files directly without writing boilerplate code. It automatically sets up the renderer, event loop, and application container.

## Usage

```bash
python -m collagraph [options] <component.cgx>
```

Or with uv:
```bash
uv run collagraph [options] <component.cgx>
```

## Arguments

### `component`

**Required.** Path to the `.cgx` component file to render.

**Type:** File path (must exist and have `.cgx` extension)

```bash
python -m collagraph my_app.cgx
python -m collagraph examples/pyside/counter.cgx
python -m collagraph ../components/dashboard.cgx
```

**Validation:**
- File must exist
- Must be a regular file (not directory)
- Must have `.cgx` extension

## Options

### `--renderer <name>`

Specify which renderer to use.

**Type:** Choice from available renderers
**Default:** `pyside`

**Available Renderers:**
- `pyside` - PySide6/Qt renderer (default)
- `pygfx` - 3D graphics renderer using pygfx
- `dict` - Dictionary renderer (for debugging/testing)

**Note:** Only renderers with installed dependencies are available. For example, `pyside` requires PySide6 to be installed.

```bash
# Use PySide6 renderer (default)
python -m collagraph app.cgx
python -m collagraph --renderer pyside app.cgx

# Use pygfx renderer for 3D graphics
python -m collagraph --renderer pygfx graphics_app.cgx

# Use dict renderer for debugging
python -m collagraph --renderer dict debug_app.cgx
```

**Renderer-Specific Behavior:**

**PySide (`pyside`):**
- Creates a `QApplication`
- Renders into the application
- Shows top-level windows automatically
- Runs the Qt event loop (`app.exec()`)

**Pygfx (`pygfx`):**
- Creates a canvas and WGPU renderer
- Sets up a perspective camera and orbit controls
- Renders into a `gfx.Scene`
- Runs the rendercanvas event loop
- Automatically refreshes on state changes

**Dict (`dict`):**
- Renders to a plain Python dictionary
- Uses synchronous event loop
- Drops into a debugger (`breakpoint()`) for inspection
- Useful for testing and debugging component structure

---

### `--state <json>`

Provide initial state/props to pass to the root component.

**Type:** JSON string or path to JSON file
**Default:** `None` (empty state)

**As JSON string:**
```bash
python -m collagraph --state '{"title": "My App", "count": 5}' app.cgx
```

**As JSON file:**

**state.json:**
```json
{
  "title": "My Application",
  "theme": "dark",
  "user": {
    "name": "Alice",
    "role": "admin"
  }
}
```

```bash
python -m collagraph --state state.json app.cgx
```

**Accessing in Component:**

The state is passed as props to the root component:

```xml
<template>
  <label :text="title" />
  <label :text="f'Count: {count}'" />
</template>

<script>
import collagraph as cg

class MyApp(cg.Component):
    def init(self):
        # Access from props
        self.state["title"] = self.props.get("title", "Default")
        self.state["count"] = self.props.get("count", 0)
</script>
```

**Error Handling:**
- Invalid JSON raises an error with details
- File path that doesn't exist is treated as JSON string
- Non-JSON content raises helpful error message

---

### `--help`, `-h`

Show help message and exit.

```bash
python -m collagraph --help
```

**Output:**
```
usage: collagraph [-h] [--renderer {pyside,pygfx,dict}] [--state STATE] component

Run collagraph components directly

positional arguments:
  component             Path to component to render

options:
  -h, --help            show this help message and exit
  --renderer {pyside,pygfx,dict}
                        The type of renderer to use (default: pyside)
  --state STATE         Optional state/props to load (json file or string)
                        (default: None)
```

## Complete Examples

### Basic Usage

**counter.cgx:**
```xml
<template>
  <widget>
    <label :text="f'Count: {count}'" />
    <button text="Increment" @clicked="increment" />
  </widget>
</template>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1
</script>
```

**Run it:**
```bash
python -m collagraph counter.cgx
```

---

### With Initial State

**todo_list.cgx:**
```xml
<template>
  <widget>
    <label :text="title" />
    <div v-for="item in items" :key="item.id">
      <label :text="item.text" />
    </div>
  </widget>
</template>

<script>
import collagraph as cg

class TodoList(cg.Component):
    def init(self):
        self.state["title"] = self.props.get("title", "Todo List")
        self.state["items"] = self.props.get("items", [])
</script>
```

**initial_state.json:**
```json
{
  "title": "My Tasks",
  "items": [
    {"id": 1, "text": "Learn Collagraph"},
    {"id": 2, "text": "Build an app"}
  ]
}
```

**Run it:**
```bash
python -m collagraph --state initial_state.json todo_list.cgx
```

---

### Using Dict Renderer for Debugging

```bash
python -m collagraph --renderer dict app.cgx
```

**What happens:**
1. Component is rendered to a dictionary
2. Drops into Python debugger
3. Inspect the container:

```python
(Pdb) container
{'root': {'type': 'widget', 'children': [...]}}

(Pdb) from collagraph.renderers.dict_renderer import format_dict
(Pdb) print(format_dict(container['root']))
<widget>
  <label text="Hello, World!" />
  <button text="Click me" />
</widget>
```

---

### Using Pygfx Renderer

**point_cloud.cgx:**
```xml
<template>
  <mesh>
    <geometry type="points" :positions="positions" />
    <material type="points" size=10 />
  </mesh>
</template>

<script>
import collagraph as cg
import numpy as np

class PointCloud(cg.Component):
    def init(self):
        # Generate random points
        self.state["positions"] = np.random.rand(1000, 3) * 10
</script>
```

**Run it:**
```bash
python -m collagraph --renderer pygfx point_cloud.cgx
```

## Implementation Details

The CLI uses `argparse` for argument parsing and performs the following steps:

1. **Parse arguments** - Validate component file and options
2. **Load component** - Import the `.cgx` file as a module
3. **Create renderer** - Instantiate the appropriate renderer
4. **Setup container** - Create renderer-specific container
5. **Initialize Collagraph** - Create `Collagraph` instance
6. **Render component** - Call `gui.render()` with component and state
7. **Run event loop** - Execute renderer-specific event loop

**Source Code Location:** `/home/user/collagraph/collagraph/__main__.py`

## Programmatic Alternative

Instead of using the CLI, you can run components programmatically:

```python
from PySide6 import QtWidgets
import collagraph as cg
from my_app import MyAppComponent  # Imported from my_app.cgx

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    gui = cg.Collagraph(renderer=cg.PySideRenderer())
    gui.render(
        MyAppComponent,
        app,
        state={"title": "My App", "count": 5}
    )
    app.exec()
```

This gives you more control over:
- Application setup
- Custom renderers
- Event loop configuration
- Integration with existing applications

## Troubleshooting

### Error: "does not exist"

```
error: argument component: /path/to/file.cgx does not exist
```

**Solution:** Check that the file path is correct and the file exists.

---

### Error: "is not a collagraph component"

```
error: argument component: /path/to/file.txt is not a collagraph component
```

**Solution:** Ensure the file has a `.cgx` extension.

---

### Error: "is not valid json"

```
error: argument --state: {"invalid": } is not valid json
```

**Solution:** Check JSON syntax. Ensure proper quoting:
```bash
# Correct
python -m collagraph --state '{"key": "value"}' app.cgx

# Incorrect (shell may parse quotes incorrectly)
python -m collagraph --state {"key": "value"} app.cgx
```

---

### Renderer not available

```
python -m collagraph --renderer pygfx app.cgx
# Error: argument --renderer: invalid choice: 'pygfx'
```

**Solution:** Install the required dependencies:
```bash
pip install pygfx rendercanvas
```

Only renderers with installed dependencies are shown as available choices.

## See Also

- [Quick Start](../getting-started/quick-start.md)
- [Hot Reloading](../guides/hot-reloading.md)
