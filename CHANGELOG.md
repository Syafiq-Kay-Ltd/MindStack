## 0.1.0 (2025-07-24)

### Feat

- Reintroduce testing documentation and update pytest configuration
- Add colour definitions in CSS and SCSS formats
- Update database configuration to use Azure SQL Database
- Refactor templates and styles for improved layout and functionality
- Add cover CSS styles and testing documentation
- update home.html style
- update navbar and notes list templates for improved layout and functionality
- enhance notes creation and listing templates; implement note context service for improved display
- add cortexdb_base.html template for consistent layout
- update template inheritance to use cortexdb_base.html for consistency
- enhance home page layout and content, update URL routing, and refactor views
- add note management features with create, update, and list views
- implement Note model and CRUD views, add forms and tests
- set up cortexdb landing page
- build a new homepage to reduce clutter
- update requirements.txt to include additional dependencies for improved functionality
- update Python version requirement to 3.12, add README.md for Git Flow installation, and create requirements.txt with necessary dependencies
- update Azure storage configuration, remove creator field from ProgressLog, and enhance progress log views and forms
- implement CRUD functionality for progress logs and update Azure storage configuration
- created progress log view on homepage,  list view and detail view
- wrote test for progress-log-model
- initialise progress app
- add initial .env and pyproject.toml configuration files
- initialised the project directory using django-admin

### Fix

- Update last edited timestamp variable in notes detail template
- fix cortexdb views.py
- fix commitizen config

### Refactor

- update Note model and related forms; enhance navbar and templates for improved UI; implement CRUD views for notes
- standardize model naming from 'Note' to 'note' and update related references; remove obsolete test files; add comprehensive CRUD tests for notes
- update and rename views.py to views_crud.py
- update models.py
- home.html
- simplified base.html
- updated readme
- setup commitizen
