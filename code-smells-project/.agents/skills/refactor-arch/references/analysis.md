# Project Analysis Heuristics

This document provides heuristics for detecting the technology stack and mapping the architecture of a project.

## 1. Stack Detection

### Language & Framework
- **Node.js/Express**:
  - Presence of `package.json`.
  - Dependencies like `express`, `body-parser` in `package.json`.
  - `require('express')` or `import express from 'express'` in code.
- **Python/Flask**:
  - Presence of `requirements.txt` or `Pipfile`.
  - Dependencies like `Flask`, `flask-sqlalchemy`, `flask-cors`.
  - `from flask import Flask` in code.
- **Python/Django**:
  - Presence of `manage.py`.
  - `django` in `requirements.txt`.

### Database
- **SQLite**: Presence of `.db`, `.sqlite`, `.sqlite3` files or `sqlite3` in dependencies.
- **PostgreSQL**: `psycopg2` or `pg` in dependencies.
- **MySQL**: `mysql-connector` or `mysql` in dependencies.
- **MongoDB**: `pymongo` or `mongoose` in dependencies.

## 2. Architecture Mapping

### Current State Assessment
- **Monolithic/Spaghetti**: Most logic in a single file (e.g., `app.py`, `AppManager.js`).
- **Partial MVC**: Folders like `models`, `routes`, but logic is still leaked.
- **Layered**: Clear separation between `controllers`, `services`, `repositories`.

### Entry Point Identification
- Search for the main file that initializes the server (e.g., `app.py`, `index.js`, `server.ts`).
- Identify route definitions (e.g., `app.route`, `app.get`, `router.use`).

### Data Flow Mapping
1. Identify where requests enter (Controllers/Routes).
2. Trace where business logic is executed (In-route? Service? Model?).
3. Trace where database access happens (Raw SQL in route? ORM in model?).
