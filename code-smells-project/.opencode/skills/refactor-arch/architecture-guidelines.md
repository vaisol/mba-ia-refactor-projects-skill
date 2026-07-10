# Architecture Guidelines — MVC Target Structure

Rules for the target MVC architecture after refactoring.

---

## Core MVC Principles

1. **Models** handle data access and business rules. They know nothing about HTTP.
2. **Views/Routes** handle HTTP concerns only: parse request, call controller, return response.
3. **Controllers** orchestrate the flow: validate input, call models/services, prepare response.
4. **Config** is extracted to a separate module and uses environment variables.
5. **Services** handle cross-cutting concerns (notifications, payments, authentication).
6. **Error Handling** is centralized, not scattered across every route.

---

## Python / Flask Target Structure

```
project-root/
├── app.py                      # Composition root — minimal imports, registers routes
├── config/
│   ├── __init__.py
│   └── settings.py             # All configuration via os.environ.get()
├── models/
│   ├── __init__.py             # Export all models
│   └── [domain].py             # One file per domain entity (user.py, product.py)
├── controllers/
│   ├── __init__.py             # Export all controllers
│   └── [domain]_controller.py  # One file per domain
├── routes/
│   ├── __init__.py             # Register all blueprints
│   └── api.py                  # Route definitions (thin — only HTTP concerns)
├── services/
│   ├── __init__.py
│   └── [service].py            # Cross-cutting concerns
├── middlewares/
│   ├── __init__.py
│   └── error_handler.py        # Centralized error handling
├── database.py                 # Database connection only
├── seed.py                     # Seed data (if needed)
└── requirements.txt
```

### Rules for Python/Flask

1. **app.py** is the composition root:
   - Import Flask, create the app
   - Import and register blueprints
   - Import and register error handlers
   - Set configuration
   - That's it — no business logic in app.py

2. **config/settings.py:**
   - Use `os.environ.get('KEY', 'default')` for all values
   - Export a settings object or individual constants
   - Never import this from models (no circular dependencies)

3. **models/[domain].py:**
   - One file per domain entity
   - Include `to_dict()` method that excludes sensitive fields (passwords, secrets)
   - Include validation methods if applicable
   - Use parameterized queries or ORM — never string concatenation

4. **controllers/[domain]_controller.py:**
   - Functions that implement business logic
   - Accept parsed data as arguments (not raw request objects)
   - Return data structures (dicts) — not JSON responses
   - Handle business errors (raise exceptions or return error dicts)

5. **routes/api.py:**
   - Thin route definitions using Flask Blueprints
   - Only: parse request → call controller → return JSON response
   - No business logic, no database queries, no validation beyond HTTP-level

6. **middlewares/error_handler.py:**
   - `@app.errorhandler(Exception)` that catches unhandled exceptions
   - Returns consistent error JSON: `{"error": "message", "status": 500}`
   - Logs the full error for debugging

### Import Convention (Python/Flask)
```python
# In app.py (composition root)
from config.settings import SECRET_KEY, DEBUG
from routes import register_routes

# In routes/api.py
from flask import Blueprint, request, jsonify
from controllers import user_controller, product_controller

# In controllers/user_controller.py
from models.user import User
from services.notification_service import send_notification

# In models/user.py
from database import get_db
```

**NEVER** use `from src.config import ...` unless `src/` is a proper Python package.

---

## Node.js / Express Target Structure

```
project-root/
├── src/
│   ├── app.js                  # Composition root — minimal, sets up and starts server
│   ├── config/
│   │   └── settings.js         # All configuration via process.env
│   ├── models/
│   │   ├── user.js             # One file per domain entity
│   │   └── [domain].js
│   ├── controllers/
│   │   ├── [domain]_controller.js
│   │   └── ...
│   ├── routes/
│   │   └── index.js            # Route definitions (thin)
│   ├── services/
│   │   └── [service].js        # Cross-cutting concerns
│   ├── middlewares/
│   │   └── error_handler.js    # Centralized error handling
│   └── database.js             # Database initialization
├── package.json
└── api.http                    # HTTP test file (if exists)
```

### Rules for Node.js/Express

1. **app.js** is the composition root:
   - Import express, create app
   - Import and mount route modules
   - Import and use error handler middleware
   - Start server
   - No business logic, no inline route handlers

2. **config/settings.js:**
   - Export config object using `process.env`
   - Never hardcode secrets

3. **models/[domain].js:**
   - Database access functions (or ORM model definitions)
   - One file per domain entity
   - Functions that return plain objects (not raw DB results)

4. **controllers/[domain]_controller.js:**
   - Async functions that implement business logic
   - Accept parsed data, return data structures
   - Throw or return errors — don't send HTTP responses

5. **routes/index.js:**
   - Import controllers
   - Define routes that parse request and call controller
   - Send JSON response
   - No business logic in route handlers

6. **middlewares/error_handler.js:**
   - Express error middleware: `(err, req, res, next)`
   - Returns consistent error JSON
   - Handles specific error types differently

### Import Convention (Node.js/Express)
```javascript
// In app.js
const express = require('express');
const { config } = require('./config/settings');
const routes = require('./routes');
const { errorHandler } = require('./middlewares/error_handler');

// In routes/index.js
const express = require('express');
const userController = require('../controllers/user_controller');

// In controllers/user_controller.js
const userModel = require('../models/user');
const { sendNotification } = require('../services/notification_service');
```

---

## General Rules (All Technologies)

### Directory Naming
- Use lowercase with underscores for Python: `controllers/`, `user_controller.py`
- Use lowercase with hyphens or camelCase for Node.js: `controllers/`, `userController.js`
- Follow the existing convention in the project

### File Naming — Python
- Models: `[entity].py` (e.g., `user.py`, `product.py`)
- Controllers: `[entity]_controller.py` (e.g., `user_controller.py`)
- Services: `[service]_service.py` (e.g., `notification_service.py`)
- Routes: `api.py` or `[entity]_routes.py`

### File Naming — Node.js
- Models: `[entity].js` or `[entity].model.js`
- Controllers: `[entity]_controller.js` or `[entity].controller.js`
- Services: `[service]_service.js` or `[service].service.js`
- Routes: `index.js` or `[entity].routes.js`

### __init__.py Files (Python)
- Every Python package directory must have `__init__.py`
- `__init__.py` should export the key classes/functions for easy importing
- Keep `__init__.py` minimal — just imports

### Configuration
- ALL secrets come from environment variables
- Provide sensible defaults for development: `os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')`
- Document required environment variables in README

### Response Format
- Maintain the same JSON response format as the original application
- Use consistent structure: `{"data": ..., "success": true}` or `{"error": "message"}`
- Don't change the API contract during refactoring

### Seed Data
- Keep seed data in a separate `seed.py` file at the project root
- Don't mix seed data with database initialization
- Seed data should be runnable independently

### Error Handling
- Every route must have error handling
- Use centralized error handler middleware for uncaught exceptions
- Return consistent error format across all endpoints
- Log errors with sufficient detail for debugging
- Never expose internal error details to clients in production
