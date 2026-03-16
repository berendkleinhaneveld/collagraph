# Working with Forms

This guide covers everything you need to know about building forms in Collagraph, from basic input handling to complex validation and submission workflows.

## Overview

Forms are a fundamental part of many applications. In Collagraph, form handling leverages reactive state and event handling to create interactive, validated forms with minimal boilerplate.

## Basic Form Structure

### Simple Form Example

Let's start with a basic login form:

```html
<widget :layout="{'type': 'form'}">
  <lineedit
    ref="username"
    :text="username"
    placeholder-text="Username"
    @text-changed="handle_username_change"
    form-label="Username:"
    form-index="0"
  />

  <lineedit
    :text="password"
    placeholder-text="Password"
    echo-mode="Password"
    @text-changed="handle_password_change"
    @return-pressed="submit"
    form-label="Password:"
    form-index="1"
  />

  <widget form-label=" " form-index="2">
    <button
      text="Login"
      @clicked="submit"
      :enabled="can_submit"
    />
  </widget>
</widget>

<script>
import collagraph as cg

class LoginForm(cg.Component):
    def init(self):
        self.state["username"] = ""
        self.state["password"] = ""
        self.state["is_submitting"] = False

    @property
    def can_submit(self):
        return (
            len(self.state["username"]) > 0 and
            len(self.state["password"]) > 0 and
            not self.state["is_submitting"]
        )

    def handle_username_change(self, text):
        self.state["username"] = text

    def handle_password_change(self, text):
        self.state["password"] = text

    def submit(self):
        if not self.can_submit:
            return

        self.state["is_submitting"] = True

        # Perform login
        username = self.state["username"]
        password = self.state["password"]

        # Emit event to parent
        self.emit("submit", {
            "username": username,
            "password": password
        })
</script>
```

## Form Input Types

### Text Input

Basic text input with single line:

```html
<lineedit
  :text="name"
  placeholder-text="Enter your name"
  @text-changed="text => state['name'] = text"
/>
```

Multi-line text input:

```html
<textedit
  :text="description"
  placeholder-text="Enter description..."
  @text-changed="text => state['description'] = text"
/>
```

### Password Input

```html
<lineedit
  :text="password"
  echo-mode="Password"
  placeholder-text="Enter password"
  @text-changed="text => state['password'] = text"
/>
```

### Checkbox

```html
<checkbox
  :checked="agree_to_terms"
  @toggled="checked => state['agree_to_terms'] = checked"
/>
<label text="I agree to the terms and conditions" />
```

### Radio Buttons

Radio buttons in Collagraph are implemented using button groups:

```html
<widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
  <label text="Select your role:" />

  <radiobutton
    text="Developer"
    :checked="role == 'developer'"
    @toggled="lambda checked: set_role('developer') if checked else None"
  />

  <radiobutton
    text="Designer"
    :checked="role == 'designer'"
    @toggled="lambda checked: set_role('designer') if checked else None"
  />

  <radiobutton
    text="Manager"
    :checked="role == 'manager'"
    @toggled="lambda checked: set_role('manager') if checked else None"
  />
</widget>

<script>
import collagraph as cg

class RoleSelector(cg.Component):
    def init(self):
        self.state["role"] = "developer"

    def set_role(self, role):
        self.state["role"] = role
</script>
```

### Select/Dropdown

```html
<combobox
  :current-index="selected_index"
  @current-index-changed="index => state['selected_index'] = index"
>
  <qstandarditemmodel>
    <standarditem
      v-for="option in options"
      :key="option['id']"
      :text="option['label']"
    />
  </qstandarditemmodel>
</combobox>

<script>
import collagraph as cg

class Dropdown(cg.Component):
    def init(self):
        self.state["options"] = [
            {"id": 1, "label": "Option 1"},
            {"id": 2, "label": "Option 2"},
            {"id": 3, "label": "Option 3"}
        ]
        self.state["selected_index"] = 0
</script>
```

### Sliders

```html
<slider
  :minimum="0"
  :maximum="100"
  :value="volume"
  orientation="Horizontal"
  @value-changed="value => state['volume'] = value"
/>
<label :text="f'Volume: {volume}%'" />
```

### Spinbox

```html
<spinbox
  :minimum="0"
  :maximum="100"
  :value="age"
  @value-changed="value => state['age'] = value"
/>
```

## Two-Way Binding

While Collagraph doesn't have built-in two-way binding like Vue's `v-model`, you can easily create it:

```html
<lineedit
  :text="email"
  @text-changed="text => state['email'] = text"
/>
```

For more complex scenarios, create a helper method:

```python
class FormComponent(cg.Component):
    def init(self):
        self.state["form_data"] = {
            "name": "",
            "email": "",
            "age": 0
        }

    def update_field(self, field_name, value):
        """Helper for updating form fields"""
        self.state["form_data"][field_name] = value
```

```html
<lineedit
  :text="form_data['name']"
  @text-changed="lambda text: update_field('name', text)"
/>

<lineedit
  :text="form_data['email']"
  @text-changed="lambda text: update_field('email', text)"
/>
```

## Form Validation

### Real-time Validation

Validate as the user types:

```python
class RegistrationForm(cg.Component):
    def init(self):
        self.state["email"] = ""
        self.state["password"] = ""
        self.state["confirm_password"] = ""

        # Error messages
        self.state["errors"] = {
            "email": "",
            "password": "",
            "confirm_password": ""
        }

    def validate_email(self, email):
        """Validate email format"""
        import re

        self.state["email"] = email

        if not email:
            self.state["errors"]["email"] = ""
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.state["errors"]["email"] = "Invalid email format"
        else:
            self.state["errors"]["email"] = ""

    def validate_password(self, password):
        """Validate password strength"""
        self.state["password"] = password

        if not password:
            self.state["errors"]["password"] = ""
        elif len(password) < 8:
            self.state["errors"]["password"] = "Password must be at least 8 characters"
        else:
            self.state["errors"]["password"] = ""

        # Re-validate confirm password
        self.validate_confirm_password(self.state["confirm_password"])

    def validate_confirm_password(self, confirm_password):
        """Validate password confirmation"""
        self.state["confirm_password"] = confirm_password

        if not confirm_password:
            self.state["errors"]["confirm_password"] = ""
        elif confirm_password != self.state["password"]:
            self.state["errors"]["confirm_password"] = "Passwords do not match"
        else:
            self.state["errors"]["confirm_password"] = ""

    @property
    def is_valid(self):
        """Check if form is valid"""
        has_values = (
            self.state["email"] and
            self.state["password"] and
            self.state["confirm_password"]
        )

        has_no_errors = not any(self.state["errors"].values())

        return has_values and has_no_errors
```

Template with error messages:

```html
<widget :layout="{'type': 'form'}">
  <!-- Email -->
  <widget form-label="Email:" form-index="0">
    <lineedit
      :text="email"
      @text-changed="validate_email"
    />
    <label
      v-if="errors['email']"
      :text="errors['email']"
      :style-sheet="'color: red; font-size: 10pt;'"
    />
  </widget>

  <!-- Password -->
  <widget form-label="Password:" form-index="1">
    <lineedit
      :text="password"
      echo-mode="Password"
      @text-changed="validate_password"
    />
    <label
      v-if="errors['password']"
      :text="errors['password']"
      :style-sheet="'color: red; font-size: 10pt;'"
    />
  </widget>

  <!-- Confirm Password -->
  <widget form-label="Confirm:" form-index="2">
    <lineedit
      :text="confirm_password"
      echo-mode="Password"
      @text-changed="validate_confirm_password"
    />
    <label
      v-if="errors['confirm_password']"
      :text="errors['confirm_password']"
      :style-sheet="'color: red; font-size: 10pt;'"
    />
  </widget>

  <!-- Submit -->
  <widget form-label=" " form-index="3">
    <button
      text="Register"
      @clicked="submit"
      :enabled="is_valid"
    />
  </widget>
</widget>
```

### Submit-time Validation

Validate when the form is submitted:

```python
def submit(self):
    """Validate and submit form"""
    # Clear previous errors
    self.state["errors"] = {
        "email": "",
        "password": "",
        "username": ""
    }

    # Validate all fields
    is_valid = True

    if not self.state["username"]:
        self.state["errors"]["username"] = "Username is required"
        is_valid = False
    elif len(self.state["username"]) < 3:
        self.state["errors"]["username"] = "Username must be at least 3 characters"
        is_valid = False

    if not self.state["email"]:
        self.state["errors"]["email"] = "Email is required"
        is_valid = False

    if not self.state["password"]:
        self.state["errors"]["password"] = "Password is required"
        is_valid = False

    if not is_valid:
        return

    # Submit the form
    self.perform_submit()
```

## Complete Form Example

Here's a comprehensive user registration form:

```html
<widget :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
  <label text="User Registration" :style-sheet="'font-size: 16pt; font-weight: bold;'" />

  <widget :layout="{'type': 'form'}">
    <!-- Username -->
    <widget form-label="Username:" form-index="0" :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
      <lineedit
        :text="username"
        placeholder-text="Choose a username"
        @text-changed="handle_username_change"
      />
      <label
        v-if="errors['username']"
        :text="errors['username']"
        :style-sheet="'color: red; font-size: 10pt;'"
      />
    </widget>

    <!-- Email -->
    <widget form-label="Email:" form-index="1" :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
      <lineedit
        :text="email"
        placeholder-text="your@email.com"
        @text-changed="handle_email_change"
      />
      <label
        v-if="errors['email']"
        :text="errors['email']"
        :style-sheet="'color: red; font-size: 10pt;'"
      />
    </widget>

    <!-- Password -->
    <widget form-label="Password:" form-index="2" :layout="{'type': 'box', 'direction': 'top-to-bottom'}">
      <lineedit
        :text="password"
        echo-mode="Password"
        placeholder-text="At least 8 characters"
        @text-changed="handle_password_change"
      />
      <label
        v-if="errors['password']"
        :text="errors['password']"
        :style-sheet="'color: red; font-size: 10pt;'"
      />
    </widget>

    <!-- Role -->
    <widget form-label="Role:" form-index="3">
      <combobox
        :current-index="role_index"
        @current-index-changed="index => state['role_index'] = index"
      >
        <qstandarditemmodel>
          <standarditem text="Developer" />
          <standarditem text="Designer" />
          <standarditem text="Manager" />
        </qstandarditemmodel>
      </combobox>
    </widget>

    <!-- Newsletter -->
    <widget form-label=" " form-index="4">
      <checkbox
        :checked="subscribe_newsletter"
        @toggled="checked => state['subscribe_newsletter'] = checked"
      />
      <label text="Subscribe to newsletter" />
    </widget>

    <!-- Buttons -->
    <widget form-label=" " form-index="5" :layout="{'type': 'box', 'direction': 'left-to-right'}">
      <button
        text="Register"
        @clicked="submit"
        :enabled="can_submit"
      />
      <button
        text="Cancel"
        @clicked="cancel"
      />
    </widget>
  </widget>

  <!-- Status message -->
  <label
    v-if="status_message"
    :text="status_message"
    :style-sheet="status_color"
  />
</widget>

<script>
import collagraph as cg
import re

class RegistrationForm(cg.Component):
    def init(self):
        # Form data
        self.state["username"] = ""
        self.state["email"] = ""
        self.state["password"] = ""
        self.state["role_index"] = 0
        self.state["subscribe_newsletter"] = False

        # Validation errors
        self.state["errors"] = {
            "username": "",
            "email": "",
            "password": ""
        }

        # UI state
        self.state["is_submitting"] = False
        self.state["status_message"] = ""
        self.state["status_color"] = ""

    @property
    def can_submit(self):
        """Check if form can be submitted"""
        has_values = (
            self.state["username"] and
            self.state["email"] and
            self.state["password"]
        )

        has_no_errors = not any(self.state["errors"].values())

        return has_values and has_no_errors and not self.state["is_submitting"]

    def handle_username_change(self, username):
        """Handle username input"""
        self.state["username"] = username

        # Validate
        if not username:
            self.state["errors"]["username"] = ""
        elif len(username) < 3:
            self.state["errors"]["username"] = "Username must be at least 3 characters"
        elif not re.match(r"^[a-zA-Z0-9_]+$", username):
            self.state["errors"]["username"] = "Username can only contain letters, numbers, and underscores"
        else:
            self.state["errors"]["username"] = ""

    def handle_email_change(self, email):
        """Handle email input"""
        self.state["email"] = email

        # Validate
        if not email:
            self.state["errors"]["email"] = ""
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.state["errors"]["email"] = "Invalid email format"
        else:
            self.state["errors"]["email"] = ""

    def handle_password_change(self, password):
        """Handle password input"""
        self.state["password"] = password

        # Validate
        if not password:
            self.state["errors"]["password"] = ""
        elif len(password) < 8:
            self.state["errors"]["password"] = "Password must be at least 8 characters"
        elif not re.search(r"[A-Z]", password):
            self.state["errors"]["password"] = "Password must contain at least one uppercase letter"
        elif not re.search(r"[0-9]", password):
            self.state["errors"]["password"] = "Password must contain at least one number"
        else:
            self.state["errors"]["password"] = ""

    def submit(self):
        """Submit the registration form"""
        if not self.can_submit:
            return

        self.state["is_submitting"] = True
        self.state["status_message"] = "Submitting..."
        self.state["status_color"] = "color: blue;"

        # Get role name
        roles = ["Developer", "Designer", "Manager"]
        role = roles[self.state["role_index"]]

        # Prepare data
        data = {
            "username": self.state["username"],
            "email": self.state["email"],
            "password": self.state["password"],
            "role": role,
            "subscribe_newsletter": self.state["subscribe_newsletter"]
        }

        # Emit to parent (parent would handle actual submission)
        self.emit("submit", data)

        # Simulate success
        self.state["status_message"] = "Registration successful!"
        self.state["status_color"] = "color: green; font-weight: bold;"
        self.state["is_submitting"] = False

    def cancel(self):
        """Cancel and reset form"""
        self.state["username"] = ""
        self.state["email"] = ""
        self.state["password"] = ""
        self.state["role_index"] = 0
        self.state["subscribe_newsletter"] = False
        self.state["errors"] = {
            "username": "",
            "email": "",
            "password": ""
        }
        self.state["status_message"] = ""

        self.emit("cancel")
</script>
```

## Form State Management

### Centralized Form State

For complex forms, organize state in a structured way:

```python
class ComplexForm(cg.Component):
    def init(self):
        # All form data in one place
        self.state["form"] = {
            "personal": {
                "first_name": "",
                "last_name": "",
                "email": ""
            },
            "address": {
                "street": "",
                "city": "",
                "zip": ""
            },
            "preferences": {
                "newsletter": False,
                "notifications": True
            }
        }

        # Separate validation state
        self.state["validation"] = {
            "personal": {},
            "address": {},
            "preferences": {}
        }

        # UI state
        self.state["current_step"] = 0
        self.state["is_submitting"] = False

    def update_field(self, section, field, value):
        """Update a form field"""
        self.state["form"][section][field] = value

        # Trigger validation
        self.validate_field(section, field)

    def validate_field(self, section, field):
        """Validate a specific field"""
        # Validation logic here
        pass
```

### Multi-Step Forms

```python
class MultiStepForm(cg.Component):
    def init(self):
        self.state["current_step"] = 0
        self.state["steps"] = [
            "Personal Info",
            "Contact Details",
            "Preferences",
            "Review"
        ]

        # Form data for all steps
        self.state["form_data"] = {
            "name": "",
            "email": "",
            "phone": "",
            "newsletter": False
        }

    @property
    def can_proceed(self):
        """Check if can go to next step"""
        step = self.state["current_step"]

        if step == 0:
            return bool(self.state["form_data"]["name"])
        elif step == 1:
            return bool(self.state["form_data"]["email"])
        else:
            return True

    def next_step(self):
        """Go to next step"""
        if self.can_proceed and self.state["current_step"] < len(self.state["steps"]) - 1:
            self.state["current_step"] += 1

    def prev_step(self):
        """Go to previous step"""
        if self.state["current_step"] > 0:
            self.state["current_step"] -= 1
```

## Common Pitfalls

### 1. Forgetting to Update State

```python
# Wrong: Event handler doesn't update state
def handle_input(self, text):
    # Missing: self.state["field"] = text
    print(f"Input: {text}")

# Correct: Always update state
def handle_input(self, text):
    self.state["field"] = text
```

### 2. Not Handling Empty Values

```python
# Wrong: Doesn't handle empty input
def validate_email(self, email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        self.state["errors"]["email"] = "Invalid"

# Correct: Clear error on empty
def validate_email(self, email):
    if not email:
        self.state["errors"]["email"] = ""
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        self.state["errors"]["email"] = "Invalid"
```

### 3. Validating on Every Keystroke

For expensive validations, debounce:

```python
import threading

class DebouncedForm(cg.Component):
    def init(self):
        self.state["email"] = ""
        self.validation_timer = None

    def handle_email_change(self, email):
        self.state["email"] = email

        # Cancel previous validation
        if self.validation_timer:
            self.validation_timer.cancel()

        # Schedule new validation
        self.validation_timer = threading.Timer(0.5, lambda: self.validate_email(email))
        self.validation_timer.start()
```

## Best Practices

1. **Initialize all form fields in `init()`** - Define all form state upfront
2. **Use computed properties for validation state** - Derive `is_valid` from form data
3. **Provide immediate feedback** - Validate as user types when appropriate
4. **Clear error messages** - Make validation errors helpful and specific
5. **Disable submit during submission** - Prevent duplicate submissions
6. **Handle edge cases** - Empty values, whitespace, special characters
7. **Focus management** - Use template refs to focus first error field
8. **Accessibility** - Use proper labels and form structure

## See Also

- [Events](../core-concepts/events.md)
- [State Management](../core-concepts/state-management.md)
- [Template Refs](../core-concepts/template-refs.md)
- [PySide Widgets](../renderers/pyside-widgets.md)
