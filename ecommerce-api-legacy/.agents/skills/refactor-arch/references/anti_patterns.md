# Anti-Patterns Catalog

This catalog lists common anti-patterns, their detection signs, and severity.

## 1. SQL Injection (CRITICAL)
- **Signs**: String concatenation or f-strings used to build SQL queries.
- **Example**: `cursor.execute("SELECT * FROM users WHERE id = " + user_id)`
- **Risk**: Unauthorized data access or modification.

## 2. Hardcoded Secrets (CRITICAL)
- **Signs**: API keys, passwords, or secret tokens assigned directly to variables.
- **Example**: `API_KEY = "12345-ABCDE"` or `db_password = "root"`
- **Risk**: Security breach if code is exposed.

## 3. Sensitive Data Exposure in Logs (CRITICAL)
- **Signs**: Printing or logging raw request bodies, credit card numbers, or passwords.
- **Example**: `console.log("Processando cartão " + card_number)`
- **Risk**: Compliance violation (PCI-DSS), data theft.

## 4. Admin Backdoor / Arbitrary Query Execution (CRITICAL)
- **Signs**: Endpoints that accept and execute raw SQL or shell commands from the user.
- **Example**: `cursor.execute(request.json['query'])`
- **Risk**: Remote Code Execution (RCE), full database takeover.

## 5. God Object / Massive Controller (HIGH)
- **Signs**: A single class or file exceeding 300-500 lines handling multiple responsibilities (DB, Routes, Logic).
- **Example**: `AppManager.js` containing all route logic and database setup.
- **Risk**: Poor maintainability, difficult testing.

## 6. Business Logic in Presentation Layer (HIGH)
- **Signs**: Complex calculations, validations, or orchestration directly inside route handlers.
- **Example**: Calculating sales commission inside a `GET /reports` route.
- **Risk**: Logic duplication, inability to reuse business rules.

## 7. Weak Cryptography (HIGH)
- **Signs**: Using MD5, SHA1 for passwords, or custom "obfuscation" algorithms.
- **Example**: `base64(password)` as a hash.
- **Risk**: Easy password cracking.

## 8. N+1 Query Problem (MEDIUM)
- **Signs**: Executing a database query inside a loop for each item in a collection.
- **Example**: `for user in users: db.get_profile(user.id)`
- **Risk**: Significant performance degradation.

## 9. Inconsistent Error Handling (MEDIUM)
- **Signs**: Mixing `try-except` with empty `except`, or returning different data formats (JSON vs Text) on error.
- **Risk**: Unpredictable API behavior, difficult debugging.

## 10. Magic Numbers / Strings (LOW)
- **Signs**: Literal values used without explanation or constants.
- **Example**: `if status == 3:` instead of `if status == Status.COMPLETED:`.
- **Risk**: Reduced readability.

## 11. Deprecated API Usage (MEDIUM)
- **Signs**: Using obsolete libraries or methods.
- **Examples**:
  - Python: Using `os.path` instead of `pathlib`.
  - Node.js: Using `request` library (deprecated) instead of `axios` or `fetch`.
  - Express: Using `app.configure()` (removed in v4).
- **Risk**: Security vulnerabilities, incompatibility with future updates.
