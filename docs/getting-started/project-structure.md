# Project Structure

## Recommended Structure

Here's a typical Collagraph project structure:

```
my-app/
├── main.cgx                 # Entry point component
├── components/              # Reusable components
│   ├── __init__.py
│   ├── button.cgx
│   ├── input.cgx
│   └── card.cgx
├── views/                   # Page/view components
│   ├── __init__.py
│   ├── home.cgx
│   ├── settings.cgx
│   └── about.cgx
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── helpers.py
├── assets/                  # Static assets
│   ├── images/
│   └── styles/
├── requirements.txt         # Dependencies
└── README.md
```

## Simple App Structure

For small applications, a flat structure works well:

```
my-app/
├── main.cgx
├── counter.cgx
├── todo_list.cgx
└── requirements.txt
```

## Module Organization

### Components Directory

Store reusable UI components:

```
components/
├── __init__.py
├── forms/
│   ├── __init__.py
│   ├── text_input.cgx
│   ├── checkbox.cgx
│   └── select.cgx
├── layout/
│   ├── __init__.py
│   ├── header.cgx
│   ├── sidebar.cgx
│   └── footer.cgx
└── ui/
    ├── __init__.py
    ├── button.cgx
    ├── card.cgx
    └── modal.cgx
```

### Views Directory

Store page-level components:

```
views/
├── __init__.py
├── dashboard.cgx
├── user_profile.cgx
└── settings.cgx
```

## Importing Components

### From Same Directory

```python
from .counter import Counter
```

### From Subdirectory

```python
from .components.button import Button
from .components.forms.text_input import TextInput
```

### From Package

```python
from my_app.components import Button, Card
from my_app.views import Dashboard
```

## Entry Point

Create a main entry point for your app:

**main.py:**
```python
import collagraph as cg
from collagraph.renderers import PySideRenderer
from .app import App

if __name__ == "__main__":
    app = cg.Collagraph(App, PySideRenderer)
    app.run()
```

Or run a `.cgx` file directly:

```bash
python -m collagraph main.cgx
```

## Configuration Files

### requirements.txt

```txt
collagraph>=0.8.11
PySide6>=6.6.2
# Add other dependencies
```

### pyproject.toml

For packaging your app:

```toml
[project]
name = "my-app"
version = "0.1.0"
dependencies = [
    "collagraph>=0.8.11",
    "PySide6>=6.6.2",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Best Practices

1. **Keep components small and focused** - Each component should do one thing well
2. **Use descriptive names** - Name components after what they represent, not how they look
3. **Organize by feature** - Group related components together
4. **Separate concerns** - Keep business logic separate from UI components
5. **Use `.cgx` for UI components** - Use pure Python for utilities and business logic

## Next Steps

- Learn about [Components](../core-concepts/components.md)
- Explore [Code Organization](../guides/code-organization.md)
