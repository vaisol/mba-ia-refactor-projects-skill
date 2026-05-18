# Refactoring Playbook

Concrete transformation patterns for anti-patterns.

## 1. SQL Injection -> Parameterized Queries
**Before (Python)**:
```python
cursor.execute("SELECT * FROM users WHERE email = '" + email + "'")
```
**After (Python)**:
```python
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

## 2. Hardcoded Secrets -> Env Vars
**Before (Node.js)**:
```javascript
const API_KEY = "sk_live_12345";
```
**After (Node.js)**:
```javascript
require('dotenv').config();
const API_KEY = process.env.API_KEY;
```

## 3. Business Logic in Route -> Service Layer
**Before (Flask)**:
```python
@app.route('/checkout')
def checkout():
    # 50 lines of payment and stock logic
```
**After (Flask)**:
```python
@app.route('/checkout')
def checkout():
    result = checkout_service.process_order(request.json)
    return jsonify(result)
```

## 4. N+1 Query -> Eager Loading / Join
**Before**:
```python
for task in tasks:
    user = User.query.get(task.user_id) # Loop query
```
**After**:
```python
tasks = Task.query.options(joinedload(Task.user)).all() # Single query with join
```

## 5. Weak Crypto -> Standard Library
**Before**:
```javascript
const hash = base64(pwd).substring(0, 10);
```
**After**:
```javascript
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(pwd, 10);
```

## 6. Logging Sensitive Data -> Sanitized Log
**Before**:
```javascript
console.log("Card: " + cc_number);
```
**After**:
```javascript
logger.info("Processing payment", { last4: cc_number.slice(-4) });
```

## 7. Arbitrary SQL -> Fixed Methods
**Before**:
```python
cursor.execute(request.json['sql'])
```
**After**:
```python
# Implement specific endpoints for allowed operations
# NEVER execute raw SQL from input
```

## 8. Inconsistent Responses -> Unified Utility
**Before**:
```python
return "Error", 500
# or
return jsonify({"err": "msg"}), 400
```
**After**:
```python
return Response.error("Message", 400)
```
