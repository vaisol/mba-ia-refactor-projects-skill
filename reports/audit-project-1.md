# Architecture Audit Report

**Project:** code-smells-project
**Stack:** Python + Flask 3.1.1
**Date:** 2026-07-10
**Files analyzed:** 4 | **~780 lines of code**

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 4 |
| HIGH | 4 |
| MEDIUM | 2 |
| LOW | 3 |
| **Total** | **13** |

---

## Findings

### CRITICAL

#### [C1] SQL Injection via String Concatenation
- **File:** `models.py:28,48-49,57-60,68,92,110,127-128,140,148-150,155,157-160,163-165,174,188,220,224,280,291-297`
- **Description:** SQL queries are built using Python string concatenation with user-controlled values throughout models.py. Every single query function uses this dangerous pattern. For example, line 28: `cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))` and line 110: `cursor.execute("SELECT * FROM usuarios WHERE email = '" + email + "' AND senha = '" + senha + "'")`.
- **Impact:** Attackers can inject arbitrary SQL commands to steal, modify, or destroy all data in the database. This is the most critical security vulnerability.
- **Recommendation:** Replace all string-concatenated SQL with parameterized queries using `?` placeholders. See refactoring-playbook.md Pattern 2.

#### [C2] Arbitrary SQL Execution Endpoint
- **File:** `app.py:59-78`
- **Description:** The `/admin/query` endpoint accepts arbitrary SQL from the request body and executes it directly: `cursor.execute(query)`. This allows anyone to run any SQL statement including DROP TABLE, DELETE, or data extraction.
- **Impact:** Complete database compromise. Any attacker can extract all data or destroy the database.
- **Recommendation:** Remove this endpoint entirely. If admin functionality is needed, implement specific, controlled admin operations.

#### [C3] Hardcoded Secret Key
- **File:** `app.py:7`
- **Description:** Flask SECRET_KEY is hardcoded as `"minha-chave-super-secreta-123"`. This key is used for session signing and CSRF protection.
- **Impact:** Anyone with source code access can forge sessions and bypass security controls.
- **Recommendation:** Use environment variable: `os.environ.get("SECRET_KEY", "dev-secret-change-in-production")`

#### [C4] Secret Key Leaked in Health Check Response
- **File:** `controllers.py:289`
- **Description:** The health_check endpoint returns the SECRET_KEY in its JSON response: `"secret_key": "minha-chave-super-secreta-123"`. It also exposes debug mode and db_path.
- **Impact:** Complete exposure of application secrets to any client that calls /health.
- **Recommendation:** Remove secret_key, debug flag, and db_path from health check response. Only return operational status.

---

### HIGH

#### [H1] God File: controllers.py (292 lines)
- **File:** `controllers.py:1-292`
- **Description:** A single file contains ALL business logic for products, users, orders, and reports. It handles HTTP parsing, validation, database operations, and notification (via print statements).
- **Impact:** Impossible to test individual domains in isolation, changes in one domain risk breaking others, no code reuse.
- **Recommendation:** Split into domain-specific controllers: produto_controller.py, usuario_controller.py, pedido_controller.py, relatorio_controller.py.

#### [H2] God File: models.py (314 lines)
- **File:** `models.py:1-314`
- **Description:** A single file contains ALL database operations for 4 domains (products, users, orders, reports). It mixes raw SQL, data mapping, and business rules.
- **Impact:** High coupling, difficult to maintain, every model change affects the entire file.
- **Recommendation:** Split into domain-specific model files: produto.py, usuario.py, pedido.py, relatorio.py.

#### [H3] N+1 Query Problem
- **File:** `models.py:171-201,203-233`
- **Description:** `get_pedidos_usuario()` and `get_todos_pedidos()` execute nested loops with individual queries: for each order, query its items; for each item, query the product name. With 100 orders of 3 items each, this produces 1 + 100 + 300 = 401 queries.
- **Impact:** Severe performance degradation. Response time grows linearly with data volume.
- **Recommendation:** Use JOINs or batch queries with `IN` clauses to fetch related data in fewer queries.

#### [H4] Passwords Exposed in API Responses
- **File:** `models.py:79-86`
- **Description:** `get_todos_usuarios()` returns the `senha` field in its response dict, exposing password data to API consumers.
- **Impact:** Password hashes exposed to any client calling GET /usuarios.
- **Recommendation:** Exclude sensitive fields from model serialization. Use `to_dict()` methods that explicitly exclude passwords.

---

### MEDIUM

#### [M1] Notification via Print Statements
- **File:** `controllers.py:208-210,248-250`
- **Description:** Order creation and status changes trigger notifications via `print("ENVIANDO EMAIL: ...")`. This is not a real notification system and pollutes stdout.
- **Impact:** No actual notifications sent, debug output in production logs, tight coupling to stdout.
- **Recommendation:** Extract to a notification service that can be swapped for real implementations (email, SMS, push).

#### [M2] Duplicated Validation Logic
- **File:** `controllers.py:24-62,64-96`
- **Description:** Product validation logic (required fields, range checks, category validation) is duplicated verbatim between `criar_produto()` and `atualizar_produto()`.
- **Impact:** Bugs from inconsistent fixes, violation of DRY principle, larger codebase.
- **Recommendation:** Extract shared validation into a single `validate_produto_data()` function.

---

### LOW

#### [L1] Debug Print Statements Throughout
- **File:** `controllers.py:8,57,106,161,179,182,219`
- **Description:** Debug `print()` calls scattered across controllers: `print("Listando " + str(len(produtos)) + " produtos")`, `print("Produto criado com ID: " + str(id))`, etc.
- **Impact:** Pollutes stdout, no structured logging, difficult to control log levels.
- **Recommendation:** Replace with Python `logging` module for structured, configurable logging.

#### [L2] Bare Exception Handling
- **File:** `controllers.py:10-12,21-22,60-62,95-96,108-109,125-126,133-134,143-144,164-165,185-186,218-220,226-227,234-235,254-255,261-262,291-292`
- **Description:** Every route handler catches `Exception` generically and returns `str(e)` to the client, potentially leaking internal details.
- **Impact:** Internal error details exposed to clients, difficult to handle specific error types.
- **Recommendation:** Use centralized error handling middleware with specific exception types.

#### [L3] Manual Dict Construction
- **File:** `models.py:12-21,31-40,79-86,94-102,114-119,178-184,211-218,264-273,304-313`
- **Description:** Every model function manually constructs return dictionaries field-by-field instead of using a `to_dict()` method or serialization utility.
- **Impact:** Tedious to maintain, easy to forget fields, inconsistent serialization.
- **Recommendation:** Add `to_dict()` methods to model representations that can be reused across the application.

---

## Recommendations Summary

1. **Immediate (CRITICAL):** Remove /admin/query endpoint, parameterize all SQL queries, extract SECRET_KEY to env vars, remove secret from health check response.
2. **Short-term (HIGH):** Split God files into MVC layers, fix N+1 queries, exclude passwords from API responses.
3. **Medium-term (MEDIUM):** Create notification service, extract shared validation logic.
4. **Optional (LOW):** Replace print statements with logging, add centralized error handling, add to_dict() methods.
