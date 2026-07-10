# Architecture Audit Report

**Project:** ecommerce-api-legacy
**Stack:** Node.js + Express 4.18.2
**Date:** 2026-07-10
**Files analyzed:** 3 | **~180 lines of code**

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 3 |
| HIGH | 4 |
| MEDIUM | 2 |
| LOW | 2 |
| **Total** | **11** |

---

## Findings

### CRITICAL

#### [C1] Hardcoded Credentials and API Keys
- **File:** `utils.js:2-4`
- **Description:** Database credentials (`dbUser: "admin_master"`, `dbPass: "senha_super_secreta_prod_123"`) and payment gateway key (`paymentGatewayKey: "pk_live_1234567890abcdef"`) are hardcoded in source code.
- **Impact:** Anyone with repo access has production database credentials and payment API keys. Credentials in version control cannot be rotated without code changes.
- **Recommendation:** Move all secrets to environment variables with dev defaults. See refactoring-playbook.md Pattern 1.

#### [C2] Broken Cryptography (badCrypto)
- **File:** `utils.js:17-23`
- **Description:** `badCrypto()` is not real cryptographic hashing. It loops 10,000 times concatenating base64 substrings, producing a 10-character output. This is trivially reversible and provides zero security.
- **Impact:** Passwords can be cracked instantly. Any attacker can impersonate any user.
- **Recommendation:** Replace with bcrypt using proper salt rounds. See refactoring-playbook.md Pattern 9.

#### [C3] Raw Credit Card Processing and Logging
- **File:** `AppManager.js:33,45`
- **Description:** The checkout endpoint accepts a raw card number (`req.body.card`) and logs it to console: `console.log(\`Processando cartão ${cc} na chave ${config.paymentGatewayKey}\`)`. Card numbers are stored and transmitted in plaintext.
- **Impact:** PCI DSS violation. Card data exposed in logs, memory, and potentially database. Payment gateway key exposed alongside card data.
- **Recommendation:** Never log card numbers. Use a payment gateway tokenization system. Mask card numbers in any storage.

---

### HIGH

#### [H1] God Object: AppManager Class
- **File:** `AppManager.js:4-139`
- **Description:** The `AppManager` class handles database initialization, table creation, seed data, route setup, and all business logic (checkout, financial reporting, user deletion) in a single 139-line file.
- **Impact:** Impossible to test individual functions, all concerns coupled together, any change risks breaking unrelated functionality.
- **Recommendation:** Split into database.js (init), models/ (data access), controllers/ (business logic), routes/ (HTTP). See refactoring-playbook.md Pattern 3.

#### [H2] Callback Hell in Financial Report
- **File:** `AppManager.js:80-128`
- **Description:** The financial report endpoint has 4 levels of nested callbacks: `db.all(courses) → forEach → db.all(enrollments) → forEach → db.get(user) → db.get(payment)`. Complex counter logic (`coursesPending`, `enrPending`) tracks when all async operations complete.
- **Impact:** Unreadable code, fragile error handling, impossible to debug, race conditions with counter-based completion tracking.
- **Recommendation:** Convert to async/await with promisified database helpers. See refactoring-playbook.md Pattern 6.

#### [H3] Global Mutable State
- **File:** `utils.js:9-10`
- **Description:** `globalCache = {}` and `totalRevenue = 0` are module-level mutable variables shared across all requests without synchronization.
- **Impact:** Race conditions in concurrent requests, memory leak from unbounded cache growth, unpredictable behavior.
- **Recommendation:** Use request-scoped state or database for persistent data. Remove global mutable variables.

#### [H4] Orphaned Records on User Delete
- **File:** `AppManager.js:131-137`
- **Description:** `DELETE /api/users/:id` deletes only the user record, leaving enrollments, payments, and audit logs orphaned. The response even acknowledges this: "mas as matrículas e pagamentos ficaram sujos no banco."
- **Impact:** Data integrity violation. Orphaned records accumulate, breaking referential integrity and causing incorrect financial reports.
- **Recommendation:** Implement cascade delete or soft delete. Delete dependent records before or after deleting the user.

---

### MEDIUM

#### [M1] No Input Validation on Checkout
- **File:** `AppManager.js:28-35`
- **Description:** The checkout endpoint only checks for presence of required fields (`if (!u || !e || !cid || !cc)`). No validation of email format, card number format, course ID type, or user name length.
- **Impact:** Application crashes on malformed input, potential injection through unexpected data types.
- **Recommendation:** Add proper validation for all input fields (email format, numeric types, string lengths).

#### [M2] Deprecated/Insecure Buffer Usage
- **File:** `utils.js:20`
- **Description:** `Buffer.from(pwd).toString('base64')` used in the crypto function. While Buffer itself isn't deprecated, using it for password "hashing" is a security anti-pattern.
- **Impact:** Part of the broken cryptography system. Base64 is encoding, not hashing.
- **Recommendation:** Remove entirely and replace with bcrypt.

---

### LOW

#### [L1] Sensitive Data in Console Logs
- **File:** `AppManager.js:45`
- **Description:** Payment gateway key and card number logged to console: `console.log(\`Processando cartão ${cc} na chave ${config.paymentGatewayKey}\`)`.
- **Impact:** Secrets exposed in log files, container logs, and monitoring systems.
- **Recommendation:** Never log sensitive data. Use structured logging with redaction.

#### [L2] Magic Strings Throughout
- **File:** `AppManager.js:18,19,46,57`
- **Description:** Hardcoded strings like `"PAID"`, `"DENIED"`, seed data values, and SQL queries scattered throughout the code.
- **Impact:** Typos cause silent failures, difficult to change values consistently.
- **Recommendation:** Extract constants to config or dedicated constants file.

---

## Recommendations Summary

1. **Immediate (CRITICAL):** Move secrets to env vars, replace badCrypto with bcrypt, remove card number logging, add payment tokenization.
2. **Short-term (HIGH):** Break God Object into MVC layers, convert callbacks to async/await, remove global state, implement cascade delete.
3. **Medium-term (MEDIUM):** Add input validation, fix deprecated patterns.
4. **Optional (LOW):** Remove sensitive logging, extract constants.
