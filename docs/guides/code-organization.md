# Code Organization

This guide provides best practices for organizing Collagraph projects, from simple single-file applications to large-scale applications with many components.

## Overview

Good code organization makes your application:
- **Easier to navigate** - Find files quickly
- **More maintainable** - Changes are localized
- **More testable** - Components are isolated
- **More reusable** - Components can be shared across projects

## Project Structure

### Small Project Structure

For simple applications with few components:

```
my_app/
├── app.cgx              # Main application component
├── components/          # Reusable components
│   ├── button.cgx
│   ├── input.cgx
│   └── modal.cgx
├── main.py             # Entry point
└── requirements.txt
```

**main.py:**
```python
from PySide6 import QtWidgets
import collagraph as cg
from app import App

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    gui = cg.Collagraph(renderer=cg.PySideRenderer())
    gui.render(App, app)
    app.exec()
```

### Medium Project Structure

For applications with multiple pages or features:

```
my_app/
├── app.cgx                 # Root component
├── components/             # Shared components
│   ├── layout/
│   │   ├── header.cgx
│   │   ├── footer.cgx
│   │   └── sidebar.cgx
│   ├── common/
│   │   ├── button.cgx
│   │   ├── input.cgx
│   │   ├── modal.cgx
│   │   └── spinner.cgx
│   └── forms/
│       ├── text_field.cgx
│       ├── select.cgx
│       └── checkbox.cgx
├── pages/                  # Page components
│   ├── dashboard.cgx
│   ├── users.cgx
│   ├── settings.cgx
│   └── login.cgx
├── services/              # Business logic
│   ├── api.py
│   ├── auth.py
│   └── storage.py
├── utils/                 # Utility functions
│   ├── formatters.py
│   ├── validators.py
│   └── helpers.py
├── state/                 # State management
│   └── store.py
├── main.py
└── requirements.txt
```

### Large Project Structure

For enterprise applications with many features:

```
my_app/
├── src/
│   ├── app.cgx            # Root component
│   ├── components/        # Shared UI components
│   │   ├── base/          # Base components
│   │   │   ├── button.cgx
│   │   │   ├── input.cgx
│   │   │   ├── card.cgx
│   │   │   └── table.cgx
│   │   ├── layout/        # Layout components
│   │   │   ├── app_layout.cgx
│   │   │   ├── header.cgx
│   │   │   ├── sidebar.cgx
│   │   │   └── footer.cgx
│   │   └── domain/        # Domain-specific components
│   │       ├── user_card.cgx
│   │       ├── product_card.cgx
│   │       └── order_summary.cgx
│   ├── features/          # Feature modules
│   │   ├── auth/
│   │   │   ├── login.cgx
│   │   │   ├── register.cgx
│   │   │   ├── auth_service.py
│   │   │   └── auth_state.py
│   │   ├── users/
│   │   │   ├── user_list.cgx
│   │   │   ├── user_detail.cgx
│   │   │   ├── user_form.cgx
│   │   │   ├── user_service.py
│   │   │   └── user_state.py
│   │   └── products/
│   │       ├── product_list.cgx
│   │       ├── product_detail.cgx
│   │       ├── product_service.py
│   │       └── product_state.py
│   ├── services/          # Shared services
│   │   ├── api/
│   │   │   ├── client.py
│   │   │   ├── interceptors.py
│   │   │   └── endpoints.py
│   │   ├── storage/
│   │   │   ├── local_storage.py
│   │   │   └── session_storage.py
│   │   └── notifications/
│   │       └── notification_service.py
│   ├── state/             # Global state
│   │   ├── store.py
│   │   ├── actions.py
│   │   └── reducers.py
│   ├── utils/             # Utilities
│   │   ├── formatters.py
│   │   ├── validators.py
│   │   ├── decorators.py
│   │   └── constants.py
│   └── types/             # Type definitions
│       ├── user.py
│       ├── product.py
│       └── order.py
├── tests/                 # Tests
│   ├── components/
│   ├── features/
│   ├── services/
│   └── conftest.py
├── assets/                # Static assets
│   ├── images/
│   └── styles/
├── config/                # Configuration
│   ├── development.py
│   ├── production.py
│   └── test.py
├── main.py
├── pyproject.toml
└── README.md
```

## Component Organization

### When to Create a Component

Create a new component when:

1. **Reusability** - Used in multiple places
2. **Complexity** - Component is getting too large (>200 lines)
3. **Separation of concerns** - Distinct responsibility
4. **Independent state** - Manages its own state
5. **Testing** - Needs to be tested independently

**Example - Extracting a component:**

**Before (monolithic):**
```html
<!-- user_profile.cgx -->
<widget>
  <label :text="user['name']" />
  <label :text="user['email']" />

  <!-- Inline address display -->
  <widget>
    <label :text="user['address']['street']" />
    <label :text="user['address']['city']" />
    <label :text="user['address']['zip']" />
  </widget>

  <!-- Inline contact info -->
  <widget>
    <label :text="user['phone']" />
    <label :text="user['website']" />
  </widget>
</widget>
```

**After (componentized):**
```html
<!-- user_profile.cgx -->
<widget>
  <label :text="user['name']" />
  <label :text="user['email']" />

  <AddressDisplay :address="user['address']" />
  <ContactInfo :phone="user['phone']" :website="user['website']" />
</widget>
```

```html
<!-- address_display.cgx -->
<widget>
  <label :text="address['street']" />
  <label :text="address['city']" />
  <label :text="address['zip']" />
</widget>
```

```html
<!-- contact_info.cgx -->
<widget>
  <label :text="phone" />
  <label :text="website" />
</widget>
```

### Component Naming Conventions

**Use descriptive, specific names:**

```
# Good
user_profile_card.cgx
product_list_item.cgx
navigation_sidebar.cgx
login_form.cgx

# Bad
card.cgx
item.cgx
nav.cgx
form.cgx
```

**Follow patterns:**

- **Pages**: `{feature}_page.cgx` (dashboard_page.cgx)
- **Lists**: `{item}_list.cgx` (user_list.cgx)
- **Forms**: `{feature}_form.cgx` (registration_form.cgx)
- **Modals**: `{purpose}_modal.cgx` (confirm_modal.cgx)
- **Cards**: `{content}_card.cgx` (product_card.cgx)

### Component Size Guidelines

**Small component (< 100 lines):**
- Simple, focused functionality
- Minimal state
- Few props
- Example: Button, Input, Label wrapper

**Medium component (100-300 lines):**
- Moderate complexity
- Some local state
- Multiple props
- Example: Form, Card, List item

**Large component (300+ lines):**
- Complex functionality
- Should be split into smaller components
- Exception: Page-level components

**When to split:**

```python
# Signs a component is too large:

# 1. Too many methods (>10)
class LargeComponent(cg.Component):
    def method1(self): pass
    def method2(self): pass
    # ... 10+ methods
    def method15(self): pass  # Too many!

# 2. Too much state (>8 properties)
def init(self):
    self.state["field1"] = ""
    self.state["field2"] = ""
    # ... 8+ state properties
    self.state["field12"] = ""  # Too much!

# 3. Deep nesting in template (>4 levels)
<widget>
  <widget>
    <widget>
      <widget>
        <widget>  <!-- Too deep! -->
        </widget>
      </widget>
    </widget>
  </widget>
</widget>
```

## Separating Business Logic

### Service Layer

Keep business logic separate from UI components:

**services/user_service.py:**
```python
class UserService:
    """Handles user-related business logic"""

    def __init__(self, api_client):
        self.api = api_client

    def get_users(self, filters=None):
        """Fetch users with optional filters"""
        params = self._build_params(filters)
        return self.api.get("/users", params=params)

    def create_user(self, user_data):
        """Create a new user"""
        self._validate_user_data(user_data)
        return self.api.post("/users", data=user_data)

    def update_user(self, user_id, updates):
        """Update existing user"""
        self._validate_user_data(updates)
        return self.api.patch(f"/users/{user_id}", data=updates)

    def delete_user(self, user_id):
        """Delete a user"""
        return self.api.delete(f"/users/{user_id}")

    def _validate_user_data(self, data):
        """Validate user data"""
        if not data.get("email"):
            raise ValueError("Email is required")
        if not data.get("name"):
            raise ValueError("Name is required")

    def _build_params(self, filters):
        """Build query parameters from filters"""
        if not filters:
            return {}

        params = {}
        if filters.get("role"):
            params["role"] = filters["role"]
        if filters.get("active") is not None:
            params["active"] = filters["active"]

        return params
```

**Using in component:**
```python
from services.user_service import UserService
from services.api import api_client

class UserList(cg.Component):
    def init(self):
        self.user_service = UserService(api_client)

        self.state["users"] = []
        self.state["loading"] = False
        self.state["error"] = None

    def mounted(self):
        self.load_users()

    def load_users(self):
        """Load users using service"""
        self.state["loading"] = True
        self.state["error"] = None

        try:
            users = self.user_service.get_users()
            self.state["users"] = users
        except Exception as e:
            self.state["error"] = str(e)
        finally:
            self.state["loading"] = False
```

### Utility Functions

Extract reusable utilities:

**utils/formatters.py:**
```python
def format_date(date, format="YYYY-MM-DD"):
    """Format date string"""
    from datetime import datetime

    if isinstance(date, str):
        date = datetime.fromisoformat(date)

    if format == "YYYY-MM-DD":
        return date.strftime("%Y-%m-%d")
    elif format == "MM/DD/YYYY":
        return date.strftime("%m/%d/%Y")
    else:
        return str(date)


def format_currency(amount, currency="USD"):
    """Format currency amount"""
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }

    symbol = symbols.get(currency, "$")
    return f"{symbol}{amount:,.2f}"


def format_phone(phone):
    """Format phone number"""
    # Remove non-digits
    digits = "".join(c for c in phone if c.isdigit())

    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone
```

**utils/validators.py:**
```python
import re

def validate_email(email):
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number"""
    digits = "".join(c for c in phone if c.isdigit())
    return len(digits) == 10


def validate_password(password):
    """Validate password strength"""
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters")

    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain an uppercase letter")

    if not re.search(r"[a-z]", password):
        errors.append("Password must contain a lowercase letter")

    if not re.search(r"[0-9]", password):
        errors.append("Password must contain a number")

    return errors
```

**Using in components:**
```python
from utils.formatters import format_date, format_currency
from utils.validators import validate_email

class UserCard(cg.Component):
    @property
    def formatted_created_date(self):
        created = self.props.get("created_at")
        return format_date(created, "MM/DD/YYYY")

    @property
    def formatted_balance(self):
        balance = self.props.get("balance", 0)
        return format_currency(balance, "USD")
```

## State Management Organization

### Centralized State

**state/store.py:**
```python
from observ import reactive

# Global application state
store = reactive({
    "user": None,
    "session": None,
    "ui": {
        "theme": "light",
        "sidebar_open": True,
        "notifications": []
    },
    "data": {
        "users": [],
        "products": [],
        "orders": []
    }
})
```

**state/actions.py:**
```python
from .store import store

# User actions
def login(user_data, session_data):
    """Login user"""
    store["user"] = user_data
    store["session"] = session_data


def logout():
    """Logout user"""
    store["user"] = None
    store["session"] = None


# UI actions
def set_theme(theme):
    """Set UI theme"""
    store["ui"]["theme"] = theme


def toggle_sidebar():
    """Toggle sidebar"""
    store["ui"]["sidebar_open"] = not store["ui"]["sidebar_open"]


def add_notification(message, type="info"):
    """Add notification"""
    store["ui"]["notifications"].append({
        "message": message,
        "type": type,
        "timestamp": time.time()
    })


# Data actions
def set_users(users):
    """Set users data"""
    store["data"]["users"] = users


def add_user(user):
    """Add user"""
    store["data"]["users"].append(user)


def update_user(user_id, updates):
    """Update user"""
    for user in store["data"]["users"]:
        if user["id"] == user_id:
            user.update(updates)
            break


def delete_user(user_id):
    """Delete user"""
    store["data"]["users"] = [
        u for u in store["data"]["users"]
        if u["id"] != user_id
    ]
```

**Using in components:**
```python
from state.store import store
from state.actions import login, logout, add_notification

class App(cg.Component):
    def init(self):
        # Provide store to all descendants
        self.provide("store", store)
        self.provide("actions", {
            "login": login,
            "logout": logout,
            "add_notification": add_notification
        })


class LoginForm(cg.Component):
    def init(self):
        self.store = self.inject("store")
        self.actions = self.inject("actions")

    def handle_login(self):
        # Use action to update store
        self.actions["login"](user_data, session_data)
```

## Feature-Based Organization

Group related components by feature:

```
features/
├── auth/
│   ├── components/
│   │   ├── login_form.cgx
│   │   ├── register_form.cgx
│   │   └── password_reset.cgx
│   ├── auth_service.py
│   ├── auth_state.py
│   └── auth_utils.py
├── users/
│   ├── components/
│   │   ├── user_list.cgx
│   │   ├── user_detail.cgx
│   │   ├── user_form.cgx
│   │   └── user_card.cgx
│   ├── user_service.py
│   ├── user_state.py
│   └── user_types.py
└── products/
    ├── components/
    │   ├── product_list.cgx
    │   ├── product_detail.cgx
    │   └── product_card.cgx
    ├── product_service.py
    └── product_state.py
```

Each feature is self-contained with:
- Components
- Services
- State management
- Types/utilities

## Import Organization

### Import Order

Follow consistent import ordering:

```python
# 1. Standard library imports
import os
import sys
from datetime import datetime

# 2. Third-party imports
from PySide6 import QtWidgets
from observ import reactive, watch

# 3. Collagraph imports
import collagraph as cg

# 4. Local application imports
from services.api import api_client
from utils.formatters import format_date
from state.store import store

# 5. Component imports
from components.button import Button
from components.input import Input
```

### Absolute vs Relative Imports

**Use absolute imports for better clarity:**

```python
# Good: Absolute imports
from components.common.button import Button
from services.user_service import UserService
from utils.formatters import format_date

# Avoid: Relative imports
from ..components.button import Button
from .utils import format_date
```

### Importing CGX Components

Components defined in `.cgx` files can be imported like regular Python modules:

```python
# Import component from .cgx file
from user_card import UserCard
from components.button import Button
from pages.dashboard import Dashboard

# Use in template
```

```html
<UserCard :user="user" />
<Button text="Click" @clicked="handle_click" />
```

## Configuration Management

### Environment-Based Configuration

**config/base.py:**
```python
class BaseConfig:
    """Base configuration"""
    APP_NAME = "My App"
    VERSION = "1.0.0"
    DEBUG = False
```

**config/development.py:**
```python
from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    API_URL = "http://localhost:8000"
    LOG_LEVEL = "DEBUG"
```

**config/production.py:**
```python
from .base import BaseConfig

class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    API_URL = "https://api.example.com"
    LOG_LEVEL = "ERROR"
```

**config/__init__.py:**
```python
import os
from .development import DevelopmentConfig
from .production import ProductionConfig

ENV = os.getenv("APP_ENV", "development")

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

current_config = config[ENV]
```

**Using configuration:**
```python
from config import current_config

class ApiClient:
    def __init__(self):
        self.base_url = current_config.API_URL
```

## Best Practices

1. **Keep components focused** - One responsibility per component
2. **Extract business logic** - Separate UI from business logic in services
3. **Use consistent naming** - Follow naming conventions
4. **Organize by feature** - Group related code together
5. **Centralize state** - Keep global state in one place
6. **Write reusable utilities** - Extract common functions
7. **Document structure** - README in each major directory
8. **Follow import order** - Consistent import organization
9. **Use type hints** - Add type annotations where helpful
10. **Keep files small** - Split large files into smaller modules

## Example README for Feature

**features/users/README.md:**
```markdown
# Users Feature

User management functionality.

## Components

- `user_list.cgx` - List of users with filtering and sorting
- `user_detail.cgx` - Detailed user view
- `user_form.cgx` - Create/edit user form
- `user_card.cgx` - Reusable user card component

## Services

- `user_service.py` - User API calls and business logic

## State

- `user_state.py` - User-related state management

## Usage

```python
from features.users.components.user_list import UserList
from features.users.user_service import UserService

# Create service
user_service = UserService(api_client)

# Use in component
users = user_service.get_users()
```
```

## See Also

- [Components](../core-concepts/components.md)
- [Best Practices](best-practices.md)
- [Single-File Components](../core-concepts/single-file-components.md)
