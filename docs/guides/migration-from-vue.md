# Migration from Vue.js

This guide helps Vue.js developers transition to Collagraph by highlighting similarities, differences, and equivalent patterns.

## Overview

Collagraph is heavily inspired by Vue.js, making the transition smooth for Vue developers. If you know Vue, you'll feel right at home with Collagraph.

**Key Similarity:** Both use reactive state, component-based architecture, and declarative templates.

**Key Difference:** Collagraph is Python-based and designed for desktop/graphics applications, not web browsers.

## Template Syntax Comparison

### Basic Directives

| Feature | Vue 3 | Collagraph |
|---------|-------|------------|
| Text binding | `{{ message }}` | `:text="message"` |
| Attribute binding | `:href="url"` | `:href="url"` ✓ Same |
| Event handling | `@click="handler"` | `@clicked="handler"` |
| Conditional | `v-if="show"` | `v-if="show"` ✓ Same |
| List rendering | `v-for="item in items"` | `v-for="item in items"` ✓ Same |
| Two-way binding | `v-model="value"` | Manual (see below) |

### Text Interpolation

**Vue:**
```html
<div>{{ message }}</div>
<div>{{ count + 1 }}</div>
<div>{{ user.name }}</div>
```

**Collagraph:**
```html
<label :text="message" />
<label :text="count + 1" />
<label :text="user['name']" />
```

**Note:** Collagraph uses attribute binding (`:text`) instead of mustache syntax because it renders to native widgets, not HTML.

### v-bind

**Vue & Collagraph:** Same syntax! ✓

```html
<!-- Both frameworks -->
<component :prop="value" />
<component v-bind="object" />
```

### v-on Events

**Vue:**
```html
<button @click="handleClick">Click</button>
<input @input="handleInput" />
```

**Collagraph:**
```html
<button @clicked="handleClick" text="Click" />
<lineedit @text-changed="handleInput" />
```

**Difference:** Event names match the underlying widget signals (e.g., `clicked` for Qt buttons).

### v-if / v-else

**Vue & Collagraph:** Same! ✓

```html
<!-- Both frameworks -->
<div v-if="loading">Loading...</div>
<div v-else-if="error">Error!</div>
<div v-else>Content</div>
```

### v-for

**Vue & Collagraph:** Nearly identical! ✓

**Vue:**
```html
<div v-for="item in items" :key="item.id">
  {{ item.name }}
</div>
```

**Collagraph:**
```html
<widget v-for="item in items" :key="item['id']">
  <label :text="item['name']" />
</widget>
```

**Difference:** Use dictionary syntax (`item['name']`) instead of dot notation in Collagraph.

### v-model (Two-Way Binding)

**Vue:**
```html
<input v-model="username" />
```

**Collagraph:**
```html
<!-- Manual two-way binding -->
<lineedit
  :text="username"
  @text-changed="text => state['username'] = text"
/>
```

**Difference:** Collagraph doesn't have `v-model`. Implement manually with prop + event.

## Component Structure Comparison

### Component Definition

**Vue 3 (Options API):**
```vue
<template>
  <div>{{ message }}</div>
</template>

<script>
export default {
  data() {
    return {
      message: 'Hello'
    }
  },
  methods: {
    greet() {
      console.log(this.message)
    }
  }
}
</script>
```

**Collagraph:**
```html
<label :text="message" />

<script>
import collagraph as cg

class MyComponent(cg.Component):
    def init(self):
        self.state["message"] = "Hello"

    def greet(self):
        print(self.state["message"])
</script>
```

### Props

**Vue:**
```javascript
export default {
  props: {
    title: String,
    count: {
      type: Number,
      default: 0
    }
  }
}
```

**Collagraph:**
```python
class MyComponent(cg.Component):
    def init(self):
        # Access props
        self.state["title"] = self.props.get("title", "")
        self.state["count"] = self.props.get("count", 0)
```

**Difference:** Collagraph doesn't enforce prop types (Python is dynamically typed).

### Emitting Events

**Vue:**
```javascript
export default {
  methods: {
    handleClick() {
      this.$emit('clicked', someData)
    }
  }
}
```

**Collagraph:**
```python
class MyComponent(cg.Component):
    def handle_click(self):
        self.emit('clicked', some_data)
```

**Note:** Nearly identical! ✓

## Lifecycle Hooks Comparison

| Vue 3 | Collagraph | Description |
|-------|------------|-------------|
| `setup()` | `init()` | Component initialization |
| `onMounted()` | `mounted()` | After mount to DOM |
| `onUpdated()` | `updated()` | After re-render |
| `onBeforeUnmount()` | `before_unmount()` | Before destroy |

**Vue 3 (Composition API):**
```javascript
import { onMounted, onBeforeUnmount } from 'vue'

export default {
  setup() {
    const timer = ref(null)

    onMounted(() => {
      timer.value = setInterval(() => {
        console.log('tick')
      }, 1000)
    })

    onBeforeUnmount(() => {
      clearInterval(timer.value)
    })
  }
}
```

**Collagraph:**
```python
class MyComponent(cg.Component):
    def mounted(self):
        self.timer = start_timer(1000, lambda: print('tick'))

    def before_unmount(self):
        cancel_timer(self.timer)
```

## Reactivity Comparison

### Reactive State

**Vue 3:**
```javascript
import { reactive } from 'vue'

const state = reactive({
  count: 0
})

state.count++ // Reactive
```

**Collagraph:**
```python
from observ import reactive

state = reactive({
    "count": 0
})

state["count"] += 1  # Reactive
```

**Note:** Collagraph uses the `observ` library, which works similarly to Vue's reactivity.

### Computed Properties

**Vue 3:**
```javascript
import { computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)
```

**Collagraph:**
```python
class MyComponent(cg.Component):
    def init(self):
        self.state["count"] = 0

    @property
    def doubled(self):
        return self.state["count"] * 2
```

### Watchers

**Vue 3:**
```javascript
import { watch } from 'vue'

watch(count, (newVal, oldVal) => {
  console.log(`Count changed from ${oldVal} to ${newVal}`)
})
```

**Collagraph:**
```python
from observ import watch

class MyComponent(cg.Component):
    def mounted(self):
        self.watchers = {}
        self.watchers["count"] = watch(
            lambda: self.state["count"],
            lambda new, old=None: print(f"Count: {old} → {new}")
        )

    def before_unmount(self):
        for watcher in self.watchers.values():
            watcher.stop()
```

## State Management Comparison

### Vuex vs Collagraph State

**Vuex (Vue):**
```javascript
import { createStore } from 'vuex'

const store = createStore({
  state: {
    count: 0
  },
  mutations: {
    increment(state) {
      state.count++
    }
  }
})
```

**Collagraph:**
```python
from observ import reactive

# Global store
store = reactive({
    "count": 0
})

# Actions
def increment():
    store["count"] += 1
```

## Composition API vs Python Patterns

### Composables (Vue) vs Mixins/Utilities (Collagraph)

**Vue 3 Composable:**
```javascript
// useCounter.js
import { ref } from 'vue'

export function useCounter() {
  const count = ref(0)

  function increment() {
    count.value++
  }

  return { count, increment }
}

// Component
import { useCounter } from './useCounter'

export default {
  setup() {
    const { count, increment } = useCounter()
    return { count, increment }
  }
}
```

**Collagraph Mixin:**
```python
# counter_mixin.py
class CounterMixin:
    def setup_counter(self):
        self.state["count"] = 0

    def increment(self):
        self.state["count"] += 1

# Component
class MyComponent(CounterMixin, cg.Component):
    def init(self):
        self.setup_counter()
```

## Provide/Inject

**Vue & Collagraph:** Same concept! ✓

**Vue:**
```javascript
// Ancestor
provide('theme', 'dark')

// Descendant
const theme = inject('theme')
```

**Collagraph:**
```python
# Ancestor
class Ancestor(cg.Component):
    def init(self):
        self.provide("theme", "dark")

# Descendant
class Descendant(cg.Component):
    def init(self):
        theme = self.inject("theme")
```

## Common Gotchas for Vue Developers

### 1. Dictionary Syntax Instead of Dot Notation

**Vue:**
```javascript
user.name
item.id
```

**Collagraph:**
```python
user["name"]
item["id"]
```

### 2. No v-model

**Vue:**
```html
<input v-model="text" />
```

**Collagraph:**
```html
<lineedit :text="text" @text-changed="t => state['text'] = t" />
```

### 3. Different Event Names

**Vue:** `@click`, `@input`, `@change`
**Collagraph:** `@clicked`, `@text-changed` (widget-specific)

### 4. No Template Refs Syntax

**Vue:**
```html
<input ref="myInput" />
```

**Collagraph:**
```html
<!-- Same! ✓ -->
<lineedit ref="myInput" />
```

### 5. Python Syntax in Templates

**Vue (JavaScript):**
```html
<div v-if="count > 0">{{ count }}</div>
```

**Collagraph (Python):**
```html
<label v-if="count > 0" :text="count" />
```

## Migration Checklist

When migrating from Vue to Collagraph:

- [ ] Replace `{{ }}` with `:text=""`
- [ ] Change `item.property` to `item['property']`
- [ ] Update event names to widget signals
- [ ] Replace `v-model` with manual binding
- [ ] Move `data()` to `init()`
- [ ] Convert computed to `@property`
- [ ] Update lifecycle hooks
- [ ] Replace `$emit` with `self.emit`
- [ ] Adapt provide/inject (minimal changes)

## Example: Complete Component Comparison

**Vue 3:**
```vue
<template>
  <div>
    <input v-model="newTodo" @keyup.enter="addTodo" />
    <ul>
      <li v-for="todo in todos" :key="todo.id">
        {{ todo.text }}
        <button @click="removeTodo(todo.id)">×</button>
      </li>
    </ul>
    <p>{{ remaining }} remaining</p>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  setup() {
    const newTodo = ref('')
    const todos = ref([])
    const nextId = ref(1)

    const remaining = computed(() =>
      todos.value.filter(t => !t.completed).length
    )

    function addTodo() {
      if (!newTodo.value) return

      todos.value.push({
        id: nextId.value++,
        text: newTodo.value,
        completed: false
      })
      newTodo.value = ''
    }

    function removeTodo(id) {
      todos.value = todos.value.filter(t => t.id !== id)
    }

    return { newTodo, todos, remaining, addTodo, removeTodo }
  }
}
</script>
```

**Collagraph:**
```html
<widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
  <lineedit
    :text="new_todo"
    @text-changed="t => state['new_todo'] = t"
    @return-pressed="add_todo"
  />
  <widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
    <widget
      v-for="todo in todos"
      :key="todo['id']"
      :layout="{'type': 'box', 'direction': 'left-to-right'}"
    >
      <label :text="todo['text']" />
      <button text="×" @clicked="lambda: remove_todo(todo['id'])" />
    </widget>
  </widget>
  <label :text="f'{remaining} remaining'" />
</widget>

<script>
import collagraph as cg

class TodoList(cg.Component):
    def init(self):
        self.state["new_todo"] = ""
        self.state["todos"] = []
        self.state["next_id"] = 1

    @property
    def remaining(self):
        return sum(1 for t in self.state["todos"] if not t["completed"])

    def add_todo(self):
        if not self.state["new_todo"]:
            return

        self.state["todos"].append({
            "id": self.state["next_id"],
            "text": self.state["new_todo"],
            "completed": False
        })
        self.state["next_id"] += 1
        self.state["new_todo"] = ""

    def remove_todo(self, id):
        self.state["todos"] = [
            t for t in self.state["todos"] if t["id"] != id
        ]
</script>
```

## See Also

- [Template Syntax](../core-concepts/template-syntax.md)
- [Components](../core-concepts/components.md)
- [Reactivity](../core-concepts/reactivity.md)
- [State Management](../core-concepts/state-management.md)
