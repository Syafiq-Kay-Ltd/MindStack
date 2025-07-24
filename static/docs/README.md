# Template Token Testing Guide

This guide explains how to use the tokenisation functions in `mindstack/services.py` to test and verify which HTML templates are rendered by your Django views.

## Functions

- `generate_template_token(template_name: str) -> str`
  - Generates a unique token for a given template name.
- `get_or_create_template_token(template_name: str) -> str`
  - Returns a single token for the template, creating it if it doesn't exist.

## How to Use in Tests

### 1. Import the function
```python
from mindstack.services import generate_template_token
```

### 2. Use in a test for any view
```python
from django.test import TestCase, Client
from mindstack.services import generate_template_token

class TestAnyView(TestCase):
    def test_view_renders_template_with_token(self):
        client = Client()
        response = client.get('/your-url/')  # Replace with your view's URL
        self.assertEqual(response.status_code, 200)
        # Generate expected token
        expected_token = generate_template_token('your_template.html')
        # Check token in response (if rendered in HTML)
        self.assertIn(expected_token, response.content.decode())
```

### 3. Use with database logging
If you use `get_or_create_template_token`, you can check the token in the database:
```python
from mindstack.services import get_or_create_template_token
from home.models import TemplateTokenLog

token = get_or_create_template_token('your_template.html')
assert TemplateTokenLog.objects.filter(template_name='your_template.html', token=token).exists()
```

## Example Scenarios
- Test that a view renders the correct template and includes the token.
- Audit which templates are used by which views.
- Clean up old tokens in the database.

## Notes
- Make sure your templates render the token (e.g., as a comment or in a visible tag) for HTML-based verification.
- For database verification, use the logging functions and check the `TemplateTokenLog` model.

---

For more advanced usage, see the manual section in `mindstack/services.py`.
