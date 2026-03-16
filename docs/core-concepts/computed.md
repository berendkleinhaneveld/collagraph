# Computed Properties

## Overview

Computed properties are reactive values that are automatically derived from other reactive data. They are powered by the [observ](https://github.com/fork-tongue/observ) library and provide an efficient way to calculate values based on component state or props without manual tracking.

Computed properties are **cached** and only re-evaluated when their reactive dependencies change, making them more efficient than calling methods repeatedly.

## Creating Computed Properties

### Using Python Properties

The simplest way to create computed properties is using Python's `@property` decorator:

```python
import collagraph as cg

class ShoppingCart(cg.Component):
    def init(self):
        self.state["items"] = []

    @property
    def total(self):
        """Computed property: sum of all item prices"""
        return sum(item["price"] * item["quantity"] for item in self.state["items"])

    @property
    def item_count(self):
        """Computed property: total number of items"""
        return sum(item["quantity"] for item in self.state["items"])
```

Use computed properties in templates like regular variables:

```html
<widget>
  <label :text="f'Total: ${total:.2f}'" />
  <label :text="f'Items: {item_count}'" />
</widget>
```

### Using `observ.computed()`

For more advanced use cases, you can use the `computed()` function from the `observ` library:

```python
from observ import computed
import collagraph as cg

class DataAnalyzer(cg.Component):
    def init(self):
        self.state["numbers"] = [1, 2, 3, 4, 5]

        # Create computed property explicitly
        self.average = computed(lambda: sum(self.state["numbers"]) / len(self.state["numbers"]))

        # Access value with .value
        print(f"Average: {self.average.value}")
```

In templates:

```html
<label :text="f'Average: {average.value:.2f}'" />
```

## Reactive Dependencies

Computed properties automatically track their dependencies:

```python
class TodoList(cg.Component):
    def init(self):
        self.state["todos"] = [
            {"text": "Task 1", "completed": False},
            {"text": "Task 2", "completed": True},
            {"text": "Task 3", "completed": False},
        ]

    @property
    def completed_count(self):
        """Automatically depends on state["todos"]"""
        return sum(1 for todo in self.state["todos"] if todo["completed"])

    @property
    def incomplete_count(self):
        """Depends on state["todos"] and computed property completed_count"""
        return len(self.state["todos"]) - self.completed_count

    @property
    def completion_percentage(self):
        """Computed from other computed properties"""
        total = len(self.state["todos"])
        if total == 0:
            return 0
        return (self.completed_count / total) * 100
```

When `self.state["todos"]` changes, all dependent computed properties automatically update.

## Caching and Performance

### Automatic Caching

Computed properties are cached and only re-evaluated when dependencies change:

```python
class ExpensiveCalculation(cg.Component):
    def init(self):
        self.state["data"] = list(range(10000))
        self.computation_count = 0

    @property
    def processed_data(self):
        """This only runs when state["data"] changes"""
        self.computation_count += 1
        print(f"Computing... (count: {self.computation_count})")

        # Expensive operation
        return [x * 2 for x in self.state["data"]]
```

Even if you access `processed_data` multiple times in your template, it only calculates once per change.

### Computed vs Methods

Use **computed properties** when:
- The value is derived from reactive state
- The calculation is expensive
- You access the value multiple times
- You want automatic caching

Use **methods** when:
- The value depends on non-reactive data
- You need to pass arguments
- You want to force recalculation each time

```python
class Example(cg.Component):
    def init(self):
        self.state["items"] = []

    # ✅ Computed: Cached, reactive
    @property
    def item_count(self):
        return len(self.state["items"])

    # ✅ Method: Accepts arguments
    def get_items_by_category(self, category):
        return [item for item in self.state["items"] if item["category"] == category]

    # ❌ Method when computed would be better
    def get_total(self):
        # This recalculates every time, even if items didn't change
        return sum(item["price"] for item in self.state["items"])

    # ✅ Better as computed
    @property
    def total(self):
        # Cached until items change
        return sum(item["price"] for item in self.state["items"])
```

## Common Patterns

### Filtering Lists

```python
class UserList(cg.Component):
    def init(self):
        self.state["users"] = []
        self.state["search_query"] = ""

    @property
    def filtered_users(self):
        """Filter users based on search query"""
        query = self.state["search_query"].lower()
        if not query:
            return self.state["users"]

        return [
            user for user in self.state["users"]
            if query in user["name"].lower() or query in user["email"].lower()
        ]
```

Template:

```html
<line-edit
  placeholder="Search users..."
  @text-changed="lambda: state.__setitem__('search_query', refs['search'].text())"
  ref="search"
/>

<user-card
  v-for="user in filtered_users"
  :key="user['id']"
  v-bind="user"
/>
```

### Sorting Lists

```python
class SortableList(cg.Component):
    def init(self):
        self.state["items"] = []
        self.state["sort_by"] = "name"
        self.state["sort_order"] = "asc"

    @property
    def sorted_items(self):
        """Sort items based on current sort settings"""
        items = self.state["items"].copy()
        reverse = self.state["sort_order"] == "desc"

        return sorted(
            items,
            key=lambda item: item[self.state["sort_by"]],
            reverse=reverse
        )
```

### Aggregations

```python
class SalesData(cg.Component):
    def init(self):
        self.state["sales"] = []

    @property
    def total_revenue(self):
        return sum(sale["amount"] for sale in self.state["sales"])

    @property
    def average_sale(self):
        if not self.state["sales"]:
            return 0
        return self.total_revenue / len(self.state["sales"])

    @property
    def top_sale(self):
        if not self.state["sales"]:
            return None
        return max(self.state["sales"], key=lambda s: s["amount"])

    @property
    def sales_by_category(self):
        """Group sales by category"""
        from collections import defaultdict
        result = defaultdict(list)
        for sale in self.state["sales"]:
            result[sale["category"]].append(sale)
        return dict(result)
```

### Boolean Flags

```python
class FormValidator(cg.Component):
    def init(self):
        self.state["username"] = ""
        self.state["email"] = ""
        self.state["password"] = ""

    @property
    def is_username_valid(self):
        return len(self.state["username"]) >= 3

    @property
    def is_email_valid(self):
        return "@" in self.state["email"]

    @property
    def is_password_valid(self):
        return len(self.state["password"]) >= 8

    @property
    def is_form_valid(self):
        """Derived from other computed properties"""
        return (
            self.is_username_valid
            and self.is_email_valid
            and self.is_password_valid
        )
```

Template:

```html
<button
  text="Submit"
  :enabled="is_form_valid"
  @clicked="submit"
/>
```

### Data Transformations

```python
class DataFormatter(cg.Component):
    def init(self):
        self.state["raw_data"] = []

    @property
    def formatted_data(self):
        """Transform raw data into displayable format"""
        return [
            {
                "id": item["id"],
                "display_name": f"{item['first_name']} {item['last_name']}",
                "email": item["email"].lower(),
                "joined_date": format_date(item["created_at"]),
                "status_label": "Active" if item["active"] else "Inactive"
            }
            for item in self.state["raw_data"]
        ]
```

## Advanced: Computed with Dependencies

### Chaining Computed Properties

Computed properties can depend on other computed properties:

```python
class Statistics(cg.Component):
    def init(self):
        self.state["values"] = [10, 20, 30, 40, 50]

    @property
    def sum(self):
        return sum(self.state["values"])

    @property
    def count(self):
        return len(self.state["values"])

    @property
    def average(self):
        """Depends on sum and count (both computed)"""
        if self.count == 0:
            return 0
        return self.sum / self.count

    @property
    def variance(self):
        """Depends on average (computed)"""
        if self.count == 0:
            return 0
        avg = self.average
        return sum((x - avg) ** 2 for x in self.state["values"]) / self.count

    @property
    def std_deviation(self):
        """Depends on variance (computed)"""
        return self.variance ** 0.5
```

### Computed from Props

Computed properties can derive from props:

```python
class UserDisplay(cg.Component):
    @property
    def full_name(self):
        """Compute from props"""
        first = self.props.get("first_name", "")
        last = self.props.get("last_name", "")
        return f"{first} {last}".strip()

    @property
    def display_email(self):
        """Format email from props"""
        email = self.props.get("email", "")
        return email.lower()
```

### Computed with External Data

```python
class CurrencyConverter(cg.Component):
    def init(self):
        self.state["amount"] = 0
        self.state["from_currency"] = "USD"
        self.state["to_currency"] = "EUR"

        # External exchange rates
        self.exchange_rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.73,
        }

    @property
    def converted_amount(self):
        """Compute using state and external data"""
        from_rate = self.exchange_rates[self.state["from_currency"]]
        to_rate = self.exchange_rates[self.state["to_currency"]]

        usd_amount = self.state["amount"] / from_rate
        return usd_amount * to_rate
```

## Using `computed()` Explicitly

For more control, use the `computed()` function:

```python
from observ import computed

class AdvancedComponent(cg.Component):
    def init(self):
        self.state["a"] = 1
        self.state["b"] = 2

        # Create computed value
        self.sum_value = computed(lambda: self.state["a"] + self.state["b"])

        # Create computed with transformation
        self.doubled = computed(lambda: self.sum_value.value * 2)

    def get_values(self):
        # Access with .value
        print(f"Sum: {self.sum_value.value}")
        print(f"Doubled: {self.doubled.value}")
```

## Best Practices

### 1. Use Properties for Simple Computations

For most cases, Python properties are cleaner:

```python
# ✅ Good: Simple and clean
@property
def full_name(self):
    return f"{self.state['first']} {self.state['last']}"

# ❌ Unnecessary: Too complex
from observ import computed

def init(self):
    self.full_name = computed(
        lambda: f"{self.state['first']} {self.state['last']}"
    )
```

### 2. Keep Computed Properties Pure

Computed properties should not have side effects:

```python
# ❌ Bad: Has side effect
@property
def total(self):
    result = sum(self.state["items"])
    print("Calculating total")  # Side effect!
    return result

# ✅ Good: Pure computation
@property
def total(self):
    return sum(self.state["items"])
```

### 3. Name Computed Properties Clearly

Use descriptive names that indicate they are derived values:

```python
# ✅ Good names
@property
def filtered_items(self): ...

@property
def total_price(self): ...

@property
def is_valid(self): ...

# ❌ Less clear
@property
def items(self): ...  # Unclear if computed or state

@property
def value(self): ...  # Too generic
```

### 4. Avoid Expensive Computations

If a computation is very expensive, consider:
- Debouncing updates
- Caching results separately
- Using web workers or threads for heavy processing

```python
# For expensive computations
def init(self):
    self.cached_result = None
    self.last_input = None

@property
def expensive_result(self):
    current_input = self.state["data"]

    # Only recalculate if input changed
    if current_input != self.last_input:
        self.cached_result = expensive_computation(current_input)
        self.last_input = current_input

    return self.cached_result
```

### 5. Document Complex Computed Properties

Add docstrings to explain what the computed property calculates:

```python
@property
def risk_score(self):
    """
    Calculate risk score based on multiple factors.

    Returns:
        float: Risk score from 0.0 (low) to 1.0 (high)

    Depends on:
        - state["transaction_amount"]
        - state["user_history"]
        - state["location"]
    """
    # Complex calculation...
    return score
```

### 6. Use Computed for Derived State

If data can be calculated from existing state, use computed properties instead of storing it:

```python
# ❌ Bad: Storing derived state
def init(self):
    self.state["items"] = []
    self.state["item_count"] = 0  # Redundant!

def add_item(self, item):
    self.state["items"].append(item)
    self.state["item_count"] = len(self.state["items"])  # Manual sync

# ✅ Good: Computed from state
def init(self):
    self.state["items"] = []

@property
def item_count(self):
    return len(self.state["items"])

def add_item(self, item):
    self.state["items"].append(item)
    # item_count updates automatically
```

## See Also

- [Reactivity System](reactivity.md)
- [Watchers](watchers.md)
