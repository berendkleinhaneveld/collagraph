# Example: Form Validation

A registration form with comprehensive validation demonstrating input handling, validation logic, and error display.

## Overview

This example demonstrates how to build forms with client-side validation in Collagraph. You'll learn how to validate different input types, display error messages, enable/disable submit buttons based on validity, and provide real-time feedback to users.

### What You'll Learn

- How to handle multiple form inputs
- How to implement validation logic
- How to display error messages conditionally
- How to use computed properties for validation state
- How to style widgets based on validation status
- How to prevent invalid form submission
- Best practices for user-friendly forms

## Complete Code

Create a file called `registration_form.cgx`:

```html
<window title="Registration Form">
  <v-box>
    <label text="User Registration" />

    <!-- Username field -->
    <v-box>
      <label text="Username:" />
      <line-edit
        :text="username"
        @text-changed="lambda text: set_field('username', text)"
        placeholder-text="Enter username"
      />
      <label
        v-if="username_error"
        :text="username_error"
        :style-sheet="'color: red;'"
      />
    </v-box>

    <!-- Email field -->
    <v-box>
      <label text="Email:" />
      <line-edit
        :text="email"
        @text-changed="lambda text: set_field('email', text)"
        placeholder-text="user@example.com"
      />
      <label
        v-if="email_error"
        :text="email_error"
        :style-sheet="'color: red;'"
      />
    </v-box>

    <!-- Password field -->
    <v-box>
      <label text="Password:" />
      <line-edit
        :text="password"
        @text-changed="lambda text: set_field('password', text)"
        placeholder-text="Enter password"
        echo-mode="Password"
      />
      <label
        v-if="password_error"
        :text="password_error"
        :style-sheet="'color: red;'"
      />
    </v-box>

    <!-- Confirm password field -->
    <v-box>
      <label text="Confirm Password:" />
      <line-edit
        :text="confirm_password"
        @text-changed="lambda text: set_field('confirm_password', text)"
        placeholder-text="Re-enter password"
        echo-mode="Password"
      />
      <label
        v-if="confirm_password_error"
        :text="confirm_password_error"
        :style-sheet="'color: red;'"
      />
    </v-box>

    <!-- Age field -->
    <v-box>
      <label text="Age:" />
      <spin-box
        :value="age"
        @value-changed="lambda val: set_field('age', val)"
        :minimum="0"
        :maximum="150"
      />
      <label
        v-if="age_error"
        :text="age_error"
        :style-sheet="'color: red;'"
      />
    </v-box>

    <!-- Terms checkbox -->
    <v-box>
      <checkbox
        :checked="terms_accepted"
        @toggled="lambda checked: set_field('terms_accepted', checked)"
        text="I accept the terms and conditions"
      />
      <label
        v-if="terms_error"
        :text="terms_error"
        :style-sheet="'color: red;'"
      />
    </v-box>

    <!-- Submit button -->
    <h-box>
      <button
        text="Register"
        @clicked="submit_form"
        :enabled="is_valid"
      />
      <button
        text="Reset"
        @clicked="reset_form"
      />
    </h-box>

    <!-- Success message -->
    <label
      v-if="submitted"
      text="Registration successful!"
      :style-sheet="'color: green; font-weight: bold;'"
    />
  </v-box>
</window>

<script>
import collagraph as cg
import re


class RegistrationForm(cg.Component):
    def init(self):
        # Form fields
        self.state["username"] = ""
        self.state["email"] = ""
        self.state["password"] = ""
        self.state["confirm_password"] = ""
        self.state["age"] = 18
        self.state["terms_accepted"] = False

        # UI state
        self.state["submitted"] = False
        self.state["touched"] = {
            "username": False,
            "email": False,
            "password": False,
            "confirm_password": False,
            "age": False,
            "terms_accepted": False,
        }

    def set_field(self, field, value):
        """Update a form field and mark it as touched."""
        self.state[field] = value
        self.state["touched"][field] = True
        self.state["submitted"] = False

    # Validation methods

    @property
    def username_error(self):
        """Validate username field."""
        if not self.state["touched"]["username"]:
            return None

        username = self.state["username"]
        if not username:
            return "Username is required"
        if len(username) < 3:
            return "Username must be at least 3 characters"
        if len(username) > 20:
            return "Username must be less than 20 characters"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return "Username can only contain letters, numbers, and underscores"
        return None

    @property
    def email_error(self):
        """Validate email field."""
        if not self.state["touched"]["email"]:
            return None

        email = self.state["email"]
        if not email:
            return "Email is required"
        # Simple email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return "Invalid email format"
        return None

    @property
    def password_error(self):
        """Validate password field."""
        if not self.state["touched"]["password"]:
            return None

        password = self.state["password"]
        if not password:
            return "Password is required"
        if len(password) < 8:
            return "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return "Password must contain at least one lowercase letter"
        if not re.search(r'[0-9]', password):
            return "Password must contain at least one number"
        return None

    @property
    def confirm_password_error(self):
        """Validate confirm password field."""
        if not self.state["touched"]["confirm_password"]:
            return None

        if self.state["confirm_password"] != self.state["password"]:
            return "Passwords do not match"
        return None

    @property
    def age_error(self):
        """Validate age field."""
        if not self.state["touched"]["age"]:
            return None

        age = self.state["age"]
        if age < 13:
            return "You must be at least 13 years old"
        return None

    @property
    def terms_error(self):
        """Validate terms acceptance."""
        if not self.state["touched"]["terms_accepted"]:
            return None

        if not self.state["terms_accepted"]:
            return "You must accept the terms and conditions"
        return None

    @property
    def is_valid(self):
        """Check if the entire form is valid."""
        # Check all fields have been touched
        if not all(self.state["touched"].values()):
            return False

        # Check no errors exist
        return not any([
            self.username_error,
            self.email_error,
            self.password_error,
            self.confirm_password_error,
            self.age_error,
            self.terms_error,
        ])

    def submit_form(self):
        """Handle form submission."""
        if self.is_valid:
            # In a real app, send data to server here
            print(f"Registering user: {self.state['username']}")
            print(f"Email: {self.state['email']}")
            print(f"Age: {self.state['age']}")
            self.state["submitted"] = True

    def reset_form(self):
        """Reset all form fields."""
        self.state["username"] = ""
        self.state["email"] = ""
        self.state["password"] = ""
        self.state["confirm_password"] = ""
        self.state["age"] = 18
        self.state["terms_accepted"] = False
        self.state["submitted"] = False
        self.state["touched"] = {k: False for k in self.state["touched"]}
</script>
```

## Step-by-Step Breakdown

### 1. Form State Structure

```python
def init(self):
    # Form fields
    self.state["username"] = ""
    self.state["email"] = ""
    self.state["password"] = ""
    # ...

    # Track which fields have been touched
    self.state["touched"] = {
        "username": False,
        "email": False,
        # ...
    }
```

We track:
- Field values in state
- Which fields have been touched (to avoid showing errors prematurely)
- Submission status

### 2. Two-Way Binding Pattern

```html
<line-edit
  :text="username"
  @text-changed="lambda text: set_field('username', text)"
/>
```

```python
def set_field(self, field, value):
    self.state[field] = value
    self.state["touched"][field] = True
```

This pattern:
- Binds the input value to state
- Updates state when user types
- Marks the field as touched for validation

### 3. Validation with Computed Properties

```python
@property
def username_error(self):
    if not self.state["touched"]["username"]:
        return None  # Don't show errors until field is touched

    username = self.state["username"]
    if not username:
        return "Username is required"
    if len(username) < 3:
        return "Username must be at least 3 characters"
    # More validation...
    return None
```

Each field has a computed property that:
- Returns `None` if field hasn't been touched yet
- Returns an error message string if invalid
- Returns `None` if valid

### 4. Conditional Error Display

```html
<label
  v-if="username_error"
  :text="username_error"
  :style-sheet="'color: red;'"
/>
```

Error labels only appear when the error property is truthy (not `None`).

### 5. Password Input

```html
<line-edit
  :text="password"
  echo-mode="Password"
/>
```

The `echo-mode="Password"` attribute makes the input display dots instead of characters.

### 6. Overall Form Validation

```python
@property
def is_valid(self):
    # Check all fields touched
    if not all(self.state["touched"].values()):
        return False

    # Check no errors exist
    return not any([
        self.username_error,
        self.email_error,
        # ...
    ])
```

The submit button is only enabled when the entire form is valid.

### 7. Form Submission

```python
def submit_form(self):
    if self.is_valid:
        # Process form data
        print(f"Registering user: {self.state['username']}")
        self.state["submitted"] = True
```

## How to Run

### Using the CLI

```bash
uv run collagraph registration_form.cgx
```

Or:

```bash
python -m collagraph registration_form.cgx
```

### With a Python Entry Point

```python
# main.py
from PySide6 import QtWidgets
import collagraph as cg
from registration_form import RegistrationForm

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    gui = cg.Collagraph(renderer=cg.PySideRenderer())
    gui.render(RegistrationForm, app)
    app.exec()
```

## Key Concepts

### Touched State Pattern

Only show validation errors after a user has interacted with a field:

```python
def set_field(self, field, value):
    self.state[field] = value
    self.state["touched"][field] = True  # Mark as touched

@property
def field_error(self):
    if not self.state["touched"]["field"]:
        return None  # No error message yet
    # ... validation logic
```

This provides a better user experience than showing errors immediately.

### Validation Computed Properties

Use computed properties for validation:

```python
@property
def email_error(self):
    email = self.state["email"]
    if not re.match(r'^.+@.+\..+$', email):
        return "Invalid email"
    return None
```

Benefits:
- Automatically recalculate when field changes
- Can be used in templates
- Easy to test in isolation

### Regular Expressions for Validation

Common patterns:

```python
# Email
r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Username (alphanumeric + underscore)
r'^[a-zA-Z0-9_]+$'

# Password strength checks
re.search(r'[A-Z]', password)  # Has uppercase
re.search(r'[0-9]', password)  # Has number
```

### Conditional Styling

Apply styles based on validation state:

```html
<label
  :style-sheet="'color: red;'"  # Error styling
/>

<label
  :style-sheet="'color: green; font-weight: bold;'"  # Success styling
/>
```

## Possible Extensions

### 1. Add Real-Time Validation Feedback

Show a checkmark when fields are valid:

```html
<h-box>
  <line-edit ... />
  <label
    v-if="!username_error && username"
    text="✓"
    :style-sheet="'color: green;'"
  />
</h-box>
```

### 2. Add Password Strength Indicator

Show visual feedback for password strength:

```python
@property
def password_strength(self):
    password = self.state["password"]
    strength = 0
    if len(password) >= 8:
        strength += 1
    if re.search(r'[A-Z]', password):
        strength += 1
    if re.search(r'[a-z]', password):
        strength += 1
    if re.search(r'[0-9]', password):
        strength += 1
    if re.search(r'[^A-Za-z0-9]', password):  # Special chars
        strength += 1
    return strength

@property
def password_strength_text(self):
    strength = self.password_strength
    if strength <= 2:
        return "Weak"
    elif strength <= 3:
        return "Medium"
    else:
        return "Strong"
```

```html
<label :text="f'Strength: {password_strength_text}'" />
```

### 3. Add Server-Side Validation

Check if username/email already exists:

```python
async def check_username_available(self):
    # Make API call to check availability
    response = await api.check_username(self.state["username"])
    if not response["available"]:
        return "Username already taken"
    return None
```

### 4. Add Field Character Counter

Show remaining characters for limited fields:

```python
@property
def username_chars_remaining(self):
    return 20 - len(self.state["username"])
```

```html
<label :text="f'{username_chars_remaining} characters remaining'" />
```

### 5. Add Multi-Step Form

Split into multiple pages:

```python
def init(self):
    self.state["step"] = 1  # Current step (1, 2, 3)

@property
def can_proceed_to_step_2(self):
    return not any([self.username_error, self.email_error])

def next_step(self):
    if self.state["step"] < 3:
        self.state["step"] += 1
```

```html
<v-box v-if="step == 1">
  <!-- Step 1 fields -->
</v-box>
<v-box v-if="step == 2">
  <!-- Step 2 fields -->
</v-box>
```

### 6. Add Custom Validators

Create reusable validation functions:

```python
def validate_required(value, field_name):
    if not value or not str(value).strip():
        return f"{field_name} is required"
    return None

def validate_min_length(value, min_len, field_name):
    if len(str(value)) < min_len:
        return f"{field_name} must be at least {min_len} characters"
    return None

@property
def username_error(self):
    if not self.state["touched"]["username"]:
        return None

    username = self.state["username"]
    return (
        validate_required(username, "Username") or
        validate_min_length(username, 3, "Username") or
        validate_pattern(username, r'^[a-zA-Z0-9_]+$', "Username can only contain letters, numbers, and underscores")
    )
```

## Topics Covered

- Form input handling (line-edit, spin-box, checkbox)
- Validation logic with computed properties
- Conditional error message display
- Regular expressions for pattern matching
- Password input fields
- Form submission and reset
- Touched state pattern for better UX
- Conditional button enabling
- Dynamic styling based on state
- Two-way data binding

## See Also

- [State Management](../core-concepts/state-management.md)
- [Computed Properties](../core-concepts/computed.md)
- [v-if Directive](../core-concepts/directives/v-if.md)
- [PySide Widgets](../renderers/pyside-widgets.md)
- [Events](../core-concepts/events.md)
