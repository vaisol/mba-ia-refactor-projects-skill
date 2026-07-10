# Anti-Pattern Catalog

Catalog of architectural anti-patterns and code smells for web applications. Each entry includes detection signals, severity classification, and examples.

---

## Severity Scale

- **CRITICAL:** Security vulnerabilities, data exposure, or complete architectural violations that prevent correct functioning
- **HIGH:** Strong violations of MVC/SOLID principles that severely hinder maintainability and testing
- **MEDIUM:** Code duplication, moderate performance issues, or missing best practices
- **LOW:** Readability issues, poor naming, magic numbers, minor improvements

---

## 1. SQL Injection

**Severity:** CRITICAL

**Detection Signals:**
- SQL queries built with string concatenation: `"SELECT * FROM users WHERE id = " + str(id)`
- SQL queries built with f-strings: `f"SELECT * FROM users WHERE id = {id}"`
- SQL queries built with `.format()`: `"SELECT * FROM users WHERE id = {}".format(id)`
- User input passed directly into SQL strings without parameterization
- `cursor.execute(query)` where `query` is constructed from user input

**Impact:** Attackers can execute arbitrary SQL, steal data, modify data, or destroy the database.

**Fix:** Use parameterized queries (`cursor.execute("SELECT * FROM users WHERE id = ?", (id,))`) or an ORM.

---

## 2. Hardcoded Secrets

**Severity:** CRITICAL

**Detection Signals:**
- API keys, passwords, or tokens hardcoded in source files
- `SECRET_KEY = "some-value"` in application code
- Database credentials in source: `db_password = "admin123"`
- Payment gateway keys: `paymentKey = "pk_live_..."`
- SMTP credentials: `email_password = "senha123"`
- Any string that looks like a secret assigned to a variable in source code

**Impact:** Secrets are exposed in version control, to anyone with repo access, and in deployment logs.

**Fix:** Use environment variables (`os.environ.get('SECRET_KEY', 'dev-default')`) or a config file excluded from version control.

---

## 3. God Class / God File

**Severity:** HIGH

**Detection Signals:**
- A single file containing more than 200 lines of business logic
- A single file handling multiple unrelated domains (e.g., users + products + orders)
- A single class with more than 10 methods doing different things
- A file that imports and uses database, routes, business logic, and utilities all together
- "Manager" or "Service" classes that do everything

**Impact:** Impossible to test in isolation, changes in one area break others, no reusability, merge conflicts.

**Fix:** Split into separate files by domain/responsibility: models, controllers, services, routes.

---

## 4. N+1 Query Problem

**Severity:** HIGH

**Detection Signals:**
- Query inside a `for` loop: `for item in items: cursor.execute("SELECT ... WHERE id = ?", item.id)`
- Nested loops that query the database: fetching orders, then for each order fetching items, then for each item fetching product name
- Using `relationship().all()` inside a loop when eager loading would work
- Multiple sequential queries where a JOIN would be more efficient
- Creating new cursor objects inside loops

**Impact:** Severe performance degradation. 100 items = 100+ database queries instead of 1-2.

**Fix:** Use JOINs, eager loading, batch queries, or `IN` clauses to fetch related data in fewer queries.

---

## 5. Callback Hell (Node.js)

**Severity:** HIGH

**Detection Signals:**
- Nested callbacks more than 3 levels deep
- Arrow functions nested inside `.get()`, `.run()`, `.all()` callbacks
- "Pyramid of doom" indentation pattern
- `self = this` workarounds
- Complex flow control with counters to track when all async operations complete

**Impact:** Unreadable code, impossible to debug, error handling is fragile, logic flow is hard to follow.

**Fix:** Use async/await with Promises, or extract callback logic into named functions, or use a control-flow library.

---

## 6. Missing Input Validation

**Severity:** MEDIUM

**Detection Signals:**
- Endpoints that read `request.get_json()` without checking required fields
- No validation of data types (e.g., expecting int but getting string)
- No validation of data ranges (e.g., negative prices, empty strings)
- No email format validation
- No length checks on string inputs
- Endpoints that accept arbitrary SQL or code input without sanitization

**Impact:** Application crashes on bad input, data corruption, security vulnerabilities.

**Fix:** Add validation at the controller/route level for all inputs. Use schema validation libraries (marshmallow, joi, pydantic).

---

## 7. Global Mutable State

**Severity:** MEDIUM

**Detection Signals:**
- Module-level variables that are modified at runtime: `globalCache = {}`, `totalRevenue = 0`
- `global` keyword in Python functions
- Shared state between requests without proper synchronization
- Singletons that hold mutable state
- Application-level counters or caches without expiration

**Impact:** Race conditions, unpredictable behavior, impossible to test, data corruption in concurrent environments.

**Fix:** Use request-scoped state, database for persistent state, Redis/cache for shared state, or dependency injection.

---

## 8. Deprecated API Usage

**Severity:** MEDIUM

**Detection Signals:**
- Python: `@app.before_first_request` (removed in Flask 2.3)
- Python: `from werkzeug.contrib` (removed)
- Python: `hashlib.md5()` for password hashing (deprecated for security)
- Node.js: `new Buffer()` (deprecated since Node 6)
- Node.js: `url.parse()` (deprecated in favor of `new URL()`)
- Node.js: `path.exists()` (deprecated, use `fs.existsSync()`)
- Node.js: `res.json(status, obj)` (deprecated, use `res.status(status).json(obj)`)
- Express: `app.del()` (use `app.delete()`)
- Any use of libraries marked as deprecated in their documentation

**Impact:** May break on framework upgrades, security vulnerabilities, missing improvements in newer APIs.

**Fix:** Replace with the recommended modern alternative.

---

## 9. Broken / Weak Cryptography

**Severity:** HIGH

**Detection Signals:**
- MD5 or SHA1 used for password hashing
- Custom "encryption" functions that are not real cryptographic operations
- `base64` encoding presented as "encryption" or "hashing"
- Passwords stored in plaintext
- Symmetric encryption for sensitive data without proper key management
- `hashlib.md5(password.encode()).hexdigest()` for password storage

**Impact:** Passwords can be cracked in seconds, data is easily compromised, regulatory violations.

**Fix:** Use bcrypt, scrypt, or argon2 for password hashing. Use proper encryption libraries (cryptography, crypto) for data encryption.

---

## 10. Duplicated Code

**Severity:** MEDIUM

**Detection Signals:**
- The same validation logic appearing in multiple files
- The same database query pattern repeated across functions
- The same business logic (e.g., overdue checking) implemented in 3+ places
- Copy-pasted blocks with minor variations
- Similar `to_dict()` or serialization methods in multiple places
- Same error handling pattern repeated in every route

**Impact:** Bugs from inconsistent fixes, higher maintenance cost, larger codebase than necessary.

**Fix:** Extract shared logic into utility functions, model methods, or service classes. Follow DRY principle.

---

## 11. Fat Controller / Fat Route

**Severity:** HIGH

**Detection Signals:**
- Business logic inside route handler functions (validation, computation, notification)
- Database queries directly in route handlers
- Complex conditional logic in route handlers
- Route files that are hundreds of lines long
- Routes that call models directly instead of going through controllers

**Impact:** Routes become untestable, business logic is tied to HTTP layer, impossible to reuse logic.

**Fix:** Extract business logic into controller functions or service classes. Routes should only handle HTTP concerns (parse request, call controller, return response).

---

## 12. Exposed Sensitive Data in Responses

**Severity:** CRITICAL

**Detection Signals:**
- API responses that include password hashes, salt, or plaintext passwords
- Health check endpoints that return secret keys, debug flags, or internal paths
- Error messages that expose stack traces, SQL queries, or internal file paths
- Debug mode enabled in production configuration
- Verbose error responses to clients

**Impact:** Information disclosure to attackers, credential theft, security audit failures.

**Fix:** Exclude sensitive fields from serialization, remove debug info from production responses, use proper error handling that hides internals.

---

## 13. Orphaned Records (Missing Cascade Delete)

**Severity:** MEDIUM

**Detection Signals:**
- Deleting a parent record without deleting related child records
- No foreign key constraints or cascade rules
- Manual deletion of parent without handling dependents
- Comments like "mas as matrículas e pagamentos ficaram sujos no banco"

**Impact:** Data integrity issues, orphaned records accumulate, broken references, inconsistent state.

**Fix:** Implement cascade deletes (database-level or application-level), use soft deletes, or add foreign key constraints with ON DELETE CASCADE.

---

## 14. Missing Error Handling

**Severity:** MEDIUM

**Detection Signals:**
- Bare `except:` or `except Exception:` without specific exception types
- `try/except` that just prints the error and returns a generic 500
- No error handling middleware
- Swallowed exceptions (except block that does nothing useful)
- Inconsistent error response formats across endpoints

**Impact:** Difficult to debug production issues, inconsistent error responses, potential data corruption on partial failures.

**Fix:** Catch specific exceptions, use centralized error handling middleware, return consistent error response format, log errors properly.
