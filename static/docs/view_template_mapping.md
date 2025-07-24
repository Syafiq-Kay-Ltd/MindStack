# View-Template Mapping Guide

This document describes how views in the MindStack project are mapped to their corresponding HTML templates, and how to use this mapping for template token verification in tests.

## Purpose
- Ensure each view renders the correct template.
- Enable automated and manual verification of template tokens for security and testing.

## Example Mapping

| View Name                        | URL Pattern                        | Template Name              | Description                       |
|----------------------------------|------------------------------------|----------------------------|------------------------------------|
| `progress:progress-main`         | `/progress/`                       | `progress_mainpage.html`   | Main progress log page             |
| `progress:progress-log-list`     | `/progress/logs/`                  | `progress_log_list.html`   | List of progress logs              |
| `progress:progress-log-detail`   | `/progress/logs/<id>/`             | `progress_log_detail.html` | Detail view for a single log       |
| `home:home`                      | `/`                                | `home.html`                | Homepage                           |
| `cortexdb:main`                  | `/cortexdb/`                       | `cortexdb_main.html`       | CortexDB main page                 |
| ...                              | ...                                | ...                        | ...                                |

## How to Use in Tests
- Use the mapping to determine which template should be rendered for each view.
- In your test, check the response's `templates` attribute to verify the correct template was used.
- Extract the token from the rendered HTML and compare it to the expected token for that template.

## Manual Token Hardcoding
1. For each template, generate a token using:
   ```python
   from mindstack.services import generate_template_token
   token = generate_template_token('template_name.html')
   ```
2. Add the token as a comment at the top of the template:
   ```html
   <!-- TOKEN: <token> -->
   ```
3. In your test, hardcode the expected token for each view/template.

## Dynamic Template Selection
- Use Django's response object:
  ```python
  rendered_templates = [t.name for t in getattr(response, 'templates', []) if t.name]
  assert template_name in rendered_templates
  ```
- Extract the token from the HTML and verify it matches the expected token.

## Updating the Mapping
- Add new views and templates to the table above as your project grows.
- Keep the mapping up to date for reliable automated testing and auditing.

---

For more details, see the test class `TestViewTemplateTokenVerification` in `progress/tests.py`.
