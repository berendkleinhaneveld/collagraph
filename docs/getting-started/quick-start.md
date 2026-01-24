# Quick Start

This guide will help you create your first Collagraph application in minutes.

## Your First App

Create a file called `counter.cgx`:

```html
<window title="Counter App">
  <v-box>
    <label :text="f'Count: {count}'" />
    <button text="Increment" @clicked="increment" />
  </v-box>
</window>

<script>
import collagraph as cg

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1
</script>
```

## Run Your App

```bash
python -m collagraph counter.cgx
```

That's it! You should see a window with a label showing the count and a button to increment it.

## What's Happening?

1. **Template**: The HTML-like syntax defines your UI structure
2. **Reactive Binding**: `:text` binds the label's text to a reactive expression
3. **Event Handling**: `@clicked` connects the button click to a method
4. **State Management**: `self.state` is a reactive dictionary that triggers re-renders

## Using Pure Python

You can also write Collagraph apps without `.cgx` files:

```python
import collagraph as cg
from collagraph.renderers import PySideRenderer

class Counter(cg.Component):
    def init(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1

    def render(self):
        return {
            "type": "window",
            "title": "Counter App",
            "children": [
                {
                    "type": "v-box",
                    "children": [
                        {
                            "type": "label",
                            "text": f"Count: {self.state['count']}"
                        },
                        {
                            "type": "button",
                            "text": "Increment",
                            "on_clicked": self.increment
                        }
                    ]
                }
            ]
        }

if __name__ == "__main__":
    app = cg.Collagraph(Counter, PySideRenderer)
    app.run()
```

## Next Steps

- Learn about [Components](../core-concepts/components.md)
- Explore [Template Syntax](../core-concepts/template-syntax.md)
- Check out more [Examples](../examples/counter.md)
