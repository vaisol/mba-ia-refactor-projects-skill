---
name: refactor-arch
description: Analyze any codebase, audit for anti-patterns and architectural issues, then refactor to clean MVC architecture. Technology-agnostic — works with Python/Flask, Node.js/Express, and other web frameworks.
---

# Refactor Architecture Skill

This skill analyzes a codebase, generates an architecture audit report, and refactors the project to a clean MVC (Model-View-Controller) pattern. It works with any web framework.

## Reference Files

Before executing each phase, read the relevant reference files:

- **project-analysis.md** — Heuristics for detecting language, framework, database, and domain
- **anti-pattern-catalog.md** — Catalog of anti-patterns with detection signals and severity levels
- **report-template.md** — Standardized format for the audit report
- **architecture-guidelines.md** — Target MVC structure rules per technology
- **refactoring-playbook.md** — Concrete transformation patterns with before/after code examples

---

## PHASE 1: PROJECT ANALYSIS

**Goal:** Detect the technology stack, map the current architecture, and print a summary.

### Steps

1. **Detect language and framework:**
   - Read dependency files: `requirements.txt`, `setup.py`, `pyproject.toml` (Python), `package.json` (Node.js), `Gemfile` (Ruby), `go.mod` (Go), `pom.xml` / `build.gradle` (Java)
   - Scan source files for import patterns (e.g., `from flask import` → Flask, `require('express')` → Express)
   - Read `project-analysis.md` for full detection heuristics

2. **Map the current architecture:**
   - List all source files (exclude node_modules, venv, __pycache__, .git, dist, build)
   - Identify the entry point (e.g., `app.js`, `app.py`, `main.py`, `index.js`, `server.js`)
   - Detect current layer separation: Are there separate models/, controllers/, routes/, services/ directories?
   - Count total source files and approximate lines of code

3. **Detect the application domain:**
   - Read route/endpoint definitions to understand the business domain
   - Read model/table definitions to understand data structures
   - Describe the domain in 1 sentence (e.g., "E-commerce API for products, orders, and users")

4. **Detect database:**
   - Look for database driver imports (sqlite3, psycopg2, mysql, mongoose, sequelize, knex, typeorm, sqlalchemy, flask_sqlalchemy)
   - Check for ORM usage
   - List detected tables/models

5. **Print the summary:**

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      [detected language]
Framework:     [detected framework + version]
Dependencies:  [list key dependencies]
Domain:        [application domain description]
Architecture:  [current architecture description]
Source files:  [N files analyzed]
DB tables:     [list tables/models]
Entry point:   [entry point file]
================================
```

**Proceed to Phase 2 after printing the summary.**

---

## PHASE 2: ARCHITECTURE AUDIT

**Goal:** Scan the codebase against the anti-pattern catalog, generate a structured audit report, and **pause for user confirmation before proceeding to Phase 3.**

### Steps

1. **Load the anti-pattern catalog:**
   - Read `anti-pattern-catalog.md` completely
   - Understand each anti-pattern's detection signals and severity

2. **Scan every source file:**
   For each source file, check for every anti-pattern in the catalog:
   - Read the file content
   - Apply detection signals from the catalog
   - When a match is found, record:
     - **Severity** (CRITICAL / HIGH / MEDIUM / LOW)
     - **Anti-pattern name**
     - **File path and line numbers** (exact)
     - **Description** of the issue
     - **Impact** on maintainability/security
     - **Recommendation** for fixing

3. **Check for deprecated APIs:**
   - Look for deprecated function calls, library methods, or patterns
   - Common examples:
     - Python: `@app.before_first_request` (removed in Flask 2.3), `werkzeug.contrib` (removed)
     - Node.js: `new Buffer()` (deprecated), `url.parse()` (deprecated in favor of `new URL()`), `path.exists` (deprecated)
     - Express: `app.del()` (use `app.delete()`), `res.json(status, obj)` (use `res.status(status).json(obj)`)

4. **Generate the audit report:**
   - Read `report-template.md` for the exact format
   - Sort findings by severity: CRITICAL first, then HIGH, MEDIUM, LOW
   - Within same severity, sort by file path alphabetically
   - Include exact line numbers for every finding

5. **Print the report to the user:**

```
================================
PHASE 2: ARCHITECTURE AUDIT REPORT
================================
Project: [project name]
Stack:   [language + framework]
Files:   [N analyzed] | ~[M] lines of code

Summary
CRITICAL: [count] | HIGH: [count] | MEDIUM: [count] | LOW: [count]

Findings

[SEVERITY] Anti-Pattern Name
File: [path:line-start-line-end]
Description: [what is wrong]
Impact: [what this causes]
Recommendation: [how to fix]

[... repeat for each finding ...]

================================
Total: [N] findings
================================
```

6. **SAVE THE REPORT:** Write the full report to `reports/audit-[project-name].md` in the project root. Create the `reports/` directory if it does not exist.

7. **PAUSE AND ASK FOR CONFIRMATION:**
   - After printing the report, STOP and ask the user:
     > "Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]"
   - **DO NOT proceed to Phase 3 unless the user explicitly confirms with "y" or "yes".**
   - If the user says no, stop and wait for further instructions.

---

## PHASE 3: MVC REFACTORING

**Goal:** Restructure the project to clean MVC architecture, fix all findings, and validate the result.

### Prerequisites
- User has confirmed with "y" or "yes" to proceed from Phase 2

### Steps

1. **Load refactoring guidelines:**
   - Read `architecture-guidelines.md` for the target structure
   - Read `refactoring-playbook.md` for transformation patterns
   - Determine the correct target structure based on the detected technology stack

2. **Plan the target directory structure:**
   - Based on the technology stack, determine the MVC layout
   - **CRITICAL RULE:** Import paths MUST match the actual file locations. Do NOT create imports like `from src.config import settings` if `src/` does not exist as a package. Keep imports relative to the project root.

3. **Create the target directory structure:**
   - Create all necessary directories and `__init__.py` files (Python) or index files (Node.js)
   - Keep the original entry point file (e.g., `app.py`, `app.js`) as the composition root

4. **Apply transformations from the playbook:**
   For each finding in the audit report, apply the corresponding transformation:
   - Extract configuration to a config module
   - Replace string-concatenated SQL with parameterized queries or ORM
   - Break God classes/files into separate model, controller, and route files
   - Extract business logic from routes into controllers
   - Create proper model classes with serialization methods
   - Extract services for cross-cutting concerns (notifications, payments, etc.)
   - Add centralized error handling middleware
   - Fix deprecated API usage
   - Fix security issues (hardcoded secrets, weak crypto, SQL injection)
   - Eliminate duplicated code by extracting shared utilities

5. **Ensure all original endpoints are preserved:**
   - List every endpoint from the original code
   - Verify each one exists in the new structure
   - Ensure request/response format is identical

6. **Validate the refactored application:**
   - **Install dependencies:** Run the appropriate install command (`pip install -r requirements.txt` or `npm install`)
   - **Boot the application:** Start the server and check for import errors or crashes
   - **Test endpoints:** Hit each endpoint and verify it returns the expected response
   - If validation fails, fix the issues and re-validate

7. **Print the completion summary:**

```
================================
PHASE 3: REFACTORING COMPLETE
================================
New Project Structure:
[tree of new directory structure]

Validation
  [checkmark] Application boots without errors
  [checkmark] All endpoints respond correctly
  [checkmark] Anti-patterns resolved

Changes Made:
  - [list major transformations applied]

================================
```

**The skill is complete. The project is now structured in MVC pattern.**

---

## IMPORTANT RULES

1. **NEVER delete business logic.** When breaking a God file apart, EVERY function and piece of logic must be redistributed to the appropriate MVC layer. Code must be MOVED, not removed.

2. **Import paths must match file system.** If the project root is `myproject/` and files are at `myproject/models/user.py`, the import should be `from models.user import User` (relative to root), NOT `from src.models.user import User`.

3. **Preserve all endpoints.** Every API endpoint that existed before refactoring must exist after, with the same URL, HTTP method, and response format.

4. **Preserve seed data.** If the project has seed/fixture data, keep it in a `seed.py` or similar file at the project root.

5. **Config must use environment variables.** Replace all hardcoded secrets and configuration values with `os.environ.get()` calls, with sensible defaults for development.

6. **Always pause between Phase 2 and Phase 3.** The user MUST review the audit report before any files are modified.

7. **Validation is mandatory.** Phase 3 is not complete until the application boots and endpoints respond. If boot fails, fix the errors before declaring completion.
