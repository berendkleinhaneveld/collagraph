# Pygfx Renderer

The Pygfx renderer enables 3D graphics and scientific visualization using the [Pygfx library](https://github.com/pygfx/pygfx). It provides a reactive way to create and manipulate 3D scenes.

## Overview

The Pygfx renderer converts Collagraph components into Pygfx 3D objects. It supports:
- 3D meshes, lines, points, and volumes
- Materials and textures
- Lighting (ambient, point, directional, spot)
- Cameras and controls
- Events and interactions
- Integration with PySide for GUI applications

## Installation

```bash
pip install collagraph[pygfx]
```

This installs Collagraph with Pygfx and its dependencies including WGPU for GPU rendering.

## Basic 3D Scene

### Standalone Scene

```python
import collagraph as cg
import pygfx as gfx

class SimpleScene(cg.Component):
    def render(self):
        return {
            "type": "group",
            "children": [
                {
                    "type": "ambient-light",
                    "intensity": 0.5
                },
                {
                    "type": "point-light",
                    "local.position": (10, 10, 10)
                },
                {
                    "type": "mesh",
                    "geometry": gfx.sphere_geometry(radius=2),
                    "material": gfx.MeshPhongMaterial(color=(1, 0, 0))
                }
            ]
        }

# Run with pygfx renderer
app = cg.Collagraph(SimpleScene, cg.PygfxRenderer)
app.run()
```

```xml
<!-- scene.cgx -->
<group>
  <ambient-light :intensity="0.5" />
  <point-light :local.position="(10, 10, 10)" />
  <mesh
    :geometry="sphere_geometry"
    :material="red_material"
  />
</group>

<script>
import pygfx as gfx
import collagraph as cg

sphere_geometry = gfx.sphere_geometry(radius=2)
red_material = gfx.MeshPhongMaterial(color=(1, 0, 0))

class SimpleScene(cg.Component):
    pass
</script>
```

Run with: `collagraph --renderer pygfx scene.cgx`

## Available 3D Objects

### Mesh

3D objects with geometry and material.

**Attributes:**
- `geometry` - Geometry object (e.g., `gfx.sphere_geometry()`)
- `material` - Material object (e.g., `gfx.MeshPhongMaterial()`)
- `local.position` - Position tuple (x, y, z)
- `local.rotation` - Rotation (Quaternion or Euler angles)
- `local.scale` - Scale tuple (x, y, z)
- `visible` - Visibility (boolean)

**Events:**
- `@click` - Mouse click on object
- `@pointer-move` - Pointer movement over object
- `@pointer-enter` - Pointer enters object
- `@pointer-leave` - Pointer leaves object

```python
{
    "type": "mesh",
    "geometry": gfx.box_geometry(width=2, height=2, depth=2),
    "material": gfx.MeshPhongMaterial(color=(0, 1, 0)),
    "local.position": (0, 0, 0),
    "@click": self.handle_click
}
```

### Group

Container for organizing 3D objects.

```python
{
    "type": "group",
    "local.position": (5, 0, 0),
    "children": [
        {"type": "mesh", ...},
        {"type": "mesh", ...}
    ]
}
```

### Line

Line segments for wireframes or paths.

```python
{
    "type": "line",
    "geometry": gfx.Geometry(positions=points),
    "material": gfx.LineMaterial(color=(1, 1, 1))
}
```

### Points

Point cloud visualization.

```python
{
    "type": "points",
    "geometry": gfx.Geometry(positions=point_positions),
    "material": gfx.PointsMaterial(size=5, color=(1, 1, 1))
}
```

## Geometries

Pygfx provides built-in geometries:

```python
import pygfx as gfx

# Primitives
sphere = gfx.sphere_geometry(radius=1)
box = gfx.box_geometry(width=1, height=1, depth=1)
cylinder = gfx.cylinder_geometry(radius=1, height=2)
cone = gfx.cone_geometry(radius=1, height=2)
torus = gfx.torus_geometry(radius=1, tube_radius=0.3)
plane = gfx.plane_geometry(width=10, height=10)

# Custom geometry
custom = gfx.Geometry(
    positions=[[0, 0, 0], [1, 0, 0], [0, 1, 0]],  # Triangle vertices
    indices=[[0, 1, 2]]  # Triangle indices
)
```

## Materials

### Mesh Materials

**MeshPhongMaterial** - Shiny material with specular highlights:
```python
gfx.MeshPhongMaterial(
    color=(1, 0, 0),           # RGB color (0-1)
    emissive=(0, 0, 0),        # Emissive color
    specular=(1, 1, 1),        # Specular color
    shininess=30,              # Shininess value
    opacity=1.0,               # Transparency (0-1)
    pick_write=True            # Enable picking/interaction
)
```

**MeshBasicMaterial** - Simple unlit material:
```python
gfx.MeshBasicMaterial(
    color=(0, 1, 0),
    opacity=1.0,
    wireframe=False
)
```

**MeshStandardMaterial** - PBR material:
```python
gfx.MeshStandardMaterial(
    color=(1, 1, 1),
    metalness=0.5,
    roughness=0.5
)
```

### Line and Point Materials

**LineMaterial**:
```python
gfx.LineMaterial(
    color=(1, 1, 1),
    thickness=2
)
```

**PointsMaterial**:
```python
gfx.PointsMaterial(
    color=(1, 1, 1),
    size=5,
    size_space='screen'  # 'screen' or 'world'
)
```

## Lighting

### Ambient Light

Global ambient illumination:
```python
{
    "type": "ambient-light",
    "intensity": 0.5,
    "color": (1, 1, 1)
}
```

### Point Light

Omnidirectional light source:
```python
{
    "type": "point-light",
    "local.position": (10, 10, 10),
    "intensity": 1.0,
    "color": (1, 1, 1),
    "distance": 100,  # Max distance
    "decay": 2        # Light falloff
}
```

### Directional Light

Parallel light rays (like sunlight):
```python
{
    "type": "directional-light",
    "local.position": (5, 10, 5),
    "intensity": 1.0,
    "color": (1, 1, 1)
}
```

### Spot Light

Cone-shaped light:
```python
{
    "type": "spot-light",
    "local.position": (0, 10, 0),
    "intensity": 1.0,
    "angle": 0.5,     # Cone angle
    "penumbra": 0.1   # Softness
}
```

## Transformations

Use dot notation to set nested properties:

```python
{
    "type": "mesh",
    "geometry": sphere_geom,
    "material": material,
    # Position
    "local.position": (x, y, z),
    # Rotation (quaternion or Euler)
    "local.rotation": (x, y, z, w),
    # Scale
    "local.scale": (sx, sy, sz),
    # Or uniform scale
    "local.scale": 2.0
}
```

## Interactive Example

```python
import collagraph as cg
import pygfx as gfx

class InteractivePoint(cg.Component):
    def init(self):
        self.sphere_geom = gfx.sphere_geometry(radius=0.5)
        self.materials = {
            "default": gfx.MeshPhongMaterial(color=(1, 1, 1), pick_write=True),
            "selected": gfx.MeshPhongMaterial(color=(1, 0, 0), pick_write=True),
            "hovered": gfx.MeshPhongMaterial(color=(1, 0.6, 0), pick_write=True)
        }

    def render(self):
        material_key = (
            "selected" if self.props.get("selected", False)
            else "hovered" if self.props.get("hovered", False)
            else "default"
        )

        return {
            "type": "mesh",
            "geometry": self.sphere_geom,
            "material": self.materials[material_key],
            "local.position": self.props["position"],
            "@click": self.on_click,
            "@pointer-move": self.on_hover
        }

    def on_click(self, event):
        self.emit("selected", self.props["index"])

    def on_hover(self, event):
        self.emit("hovered", self.props["index"])


class PointCloud(cg.Component):
    def init(self):
        self.state["positions"] = [
            (0, 0, 0), (5, 0, 0), (0, 5, 0), (5, 5, 0)
        ]
        self.state["selected"] = -1
        self.state["hovered"] = -1

    def render(self):
        return {
            "type": "group",
            "children": [
                {"type": "ambient-light", "intensity": 0.5},
                {"type": "point-light", "local.position": (10, 10, 10)},
                {
                    "type": "group",
                    "children": [
                        {
                            "type": InteractivePoint,
                            "key": idx,
                            "index": idx,
                            "position": pos,
                            "selected": idx == self.state["selected"],
                            "hovered": idx == self.state["hovered"],
                            "@selected": self.set_selected,
                            "@hovered": self.set_hovered
                        }
                        for idx, pos in enumerate(self.state["positions"])
                    ]
                }
            ]
        }

    def set_selected(self, index):
        self.state["selected"] = index if self.state["selected"] != index else -1

    def set_hovered(self, index):
        self.state["hovered"] = index
```

## Combining with PySide

Integrate 3D graphics into Qt applications:

```python
from PySide6 import QtWidgets
from rendercanvas.qt import RenderCanvas
import pygfx as gfx
import collagraph as cg

class App3D(cg.Component):
    def render(self):
        return {
            "type": "window",
            "title": "3D Viewer",
            "children": [
                {
                    "type": "RenderWidget",
                    "scene": PointCloud,
                    "count": 100
                }
            ]
        }


class RenderWidget(cg.Component):
    def mounted(self):
        # Create Pygfx renderer
        renderer = gfx.renderers.WgpuRenderer(self.element)

        # Setup camera
        camera = gfx.PerspectiveCamera(60, 16 / 9)
        camera.local.z = 25

        # Add orbit controls
        controls = gfx.OrbitController(camera, register_events=renderer)

        # Create Collagraph instance for 3D scene
        self.gui = cg.Collagraph(renderer=cg.PygfxRenderer())
        container = gfx.Scene()

        # Render loop
        def animate():
            renderer.render(container, camera)

        # Re-render on changes
        self.gui.renderer.add_on_change_handler(
            lambda: self.element.request_draw(animate)
        )

        # Render the scene
        self.gui.render(self.props["scene"], container, state=self.props)

    def render(self):
        return {"type": "render-canvas", "minimum-height": 400, "minimum-width": 600}


# Register RenderCanvas with PySide renderer
pyside_renderer = cg.PySideRenderer()
pyside_renderer.register_element("RenderCanvas", RenderCanvas)

app = cg.Collagraph(App3D, pyside_renderer)
app.run()
```

## Performance Tips

1. **Reuse geometries and materials** - Create them once and reference them
2. **Use instancing** for many identical objects
3. **Limit pick_write** - Only enable on interactive objects
4. **Frustum culling** - Objects outside camera view are automatically culled
5. **LOD (Level of Detail)** - Use simpler geometries for distant objects

## See Also

- [3D Graphics Guide](../guides/pygfx-3d.md)
- [Examples](../examples/3d-visualization.md)
