# Audit Report Template

Use this exact format when generating the Phase 2 audit report.

---

## Report Structure

```markdown
# Architecture Audit Report

**Project:** [project-name]
**Stack:** [language] + [framework]
**Date:** [current-date]
**Files analyzed:** [N] | **Lines of code:** ~[M]

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | [N] |
| HIGH | [N] |
| MEDIUM | [N] |
| LOW | [N] |
| **Total** | **[N]** |

---

## Findings

### CRITICAL

#### [C1] [Anti-Pattern Name]
- **File:** `[file_path]:[line_start]-[line_end]`
- **Description:** [What is wrong — be specific with code references]
- **Impact:** [What this causes for security, maintainability, or correctness]
- **Recommendation:** [How to fix it — reference the playbook pattern if applicable]

#### [C2] [Anti-Pattern Name]
- **File:** `[file_path]:[line_start]-[line_end]`
- **Description:** [description]
- **Impact:** [impact]
- **Recommendation:** [recommendation]

---

### HIGH

#### [H1] [Anti-Pattern Name]
- **File:** `[file_path]:[line_start]-[line_end]`
- **Description:** [description]
- **Impact:** [impact]
- **Recommendation:** [recommendation]

---

### MEDIUM

#### [M1] [Anti-Pattern Name]
- **File:** `[file_path]:[line_start]-[line_end]`
- **Description:** [description]
- **Impact:** [impact]
- **Recommendation:** [recommendation]

---

### LOW

#### [L1] [Anti-Pattern Name]
- **File:** `[file_path]:[line_start]-[line_end]`
- **Description:** [description]
- **Impact:** [impact]
- **Recommendation:** [recommendation]

---

## Recommendations Summary

1. **Immediate (CRITICAL):** [list critical items that must be fixed]
2. **Short-term (HIGH):** [list high priority items]
3. **Medium-term (MEDIUM):** [list medium priority items]
4. **Optional (LOW):** [list low priority improvements]
```

---

## Rules for Findings

1. **Exact line numbers:** Every finding MUST include the exact file path and line numbers.
2. **Severity ordering:** CRITICAL → HIGH → MEDIUM → LOW.
3. **Alphabetical within severity:** Sort by file path within the same severity level.
4. **Specific descriptions:** "SQL injection in models.py:28" is better than "security issue in models.py".
5. **Actionable recommendations:** Each recommendation should tell the agent exactly what to do.
6. **No duplicate findings:** If the same anti-pattern appears in multiple places, group them under one finding with multiple file:line references.
7. **Impact statement:** Every finding must explain WHY it matters (security risk, maintainability burden, performance impact).

---

## Finding Number Convention

- CRITICAL findings: C1, C2, C3...
- HIGH findings: H1, H2, H3...
- MEDIUM findings: M1, M2, M3...
- LOW findings: L1, L2, L3...

---

## Example Finding

```markdown
#### [C1] SQL Injection via String Concatenation
- **File:** `models.py:28,48-49,68,92,110,127-128,140,174,188,220,224,280,291-297`
- **Description:** SQL queries are constructed using Python string concatenation with user-controlled values. For example, line 28: `cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))`. This pattern appears throughout models.py in all query functions.
- **Impact:** Attackers can inject arbitrary SQL commands to steal, modify, or destroy data. This is the most critical security vulnerability in the application.
- **Recommendation:** Replace all string-concatenated SQL with parameterized queries using `?` placeholders: `cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))`. See refactoring-playbook.md Pattern 2.
```
