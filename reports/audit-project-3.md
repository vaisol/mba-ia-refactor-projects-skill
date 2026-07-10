# Architecture Audit Report

**Project:** task-manager-api
**Stack:** Python + Flask 3.0.0
**Date:** 2026-07-10
**Files analyzed:** 12 | **~1,100 lines of code**

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| HIGH | 3 |
| MEDIUM | 3 |
| LOW | 3 |
| **Total** | **12** |

---

## Findings

### CRITICAL

#### [C1] Hardcoded SMTP Credentials
- **File:** `services/notification_service.py:9-10`
- **Description:** SMTP credentials hardcoded: `self.email_user = 'taskmanager@gmail.com'`, `self.email_password = 'senha123'`. Also `self.email_host = 'smtp.gmail.com'` and port hardcoded.
- **Impact:** Email account credentials exposed in source code. Anyone with repo access can send emails from this account.
- **Recommendation:** Use environment variables for all SMTP configuration. See refactoring-playbook.md Pattern 1.

#### [C2] MD5 Password Hashing
- **File:** `models/user.py:29,32`
- **Description:** Passwords hashed with MD5: `hashlib.md5(pwd.encode()).hexdigest()`. MD5 is cryptographically broken — it can be cracked in seconds with rainbow tables or brute force.
- **Impact:** All user passwords are easily recoverable. A database breach exposes every user's password.
- **Recommendation:** Replace with werkzeug.security.generate_password_hash (uses pbkdf2/scrypt by default). See refactoring-playbook.md Pattern 9.

#### [C3] Password Hash Exposed in API Responses
- **File:** `models/user.py:21`
- **Description:** `to_dict()` includes `'password': self.password` in its return value, exposing the password hash to any API consumer.
- **Impact:** Password hashes exposed on GET /users, GET /users/:id, and POST /users responses. Combined with weak MD5 hashing, this makes password cracking trivial.
- **Recommendation:** Remove 'password' field from to_dict() output.

---

### HIGH

#### [H1] Fake JWT Token
- **File:** `routes/user_routes.py:210`
- **Description:** Login returns `'token': 'fake-jwt-token-' + str(user.id)`. This is not a real authentication token — it's predictable and provides zero security.
- **Impact:** Any user can forge tokens for any other user by knowing their ID. No actual authentication/authorization exists.
- **Recommendation:** Implement real JWT (PyJWT) or use session-based auth. At minimum, document this as a known limitation.

#### [H2] Business Logic in Routes (No Controllers)
- **File:** `routes/task_routes.py:11-299`, `routes/user_routes.py:10-211`, `routes/report_routes.py:12-223`
- **Description:** All business logic (validation, data processing, database operations) lives directly in route handlers. Routes are 200-300 lines long with complex conditional logic.
- **Impact:** Routes are untestable without HTTP, business logic can't be reused, violating MVC separation.
- **Recommendation:** Extract business logic into controllers layer. See refactoring-playbook.md Pattern 4.

#### [H3] Duplicated Overdue Checking Logic (3x)
- **File:** `routes/task_routes.py:30-39`, `routes/report_routes.py:33-43`, `routes/user_routes.py:171-180`
- **Description:** The same overdue checking logic is implemented identically in 3 different files:
  ```python
  if t.due_date:
      if t.due_date < datetime.utcnow():
          if t.status != 'done' and t.status != 'cancelled':
              task_data['overdue'] = True
  ```
  The model already has `is_overdue()` method but it's not used in routes.
- **Impact:** Bug fixes must be applied in 3 places. Inconsistent behavior if one copy is updated but others aren't.
- **Recommendation:** Use the model's `is_overdue()` method everywhere. See refactoring-playbook.md Pattern 10.

---

### MEDIUM

#### [M1] Category CRUD Mixed into Report Routes
- **File:** `routes/report_routes.py:157-223`
- **Description:** Category CRUD operations (GET /categories, POST /categories, PUT /categories/:id, DELETE /categories/:id) are defined in report_routes.py alongside report endpoints.
- **Impact:** Misleading file organization. Category operations have nothing to do with reports.
- **Recommendation:** Move category routes to a dedicated category_routes.py.

#### [M2] Validation Duplicated (Routes vs Helpers)
- **File:** `routes/task_routes.py:86-154` vs `utils/helpers.py:57-108`
- **Description:** Task validation logic is implemented inline in routes (create_task, update_task) AND separately in utils/helpers.py process_task_data(). The helpers version is imported but rarely used.
- **Impact:** Two competing validation implementations that can diverge. Dead code in helpers.
- **Recommendation:** Consolidate validation into a single location (controllers or model methods).

#### [M3] NotificationService Class Not Used
- **File:** `services/notification_service.py:4-48`
- **Description:** The `NotificationService` class is defined with email sending capabilities but is never instantiated or called anywhere in the application.
- **Impact:** Dead code. SMTP credentials still hardcoded for no reason.
- **Recommendation:** Either integrate the service into the application or remove it. If keeping, fix hardcoded credentials.

---

### LOW

#### [L1] Unused Imports
- **File:** `app.py:7`, `routes/task_routes.py:7`, `utils/helpers.py:3-7`
- **Description:** Multiple unused imports: `os, sys, json, datetime` in app.py; `json, os, sys, time` in task_routes; `os, json, sys, math, hashlib` in helpers.
- **Impact:** Code clutter, confusion about what's actually used.
- **Recommendation:** Remove all unused imports.

#### [L2] Bare Except Clauses
- **File:** `routes/task_routes.py:62,137,204,236`, `routes/user_routes.py:130,149`
- **Description:** Multiple bare `except:` or `except:` without specific exception types. These catch ALL exceptions including KeyboardInterrupt and SystemExit.
- **Impact:** Masks real errors, makes debugging difficult, can hide critical failures.
- **Recommendation:** Catch specific exceptions (e.g., `except SQLAlchemyError:`, `except ValueError:`).

#### [L3] Magic Numbers in Validation
- **File:** `routes/task_routes.py:96-100,113-114`, `utils/helpers.py:110-116`
- **Description:** Magic numbers scattered: `3` for min title length, `200` for max, `1-5` for priority range, `4` for min password. These are defined as constants in helpers.py but not used by routes.
- **Impact:** Inconsistent values if changed in one place but not another.
- **Recommendation:** Use the constants from helpers.py consistently, or define them in the model.

---

## Recommendations Summary

1. **Immediate (CRITICAL):** Fix password hashing (MD5 → werkzeug), remove password from API responses, move SMTP credentials to env vars.
2. **Short-term (HIGH):** Add controllers layer, centralize overdue logic in model, implement real JWT auth.
3. **Medium-term (MEDIUM):** Separate category routes, consolidate validation, remove dead NotificationService code.
4. **Optional (LOW):** Clean unused imports, fix bare excepts, use validation constants consistently.
