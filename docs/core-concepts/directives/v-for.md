# List Rendering (v-for)

## Overview

The `v-for` directive renders a list of elements by iterating over an array or any Python iterable. It's one of the most powerful features in Collagraph, enabling dynamic lists that automatically update when the underlying data changes.

## Basic Usage

The simplest form of `v-for` iterates over a list and renders an element for each item:

```html
<label v-for="item in items" :text="item" />
```

This will create a label for each item in the `items` list. The `item` variable is available within the scope of the element and its children.

### Working with Object Properties

When iterating over objects (dictionaries), you can access their properties:

```html
<label v-for="user in users" :text="user['name']" />
```

## Accessing the Index

You can access the index (position) of each item using tuple unpacking with `enumerate()`:

```html
<label v-for="i, item in enumerate(items)" :text="f'{i}: {item}'" />
```

The index starts at 0, following Python conventions.

## Using Keys for Performance

When rendering lists, it's highly recommended to provide a unique key for each item using the `:key` attribute. Keys help Collagraph identify which items have changed, been added, or been removed:

```html
<label
  v-for="item in items"
  :key="item['id']"
  :text="item['name']"
/>
```

### Why Keys Matter

Keys serve several important purposes:

**1. Element Identity Preservation**

With keys, Collagraph can track which DOM elements correspond to which data items. When the list is reordered, elements are moved rather than recreated:

```python
# Without keys: elements are updated in place
# With keys: elements are moved to their new positions
```

**2. Component State Preservation**

When rendering components in a list, keys ensure that each component instance is preserved when the list changes:

```html
<Counter
  v-for="item in items"
  :key="item['id']"
  :initial="item['count']"
/>
```

If the list is reordered, each `Counter` component maintains its internal state because Collagraph tracks them by key.

**3. Performance Optimization**

Keyed lists enable efficient reconciliation. When items are added, removed, or reordered, Collagraph performs minimal DOM operations:

```python
# Reordering ["a", "b", "c"] to ["c", "b", "a"]
# With keys: moves 2 elements
# Without keys: updates content of all 3 elements
```

### What Makes a Good Key

Keys should be:
- **Unique**: Each item must have a unique key
- **Stable**: The same item should always have the same key
- **Primitive**: Use strings or numbers, not objects

**Good keys:**
```html
<item v-for="user in users" :key="user['id']" />
<item v-for="product in products" :key="product['sku']" />
<item v-for="item in items" :key="str(item['category']) + '_' + str(item['id'])" />
```

**Bad keys (avoid):**
```html
<!-- Using index as key (loses tracking on reorder) -->
<item v-for="i, user in enumerate(users)" :key="i" />

<!-- Using mutable objects -->
<item v-for="item in items" :key="item" />
```

### Duplicate Keys Error

Collagraph will raise a `RuntimeError` if duplicate keys are detected:

```python
items = [
    {"id": 1, "name": "First"},
    {"id": 1, "name": "Duplicate!"},  # Same key!
]
# RuntimeError: Duplicate keys found: 1
```

## Iterating Over Different Types

### Lists and Tuples

```html
<label v-for="color in ['red', 'green', 'blue']" :text="color" />
```

### Ranges

```html
<label v-for="i in range(10)" :text="str(i)" />
<label v-for="i in range(1, 100, 10)" :text="f'Value: {i}'" />
```

### Enumerations

```html
<label
  v-for="idx, text in enumerate(['First', 'Second', 'Third'])"
  :text="f'{idx + 1}. {text}'"
/>
```

### Complex Expressions

You can use any Python expression that returns an iterable:

```html
<label
  v-for="idx, (label, suffix) in enumerate(zip(labels, suffixes))"
  :key="idx"
  :text="f'{label} {suffix}'"
/>
```

### Dictionary Iteration

While you can iterate over dictionaries, it's typically better to iterate over `.items()`:

```python
# In component
data = {"name": "Alice", "age": 30, "role": "admin"}
```

```html
<label v-for="key, value in data.items()" :text="f'{key}: {value}'" />
```

## Nested v-for Loops

You can nest `v-for` directives to create multi-dimensional structures:

```html
<widget
  v-for="i, group in enumerate(groups)"
  :key="group['id']"
>
  <label :text="group['name']" />
  <item
    v-for="item in group['items']"
    :key="item['id']"
    :text="item['text']"
  />
</widget>
```

Each nested loop has access to variables from outer loops:

```html
<widget v-for="category in categories" :key="category['id']">
  <label
    v-for="product in category['products']"
    :key="product['id']"
    :text="f'{category['name']}: {product['name']}'"
  />
</widget>
```

## Rendering Elements with Children

Elements with `v-for` can contain child elements, and the loop variable is available to all descendants:

```html
<widget
  v-for="user in users"
  :key="user['id']"
>
  <label :text="user['name']" />
  <label :text="user['email']" />
  <button :text="f'Edit {user['name']}'" @clicked="lambda: edit_user(user)" />
</widget>
```

## Reactive Updates

Lists created with `v-for` are reactive. When you modify the source data, the rendered elements automatically update:

```python
from observ import reactive

class MyComponent(cg.Component):
    def init(self):
        self.state['items'] = reactive(['a', 'b', 'c'])

    def add_item(self):
        self.state['items'].append('d')  # Automatically updates the view

    def remove_item(self, index):
        self.state['items'].pop(index)  # Automatically updates the view

    def update_item(self, index, value):
        self.state['items'][index] = value  # Automatically updates the view
```

```html
<widget>
  <label
    v-for="i, item in enumerate(items)"
    :key="i"
    :text="item"
  />
  <button text="Add Item" @clicked="add_item" />
</widget>
```

Supported operations that trigger updates:
- `append(item)` - Add to end
- `insert(index, item)` - Insert at position
- `pop(index)` - Remove by index
- `remove(item)` - Remove by value
- `clear()` - Remove all items
- `items[index] = value` - Update by index
- `items = new_list` - Replace entire list

## v-for with Event Handlers

You can attach event handlers to elements in a `v-for` loop. Use lambdas to capture the loop variable:

```html
<button
  v-for="name in buttons"
  :key="name"
  :text="name"
  @clicked="lambda: on_button_clicked(name)"
/>
```

```python
class Buttons(cg.Component):
    def init(self):
        self.state['buttons'] = ['First', 'Second', 'Third']

    def on_button_clicked(self, name):
        print(f'Button {name} clicked')
```

Without the lambda, you can also pass method references:

```html
<button
  v-for="name, callback in button_configs"
  :key="name"
  :text="name"
  @clicked="callback"
/>
```

## Combining v-for with v-if

You can combine `v-for` with `v-if`, though be mindful of performance:

```html
<!-- v-if on container -->
<widget v-if="items">
  <label v-for="item in items" :key="item['id']" :text="item['name']" />
</widget>

<!-- v-if on items -->
<label
  v-for="item in all_items"
  v-if="item['visible']"
  :key="item['id']"
  :text="item['name']"
/>
```

However, filtering the list beforehand is often more efficient:

```python
def init(self):
    self.visible_items = [item for item in all_items if item['visible']]
```

```html
<label v-for="item in visible_items" :key="item['id']" :text="item['name']" />
```

## Multiple Consecutive v-for Lists

You can have multiple `v-for` directives in sequence:

```html
<widget>
  <label
    v-for="item in list_a"
    :key="f'a_{item['id']}'"
    :text="item['name']"
  />
  <label
    v-for="item in list_b"
    :key="f'b_{item['id']}'"
    :text="item['name']"
  />
</widget>
```

Make sure keys are unique across both lists by using prefixes or composite keys.

## Best Practices

### Always Use Keys for Dynamic Lists

When your list can change (items added, removed, or reordered), always provide a `:key`:

```html
<item
  v-for="product in products"
  :key="product['id']"
  :name="product['name']"
/>
```

### Use Stable, Unique Keys

Don't use the array index as a key if the list can be reordered:

**Avoid:**
```html
<item v-for="i, product in enumerate(products)" :key="i" />
```

**Prefer:**
```html
<item v-for="product in products" :key="product['id']" />
```

### Filter Data Before Rendering

Instead of using `v-if` on every item, filter your data first:

```python
def init(self):
    self.state['active_users'] = [u for u in users if u['active']]
```

```html
<user v-for="user in active_users" :key="user['id']" :name="user['name']" />
```

### Avoid Deep Nesting

If you find yourself nesting many `v-for` loops, consider extracting child lists into separate components:

**Instead of:**
```html
<category v-for="cat in categories">
  <group v-for="group in cat['groups']">
    <item v-for="item in group['items']">
      <!-- Complex markup -->
    </item>
  </group>
</category>
```

**Extract to components:**
```html
<Category v-for="cat in categories" :key="cat['id']" :category="cat" />
```

```html
<!-- Category.cgx -->
<category>
  <Group v-for="group in category['groups']" :key="group['id']" :group="group" />
</category>
```

### Use Meaningful Variable Names

Choose descriptive names for loop variables:

```html
<!-- Good -->
<user-card v-for="user in users" :key="user['id']" />
<product-item v-for="product in products" :key="product['sku']" />

<!-- Less clear -->
<user-card v-for="u in users" :key="u['id']" />
<product-item v-for="p in products" :key="p['sku']" />
```

## Edge Cases and Gotchas

### Empty Lists

An empty list renders nothing (no error):

```html
<label v-for="item in []" :text="item" />
<!-- Renders nothing -->
```

### Variable Name Conflicts

The loop variable shadows outer variables with the same name:

```html
<!-- item from outer scope -->
<widget v-for="group in groups">
  <!-- 'item' here refers to the loop variable, not outer 'item' -->
  <label v-for="item in group['items']" :text="item" />
</widget>
```

### Modifying List During Iteration

Be careful when modifying a list while iterating. Use reactive operations and let Collagraph handle the updates:

```python
# Correct: modify the reactive list
self.state['items'].append(new_item)

# Avoid: replacing with a new list loses reactivity if not reassigned properly
# Better to use clear() and extend() if you need to replace contents
```

### Very Large Lists

For lists with thousands of items, consider:
- Pagination or lazy loading
- Virtual scrolling (if supported by your renderer)
- Filtering data before rendering

```python
# Example: pagination
def init(self):
    self.state['page'] = 0
    self.state['page_size'] = 100

@property
def visible_items(self):
    start = self.state['page'] * self.state['page_size']
    end = start + self.state['page_size']
    return self.all_items[start:end]
```

## Common Patterns

### Rendering with Index Labels

```html
<label
  v-for="i, task in enumerate(tasks)"
  :text="f'{i + 1}. {task['title']}'"
/>
```

### Rendering Grouped Data

```html
<widget v-for="category in grouped_data" :key="category['name']">
  <label :text="category['name']" />
  <item
    v-for="item in category['items']"
    :key="item['id']"
    :text="item['title']"
  />
</widget>
```

### Rendering with Actions

```html
<widget v-for="user in users" :key="user['id']">
  <label :text="user['name']" />
  <button text="Edit" @clicked="lambda: edit_user(user)" />
  <button text="Delete" @clicked="lambda: delete_user(user['id'])" />
</widget>
```

### Alternating Styles

```html
<label
  v-for="i, item in enumerate(items)"
  :key="item['id']"
  :text="item['name']"
  :class="'even' if i % 2 == 0 else 'odd'"
/>
```

### Conditional Rendering in Lists

```html
<widget>
  <header v-if="items">
    <label :text="f'Total items: {len(items)}'" />
  </header>
  <item v-for="item in items" :key="item['id']" :data="item" />
  <footer v-if="not items">
    <label text="No items to display" />
  </footer>
</widget>
```

## Performance Comparison: Keyed vs Unkeyed

**Keyed lists:**
- Elements maintain identity through reordering
- DOM elements are moved, not recreated
- Component state is preserved
- Event handlers remain attached
- Best for dynamic lists that can be reordered

**Unkeyed lists:**
- Elements are updated in place
- Content is changed, but DOM elements stay in position
- Simpler reconciliation
- Best for static lists or lists that only change content

## See Also

- [Template Syntax](../template-syntax.md)
- [v-if Directive](v-if.md)
- [Reactivity](../reactivity.md)
- [Component Props](../props.md)
