# Example: 3D Visualization

An interactive 3D solar system visualization using the Pygfx renderer, demonstrating 3D graphics, animation, and user interaction.

## Overview

This example demonstrates how to create 3D visualizations with Collagraph using the Pygfx renderer. You'll learn how to create 3D meshes, apply materials, set up lighting, handle animations, respond to user interactions, and combine reactive state with 3D graphics.

### What You'll Learn

- How to use the Pygfx renderer
- How to create 3D meshes with geometries and materials
- How to set up lighting in a 3D scene
- How to animate 3D objects
- How to handle 3D pointer events (hover, click)
- How to integrate 3D graphics with reactive state
- How to structure a complete 3D application
- How to use camera controls

## Complete Code

Create a file called `solar_system.cgx`:

```html
<group>
  <!-- Lighting -->
  <ambient-light :intensity="0.3" />
  <point-light :local.position="[0, 0, 0]" :intensity="2.0" />

  <!-- Sun at center -->
  <mesh
    :geometry="sphere"
    :material="sun_material"
    :local.scale="[2, 2, 2]"
  />

  <!-- Planets -->
  <group
    v-for="planet in planets"
    :key="planet['name']"
    :local.rotation="planet['orbit_rotation']"
  >
    <mesh
      :local.position="planet['orbit_position']"
      :geometry="sphere"
      :material="planet['material']"
      :local.scale="planet['scale']"
      :local.rotation="planet['self_rotation']"
      @pointer_enter="lambda ev: hover_planet(planet['name'], True)"
      @pointer_leave="lambda ev: hover_planet(planet['name'], False)"
      @click="lambda ev: select_planet(planet['name'])"
    />
  </group>

  <!-- Orbit paths -->
  <line
    v-for="planet in planets"
    :key="f\"{planet['name']}_orbit\""
    :geometry="create_orbit_geometry(planet['distance'])"
    :material="orbit_line_material"
  />

  <!-- Info display (using a simple marker) -->
  <group v-if="selected_planet">
    <mesh
      :local.position="selected_planet_position"
      :geometry="marker_geometry"
      :material="marker_material"
    />
  </group>
</group>

<script>
import pygfx as gfx
from rendercanvas.auto import loop
import collagraph as cg
import math


# Create shared geometries
sphere = gfx.sphere_geometry(radius=1)
marker_geometry = gfx.cone_geometry(radius=0.2, height=0.5)

# Create materials
sun_material = gfx.MeshBasicMaterial(color=(1.0, 0.9, 0.2))
orbit_line_material = gfx.LineMaterial(color=(0.5, 0.5, 0.5), thickness=1)
marker_material = gfx.MeshBasicMaterial(color=(0, 1, 0))


class SolarSystem(cg.Component):
    def init(self):
        # Planet data
        self.state["planet_data"] = [
            {
                "name": "Mercury",
                "color": (0.7, 0.7, 0.7),
                "distance": 4,
                "size": 0.4,
                "orbit_speed": 0.04,
                "rotation_speed": 0.02,
            },
            {
                "name": "Venus",
                "color": (0.9, 0.7, 0.4),
                "distance": 6,
                "size": 0.6,
                "orbit_speed": 0.03,
                "rotation_speed": 0.015,
            },
            {
                "name": "Earth",
                "color": (0.2, 0.4, 0.8),
                "distance": 8,
                "size": 0.6,
                "orbit_speed": 0.02,
                "rotation_speed": 0.03,
            },
            {
                "name": "Mars",
                "color": (0.8, 0.3, 0.2),
                "distance": 10,
                "size": 0.5,
                "orbit_speed": 0.015,
                "rotation_speed": 0.025,
            },
        ]

        # Animation state
        self.state["time"] = 0.0
        self.state["paused"] = False

        # Interaction state
        self.state["hovered_planet"] = None
        self.state["selected_planet"] = None

        # Start animation loop
        self.animate()

    @property
    def planets(self):
        """Generate planet data with current positions."""
        result = []
        for planet_info in self.state["planet_data"]:
            # Calculate orbital angle
            orbit_angle = self.state["time"] * planet_info["orbit_speed"]

            # Calculate position
            distance = planet_info["distance"]
            x = distance * math.cos(orbit_angle)
            z = distance * math.sin(orbit_angle)

            # Self rotation
            self_rotation_angle = self.state["time"] * planet_info["rotation_speed"]

            # Check if this planet is hovered
            is_hovered = self.state["hovered_planet"] == planet_info["name"]
            is_selected = self.state["selected_planet"] == planet_info["name"]

            # Adjust color if hovered or selected
            color = planet_info["color"]
            if is_selected:
                # Brighten selected planet
                color = tuple(min(c * 1.5, 1.0) for c in color)
            elif is_hovered:
                # Slightly brighten hovered planet
                color = tuple(min(c * 1.2, 1.0) for c in color)

            result.append({
                "name": planet_info["name"],
                "orbit_position": [x, 0, z],
                "orbit_rotation": [0, orbit_angle, 0],
                "self_rotation": [0, self_rotation_angle, 0],
                "distance": distance,
                "scale": [planet_info["size"]] * 3,
                "material": gfx.MeshPhongMaterial(
                    color=color,
                    pick_write=True  # Enable mouse picking
                ),
            })

        return result

    @property
    def selected_planet_position(self):
        """Get position of selected planet for marker."""
        if not self.state["selected_planet"]:
            return [0, 0, 0]

        for planet in self.planets:
            if planet["name"] == self.state["selected_planet"]:
                pos = planet["orbit_position"]
                # Place marker above planet
                return [pos[0], pos[1] + 2, pos[2]]

        return [0, 0, 0]

    def create_orbit_geometry(self, radius):
        """Create a circular orbit path."""
        segments = 64
        points = []

        for i in range(segments + 1):
            angle = (i / segments) * 2 * math.pi
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            points.append([x, 0, z])

        return gfx.Geometry(positions=points)

    def hover_planet(self, planet_name, is_hovering):
        """Handle planet hover state."""
        if is_hovering:
            self.state["hovered_planet"] = planet_name
            print(f"Hovering over {planet_name}")
        else:
            if self.state["hovered_planet"] == planet_name:
                self.state["hovered_planet"] = None

    def select_planet(self, planet_name):
        """Handle planet selection."""
        if self.state["selected_planet"] == planet_name:
            self.state["selected_planet"] = None
            print(f"Deselected {planet_name}")
        else:
            self.state["selected_planet"] = planet_name
            print(f"Selected {planet_name}")

            # Print planet info
            for planet_info in self.state["planet_data"]:
                if planet_info["name"] == planet_name:
                    print(f"  Distance from sun: {planet_info['distance']}")
                    print(f"  Size: {planet_info['size']}")
                    print(f"  Orbit speed: {planet_info['orbit_speed']}")

    def toggle_pause(self):
        """Toggle animation pause."""
        self.state["paused"] = not self.state["paused"]

    def animate(self):
        """Animation loop."""
        if not self.state["paused"]:
            self.state["time"] += 0.016  # ~60 FPS

        # Schedule next frame
        loop.call_later(0.016, self.animate)
</script>
```

## Running the Example

### Standalone Application

Create a runner file `run_solar_system.py`:

```python
import pygfx as gfx
from rendercanvas.auto import RenderCanvas, loop
import collagraph as cg
from solar_system import SolarSystem

# Create canvas and renderer
canvas = RenderCanvas(size=(800, 600), title="Solar System")
renderer = gfx.renderers.WgpuRenderer(canvas)

# Set up camera
camera = gfx.PerspectiveCamera(60, 16 / 9)
camera.local.position = (0, 15, 20)
camera.show_pos((0, 0, 0))

# Add orbit controls
controls = gfx.OrbitController(camera, register_events=renderer)

# Create scene container
scene = gfx.Scene()

# Render callback
def animate():
    renderer.render(scene, camera)
    canvas.request_draw()

# Set up Collagraph
gui = cg.Collagraph(renderer=cg.PygfxRenderer())
gui.renderer.add_on_change_handler(lambda: canvas.request_draw(animate))
gui.render(SolarSystem, scene)

# Start loop
canvas.request_draw(animate)
loop.run()
```

Run with:

```bash
python run_solar_system.py
```

### Using the CLI

```bash
uv run collagraph --renderer pygfx solar_system.cgx
```

## Step-by-Step Breakdown

### 1. Scene Structure

```html
<group>
  <ambient-light />
  <point-light />
  <mesh />  <!-- Sun -->
  <group v-for="planet in planets">
    <mesh />  <!-- Planet -->
  </group>
</group>
```

The scene is organized hierarchically:
- Root group contains all objects
- Lights illuminate the scene
- Each planet is in its own group for rotation

### 2. Creating Geometries

```python
sphere = gfx.sphere_geometry(radius=1)
```

Geometries define the shape. We reuse the sphere geometry for all planets (scaled differently).

### 3. Materials

```python
sun_material = gfx.MeshBasicMaterial(color=(1.0, 0.9, 0.2))

planet_material = gfx.MeshPhongMaterial(
    color=planet_info["color"],
    pick_write=True  # Enable mouse interaction
)
```

Materials define appearance:
- `MeshBasicMaterial`: Unlit (for the sun)
- `MeshPhongMaterial`: Lit with specular highlights (for planets)

### 4. Transformations

```html
<mesh
  :local.position="planet['orbit_position']"
  :local.scale="planet['scale']"
  :local.rotation="planet['self_rotation']"
/>
```

Transform properties:
- `local.position`: Move object in 3D space
- `local.scale`: Resize object
- `local.rotation`: Rotate object

### 5. Animation Loop

```python
def animate(self):
    if not self.state["paused"]:
        self.state["time"] += 0.016

    loop.call_later(0.016, self.animate)
```

The animation:
- Updates `time` state every frame
- Planets' positions recalculate based on time
- Runs at ~60 FPS

### 6. Orbital Mechanics

```python
orbit_angle = self.state["time"] * planet_info["orbit_speed"]
x = distance * math.cos(orbit_angle)
z = distance * math.sin(orbit_angle)
```

Each planet orbits in a circle using trigonometry.

### 7. Interaction Events

```html
<mesh
  @pointer_enter="lambda ev: hover_planet(planet['name'], True)"
  @pointer_leave="lambda ev: hover_planet(planet['name'], False)"
  @click="lambda ev: select_planet(planet['name'])"
/>
```

3D objects can respond to:
- `@pointer_enter`: Mouse enters object
- `@pointer_leave`: Mouse leaves object
- `@click`: Object is clicked

### 8. Lighting

```html
<ambient-light :intensity="0.3" />
<point-light :local.position="[0, 0, 0]" :intensity="2.0" />
```

Lighting setup:
- Ambient light: Soft global illumination
- Point light: Sun at center casting light in all directions

### 9. Orbit Paths

```python
def create_orbit_geometry(self, radius):
    segments = 64
    points = []
    for i in range(segments + 1):
        angle = (i / segments) * 2 * math.pi
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        points.append([x, 0, z])
    return gfx.Geometry(positions=points)
```

Create custom geometry for orbit circles using line segments.

## How to Run

### Prerequisites

```bash
pip install collagraph[pygfx]
```

This installs:
- `pygfx`: 3D graphics library
- `wgpu`: GPU rendering backend
- `rendercanvas`: Window/canvas management

### Using the CLI

```bash
uv run collagraph --renderer pygfx solar_system.cgx
```

### Custom Runner

For more control (camera, controls, window size):

```python
import pygfx as gfx
from rendercanvas.auto import RenderCanvas, loop
import collagraph as cg
from solar_system import SolarSystem

canvas = RenderCanvas(size=(1024, 768))
renderer = gfx.renderers.WgpuRenderer(canvas)

camera = gfx.PerspectiveCamera(60, 16 / 9)
camera.local.position = (0, 20, 30)

controls = gfx.OrbitController(camera, register_events=renderer)

scene = gfx.Scene()

gui = cg.Collagraph(renderer=cg.PygfxRenderer())
gui.renderer.add_on_change_handler(lambda: canvas.request_draw())
gui.render(SolarSystem, scene)

def animate():
    renderer.render(scene, camera)

canvas.request_draw(animate)
loop.run()
```

## Key Concepts

### Pygfx Renderer

The Pygfx renderer translates Collagraph components into 3D objects:

```html
<mesh :geometry="sphere" :material="material" />
```

Becomes a `gfx.Mesh` object in the scene.

### 3D Transformations

Objects have local transforms:
- `local.position = [x, y, z]`
- `local.rotation = [x, y, z]` (Euler angles in radians)
- `local.scale = [x, y, z]`

### Material Properties

Materials control appearance:
- `color`: RGB tuple (0-1)
- `opacity`: Transparency (0-1)
- `pick_write`: Enable mouse interaction
- `emissive`: Self-illumination color
- `specular`, `shininess`: Reflection properties

### Animation with State

Animate by updating state over time:

```python
self.state["time"] += delta_time
```

Computed properties recalculate positions based on time.

### Camera and Controls

```python
camera = gfx.PerspectiveCamera(fov=60, aspect=16/9)
camera.local.position = (x, y, z)
camera.show_pos((0, 0, 0))  # Look at origin

controls = gfx.OrbitController(camera)
```

OrbitController provides:
- Mouse drag to rotate
- Scroll to zoom
- Right-drag to pan

## Possible Extensions

### 1. Add Moons

Add satellites orbiting planets:

```python
# In planet group
<group v-if="planet['has_moon']">
  <mesh
    :local.position="calculate_moon_position(planet)"
    :geometry="sphere"
    :local.scale="[0.2, 0.2, 0.2]"
  />
</group>
```

### 2. Add Planet Rotation Axis Tilt

Tilt planets for realism:

```python
planet["axis_tilt"] = 0.4  # radians

# Apply tilt before self-rotation
rotation = [planet["axis_tilt"], self_rotation_angle, 0]
```

### 3. Add Texture Mapping

Use images for planet surfaces:

```python
texture = gfx.Texture(image_data)
material = gfx.MeshPhongMaterial(
    map=texture,
    pick_write=True
)
```

### 4. Add Speed Control

Allow user to control animation speed:

```html
<slider
  :value="speed"
  :minimum="0"
  :maximum="5"
  @value-changed="lambda v: set_speed(v)"
/>
```

```python
self.state["speed"] = 1.0
self.state["time"] += 0.016 * self.state["speed"]
```

### 5. Add Information Panel

Use PySide overlay with planet info:

```html
<widget v-if="selected_planet">
  <v-box>
    <label :text="f'Planet: {selected_planet}'" />
    <label :text="f'Distance: {selected_planet_data[\"distance\"]}'" />
    <label :text="f'Size: {selected_planet_data[\"size\"]}'" />
  </v-box>
</widget>
```

### 6. Add Asteroid Belt

Render many small objects:

```python
@property
def asteroids(self):
    import random
    asteroids = []
    for i in range(200):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(12, 14)
        asteroids.append({
            "position": [
                distance * math.cos(angle),
                random.uniform(-0.5, 0.5),
                distance * math.sin(angle)
            ],
            "size": random.uniform(0.05, 0.15)
        })
    return asteroids
```

```html
<mesh
  v-for="(asteroid, i) in asteroids"
  :key="i"
  :local.position="asteroid['position']"
  :local.scale="[asteroid['size']] * 3"
  :geometry="sphere"
  :material="asteroid_material"
/>
```

### 7. Add Camera Animation

Animate camera to follow selected planet:

```python
def follow_planet(self, planet_name):
    planet = self.get_planet_by_name(planet_name)
    target_pos = planet["orbit_position"]
    # Smoothly move camera
    self.animate_camera_to(target_pos)
```

## Topics Covered

- Pygfx renderer setup and usage
- 3D mesh creation with geometry and materials
- Lighting (ambient, point)
- 3D transformations (position, rotation, scale)
- Animation loops with state updates
- 3D pointer events (hover, click)
- Orbital mechanics with trigonometry
- Custom geometry creation
- Material properties and picking
- Camera and orbit controls
- Combining reactive state with 3D graphics

## See Also

- [Pygfx Renderer](../renderers/pygfx.md)
- [State Management](../core-concepts/state-management.md)
- [v-for Directive](../core-concepts/directives/v-for.md)
- [Events](../core-concepts/events.md)
- [Computed Properties](../core-concepts/computed.md)
